from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.nutrition_analysis import NutritionAnalysis

class HealthierRecommender:
    @staticmethod
    async def get_healthier_alternatives(
        product_id: int,
        category: Optional[str],
        current_score: int,
        db: AsyncSession,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Finds healthier products within the same category (or generally)
        that have a higher TruthIn score and a GREEN/YELLOW rating.
        """
        query = (
            select(Product)
            .join(NutritionAnalysis, Product.id == NutritionAnalysis.product_id)
            .options(selectinload(Product.analyses))
            .where(
                Product.id != product_id,
                NutritionAnalysis.truthin_score > current_score
            )
        )
        
        if category:
            query = query.where(Product.category.ilike(f"%{category}%"))

        query = query.order_by(desc(NutritionAnalysis.truthin_score)).limit(limit)
        result = await db.execute(query)
        candidates = result.scalars().all()

        if len(candidates) < limit:
            fallback_query = (
                select(Product)
                .join(NutritionAnalysis, Product.id == NutritionAnalysis.product_id)
                .options(selectinload(Product.analyses))
                .where(
                    Product.id != product_id,
                    NutritionAnalysis.truthin_score >= 70,
                    NutritionAnalysis.health_flag == "GREEN"
                )
                .order_by(desc(NutritionAnalysis.truthin_score))
                .limit(limit - len(candidates))
            )
            
            fb_res = await db.execute(fallback_query)
            additional = fb_res.scalars().all()
            for item in additional:
                if item.id not in [c.id for c in candidates]:
                    candidates.append(item)

        alternatives = []
        for p in candidates:
            analysis = p.latest_analysis
            score = analysis.truthin_score if analysis else 50
            flag = analysis.health_flag if analysis else "YELLOW"
            reasons = analysis.flag_reasons[:2] if analysis else []
            
            alternatives.append({
                "id": p.id,
                "barcode": p.barcode,
                "name": p.name,
                "brand": p.brand,
                "category": p.category,
                "image_url": p.image_url,
                "truthin_score": score,
                "health_flag": flag,
                "score_improvement": score - current_score,
                "flag_reasons": reasons
            })
            
        return alternatives
