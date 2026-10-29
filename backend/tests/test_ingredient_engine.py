import pytest
from app.services.ingredient_engine import IngredientEngine

def test_extract_additives_hazard_levels():
    """Verify additive extraction and appropriate hazard classification."""
    text = "Noodles (Refined wheat flour, Palm oil, INS 621, Thickener (508), Caramel (150d), Preservative E211, INS 102)."
    additives = IngredientEngine.extract_additives(text)
    
    codes_to_hazard = {a["code"]: a["hazard"] for a in additives}
    assert codes_to_hazard.get("INS 621") == "CAUTION"
    assert codes_to_hazard.get("INS 150d") == "CAUTION"
    assert codes_to_hazard.get("INS 211") == "CAUTION"
    assert codes_to_hazard.get("INS 102") == "AVOID"

def test_detect_allergens_comprehensive():
    """Verify allergen detection across multiple standard categories."""
    text = "Contains Wheat flour, Skimmed Milk Powder, Soy lecithin, groundnuts, Cashew nuts, and Dried Egg Whites."
    allergens = IngredientEngine.detect_allergens(text)
    
    assert "gluten" in allergens
    assert "milk" in allergens
    assert "soy" in allergens
    assert "peanuts" in allergens
    assert "tree_nuts" in allergens
    assert "eggs" in allergens

def test_palm_oil_detection_variants():
    """Verify detection of various palm oil fraction labels."""
    assert IngredientEngine.has_palm_oil("Refined Palm Oil, Sugar, Salt.") is True
    assert IngredientEngine.has_palm_oil("Edible vegetable oil (Palmolein), Salt.") is True
    assert IngredientEngine.has_palm_oil("Palm kernel fat, Cocoa powder.") is True
    assert IngredientEngine.has_palm_oil("Cold pressed coconut oil, Salt.") is False
    assert IngredientEngine.has_palm_oil("Mustard oil, Spices.") is False

def test_vegetarian_classification():
    """Verify accurate detection of non-vegetarian animal byproducts."""
    assert IngredientEngine.is_vegetarian("Milk solids, Sugar, Wheat flour.") is True
    assert IngredientEngine.is_vegetarian("Sugar, Gelatin, Artificial Strawberry Flavor.") is False
    assert IngredientEngine.is_vegetarian("Chicken broth, Salt, Onion.") is False
    assert IngredientEngine.is_vegetarian("Confectioner glaze, Carmine (INS 120).") is False

def test_ingredient_hazard_evaluation():
    """Verify ingredient hazard deductions and alerts."""
    profile = {
        "allergies": ["peanuts", "milk"],
        "dietary_preference": "vegetarian"
    }
    additives = [{"code": "INS 102", "name": "Tartrazine", "hazard": "AVOID"}]
    allergens = ["peanuts"]
    text = "Peanuts, Refined Palm Oil, INS 102."

    hazards = IngredientEngine.evaluate_ingredient_hazards(
        additives=additives,
        ingredients_text=text,
        allergens=allergens,
        user_profile=profile
    )

    assert hazards["penalty"] >= 26 # 20 for AVOID + 6 for Palm Oil
    assert hazards["has_avoid_additive"] is True
    assert hazards["has_palm_oil"] is True
    assert hazards["is_vegetarian"] is True
    assert any("CRITICAL ALLERGEN WARNING" in a for a in hazards["personalized_alerts"])
    assert any("Hazardous Additive" in r for r in hazards["flag_reasons"])
