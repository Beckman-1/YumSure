import re
from typing import Dict, List, Any, Optional

# Comprehensive Database of Common Food Additives, E-numbers & INS codes
ADDITIVE_REGISTRY = {
    # High Concern / Avoid
    "102": {"code": "INS 102", "name": "Tartrazine (Yellow 5)", "category": "Color", "hazard": "AVOID", "concerns": "Azo dye linked to hyperactivity in children and hypersensitivity."},
    "110": {"code": "INS 110", "name": "Sunset Yellow FCF (Yellow 6)", "category": "Color", "hazard": "AVOID", "concerns": "Azo dye associated with hyperactivity and allergic reactions."},
    "122": {"code": "INS 122", "name": "Azorubine (Carmoisine)", "category": "Color", "hazard": "AVOID", "concerns": "Azo dye banned in several countries; respiratory and skin allergen."},
    "124": {"code": "INS 124", "name": "Ponceau 4R", "category": "Color", "hazard": "AVOID", "concerns": "Synthetic color restricted in the EU; linked to hyperactivity."},
    "127": {"code": "INS 127", "name": "Erythrosine (Red 3)", "category": "Color", "hazard": "AVOID", "concerns": "Endocrine disruptor linked to thyroid tumors in animal studies."},
    "129": {"code": "INS 129", "name": "Allura Red AC (Red 40)", "category": "Color", "hazard": "AVOID", "concerns": "Synthetic azo dye; linked to bowel inflammation and hyperactivity."},
    "171": {"code": "INS 171", "name": "Titanium Dioxide", "category": "Color", "hazard": "AVOID", "concerns": "Banned in EU due to genotoxicity concerns and nanoparticle buildup."},
    "249": {"code": "INS 249", "name": "Potassium Nitrite", "category": "Preservative", "hazard": "AVOID", "concerns": "Forms carcinogenic nitrosamines in stomach."},
    "250": {"code": "INS 250", "name": "Sodium Nitrite", "category": "Preservative", "hazard": "AVOID", "concerns": "Processed meat preservative; precursor to carcinogenic nitrosamines."},
    "319": {"code": "INS 319", "name": "TBHQ (Tert-Butylhydroquinone)", "category": "Antioxidant", "hazard": "AVOID", "concerns": "Synthetic antioxidant; high doses linked to cellular damage in animal models."},
    "320": {"code": "INS 320", "name": "BHA (Butylated Hydroxyanisole)", "category": "Antioxidant", "hazard": "AVOID", "concerns": "IARC Group 2B possible human carcinogen; endocrine disruptor."},

    # Moderate Concern / Caution
    "133": {"code": "INS 133", "name": "Brilliant Blue FCF", "category": "Color", "hazard": "CAUTION", "concerns": "Synthetic triphenylmethane dye; mild allergic potential."},
    "150c": {"code": "INS 150c", "name": "Caramel III (Ammonia Caramel)", "category": "Color", "hazard": "CAUTION", "concerns": "Manufactured with ammonia compounds."},
    "150d": {"code": "INS 150d", "name": "Caramel IV (Sulphite Ammonia Caramel)", "category": "Color", "hazard": "CAUTION", "concerns": "Prepared with ammonia & sulphites; contains trace 4-MEI."},
    "211": {"code": "INS 211", "name": "Sodium Benzoate", "category": "Preservative", "hazard": "CAUTION", "concerns": "Forms trace benzene in presence of ascorbic acid (Vitamin C)."},
    "212": {"code": "INS 212", "name": "Potassium Benzoate", "category": "Preservative", "hazard": "CAUTION", "concerns": "Similar risk profile to sodium benzoate."},
    "220": {"code": "INS 220", "name": "Sulphur Dioxide", "category": "Preservative", "hazard": "CAUTION", "concerns": "Strong respiratory trigger in asthma and sulphite-sensitive individuals."},
    "223": {"code": "INS 223", "name": "Sodium Metabisulphite", "category": "Preservative", "hazard": "CAUTION", "concerns": "May cause headaches, asthma, and skin reactions in sensitive individuals."},
    "282": {"code": "INS 282", "name": "Calcium Propionate", "category": "Preservative", "hazard": "CAUTION", "concerns": "Bread preservative; linked to irritability/restlessness in sensitive children."},
    "321": {"code": "INS 321", "name": "BHT (Butylated Hydroxytoluene)", "category": "Antioxidant", "hazard": "CAUTION", "concerns": "Synthetic preservative; potential liver and endocrine stress under chronic high intake."},
    "621": {"code": "INS 621", "name": "Monosodium Glutamate (MSG)", "category": "Flavor Enhancer", "hazard": "CAUTION", "concerns": "Glutamate flavor enhancer; may trigger headaches/sweating in sensitive individuals."},
    "627": {"code": "INS 627", "name": "Disodium Guanylate", "category": "Flavor Enhancer", "hazard": "CAUTION", "concerns": "Purine-rich; individuals with gout or hyperuricemia should exercise caution."},
    "631": {"code": "INS 631", "name": "Disodium Inosinate", "category": "Flavor Enhancer", "hazard": "CAUTION", "concerns": "Purine precursor; caution for gout sufferers; may be non-vegetarian."},
    "635": {"code": "INS 635", "name": "Disodium 5'-Ribonucleotides", "category": "Flavor Enhancer", "hazard": "CAUTION", "concerns": "Synergistic glutamate enhancer; may cause skin itching in sensitive individuals."},
    "950": {"code": "INS 950", "name": "Acesulfame Potassium", "category": "Sweetener", "hazard": "CAUTION", "concerns": "Calorie-free artificial sweetener; gut microbiome considerations."},
    "951": {"code": "INS 951", "name": "Aspartame", "category": "Sweetener", "hazard": "CAUTION", "concerns": "IARC Group 2B possible carcinogen; contains phenylalanine (risk for PKU)."},
    "954": {"code": "INS 954", "name": "Saccharin", "category": "Sweetener", "hazard": "CAUTION", "concerns": "Synthetic sweetener; microbiome alteration considerations."},
    "955": {"code": "INS 955", "name": "Sucralose", "category": "Sweetener", "hazard": "CAUTION", "concerns": "Chlorinated sweetener; recent interest in thermal stability and gut health."},

    # Safe / Natural Additives
    "300": {"code": "INS 300", "name": "Ascorbic Acid (Vitamin C)", "category": "Antioxidant", "hazard": "SAFE", "concerns": "Essential nutrient and safe natural antioxidant."},
    "322": {"code": "INS 322", "name": "Lecithin (Soy/Sunflower)", "category": "Emulsifier", "hazard": "SAFE", "concerns": "Natural plant-derived lipid emulsifier."},
    "330": {"code": "INS 330", "name": "Citric Acid", "category": "Acidity Regulator", "hazard": "SAFE", "concerns": "Natural fruit acid; completely safe acidulant."},
    "412": {"code": "INS 412", "name": "Guar Gum", "category": "Thickener", "hazard": "SAFE", "concerns": "Natural legume seed fiber."},
    "415": {"code": "INS 415", "name": "Xanthan Gum", "category": "Stabilizer", "hazard": "SAFE", "concerns": "Natural microbial fermentation polysaccharide."},
    "500": {"code": "INS 500", "name": "Sodium Carbonates (Baking Soda)", "category": "Raising Agent", "hazard": "SAFE", "concerns": "Standard mineral raising agent."},
    "503": {"code": "INS 503", "name": "Ammonium Carbonates", "category": "Raising Agent", "hazard": "SAFE", "concerns": "Volatile leavening salt that dissipates on baking."}
}

