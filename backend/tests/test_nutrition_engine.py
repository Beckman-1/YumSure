import pytest
from app.services.nutrition_engine import NutritionEngine, RULE_VERSION

def test_missing_data_preservation():
    """Verify that missing facts remain None and are NOT converted to 0.0."""
    raw = {
        "energy_kcal": 450.0,
        "sugars": 12.0,
        "fat": None,
        "saturated_fat": None,
        "fiber": None
    }
    normalized = NutritionEngine.normalize_nutrients(raw)
    
    assert normalized["energy_kcal"] == 450.0
    assert normalized["sugars"] == 12.0
    assert normalized["fat"] is None
    assert normalized["saturated_fat"] is None
    assert normalized["fiber"] is None

def test_calculate_completeness():
    """Verify data completeness score calculation."""
    # Complete facts (8 of 8)
    full_facts = {
        "energy_kcal": 400.0,
        "fat": 10.0,
        "saturated_fat": 2.0,
        "carbohydrates": 60.0,
        "sugars": 5.0,
        "fiber": 4.0,
        "proteins": 12.0,
        "sodium": 200.0
    }
    assert NutritionEngine.calculate_completeness(full_facts) == 100.0

    # Half facts (4 of 8)
    half_facts = {
        "energy_kcal": 400.0,
        "sugars": 5.0,
        "proteins": 12.0,
        "sodium": 200.0
    }
    assert NutritionEngine.calculate_completeness(half_facts) == 50.0

    # Empty facts
    assert NutritionEngine.calculate_completeness({}) == 0.0

def test_sodium_and_salt_normalization():
    """Verify sodium and salt unit conversions."""
    # Salt given as 1.5g -> sodium = (1.5 / 2.5) * 1000 = 600mg
    salt_facts = {"salt": 1.5}
    norm_salt = NutritionEngine.normalize_nutrients(salt_facts)
    assert norm_salt["sodium"] == 600.0

    # Sodium given in grams (e.g. 0.8g) -> converted to 800mg
    sodium_g_facts = {"sodium": 0.8}
    norm_sodium = NutritionEngine.normalize_nutrients(sodium_g_facts)
    assert norm_sodium["sodium"] == 800.0

    # Sodium already in mg
    sodium_mg_facts = {"sodium": 850.0}
    norm_mg = NutritionEngine.normalize_nutrients(sodium_mg_facts)
    assert norm_mg["sodium"] == 850.0

def test_sugar_threshold_boundaries():
    """Verify sugar threshold evaluations and explanations."""
    # Very high sugar (>22.5g)
    high_sugar = {"sugars": 28.0}
    res_high = NutritionEngine.evaluate_nutrition(high_sugar)
    assert res_high["breakdown"]["sugars_status"] == "VERY_HIGH"
    assert any("Very High Sugar" in r for r in res_high["flag_reasons"])
    assert res_high["nutrition_score"] <= 60

    # Low sugar (<5.0g)
    low_sugar = {"sugars": 3.0}
    res_low = NutritionEngine.evaluate_nutrition(low_sugar)
    assert res_low["breakdown"]["sugars_status"] == "LOW"
    assert any("Low Sugar" in r for r in res_low["flag_reasons"])
    assert res_low["nutrition_score"] > 80

def test_rule_versioning():
    """Verify rule version metadata is attached to every evaluation."""
    facts = {"sugars": 10.0}
    res = NutritionEngine.evaluate_nutrition(facts)
    assert res["rule_version"] == RULE_VERSION
    assert res["rule_version"] == "2026.1"

def test_personalized_nutritional_alerts():
    """Verify personalized warnings for diabetes and hypertension."""
    profile = {
        "health_goals": ["diabetes_control", "low_sodium"]
    }
    facts = {
        "sugars": 15.0,
        "sodium": 650.0
    }
    eval_res = NutritionEngine.evaluate_nutrition(facts, user_profile=profile)
    assert any("Diabetic Alert" in a for a in eval_res["personalized_alerts"])
    assert any("Cardiovascular Alert" in a for a in eval_res["personalized_alerts"])
