import datetime
from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.core.database import get_db
from app.models.product import Product
from app.models.nutrition_fact import NutritionFact
from app.models.nutrition_analysis import NutritionAnalysis
from app.schemas.assessment import ProductAssessmentResponse
from app.schemas.product import ProductCreate, ProductAlternative
from app.services.barcode_resolver import BarcodeResolver
from app.services.assessment_service import AssessmentService
from app.services.nutrition_engine import RULE_VERSION
from app.services.recommender import HealthierRecommender

router = APIRouter()

@router.get("", response_model=List[ProductAssessmentResponse], summary="Search and list products")
async def list_products(
    q: Optional[str] = Query(None, description="Search term for product name, brand or barcode"),
    category: Optional[str] = Query(None, description="Filter by category"),
    health_flag: Optional[str] = Query(None, description="Filter by GREEN, YELLOW, or RED"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Product)
        .options(selectinload(Product.nutrition_facts), selectinload(Product.analyses))
    )
    
    if q:
        query = query.where(
            or_(
                Product.name.ilike(f"%{q}%"),
                Product.brand.ilike(f"%{q}%"),
                Product.barcode.ilike(f"%{q}%")
            )
        )
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))

    if health_flag:
        query = query.join(NutritionAnalysis, Product.id == NutritionAnalysis.product_id).where(
            NutritionAnalysis.health_flag == health_flag.upper()
        )

    query = query.order_by(desc(Product.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    
    return [BarcodeResolver._format_product_response(p) for p in products]

@router.get("/categories/list", response_model=List[str], summary="Get list of all product categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product.category).distinct())
    categories = [cat for cat in result.scalars().all() if cat]
    return sorted(list(set(categories)))

@router.get("/{product_id}", response_model=ProductAssessmentResponse, summary="Get product by ID")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.nutrition_facts), selectinload(Product.analyses))
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return BarcodeResolver._format_product_response(product)

@router.get("/{product_id}/alternatives", response_model=List[ProductAlternative], summary="Get healthier alternatives")
async def get_alternatives(
    product_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.analyses))
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    current_score = product.latest_analysis.truthin_score if product.latest_analysis else 50
    alternatives = await HealthierRecommender.get_healthier_alternatives(
        product_id=product.id,
        category=product.category,
        current_score=current_score,
        db=db,
        limit=limit
    )
    return alternatives

@router.post("", response_model=ProductAssessmentResponse, status_code=status.HTTP_201_CREATED, summary="Contribute or create new product")
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    # 1. Barcode check-digit validation
    is_valid, clean_barcode, err = BarcodeResolver.validate_barcode(product_in.barcode)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "INVALID_BARCODE", "message": err}
        )

    # 2. Check for duplicate barcode
    existing = await db.execute(select(Product).where(Product.barcode == clean_barcode))
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with barcode '{clean_barcode}' already exists in database."
        )

    # 3. Compute Versioned Assessment
    assessment = AssessmentService.calculate_assessment(
        product_in.nutriments, product_in.ingredients_text or ""
    )

    now = datetime.datetime.now(timezone.utc)
    new_prod = Product(
        barcode=clean_barcode,
        name=product_in.name,
        brand=product_in.brand,
        category=product_in.category or "General",
        product_type=product_in.product_type,
        image_url=product_in.image_url,
        ingredients_text=product_in.ingredients_text or "",
        ingredients_list=[],
        source="user_contributed",
        source_url="user://contributed",
        retrieved_at=now,
        data_completeness_score=assessment["data_completeness_score"],
        verification_status="COMMUNITY"
    )
    db.add(new_prod)
    await db.flush()

    # 4. Save Separate Source Nutrition Facts
    for nutrient_name, amount in assessment["normalized_facts"].items():
        unit = "mg" if nutrient_name == "sodium" else ("kcal" if nutrient_name == "energy_kcal" else "g")
        fact = NutritionFact(
            product_id=new_prod.id,
            nutrient_name=nutrient_name,
            amount=amount, # Preserves None for missing nutrients!
            unit=unit,
            provenance_source="user_contributed",
            retrieved_at=now,
            verification_status="COMMUNITY"
        )
        db.add(fact)

    # 5. Save Versioned Nutrition Analysis
    analysis = NutritionAnalysis(
        product_id=new_prod.id,
        rule_version=RULE_VERSION,
        truthin_score=assessment["truthin_score"],
        health_flag=assessment["health_flag"],
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
    await db.refresh(new_prod)
    return BarcodeResolver._format_product_response(new_prod)