# Major Allergen Keyword Patterns
ALLERGEN_PATTERNS = {
    "gluten": [r"\bgluten\b", r"\bwheat\b", r"\bbarley\b", r"\brye\b", r"\bmaida\b", r"\battah?\b", r"\bsemolina\b", r"\boats\b"],
    "milk": [r"\bmilk\b", r"\bdairy\b", r"\bcheese\b", r"\bbutter\b", r"\bwhey\b", r"\bcasein\b", r"\byogurt\b", r"\blactose\b", r"\bghee\b", r"\bpaneer\b", r"\bmilk solids\b"],
    "soy": [r"\bsoy\b", r"\bsoya\b", r"\bsoybean\b", r"\bsoy lecithin\b", r"\btofu\b"],
    "peanuts": [r"\bpeanut\b", r"\bpeanuts\b", r"\bgroundnut\b", r"\bgroundnuts\b"],
    "tree_nuts": [r"\balmond\b", r"\bcashew\b", r"\bwalnut\b", r"\bhazelnut\b", r"\bpistachio\b", r"\bpecan\b", r"\bmacadamia\b"],
    "eggs": [r"\begg\b", r"\beggs\b", r"\balbumin\b", r"\begg yolk\b", r"\begg white\b"],
    "fish": [r"\bfish\b", r"\bsalmon\b", r"\btuna\b", r"\bcod\b", r"\banchov\b"],
    "shellfish": [r"\bshrimp\b", r"\bprawn\b", r"\bcrab\b", r"\blobster\b", r"\bclam\b", r"\boyster\b"],
    "sesame": [r"\bsesame\b", r"\btil\b", r"\btahini\b"],
    "sulfites": [r"\bsulfur dioxide\b", r"\bsulphur dioxide\b", r"\bsulfite\b", r"\bsulphite\b", r"\bmetabisulfite\b"]
}

