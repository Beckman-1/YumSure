from typing import Dict, Any, Optional, List, Tuple

RULE_VERSION = "2026.1"

# Standard expected core macro & micronutrients for completeness calculation
CORE_NUTRIENTS = [
    "energy_kcal",
    "fat",
    "saturated_fat",
    "carbohydrates",
    "sugars",
    "fiber",
    "proteins",
    "sodium"
]

class NutritionEngine:
    """
    Independent, pure nutrition scoring and evaluation engine.
    Computes nutrient normalization, thresholds, completeness, Nutri-score, and TruthIn score.
    Testable without database or network dependencies.
    """
    
    @staticmethod
    def calculate_completeness(facts: Dict[str, Optional[float]]) -> float:
        """
        Calculates the completeness score (0.0 - 100.0%) of available nutrition facts.
        None values indicate missing data and are not treated as 0.
        """
        if not facts:
            return 0.0
        
        populated = 0
        for nutrient in CORE_NUTRIENTS:
            if facts.get(nutrient) is not None:
                populated += 1
                
        return round((populated / len(CORE_NUTRIENTS)) * 100.0, 1)

    @staticmethod
    def normalize_nutrients(raw_facts: Dict[str, Any]) -> Dict[str, Optional[float]]:
        """
        Normalizes nutrient dictionary keys and values to a standard per-100g basis.
        CRITICAL: Preserves None for missing nutrients. Does NOT turn missing values to 0.0.
        """
        normalized: Dict[str, Optional[float]] = {}
        
        # Energy
        energy = raw_facts.get("energy_kcal")
        if energy is None:
            energy = raw_facts.get("energy-kcal_100g") or raw_facts.get("energy_kcal_100g")
        normalized["energy_kcal"] = NutritionEngine._to_float(energy)
        
        # Sugars
        sugars = raw_facts.get("sugars")
        if sugars is None:
            sugars = raw_facts.get("sugars_100g")
        normalized["sugars"] = NutritionEngine._to_float(sugars)
        
        # Total Fat & Saturated Fat
        fat = raw_facts.get("fat")
        if fat is None:
            fat = raw_facts.get("fat_100g")
        normalized["fat"] = NutritionEngine._to_float(fat)
        
        sat_fat = raw_facts.get("saturated_fat")
        if sat_fat is None:
            sat_fat = raw_facts.get("saturated-fat_100g") or raw_facts.get("saturated_fat_100g")
        normalized["saturated_fat"] = NutritionEngine._to_float(sat_fat)
        
        # Carbohydrates
        carbs = raw_facts.get("carbohydrates")
        if carbs is None:
            carbs = raw_facts.get("carbohydrates_100g")
        normalized["carbohydrates"] = NutritionEngine._to_float(carbs)
        
        # Fiber & Proteins
        fiber = raw_facts.get("fiber")
        if fiber is None:
            fiber = raw_facts.get("fiber_100g")
        normalized["fiber"] = NutritionEngine._to_float(fiber)
        
        proteins = raw_facts.get("proteins")
        if proteins is None:
            proteins = raw_facts.get("proteins_100g")
        normalized["proteins"] = NutritionEngine._to_float(proteins)
        
        # Sodium / Salt (normalize to mg of sodium)
        sodium = raw_facts.get("sodium")
        if sodium is None:
            sodium = raw_facts.get("sodium_100g")
        salt = raw_facts.get("salt")
        if salt is None:
            salt = raw_facts.get("salt_100g")
            
        sodium_f = NutritionEngine._to_float(sodium)
        salt_f = NutritionEngine._to_float(salt)
        
        if sodium_f is not None:
            # If sodium is in grams (<10g typically given as grams like 0.8g), convert to mg
            if 0 < sodium_f < 30.0:
                normalized["sodium"] = round(sodium_f * 1000.0, 1)
            else:
                normalized["sodium"] = round(sodium_f, 1)
        elif salt_f is not None:
            # Salt (g) -> Sodium (mg): sodium = (salt / 2.5) * 1000
            normalized["sodium"] = round((salt_f / 2.5) * 1000.0, 1)
        else:
            normalized["sodium"] = None
            
        return normalized

    @staticmethod
    def _to_float(val: Any) -> Optional[float]:
        if val is None or val == "":
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def evaluate_nutrition(
        normalized_facts: Dict[str, Optional[float]],
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates nutrition facts against versioned nutritional thresholds.
        Returns score component, flag reasons, breakdown, and personalized alerts.
        """
        score = 80 # Neutral base
        flag_reasons: List[str] = []
        breakdown: Dict[str, Any] = {}
        personalized_alerts: List[str] = []

        # 1. Sugars Evaluation
        sugars = normalized_facts.get("sugars")
        if sugars is not None:
            breakdown["sugars_g"] = sugars
            if sugars > 22.5:
                score -= 25
                flag_reasons.append(f"Very High Sugar: {sugars:.1f}g per 100g (>22.5% sugar)")
                breakdown["sugars_status"] = "VERY_HIGH"
            elif sugars > 12.0:
                score -= 12
                flag_reasons.append(f"High Sugar: {sugars:.1f}g per 100g")
                breakdown["sugars_status"] = "HIGH"
            elif sugars < 5.0 and sugars > 0:
                score += 5
                flag_reasons.append(f"Low Sugar: {sugars:.1f}g per 100g")
                breakdown["sugars_status"] = "LOW"
            else:
                breakdown["sugars_status"] = "MODERATE"
        else:
            breakdown["sugars_status"] = "UNREPORTED"

        # 2. Sodium Evaluation
        sodium = normalized_facts.get("sodium")
        if sodium is not None:
            breakdown["sodium_mg"] = sodium
            if sodium > 900:
                score -= 20
                flag_reasons.append(f"Very High Sodium: {sodium:.0f}mg per 100g")
                breakdown["sodium_status"] = "VERY_HIGH"
            elif sodium > 500:
                score -= 10
                flag_reasons.append(f"Moderate to High Sodium: {sodium:.0f}mg per 100g")
                breakdown["sodium_status"] = "HIGH"
            elif sodium < 120 and sodium > 0:
                score += 5
                breakdown["sodium_status"] = "LOW"
            else:
                breakdown["sodium_status"] = "MODERATE"
        else:
            breakdown["sodium_status"] = "UNREPORTED"

        # 3. Saturated Fat Evaluation
        sat_fat = normalized_facts.get("saturated_fat")
        if sat_fat is not None:
            breakdown["saturated_fat_g"] = sat_fat
            if sat_fat > 10.0:
                score -= 18
                flag_reasons.append(f"High Saturated Fat: {sat_fat:.1f}g per 100g")
                breakdown["saturated_fat_status"] = "HIGH"
            elif sat_fat > 5.0:
                score -= 8
                flag_reasons.append(f"Moderate Saturated Fat: {sat_fat:.1f}g per 100g")
                breakdown["saturated_fat_status"] = "MODERATE"
            else:
                breakdown["saturated_fat_status"] = "LOW"
        else:
            breakdown["saturated_fat_status"] = "UNREPORTED"

        # 4. Protein & Fiber Bonuses
        protein = normalized_facts.get("proteins")
        if protein is not None:
            breakdown["protein_g"] = protein
            if protein >= 10.0:
                score += 10
                flag_reasons.append(f"Good Source of Protein: {protein:.1f}g per 100g")
            elif protein >= 5.0:
                score += 5

        fiber = normalized_facts.get("fiber")
        if fiber is not None:
            breakdown["fiber_g"] = fiber
            if fiber >= 6.0:
                score += 10
                flag_reasons.append(f"High Dietary Fiber: {fiber:.1f}g per 100g")
            elif fiber >= 3.0:
                score += 5

        # 5. User Profile Personalization
        if user_profile:
            goals = user_profile.get("health_goals", [])
            if "diabetes_control" in goals and sugars is not None and sugars > 5.0:
                personalized_alerts.append(f"Diabetic Alert: Contains {sugars:.1f}g sugar. Unfavorable for blood glucose control.")
            
            if "weight_loss" in goals:
                energy = normalized_facts.get("energy_kcal")
                if energy is not None and energy > 400:
                    personalized_alerts.append(f"Weight Loss Alert: High calorie density ({energy:.0f} kcal/100g).")
            
            if ("low_sodium" in goals or "heart_healthy" in goals) and sodium is not None and sodium > 400:
                personalized_alerts.append(f"Cardiovascular Alert: Sodium level ({sodium:.0f}mg) exceeds low-sodium target.")

        return {
            "nutrition_score": score,
            "flag_reasons": flag_reasons,
            "breakdown": breakdown,
            "personalized_alerts": personalized_alerts,
            "rule_version": RULE_VERSION
        }
