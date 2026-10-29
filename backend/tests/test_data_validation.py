import pytest
import datetime
from datetime import timezone
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.product import Product
from app.models.nutrition_fact import NutritionFact
from app.models.nutrition_analysis import NutritionAnalysis
from app.services.nutrition_engine import NutritionEngine

@pytest.mark.anyio
async def test_missing_data_remains_null_in_db():
    """Verify that unspecified nutrients remain NULL in database and are not cast to 0.0."""
    async with AsyncSessionLocal() as session:
        # Check Amul Butter (fiber is None/unrecorded)
        stmt = (
            select(Product)
            .options(selectinload(Product.nutrition_facts))
            .where(Product.barcode == "8901262010047")
        )
        res = await session.execute(stmt)
        product = res.scalars().first()
        assert product is not None

        facts = product.get_facts_dict()
        assert facts.get("fat") == 80.0
        # Fiber must be None, NOT 0.0
        assert facts.get("fiber") is None
        assert facts["fiber"] is None

@pytest.mark.anyio
async def test_provenance_and_verification_status():
    """Verify data provenance tracking and verification status."""
    async with AsyncSessionLocal() as session:
        stmt = select(Product).where(Product.barcode == "8901058852394")
        res = await session.execute(stmt)
        product = res.scalars().first()
        assert product is not None
        assert product.source in ["local_seed", "openfoodfacts"]
        assert product.source_url is not None
        assert product.retrieved_at is not None
        assert product.verification_status in ["OFFICIAL_MANUFACTURER", "COMMUNITY", "VERIFIED_OFF"]
        assert product.data_completeness_score > 0.0

@pytest.mark.anyio
async def test_rule_evolution_does_not_mutate_facts():
    """
    Verify that updating or calculating a new assessment rule (e.g. 2026.2)
    retains original raw source facts intact.
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Product)
            .options(selectinload(Product.nutrition_facts), selectinload(Product.analyses))
            .where(Product.barcode == "8901058852394")
        )
        res = await session.execute(stmt)
        product = res.scalars().first()
        assert product is not None

        original_facts_count = len(product.nutrition_facts)
        original_analyses_count = len(product.analyses)

        # Add a new versioned analysis (e.g. Rule version 2026.2)
        new_analysis = NutritionAnalysis(
            product_id=product.id,
            rule_version="2026.2",
            truthin_score=42,
            health_flag="RED",
            flag_reasons=["Strict rule update 2026.2"],
            nutrient_breakdown={"sodium": "HIGH"},
            detected_allergens=["gluten"],
            detected_additives=[],
            is_vegetarian=True,
            has_palm_oil=True,
            calculated_at=datetime.datetime.now(timezone.utc)
        )
        session.add(new_analysis)
        await session.commit()
        await session.refresh(product)

        # Facts count must not change
        assert len(product.nutrition_facts) == original_facts_count
        # Analysis count has incremented to retain history
        assert len(product.analyses) == original_analyses_count + 1
        assert any(a.rule_version == "2026.2" for a in product.analyses)
