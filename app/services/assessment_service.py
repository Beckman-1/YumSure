from typing import Dict, Any, Optional, List
from app.services.nutrition_engine import NutritionEngine, RULE_VERSION
from app.services.ingredient_engine import IngredientEngine

class AssessmentService:
    """
    Coordinates NutritionEngine and IngredientEngine to produce a versioned assessment.
    Independent of DB models and network calls.
    """
    
    @staticmethod
    def calculate_assessment(
        nutrition_facts: Dict[str, Optional[float]],
        ingredients_text: str,
        user_profile: Optional[Dict[str, Any]] = None,
        nutriscore_grade: Optional[str] = None,
        nova_group: Optional[int] = None
    ) -> Dict[str, Any]:
        # 1. Normalize and evaluate nutrition
        normalized_facts = NutritionEngine.normalize_nutrients(nutrition_facts)
        nutr_eval = NutritionEngine.evaluate_nutrition(normalized_facts, user_profile=user_profile)
        completeness = NutritionEngine.calculate_completeness(normalized_facts)

        # 2. Extract and evaluate ingredients, allergens, and additives
        additives = IngredientEngine.extract_additives(ingredients_text)
        allergens = IngredientEngine.detect_allergens(ingredients_text)
        ing_eval = IngredientEngine.evaluate_ingredient_hazards(
            additives, ingredients_text, allergens, user_profile=user_profile
        )

        # 3. Combine scores
        raw_score = nutr_eval["nutrition_score"] - ing_eval["penalty"]
        truthin_score = max(5, min(98, raw_score))

        # 4. Determine health flag
        sugars = normalized_facts.get("sugars") or 0.0
        sodium = normalized_facts.get("sodium") or 0.0
        has_critical_allergy = any("CRITICAL ALLERGEN" in a for a in ing_eval["personalized_alerts"])

        if has_critical_allergy:
            health_flag = "RED"
            truthin_score = min(truthin_score, 20)
        elif truthin_score >= 70 and not ing_eval["has_avoid_additive"] and sugars < 15.0 and sodium < 700:
            health_flag = "GREEN"
        elif truthin_score < 45 or ing_eval["has_avoid_additive"] or sugars > 25.0:
            health_flag = "RED"
        else:
            health_flag = "YELLOW"

        # Combine flag reasons and alerts
        combined_reasons = nutr_eval["flag_reasons"] + ing_eval["flag_reasons"]
        combined_alerts = nutr_eval["personalized_alerts"] + ing_eval["personalized_alerts"]

        return {
            "truthin_score": truthin_score,
            "health_flag": health_flag,
            "rule_version": RULE_VERSION,
            "nutriscore_grade": nutriscore_grade,
            "nova_group": nova_group,
            "flag_reasons": combined_reasons,
            "personalized_alerts": combined_alerts,
            "detected_allergens": allergens,
            "detected_additives": additives,
            "nutrient_breakdown": nutr_eval["breakdown"],
            "is_vegetarian": ing_eval["is_vegetarian"],
            "has_palm_oil": ing_eval["has_palm_oil"],
            "data_completeness_score": completeness,
            "normalized_facts": normalized_facts
        }
