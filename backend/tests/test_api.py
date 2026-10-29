import pytest

@pytest.mark.anyio
async def test_root_endpoint(client):
    res = await client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "scanner_endpoint" in data

@pytest.mark.anyio
async def test_health_endpoint(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

@pytest.mark.anyio
async def test_scan_barcode_maggi(client):
    barcode = "8901058852394"
    res = await client.get(f"/api/v1/scanner/{barcode}")
    assert res.status_code == 200
    data = res.json()
    assert data["barcode"] == barcode
    assert "Maggi" in data["name"]
    assert "Nestlé" in data["brand"]
    
    # Separated assessment assertions
    assessment = data["assessment"]
    assert "truthin_score" in assessment
    assert "health_flag" in assessment
    assert assessment["rule_version"] == "2026.1"
    assert isinstance(assessment["flag_reasons"], list)
    assert len(assessment["flag_reasons"]) > 0

    # Separated nutrition facts assertions
    facts = data["nutrition_facts"]
    assert isinstance(facts, dict)
    assert "energy_kcal" in facts
    assert facts["energy_kcal"] == 427.0
    # Provenance assertions
    assert data["source"] in ("local_seed", "openfoodfacts")
    assert "retrieved_at" in data

@pytest.mark.anyio
async def test_scan_barcode_with_user_profile(client, auth_headers):
    barcode = "8901719101038" # Parle-G (valid GS1 check digit)
    headers = auth_headers("default", "demo@yumsure.app")
    
    # Update profile with gluten allergy and diabetes control
    put_res = await client.put("/api/v1/profile/me", json={
        "name": "Diabetic User",
        "dietary_preference": "vegetarian",
        "health_goals": ["diabetes_control"],
        "allergies": ["gluten"]
    }, headers=headers)
    assert put_res.status_code == 200

    # Scan with user token to receive personalized alerts
    res = await client.get(f"/api/v1/scanner/{barcode}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assessment = data["assessment"]
    assert assessment["health_flag"] == "RED"
    assert any("CRITICAL ALLERGEN WARNING" in a for a in assessment["personalized_alerts"])
    assert any("Diabetic Alert" in a for a in assessment["personalized_alerts"])

@pytest.mark.anyio
async def test_analyze_custom_ingredients(client):
    payload = {
        "ingredients_text": "Refined flour, sugar, palm oil, INS 621, INS 102, salt.",
        "product_name": "Mystery Spicy Snack",
        "nutriments": {"sugars": 15.0, "sodium": 650.0}
    }
    res = await client.post("/api/v1/analysis/ingredients", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["health_flag"] == "RED" # INS 102 is an AVOID additive
    codes = [a["code"] for a in data["detected_additives"]]
    assert "INS 621" in codes
    assert "INS 102" in codes

@pytest.mark.anyio
async def test_healthier_alternatives(client):
    # Discover a real product ID dynamically - don't assume ID=1
    product_res = await client.get("/api/v1/products?limit=1")
    assert product_res.status_code == 200
    products = product_res.json()
    if not products:
        pytest.skip("No products seeded yet")
    product_id = products[0]["id"]

    res = await client.get(f"/api/v1/products/{product_id}/alternatives")
    assert res.status_code == 200
    alts = res.json()
    assert isinstance(alts, list)
    if len(alts) > 0:
        assert "score_improvement" in alts[0]

