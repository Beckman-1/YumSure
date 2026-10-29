import asyncio
import datetime
from datetime import timezone, timedelta
import httpx
import re
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.product import Product
from app.models.nutrition_fact import NutritionFact
from app.models.nutrition_analysis import NutritionAnalysis
from app.services.assessment_service import AssessmentService
from app.services.nutrition_engine import RULE_VERSION

# Negative cache for barcodes not found anywhere (barcode -> expiry timestamp)
_NEGATIVE_CACHE: Dict[str, datetime.datetime] = {}

# In-flight request deduplication locks (barcode -> asyncio.Lock)
_IN_FLIGHT_LOCKS: Dict[str, asyncio.Lock] = {}
_LOCKS_MUTEX = asyncio.Lock()

from app.services.catalog_data import TRUTHIN_CATALOG as _CATALOG_DATA

# Curated Fallback Catalog for all 41 TruthIn products covering 14 categories.
# Ensures demo & testing reliability when DB is cold or external APIs are unavailable.
LOCAL_FALLBACK_CATALOG = {
    barcode: {**item, "source": "local_seed"}
    for barcode, item in _CATALOG_DATA.items()
}

class BarcodeResolver:
    """
    Advanced multi-source barcode resolution service.
    Implements check-digit validation, deduplication locks, negative caching,
    explicit priority routing, timeout retries, and source provenance.
    """

    @staticmethod
    def validate_barcode(raw_barcode: str) -> Tuple[bool, str, Optional[str]]:
        """
        Validates barcode string format and GS1 Modulo-10 check digit.
        Supports EAN-13, EAN-8, and UPC-A (12 digits).
        Returns: (is_valid, cleaned_barcode, error_message)
        """
        clean = re.sub(r'[^0-9]', '', str(raw_barcode).strip())
        
        if not clean:
            return False, clean, "Barcode cannot be empty or non-numeric."
        
        if len(clean) not in (8, 12, 13, 14):
            return False, clean, f"Invalid barcode length ({len(clean)} digits). Expected 8 (EAN-8), 12 (UPC-A), or 13 (EAN-13)."

        # Modulo 10 Check Digit Calculation
        # GS1 standard: multiply digits from right to left (excluding check digit) by 3, 1 alternating
        digits = [int(d) for d in clean]
        check_digit = digits[-1]
        data_digits = digits[:-1]

        total = 0
        weight = 3
        for d in reversed(data_digits):
            total += d * weight
            weight = 1 if weight == 3 else 3

        expected_check = (10 - (total % 10)) % 10
        if check_digit != expected_check:
            return False, clean, f"Invalid barcode check digit. Got {check_digit}, expected {expected_check}."

        return True, clean, None

    @staticmethod
    def get_barcode_variants(barcode: str) -> List[str]:
        """Generates standard barcode variants (UPC-A to EAN-13 with leading 0)."""
        clean = re.sub(r'[^0-9]', '', str(barcode).strip())
        variants = [clean]
        if len(clean) == 12:
            variants.append("0" + clean)
        elif len(clean) == 13 and clean.startswith("0"):
            variants.append(clean[1:])
        return variants

    @staticmethod
    async def resolve_barcode(
        barcode: str,
        db: AsyncSession,
        user_profile: Optional[Dict[str, Any]] = None,
        category_hint: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        # 1. Format & Check-Digit Validation
        is_valid, clean_barcode, err = BarcodeResolver.validate_barcode(barcode)
        if not is_valid:
            # If invalid check-digit, reject early
            return None

        # 2. Check Negative Cache
        now = datetime.datetime.now(timezone.utc)
        if clean_barcode in _NEGATIVE_CACHE:
            if now < _NEGATIVE_CACHE[clean_barcode]:
                return None
            else:
                del _NEGATIVE_CACHE[clean_barcode]

        # 3. Duplicate Concurrent Request Protection
        async with _LOCKS_MUTEX:
            if clean_barcode not in _IN_FLIGHT_LOCKS:
                _IN_FLIGHT_LOCKS[clean_barcode] = asyncio.Lock()
            lock = _IN_FLIGHT_LOCKS[clean_barcode]

        async with lock:
            # Step A: Check Local PostgreSQL Database
            variants = BarcodeResolver.get_barcode_variants(clean_barcode)
            for v in variants:
                stmt = (
                    select(Product)
                    .options(selectinload(Product.nutrition_facts), selectinload(Product.analyses))
                    .where(Product.barcode == v)
                )
                res = await db.execute(stmt)
                product = res.scalars().first()
                if product:
                    # Check staleness: if older than STALE_AFTER_DAYS, we still serve it but can log
                    return BarcodeResolver._format_product_response(product, user_profile)

            # Step B: Check Fallback Seed Catalog
            for v in variants:
                if v in LOCAL_FALLBACK_CATALOG:
                    seed_data = LOCAL_FALLBACK_CATALOG[v]
                    product = await BarcodeResolver._persist_seed_product(seed_data, db)
                    return BarcodeResolver._format_product_response(product, user_profile)

            # Step C: External Upstream Fetch (Open Food Facts & Open Beauty Facts)
            is_cosmetic_hint = category_hint and any(c in category_hint.lower() for c in ["cosmetic", "beauty", "skin", "shampoo", "soap", "lotion"])
            
            # Explicit priority routing based on category
            if is_cosmetic_hint:
                api_sequence = [
                    ("openbeautyfacts", settings.OPEN_BEAUTY_FACTS_API, "cosmetic"),
                    ("openfoodfacts", settings.OPEN_FOOD_FACTS_API, "food")
                ]
            else:
                api_sequence = [
                    ("openfoodfacts", settings.OPEN_FOOD_FACTS_API, "food"),
                    ("openbeautyfacts", settings.OPEN_BEAUTY_FACTS_API, "cosmetic")
                ]

            for v in variants:
                for src_name, base_url, p_type in api_sequence:
                    product = await BarcodeResolver._fetch_from_upstream(v, src_name, base_url, p_type, db)
                    if product:
                        return BarcodeResolver._format_product_response(product, user_profile)

            # Step D: Not Found Anywhere -> Record in Negative Cache
            _NEGATIVE_CACHE[clean_barcode] = now + timedelta(seconds=settings.NEGATIVE_CACHE_TTL_SEC)
            return None

    @staticmethod
    async def _fetch_from_upstream(
        barcode: str,
        source_name: str,
        base_url: str,
        product_type: str,
        db: AsyncSession
    ) -> Optional[Product]:
        """Fetches product from external API with retries and rate-limit handling."""
        url = f"{base_url}/product/{barcode}.json"
        headers = {"User-Agent": settings.USER_AGENT}
        
        async with httpx.AsyncClient(timeout=6.0) as client:
            for attempt in range(2): # Up to 2 attempts
                try:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code == 429: # Rate limit hit
                        await asyncio.sleep(1.0)
                        continue
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("status") == 1 and "product" in data:
                            return await BarcodeResolver._persist_external_product(
                                data["product"], barcode, source_name, url, product_type, db
                            )
                    elif resp.status_code == 404:
                        break # Product not in this registry
                except (httpx.TimeoutException, httpx.RequestError):
                    if attempt == 0:
                        await asyncio.sleep(0.5)
                        continue
        return None

    @staticmethod
    async def _persist_external_product(
        raw: Dict[str, Any],
        barcode: str,
        source: str,
        source_url: str,
        product_type: str,
        db: AsyncSession
    ) -> Product:
        name = raw.get("product_name") or raw.get("product_name_en") or "Unknown Product"
        brand = raw.get("brands") or raw.get("brand") or "Generic"
        
        cat_tags = raw.get("categories_tags", [])
        category = cat_tags[0].replace("en:", "").replace("-", " ").title() if cat_tags else raw.get("categories", "General")
        
        image_url = raw.get("image_front_url") or raw.get("image_url") or raw.get("image_small_url")
        ingredients_text = raw.get("ingredients_text") or raw.get("ingredients_text_en") or ""
        
        # 1. Parse Source Nutrition Facts
        nutriments_raw = raw.get("nutriments", {})
        raw_facts: Dict[str, Optional[float]] = {
            "energy_kcal": nutriments_raw.get("energy-kcal_100g") or nutriments_raw.get("energy-kcal"),
            "sugars": nutriments_raw.get("sugars_100g") or nutriments_raw.get("sugars"),
            "fat": nutriments_raw.get("fat_100g") or nutriments_raw.get("fat"),
            "saturated_fat": nutriments_raw.get("saturated-fat_100g") or nutriments_raw.get("saturated-fat"),
            "sodium": nutriments_raw.get("sodium_100g") or nutriments_raw.get("sodium"),
            "salt": nutriments_raw.get("salt_100g") or nutriments_raw.get("salt"),
            "carbohydrates": nutriments_raw.get("carbohydrates_100g") or nutriments_raw.get("carbohydrates"),
            "proteins": nutriments_raw.get("proteins_100g") or nutriments_raw.get("proteins"),
            "fiber": nutriments_raw.get("fiber_100g") or nutriments_raw.get("fiber")
        }

        # 2. Compute Versioned Assessment
        nutriscore = (raw.get("nutriscore_grade") or "unknown").lower()
        nova = raw.get("nova_group")
        try:
            nova = int(nova) if nova else None
        except (ValueError, TypeError):
            nova = None

        assessment = AssessmentService.calculate_assessment(
            raw_facts, ingredients_text, nutriscore_grade=nutriscore, nova_group=nova
        )

        now = datetime.datetime.now(timezone.utc)
        product = Product(
            barcode=barcode,
            name=name,
            brand=brand,
            category=category,
            product_type=product_type,
            image_url=image_url,
            ingredients_text=ingredients_text,
            ingredients_list=raw.get("ingredients_original_tags", []),
            source=source,
            source_url=source_url,
            retrieved_at=now,
            data_completeness_score=assessment["data_completeness_score"],
            verification_status="COMMUNITY"
        )
        db.add(product)
        await db.flush()

        # 3. Save Separate Source Nutrition Facts
        normalized_facts = assessment["normalized_facts"]
        for nutrient_name, amount in normalized_facts.items():
            unit = "mg" if nutrient_name == "sodium" else ("kcal" if nutrient_name == "energy_kcal" else "g")
            fact = NutritionFact(
                product_id=product.id,
                nutrient_name=nutrient_name,
                amount=amount, # Preserves None for missing nutrients!
                unit=unit,
                provenance_source=source,
                retrieved_at=now,
                verification_status="COMMUNITY"
            )
            db.add(fact)

        # 4. Save Versioned Nutrition Analysis
        analysis = NutritionAnalysis(
            product_id=product.id,
            rule_version=RULE_VERSION,
            truthin_score=assessment["truthin_score"],
            health_flag=assessment["health_flag"],
            nutriscore_grade=nutriscore,
            nova_group=nova,
            flag_reasons=assessment["flag_reasons"],
            nutrient_breakdown=assessment["nutrient_breakdown"],
            detected_allergens=assessment["detected_allergens"],
            detected_additives=assessment["detected_additives"],
            is_vegetarian=assessment["is_vegetarian"],
            has_palm_oil=assessment["has_palm_oil"],
            calculated_at=now
        )
        db.add(analysis)

        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def _persist_seed_product(data: Dict[str, Any], db: AsyncSession) -> Product:
        now = datetime.datetime.now(timezone.utc)
        raw_facts = data.get("nutrition_facts", {})
        
        assessment = AssessmentService.calculate_assessment(
            raw_facts, 
            data.get("ingredients_text", ""), 
            nutriscore_grade=data.get("nutriscore_grade"), 
            nova_group=data.get("nova_group")
        )

        product = Product(
            barcode=data["barcode"],
            name=data["name"],
            brand=data.get("brand"),
            category=data.get("category"),
            product_type=data.get("product_type", "food"),
            image_url=data.get("image_url"),
            ingredients_text=data.get("ingredients_text"),
            ingredients_list=[],
            source=data.get("source", "local_seed"),
            source_url="local://seed",
            retrieved_at=now,
            data_completeness_score=assessment["data_completeness_score"],
            verification_status=data.get("verification_status", "OFFICIAL_MANUFACTURER")
        )
        db.add(product)
        await db.flush()

        for nutrient_name, amount in assessment["normalized_facts"].items():
            unit = "mg" if nutrient_name == "sodium" else ("kcal" if nutrient_name == "energy_kcal" else "g")
            fact = NutritionFact(
                product_id=product.id,
                nutrient_name=nutrient_name,
                amount=amount,
                unit=unit,
                provenance_source="local_seed",
                retrieved_at=now,
                verification_status=data.get("verification_status", "OFFICIAL_MANUFACTURER")
            )
            db.add(fact)

        analysis = NutritionAnalysis(
            product_id=product.id,
            rule_version=RULE_VERSION,
            truthin_score=assessment["truthin_score"],
            health_flag=assessment["health_flag"],
            nutriscore_grade=data.get("nutriscore_grade"),
            nova_group=data.get("nova_group"),
            flag_reasons=assessment["flag_reasons"],
            nutrient_breakdown=assessment["nutrient_breakdown"],
            detected_allergens=assessment["detected_allergens"],
            detected_additives=assessment["detected_additives"],
            is_vegetarian=assessment["is_vegetarian"],
            has_palm_oil=assessment["has_palm_oil"],
            calculated_at=now
        )
        db.add(analysis)

        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    def _format_product_response(
        product: Product,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Formats product, source facts, and personalized assessment into API schema."""
        facts_dict = product.get_facts_dict()
        
        # If user profile provided, calculate personalized alerts on the fly
        assessment = AssessmentService.calculate_assessment(
            facts_dict,
            product.ingredients_text or "",
            user_profile=user_profile,
            nutriscore_grade=product.latest_analysis.nutriscore_grade if product.latest_analysis else None,
            nova_group=product.latest_analysis.nova_group if product.latest_analysis else None
        )

        return {
            "id": product.id,
            "barcode": product.barcode,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "product_type": product.product_type,
            "image_url": product.image_url,
            "ingredients_text": product.ingredients_text,
            "source": product.source,
            "source_url": product.source_url,
            "retrieved_at": product.retrieved_at.isoformat() if product.retrieved_at else None,
            "data_completeness_score": product.data_completeness_score,
            "verification_status": product.verification_status,
            "nutrition_facts": facts_dict, # Contains None for missing nutrients!
            "assessment": {
                "truthin_score": assessment["truthin_score"],
                "health_flag": assessment["health_flag"],
                "rule_version": assessment["rule_version"],
                "nutriscore_grade": assessment["nutriscore_grade"],
                "nova_group": assessment["nova_group"],
                "flag_reasons": assessment["flag_reasons"],
                "personalized_alerts": assessment["personalized_alerts"],
                "detected_allergens": assessment["detected_allergens"],
                "detected_additives": assessment["detected_additives"],
                "nutrient_breakdown": assessment["nutrient_breakdown"],
                "is_vegetarian": assessment["is_vegetarian"],
                "has_palm_oil": assessment["has_palm_oil"],
                "data_completeness_score": assessment["data_completeness_score"]
            }
        }