# Non-Vegetarian Identifiers
NON_VEG_PATTERNS = [
    r"\bchicken\b", r"\bmeat\b", r"\bbeef\b", r"\bpork\b", r"\bfish\b", r"\bgelatin\b", 
    r"\bgelatine\b", r"\bcarmine\b", r"\bcochineal\b", r"\blard\b", r"\btallow\b", r"\banchov\b",
    r"\bshrimp\b", r"\bprawn\b", r"\bcrustacean\b", r"\brennet\b"
]

class IngredientEngine:
    """
    Pure ingredient parsing, allergen detection, and additive evaluation engine.
    Independent of database, network, and scoring rules.
    """
    
    @staticmethod
    def extract_additives(text: str) -> List[Dict[str, Any]]:
        """Scans ingredient text for E-numbers, INS codes, and chemical additive names."""
        if not text:
            return []
        
        found_additives = []
        seen_codes = set()
        
        # Matches patterns like "INS 621", "INS-621", "E621", "E 621"
        code_matches = re.findall(r'(?:INS|E)[\s\-_]?([0-9]{3,4}[a-z]?)', text, re.IGNORECASE)
        bracket_matches = re.findall(r'\(([0-9]{3,4}[a-z]?)\)', text, re.IGNORECASE)
        
        all_numeric_matches = set([m.lower() for m in code_matches + bracket_matches])
        
        for num in all_numeric_matches:
            if num in ADDITIVE_REGISTRY and num not in seen_codes:
                found_additives.append(ADDITIVE_REGISTRY[num])
                seen_codes.add(num)
        
        # Check for named additives in text
        text_lower = text.lower()
        for num, item in ADDITIVE_REGISTRY.items():
            if num not in seen_codes:
                name_clean = item["name"].split("(")[0].strip().lower()
                if len(name_clean) > 4 and name_clean in text_lower:
                    found_additives.append(item)
                    seen_codes.add(num)
                    
        return found_additives

    @staticmethod
    def detect_allergens(text: str) -> List[str]:
        """Detects presence of major allergens from declared ingredient text."""
        if not text:
            return []
        
        text_lower = text.lower()
        detected = []
        for allergen, patterns in ALLERGEN_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text_lower):
                    detected.append(allergen)
                    break
        return detected

    @staticmethod
    def is_vegetarian(text: str) -> bool:
        """Determines if the product is free of animal/meat/gelatin products."""
        if not text:
            return True
        text_lower = text.lower()
        for pat in NON_VEG_PATTERNS:
            if re.search(pat, text_lower):
                return False
        return True

    @staticmethod
    def has_palm_oil(text: str) -> bool:
        """Detects presence of palm oil or palm fat fractions."""
        if not text:
            return False
        return bool(re.search(r'\bpalm\s*(?:oil|fat|kernel|olein|stearin)\b', text.lower()))

    @staticmethod
    def evaluate_ingredient_hazards(
        additives: List[Dict[str, Any]],
        ingredients_text: str,
        allergens: List[str],
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates additive hazard penalties, palm oil deductions, and allergen alerts.
        """
        penalty = 0
        flag_reasons = []
        has_avoid_additive = False
        personalized_alerts = []

        # 1. Additive Hazard Evaluation
        for add in additives:
            hazard = add.get("hazard", "SAFE")
            name = add.get("name", add.get("code"))
            if hazard == "AVOID":
                penalty += 20
                has_avoid_additive = True
                flag_reasons.append(f"Contains Hazardous Additive: {name} ({add.get('concerns', 'Health concern')})")
            elif hazard == "CAUTION":
                penalty += 8
                flag_reasons.append(f"Contains Additive of Caution: {name}")

        # 2. Palm Oil
        has_palm = IngredientEngine.has_palm_oil(ingredients_text)
        if has_palm:
            penalty += 6
            flag_reasons.append("Contains Palm Oil / Palm Fat (High saturated fat and environmental impact)")

        # 3. Vegetarian Check
        is_veg = IngredientEngine.is_vegetarian(ingredients_text)
        if not is_veg:
            flag_reasons.append("Contains Non-Vegetarian ingredients (Animal derivative)")

        # 4. User Profile Specific Allergen & Diet Evaluation
        if user_profile:
            user_allergies = user_profile.get("allergies", [])
            for user_alg in user_allergies:
                if user_alg in allergens:
                    personalized_alerts.append(f"CRITICAL ALLERGEN WARNING: Product contains '{user_alg.replace('_', ' ').title()}' which is in your allergen watchlist!")

            if user_profile.get("dietary_preference") == "vegetarian" and not is_veg:
                personalized_alerts.append("Dietary Warning: Product violates your Vegetarian preference.")

        return {
            "penalty": penalty,
            "has_avoid_additive": has_avoid_additive,
            "flag_reasons": flag_reasons,
            "personalized_alerts": personalized_alerts,
            "is_vegetarian": is_veg,
            "has_palm_oil": has_palm
        }
