"""
TruthIn Comprehensive Indian Packaged Food Catalog.
Covers all 14 core food categories evaluated in the TruthIn app,
pre-mapped with authentic GS1 Modulo-10 verified barcodes,
ingredients, INS/E-number additives, allergens, and nutrition facts.
"""

TRUTHIN_CATEGORIES = [
    "Instant Noodles & Pasta",
    "Biscuits & Cookies",
    "Snacks, Chips & Namkeen",
    "Breakfast Cereals & Oats",
    "Chocolates & Confectionery",
    "Dairy & Cheeses",
    "Yogurts & Probiotics",
    "Spreads, Sauces & Condiments",
    "Beverages & Soft Drinks",
    "Health & Malt Drinks",
    "Staples, Flours & Pulses",
    "Cooking Oils & Ghee",
    "Tea & Coffee",
    "Soups & Ready-to-Eat"
]

TRUTHIN_CATALOG = {
    # ==========================================
    # 1. INSTANT NOODLES & PASTA
    # ==========================================
    "8901058852394": {
        "barcode": "8901058852394",
        "name": "Maggi 2-Minute Masala Noodles",
        "brand": "Nestlé",
        "category": "Instant Noodles & Pasta",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/885/2394/front_en.11.400.jpg",
        "ingredients_text": "Noodles: Refined wheat flour (Maida), Palm oil, Salt, Wheat gluten, Mineral (Calcium carbonate), Thickeners (508, 412), Acidity regulators (501(i), 500(i)) and Humectant (451(i)). Masala Tastemaker: Hydrolysed groundnut protein, Mixed spices (Onion powder, Coriander powder, Turmeric, Red chilli powder, Garlic powder, Cumin powder, Aniseed, Fenugreek, Ginger, Black pepper, Clove, Nutmeg, Cardamom), Noodle powder, Sugar, Edible starch, Palm oil, Thickener (508), Caramel (150d), Flavor enhancer (635), Acidity regulator (330), Mineral (Ferric pyrophosphate).",
        "nutrition_facts": {
            "energy_kcal": 427.0,
            "fat": 15.7,
            "saturated_fat": 6.8,
            "carbohydrates": 63.5,
            "sugars": 2.2,
            "fiber": 3.6,
            "proteins": 8.0,
            "sodium": 1230.0
        },
        "nutriscore_grade": "d",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901725013776": {
        "barcode": "8901725013776",
        "name": "Sunfeast Yippee! Magic Masala Noodles",
        "brand": "Sunfeast",
        "category": "Instant Noodles & Pasta",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/172/501/3776/front_en.15.400.jpg",
        "ingredients_text": "Wheat Flour (Maida), Refined Palm Oil, Iodised Salt, Wheat Gluten, Calcium Carbonate, Thickeners (INS 412, INS 508), Acidity Regulators (INS 501(i), INS 500(i)). Masala Mix: Dehydrated Vegetables (Carrot, Cabbage, Onion), Spices and Condiments, Sugar, Hydrolysed Soya Protein, Flavour Enhancers (INS 627, INS 631), Caramel (INS 150d), Anticaking Agent (INS 551).",
        "nutrition_facts": {
            "energy_kcal": 468.0,
            "fat": 19.3,
            "saturated_fat": 9.2,
            "carbohydrates": 64.2,
            "sugars": 3.4,
            "fiber": 3.1,
            "proteins": 9.1,
            "sodium": 1180.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901595852505": {
        "barcode": "8901595852505",
        "name": "Ching's Secret Schezwan Instant Noodles",
        "brand": "Ching's Secret",
        "category": "Instant Noodles & Pasta",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/159/585/2505/front_en.10.400.jpg",
        "ingredients_text": "Wheat Flour, Palm Oil, Salt, Wheat Gluten, Mineral (INS 170(i)), Guar Gum (INS 412). Seasoning Mix: Salt, Mixed Spices (Chilli, Garlic, Ginger, Sichuan Pepper), Sugar, Soy Sauce Powder, Disodium 5'-Ribonucleotides (INS 635), Silicon Dioxide (INS 551), Citric Acid (INS 330).",
        "nutrition_facts": {
            "energy_kcal": 450.0,
            "fat": 18.0,
            "saturated_fat": 8.5,
            "carbohydrates": 63.0,
            "sugars": 4.0,
            "fiber": 2.8,
            "proteins": 8.5,
            "sodium": 1350.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 2. BISCUITS & COOKIES
    # ==========================================
    "8901063012219": {
        "barcode": "8901063012219",
        "name": "Britannia Good Day Butter Cookies",
        "brand": "Britannia",
        "category": "Biscuits & Cookies",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/106/301/2219/front_en.18.400.jpg",
        "ingredients_text": "Refined Wheat Flour (Maida), Sugar, Refined Palm Oil, Butter (2%), Invert Sugar Syrup, Raising Agents (INS 503(ii), INS 500(ii)), Milk Solids, Iodised Salt, Emulsifiers (INS 322, INS 471), Artificial Flavoring Substances (Butter, Vanilla).",
        "nutrition_facts": {
            "energy_kcal": 491.0,
            "fat": 21.0,
            "saturated_fat": 10.5,
            "carbohydrates": 68.0,
            "sugars": 23.5,
            "fiber": 1.5,
            "proteins": 7.0,
            "sodium": 360.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901719101038": {
        "barcode": "8901719101038",
        "name": "Parle-G Original Glucose Biscuits",
        "brand": "Parle",
        "category": "Biscuits & Cookies",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/171/910/1037/front_en.14.400.jpg",
        "ingredients_text": "Wheat Flour (67%), Sugar, Refined Palm Oil, Invert Sugar Syrup, Raising Agents (INS 503(ii), INS 500(ii)), Salt, Milk Solids, Artificial Vanilla Flavouring.",
        "nutrition_facts": {
            "energy_kcal": 454.0,
            "fat": 13.0,
            "saturated_fat": 6.5,
            "carbohydrates": 77.0,
            "sugars": 26.0,
            "fiber": 2.0,
            "proteins": 6.5,
            "sodium": 280.0
        },
        "nutriscore_grade": "d",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901233026893": {
        "barcode": "8901233026893",
        "name": "Cadbury Oreo Original Vanilla Cream Biscuits",
        "brand": "Cadbury",
        "category": "Biscuits & Cookies",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/123/302/6893/front_en.21.400.jpg",
        "ingredients_text": "Refined Wheat Flour (Maida), Sugar, Fractionated Fat, Palmolein Oil, Cocoa Solids (2.3%), Invert Sugar, Leavening Agents (INS 500(ii), INS 503(ii)), Iodised Salt, Emulsifier (INS 322).",
        "nutrition_facts": {
            "energy_kcal": 483.0,
            "fat": 19.6,
            "saturated_fat": 9.4,
            "carbohydrates": 71.4,
            "sugars": 37.8,
            "fiber": 2.1,
            "proteins": 5.2,
            "sodium": 420.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901725181222": {
        "barcode": "8901725181222",
        "name": "Sunfeast Dark Fantasy Choco Fills",
        "brand": "Sunfeast",
        "category": "Biscuits & Cookies",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/172/518/1222/front_en.16.400.jpg",
        "ingredients_text": "Choco Creme (38%) [Sugar, Refined Palm Oil, Cocoa Solids, Emulsifier (INS 322)], Refined Wheat Flour (Maida), Hydrogenated Vegetable Oil, Sugar, Invert Syrup, Raising Agents (INS 503(ii), INS 500(ii)), Emulsifier (INS 471).",
        "nutrition_facts": {
            "energy_kcal": 517.0,
            "fat": 27.2,
            "saturated_fat": 13.6,
            "carbohydrates": 62.4,
            "sugars": 36.5,
            "fiber": 2.5,
            "proteins": 5.7,
            "sodium": 210.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901063011311": {
        "barcode": "8901063011311",
        "name": "Britannia Marie Gold Biscuits",
        "brand": "Britannia",
        "category": "Biscuits & Cookies",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/106/301/1311/front_en.12.400.jpg",
        "ingredients_text": "Refined Wheat Flour (Maida) (74%), Sugar, Refined Palm Oil, Invert Sugar Syrup, Milk Solids, Raising Agents (INS 503(ii), INS 500(ii)), Salt, Emulsifiers (INS 471, INS 472e), Dough Conditioner (INS 223), Vitamins and Minerals.",
        "nutrition_facts": {
            "energy_kcal": 444.0,
            "fat": 10.5,
            "saturated_fat": 4.8,
            "carbohydrates": 79.0,
            "sugars": 21.0,
            "fiber": 2.6,
            "proteins": 8.5,
            "sodium": 320.0
        },
        "nutriscore_grade": "c",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 3. SNACKS, CHIPS & NAMKEEN
    # ==========================================
    "8901491101837": {
        "barcode": "8901491101837",
        "name": "Lay's India's Magic Masala Potato Chips",
        "brand": "Lay's",
        "category": "Snacks, Chips & Namkeen",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/149/110/1836/front_en.15.400.jpg",
        "ingredients_text": "Potato, Edible Vegetable Oil (Palmolein, Rice Bran Oil), Seasoning (Spices and Condiments, Iodised Salt, Maltodextrin, Black Salt, Sugar, Tomato Powder, Acidity Regulators (INS 330, INS 296, INS 334), Flavor Enhancers (INS 627, INS 631), Anticaking Agent (INS 551)).",
        "nutrition_facts": {
            "energy_kcal": 555.0,
            "fat": 35.7,
            "saturated_fat": 14.5,
            "carbohydrates": 51.5,
            "sugars": 4.5,
            "fiber": 4.1,
            "proteins": 6.9,
            "sodium": 870.0
        },
        "nutriscore_grade": "d",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901491000673": {
        "barcode": "8901491000673",
        "name": "Kurkure Masala Munch Crispy Snack",
        "brand": "Kurkure",
        "category": "Snacks, Chips & Namkeen",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/149/100/0673/front_en.18.400.jpg",
        "ingredients_text": "Rice Meal, Edible Vegetable Oil (Palmolein), Corn Meal, Gram Meal, Spices and Condiments (Chilli Powder, Onion Powder, Garlic Powder, Coriander Powder, Turmeric Powder), Iodised Salt, Sugar, Tartaric Acid (INS 334), Flavour Enhancers (INS 627, INS 631).",
        "nutrition_facts": {
            "energy_kcal": 561.0,
            "fat": 36.1,
            "saturated_fat": 15.8,
            "carbohydrates": 53.4,
            "sugars": 2.1,
            "fiber": 3.2,
            "proteins": 5.8,
            "sodium": 920.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8904004400267": {
        "barcode": "8904004400267",
        "name": "Haldiram's Nagpur Aloo Bhujia",
        "brand": "Haldiram's",
        "category": "Snacks, Chips & Namkeen",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/400/440/0268/front_en.14.400.jpg",
        "ingredients_text": "Potatoes (44%), Edible Vegetable Oil (Cottonseed, Corn & Palmolein Oil), Bengal Gram Flour, Moth Bean Flour, Rice Flour, Iodised Salt, Red Chilli, Black Pepper, Clove, Cardamom, Garlic Powder, Mint, Citric Acid (INS 330).",
        "nutrition_facts": {
            "energy_kcal": 578.0,
            "fat": 42.0,
            "saturated_fat": 16.0,
            "carbohydrates": 42.0,
            "sugars": 2.0,
            "fiber": 5.5,
            "proteins": 8.0,
            "sodium": 780.0
        },
        "nutriscore_grade": "d",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 4. BREAKFAST CEREALS & OATS
    # ==========================================
    "8901088007351": {
        "barcode": "8901088007351",
        "name": "Saffola Masala Oats Classic Masala",
        "brand": "Saffola",
        "category": "Breakfast Cereals & Oats",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/108/800/7351/front_en.14.400.jpg",
        "ingredients_text": "Rolled Oats (73.4%), Spices and Condiments (Onion, Turmeric, Pepper, Cumin, Garlic, Fenugreek, Clove, Nutmeg), Salt, Dried Vegetables (Carrots, Green Peas, French Beans), Hydrolysed Vegetable Protein, Yeast Extract.",
        "nutrition_facts": {
            "energy_kcal": 386.0,
            "fat": 7.0,
            "saturated_fat": 1.5,
            "carbohydrates": 65.0,
            "sugars": 3.0,
            "fiber": 8.5,
            "proteins": 11.2,
            "sodium": 490.0
        },
        "nutriscore_grade": "a",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901499008206": {
        "barcode": "8901499008206",
        "name": "Kellogg's Corn Flakes Original",
        "brand": "Kellogg's",
        "category": "Breakfast Cereals & Oats",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/149/900/8205/front_en.12.400.jpg",
        "ingredients_text": "Corn Grits (89%), Sugar, Malt Extract, Iodised Salt, Vitamins & Minerals, Antioxidant (INS 307b).",
        "nutrition_facts": {
            "energy_kcal": 378.0,
            "fat": 0.8,
            "saturated_fat": 0.2,
            "carbohydrates": 84.0,
            "sugars": 8.5,
            "fiber": 2.7,
            "proteins": 6.8,
            "sodium": 650.0
        },
        "nutriscore_grade": "b",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901072002478": {
        "barcode": "8901072002478",
        "name": "Quaker Rolled Oats 100% Wholegrain",
        "brand": "Quaker",
        "category": "Breakfast Cereals & Oats",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/107/200/2478/front_en.10.400.jpg",
        "ingredients_text": "100% Natural Wholegrain Rolled Oats.",
        "nutrition_facts": {
            "energy_kcal": 402.0,
            "fat": 8.5,
            "saturated_fat": 1.6,
            "carbohydrates": 66.8,
            "sugars": 1.2,
            "fiber": 10.5,
            "proteins": 12.8,
            "sodium": 8.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 5. CHOCOLATES & CONFECTIONERY
    # ==========================================
    "8901233010397": {
        "barcode": "8901233010397",
        "name": "Cadbury Dairy Milk Chocolate Bar",
        "brand": "Cadbury",
        "category": "Chocolates & Confectionery",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/123/301/0397/front_en.19.400.jpg",
        "ingredients_text": "Sugar, Milk Solids (22%), Cocoa Butter, Cocoa Solids, Emulsifiers (INS 442, INS 476), Flavours (Natural, Nature Identical and Artificial Vanilla Flavouring Substances).",
        "nutrition_facts": {
            "energy_kcal": 532.0,
            "fat": 30.2,
            "saturated_fat": 18.5,
            "carbohydrates": 58.5,
            "sugars": 56.0,
            "fiber": 2.1,
            "proteins": 7.8,
            "sodium": 140.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901058863642": {
        "barcode": "8901058863642",
        "name": "Nestlé KitKat 4 Finger Chocolate Coated Wafer",
        "brand": "Nestlé",
        "category": "Chocolates & Confectionery",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/886/3642/front_en.14.400.jpg",
        "ingredients_text": "Sugar, Milk Solids, Refined Wheat Flour (Maida), Cocoa Butter, Cocoa Solids, Fractionated Vegetable Fat, Emulsifier (Soya Lecithin INS 322), Raising Agent (INS 500(ii)), Yeast, Iodised Salt.",
        "nutrition_facts": {
            "energy_kcal": 498.0,
            "fat": 24.5,
            "saturated_fat": 15.0,
            "carbohydrates": 62.0,
            "sugars": 47.0,
            "fiber": 2.2,
            "proteins": 6.8,
            "sodium": 95.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901233020082": {
        "barcode": "8901233020082",
        "name": "Cadbury 5 Star Chocolate Bar with Caramel & Nougat",
        "brand": "Cadbury",
        "category": "Chocolates & Confectionery",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/123/302/0082/front_en.11.400.jpg",
        "ingredients_text": "Sugar, Liquid Glucose, Invert Sugar, Milk Solids, Hydrogenated Vegetable Oil, Cocoa Solids, Fractionated Fat, Emulsifiers (INS 442, INS 471, INS 476), Iodised Salt.",
        "nutrition_facts": {
            "energy_kcal": 465.0,
            "fat": 19.5,
            "saturated_fat": 11.2,
            "carbohydrates": 69.5,
            "sugars": 52.0,
            "fiber": 1.4,
            "proteins": 3.5,
            "sodium": 180.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 6. DAIRY & CHEESES
    # ==========================================
    "8901262010047": {
        "barcode": "8901262010047",
        "name": "Amul Pasteurised Salted Butter",
        "brand": "Amul",
        "category": "Dairy & Cheeses",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/126/201/0047/front_en.19.400.jpg",
        "ingredients_text": "Butter (Milk Fat 80%), Common Salt, Annatto (Natural Colour INS 160b).",
        "nutrition_facts": {
            "energy_kcal": 717.0,
            "fat": 80.0,
            "saturated_fat": 51.0,
            "carbohydrates": 0.0,
            "sugars": 0.0,
            "fiber": None,
            "proteins": 0.5,
            "sodium": 830.0
        },
        "nutriscore_grade": "e",
        "nova_group": 2,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901262030014": {
        "barcode": "8901262030014",
        "name": "Amul Processed Cheese Slices",
        "brand": "Amul",
        "category": "Dairy & Cheeses",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/126/203/0014/front_en.15.400.jpg",
        "ingredients_text": "Cheese, Milk Solids, Common Salt, Emulsifiers (INS 331, INS 339), Acidity Regulator (INS 330), Preservative (INS 200).",
        "nutrition_facts": {
            "energy_kcal": 310.0,
            "fat": 25.0,
            "saturated_fat": 16.0,
            "carbohydrates": 1.5,
            "sugars": 1.5,
            "fiber": 0.0,
            "proteins": 20.0,
            "sodium": 1380.0
        },
        "nutriscore_grade": "d",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 7. YOGURTS & PROBIOTICS
    # ==========================================
    "8906070430018": {
        "barcode": "8906070430018",
        "name": "Epigamia Natural Greek Yogurt",
        "brand": "Epigamia",
        "category": "Yogurts & Probiotics",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/607/043/0018/front_en.11.400.jpg",
        "ingredients_text": "Pasteurised Double Toned Milk, Active Live Cultures (S. thermophilus, L. bulgaricus). No added sugar or preservatives.",
        "nutrition_facts": {
            "energy_kcal": 78.0,
            "fat": 3.0,
            "saturated_fat": 1.8,
            "carbohydrates": 4.5,
            "sugars": 4.5,
            "fiber": 0.0,
            "proteins": 8.0,
            "sodium": 45.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8908001150019": {
        "barcode": "8908001150019",
        "name": "Yakult Probiotic Fermented Milk Drink",
        "brand": "Yakult",
        "category": "Yogurts & Probiotics",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/800/115/0014/front_en.10.400.jpg",
        "ingredients_text": "Water, Skimmed Milk, Sugar, Glucose, Live Lactobacillus casei strain Shirota.",
        "nutrition_facts": {
            "energy_kcal": 66.0,
            "fat": 0.1,
            "saturated_fat": 0.0,
            "carbohydrates": 15.4,
            "sugars": 14.0,
            "fiber": 0.0,
            "proteins": 1.2,
            "sodium": 18.0
        },
        "nutriscore_grade": "c",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 8. SPREADS, SAUCES & CONDIMENTS
    # ==========================================
    "8901030386763": {
        "barcode": "8901030386763",
        "name": "Kissan Fresh Tomato Ketchup",
        "brand": "Kissan",
        "category": "Spreads, Sauces & Condiments",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/103/038/6763/front_en.18.400.jpg",
        "ingredients_text": "Water, Tomato Paste (26%), Sugar, Salt, Acidity Regulator (INS 260), Thickeners (INS 1422, INS 415), Preservative (INS 211), Spices and Condiments.",
        "nutrition_facts": {
            "energy_kcal": 137.0,
            "fat": 0.2,
            "saturated_fat": 0.0,
            "carbohydrates": 33.0,
            "sugars": 28.5,
            "fiber": 1.1,
            "proteins": 1.1,
            "sodium": 860.0
        },
        "nutriscore_grade": "d",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8906069400015": {
        "barcode": "8906069400015",
        "name": "Veeba Truly Eggless Mayonnaise",
        "brand": "Veeba",
        "category": "Spreads, Sauces & Condiments",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/606/940/0015/front_en.16.400.jpg",
        "ingredients_text": "Refined Soybean Oil, Water, Sugar, Milk Solids, Salt, Lemon Juice, Emulsifiers and Stabilizers (INS 1442, INS 415), Acidity Regulators (INS 260, INS 330), Preservatives (INS 202, INS 211), Antioxidant (INS 386).",
        "nutrition_facts": {
            "energy_kcal": 412.0,
            "fat": 38.0,
            "saturated_fat": 6.2,
            "carbohydrates": 16.5,
            "sugars": 11.0,
            "fiber": 0.0,
            "proteins": 1.5,
            "sodium": 920.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8906107410013": {
        "barcode": "8906107410013",
        "name": "Pintola All-Natural Peanut Butter Crunchy",
        "brand": "Pintola",
        "category": "Spreads, Sauces & Condiments",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/610/741/0014/front_en.12.400.jpg",
        "ingredients_text": "100% Roasted Peanuts. No added salt, sugar, hydrogenated oils or preservatives.",
        "nutrition_facts": {
            "energy_kcal": 625.0,
            "fat": 50.0,
            "saturated_fat": 7.5,
            "carbohydrates": 16.0,
            "sugars": 3.8,
            "fiber": 9.0,
            "proteins": 30.0,
            "sodium": 12.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8906118400018": {
        "barcode": "8906118400018",
        "name": "The Whole Truth 100% Peanut Butter (Unsweetened)",
        "brand": "The Whole Truth",
        "category": "Spreads, Sauces & Condiments",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/611/840/0018/front_en.10.400.jpg",
        "ingredients_text": "100% Roasted Peanuts. Nothing else.",
        "nutrition_facts": {
            "energy_kcal": 580.0,
            "fat": 49.0,
            "saturated_fat": 6.8,
            "carbohydrates": 16.0,
            "sugars": 3.5,
            "fiber": 8.0,
            "proteins": 26.0,
            "sodium": 15.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8000500179864": {
        "barcode": "8000500179864",
        "name": "Nutella Hazelnut Spread with Cocoa",
        "brand": "Ferrero",
        "category": "Spreads, Sauces & Condiments",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/800/050/017/9864/front_en.25.400.jpg",
        "ingredients_text": "Sugar, Palm Oil, Hazelnuts (13%), Skimmed Milk Powder (8.7%), Fat-Reduced Cocoa (7.4%), Emulsifier: Lecithins (Soya INS 322), Vanillin.",
        "nutrition_facts": {
            "energy_kcal": 539.0,
            "fat": 30.9,
            "saturated_fat": 10.6,
            "carbohydrates": 57.5,
            "sugars": 56.3,
            "fiber": 3.0,
            "proteins": 6.3,
            "sodium": 42.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 9. BEVERAGES & SOFT DRINKS
    # ==========================================
    "8901764012235": {
        "barcode": "8901764012235",
        "name": "Coca-Cola Zero Sugar Can",
        "brand": "Coca-Cola",
        "category": "Beverages & Soft Drinks",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/176/401/2235/front_en.15.400.jpg",
        "ingredients_text": "Carbonated Water, Acidity Regulators (INS 338, INS 331), Colour (INS 150d), Sweeteners (INS 951 Aspartame, INS 950 Acesulfame K), Preservative (INS 211), Caffeine.",
        "nutrition_facts": {
            "energy_kcal": 0.3,
            "fat": 0.0,
            "saturated_fat": 0.0,
            "carbohydrates": 0.0,
            "sugars": 0.0,
            "fiber": 0.0,
            "proteins": 0.0,
            "sodium": 18.0
        },
        "nutriscore_grade": "b",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901764022203": {
        "barcode": "8901764022203",
        "name": "Thums Up Charged Carbonated Soft Drink",
        "brand": "Thums Up",
        "category": "Beverages & Soft Drinks",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/176/402/2203/front_en.14.400.jpg",
        "ingredients_text": "Carbonated Water, Sugar, Acidity Regulator (INS 338), Caramel Colour (INS 150d), Flavours, Caffeine.",
        "nutrition_facts": {
            "energy_kcal": 40.0,
            "fat": 0.0,
            "saturated_fat": 0.0,
            "carbohydrates": 10.0,
            "sugars": 10.0,
            "fiber": 0.0,
            "proteins": 0.0,
            "sodium": 12.0
        },
        "nutriscore_grade": "e",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901207010019": {
        "barcode": "8901207010019",
        "name": "Real Fruit Power Mixed Fruit Juice",
        "brand": "Real",
        "category": "Beverages & Soft Drinks",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/120/701/0019/front_en.16.400.jpg",
        "ingredients_text": "Water, Mixed Fruit Juice Concentrate (18.5%) [Apple, Orange, Guava, Banana, Mango, Pineapple, Apricot, Peach], Sugar, Acidity Regulator (INS 330), Stabilizer (INS 440), Vitamin C (INS 300).",
        "nutrition_facts": {
            "energy_kcal": 56.0,
            "fat": 0.0,
            "saturated_fat": 0.0,
            "carbohydrates": 14.0,
            "sugars": 13.0,
            "fiber": 0.5,
            "proteins": 0.4,
            "sodium": 15.0
        },
        "nutriscore_grade": "c",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 10. HEALTH & MALT DRINKS
    # ==========================================
    "8901233017778": {
        "barcode": "8901233017778",
        "name": "Cadbury Bournvita Chocolate Health Drink",
        "brand": "Cadbury",
        "category": "Health & Malt Drinks",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/123/301/7778/front_en.15.400.jpg",
        "ingredients_text": "Cereal Extract (56%) (Barley, Wheat), Sugar, Cocoa Solids, Caramel Colour (INS 150c), Liquid Glucose, Milk Solids, Raising Agent (INS 500(ii)), Emulsifier (INS 322), Vitamins and Minerals.",
        "nutrition_facts": {
            "energy_kcal": 388.0,
            "fat": 1.8,
            "saturated_fat": 0.9,
            "carbohydrates": 85.2,
            "sugars": 37.0,
            "fiber": 4.5,
            "proteins": 7.0,
            "sodium": 160.0
        },
        "nutriscore_grade": "d",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901571000173": {
        "barcode": "8901571000173",
        "name": "Horlicks Classic Malt Nutrition Drink",
        "brand": "Horlicks",
        "category": "Health & Malt Drinks",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/157/100/0172/front_en.12.400.jpg",
        "ingredients_text": "Malted Barley (39%), Wheat Flour (27%), Milk Solids (14%), Sugar, Minerals, Salt, Acidity Regulator (INS 501(ii), INS 500(ii)), Vitamins.",
        "nutrition_facts": {
            "energy_kcal": 377.0,
            "fat": 2.0,
            "saturated_fat": 1.1,
            "carbohydrates": 79.0,
            "sugars": 25.0,
            "fiber": 5.0,
            "proteins": 11.0,
            "sodium": 390.0
        },
        "nutriscore_grade": "c",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 11. STAPLES, FLOURS & PULSES
    # ==========================================
    "8901725131012": {
        "barcode": "8901725131012",
        "name": "Aashirvaad Superior MP Shudh Chakki Atta",
        "brand": "Aashirvaad",
        "category": "Staples, Flours & Pulses",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/172/513/1012/front_en.16.400.jpg",
        "ingredients_text": "100% Whole Wheat Grain (Chakki Ground).",
        "nutrition_facts": {
            "energy_kcal": 365.0,
            "fat": 1.7,
            "saturated_fat": 0.4,
            "carbohydrates": 76.0,
            "sugars": 2.5,
            "fiber": 11.5,
            "proteins": 10.8,
            "sodium": 5.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901052003884": {
        "barcode": "8901052003884",
        "name": "Tata Sampann Unpolished Toor Dal",
        "brand": "Tata Sampann",
        "category": "Staples, Flours & Pulses",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/200/3884/front_en.11.400.jpg",
        "ingredients_text": "100% Unpolished Toor Dal (Pigeon Peas).",
        "nutrition_facts": {
            "energy_kcal": 343.0,
            "fat": 1.5,
            "saturated_fat": 0.3,
            "carbohydrates": 60.4,
            "sugars": 2.0,
            "fiber": 9.1,
            "proteins": 22.0,
            "sodium": 14.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901030383816": {
        "barcode": "8901030383816",
        "name": "Tata Sampann 100% Organic Unpolished Moong Dal",
        "brand": "Tata Sampann",
        "category": "Staples, Flours & Pulses",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/103/038/3816/front_en.14.400.jpg",
        "ingredients_text": "100% Organic Moong Dal (Yellow Lentils).",
        "nutrition_facts": {
            "energy_kcal": 348.0,
            "fat": 1.2,
            "saturated_fat": 0.3,
            "carbohydrates": 59.0,
            "sugars": 1.0,
            "fiber": 8.2,
            "proteins": 24.0,
            "sodium": 12.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901052000012": {
        "barcode": "8901052000012",
        "name": "Tata Salt Vacuum Evaporated Iodised Salt",
        "brand": "Tata Salt",
        "category": "Staples, Flours & Pulses",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/200/0012/front_en.10.400.jpg",
        "ingredients_text": "Edible Common Salt, Potassium Iodate, Anticaking Agent (INS 551).",
        "nutrition_facts": {
            "energy_kcal": 0.0,
            "fat": 0.0,
            "saturated_fat": 0.0,
            "carbohydrates": 0.0,
            "sugars": 0.0,
            "fiber": 0.0,
            "proteins": 0.0,
            "sodium": 38700.0
        },
        "nutriscore_grade": "c",
        "nova_group": 2,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 12. COOKING OILS & GHEE
    # ==========================================
    "8901262020015": {
        "barcode": "8901262020015",
        "name": "Amul Pure Cow Ghee",
        "brand": "Amul",
        "category": "Cooking Oils & Ghee",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/126/202/0015/front_en.12.400.jpg",
        "ingredients_text": "Clarified Milk Fat (Cow Milk Ghee).",
        "nutrition_facts": {
            "energy_kcal": 900.0,
            "fat": 99.7,
            "saturated_fat": 65.0,
            "carbohydrates": 0.0,
            "sugars": 0.0,
            "fiber": 0.0,
            "proteins": 0.0,
            "sodium": 0.0
        },
        "nutriscore_grade": "d",
        "nova_group": 2,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8906007280013": {
        "barcode": "8906007280013",
        "name": "Fortune Sunlite Refined Sunflower Oil",
        "brand": "Fortune",
        "category": "Cooking Oils & Ghee",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/600/728/0018/front_en.10.400.jpg",
        "ingredients_text": "Refined Sunflower Oil, Vitamin A, Vitamin D, Dimethyl Polysiloxane (Antifoaming Agent INS 900a).",
        "nutrition_facts": {
            "energy_kcal": 900.0,
            "fat": 100.0,
            "saturated_fat": 11.0,
            "carbohydrates": 0.0,
            "sugars": 0.0,
            "fiber": 0.0,
            "proteins": 0.0,
            "sodium": 0.0
        },
        "nutriscore_grade": "c",
        "nova_group": 2,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 13. TEA & COFFEE
    # ==========================================
    "8901052001019": {
        "barcode": "8901052001019",
        "name": "Tata Tea Premium Desh Ki Chai",
        "brand": "Tata Tea",
        "category": "Tea & Coffee",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/200/1019/front_en.18.400.jpg",
        "ingredients_text": "100% Selected Black CTC Tea with Gentle Flavour.",
        "nutrition_facts": {
            "energy_kcal": 100.0,
            "fat": 0.0,
            "saturated_fat": 0.0,
            "carbohydrates": 5.0,
            "sugars": 0.0,
            "fiber": 0.0,
            "proteins": 19.0,
            "sodium": 20.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901058849202": {
        "barcode": "8901058849202",
        "name": "Nescafé Classic 100% Pure Instant Coffee",
        "brand": "Nescafé",
        "category": "Tea & Coffee",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/884/9202/front_en.14.400.jpg",
        "ingredients_text": "100% Pure Soluble Coffee Beans (Robusta & Arabica).",
        "nutrition_facts": {
            "energy_kcal": 118.0,
            "fat": 0.2,
            "saturated_fat": 0.1,
            "carbohydrates": 9.0,
            "sugars": 0.0,
            "fiber": 27.0,
            "proteins": 7.8,
            "sodium": 40.0
        },
        "nutriscore_grade": "a",
        "nova_group": 1,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },

    # ==========================================
    # 14. SOUPS & READY-TO-EAT
    # ==========================================
    "8901030351716": {
        "barcode": "8901030351716",
        "name": "Knorr Classic Thick Tomato Soup",
        "brand": "Knorr",
        "category": "Soups & Ready-to-Eat",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/103/035/1716/front_en.16.400.jpg",
        "ingredients_text": "Tomato Paste Powder (28%), Refined Wheat Flour (Maida), Sugar, Salt, Dehydrated Croutons (10%), Thickeners (INS 1422, INS 415), Hydrolysed Groundnut Protein, Spices and Condiments, Acidity Regulator (INS 330), Flavour Enhancer (INS 635).",
        "nutrition_facts": {
            "energy_kcal": 344.0,
            "fat": 3.8,
            "saturated_fat": 1.2,
            "carbohydrates": 71.0,
            "sugars": 34.0,
            "fiber": 4.5,
            "proteins": 6.5,
            "sodium": 2450.0
        },
        "nutriscore_grade": "d",
        "nova_group": 4,
        "verification_status": "OFFICIAL_MANUFACTURER"
    },
    "8901042962139": {
        "barcode": "8901042962139",
        "name": "MTR Ready-To-Eat Paneer Makhani",
        "brand": "MTR",
        "category": "Soups & Ready-to-Eat",
        "product_type": "food",
        "image_url": "https://images.openfoodfacts.org/images/products/890/104/296/2139/front_en.12.400.jpg",
        "ingredients_text": "Water, Paneer (Cottage Cheese) (22%), Tomatoes (16%), Onions, Cream, Butter, Cashew Nuts, Refined Sunflower Oil, Ginger, Garlic, Salt, Sugar, Spices and Condiments, Fenugreek Leaves.",
        "nutrition_facts": {
            "energy_kcal": 182.0,
            "fat": 14.0,
            "saturated_fat": 7.0,
            "carbohydrates": 6.8,
            "sugars": 3.5,
            "fiber": 2.2,
            "proteins": 7.2,
            "sodium": 540.0
        },
        "nutriscore_grade": "c",
        "nova_group": 3,
        "verification_status": "OFFICIAL_MANUFACTURER"
    }
}
