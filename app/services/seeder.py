import datetime
from datetime import timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.additive import Additive
from app.models.product import Product
from app.models.nutrition_fact import NutritionFact
from app.models.nutrition_analysis import NutritionAnalysis
from app.models.user_profile import UserProfile
from app.core.security import hash_password
from app.services.ingredient_engine import ADDITIVE_REGISTRY
from app.services.assessment_service import AssessmentService
from app.services.nutrition_engine import RULE_VERSION
from app.services.catalog_data import TRUTHIN_CATALOG

POPULAR_PRODUCTS = list(TRUTHIN_CATALOG.values())

async def seed_database(db: AsyncSession):
    now = datetime.datetime.now(timezone.utc)
    
    # 1. Seed Additives
    for num, item in ADDITIVE_REGISTRY.items():
        stmt = select(Additive).where(Additive.code == item["code"])
        res = await db.execute(stmt)
        if not res.scalars().first():
            db.add(Additive(
                code=item["code"],
                name=item["name"],
                category=item["category"],
                hazard_level=item["hazard"],
                description=item.get("description", item["name"]),
                health_concerns=item.get("concerns")
            ))

    # 2. Seed Default User Profile
    prof_stmt = select(UserProfile).where(UserProfile.id == "default")
    prof_res = await db.execute(prof_stmt)
    if not prof_res.scalars().first():
        db.add(UserProfile(
            id="default",
            email="demo@yumsure.app",
            hashed_password=hash_password("demo1234"),
            name="Demo User",
            dietary_preference="any",
            health_goals=["diabetes_control", "weight_loss"],
            allergies=[],
            avoid_additives=True,
            avoid_palm_oil=True,
            is_active=True
        ))

    # 3. Seed Products with Separate Facts and Analyses
    for item in POPULAR_PRODUCTS:
        prod_stmt = select(Product).where(Product.barcode == item["barcode"])
        prod_res = await db.execute(prod_stmt)
        if not prod_res.scalars().first():
            raw_facts = item.get("nutrition_facts", {})
            assessment = AssessmentService.calculate_assessment(
                raw_facts,
                item["ingredients_text"],
                nutriscore_grade=item.get("nutriscore_grade"),
                nova_group=item.get("nova_group")
            )

            product = Product(
                barcode=item["barcode"],
                name=item["name"],
                brand=item.get("brand"),
                category=item.get("category"),
                product_type=item.get("product_type", "food"),
                image_url=item.get("image_url"),
                ingredients_text=item.get("ingredients_text"),
                ingredients_list=[],
                source="local_seed",
                source_url="local://seed",
                retrieved_at=now,
                data_completeness_score=assessment["data_completeness_score"],
                verification_status=item.get("verification_status", "OFFICIAL_MANUFACTURER")
            )
            db.add(product)
            await db.flush()

            for nutrient_name, amount in assessment["normalized_facts"].items():
                unit = "mg" if nutrient_name == "sodium" else ("kcal" if nutrient_name == "energy_kcal" else "g")
                db.add(NutritionFact(
                    product_id=product.id,
                    nutrient_name=nutrient_name,
                    amount=amount, # Preserves None for missing nutrients!
                    unit=unit,
                    provenance_source="local_seed",
                    retrieved_at=now,
                    verification_status=item.get("verification_status", "OFFICIAL_MANUFACTURER")
                ))

            db.add(NutritionAnalysis(
                product_id=product.id,
                rule_version=RULE_VERSION,
                truthin_score=assessment["truthin_score"],
                health_flag=assessment["health_flag"],
                nutriscore_grade=item.get("nutriscore_grade"),
                nova_group=item.get("nova_group"),
                flag_reasons=assessment["flag_reasons"],
                nutrient_breakdown=assessment["nutrient_breakdown"],
                detected_allergens=assessment["detected_allergens"],
                detected_additives=assessment["detected_additives"],
                is_vegetarian=assessment["is_vegetarian"],
                has_palm_oil=assessment["has_palm_oil"],
                calculated_at=now
            ))

    await db.commit()
