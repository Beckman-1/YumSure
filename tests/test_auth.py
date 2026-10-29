import pytest
import uuid

@pytest.mark.anyio
async def test_register_and_login(client):
    """Verify user registration and authentication flow."""
    unique_email = f"tester_{uuid.uuid4().hex[:8]}@yumsure.app"
    user_payload = {
        "email": unique_email,
        "password": "Password123!",
        "name": "Auth Tester",
        "dietary_preference": "vegan",
        "health_goals": ["clean_eating"],
        "allergies": ["peanuts"]
    }

    # 1. Register
    reg_res = await client.post("/api/v1/auth/register", json=user_payload)
    assert reg_res.status_code == 201
    data = reg_res.json()
    assert "access_token" in data
    assert data["user"]["email"] == unique_email
    assert data["user"]["dietary_preference"] == "vegan"

    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Duplicate registration should fail
    dup_res = await client.post("/api/v1/auth/register", json=user_payload)
    assert dup_res.status_code == 409

    # 3. Login with valid password
    login_res = await client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 4. Login with invalid password
    bad_login = await client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401

    # 5. Access /auth/me
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == unique_email

@pytest.mark.anyio
async def test_unauthenticated_access_denied(client):
    """Verify protected endpoints reject requests without token."""
    res_me = await client.get("/api/v1/auth/me")
    assert res_me.status_code == 401

    res_profile = await client.get("/api/v1/profile/me")
    assert res_profile.status_code == 401

    res_history = await client.get("/api/v1/history")
    assert res_history.status_code == 401

@pytest.mark.anyio
async def test_cross_user_isolation(client):
    """Verify User A cannot access or modify User B's records."""
    # Register User A
    uid_a = uuid.uuid4().hex[:6]
    res_a = await client.post("/api/v1/auth/register", json={
        "email": f"user_iso_a_{uid_a}@yumsure.app",
        "password": "PasswordA123!",
        "name": "User Alpha"
    })
    assert res_a.status_code == 201
    token_a = res_a.json()["access_token"]
    headers_user_a = {"Authorization": f"Bearer {token_a}"}

    # Register User B
    uid_b = uuid.uuid4().hex[:6]
    res_b = await client.post("/api/v1/auth/register", json={
        "email": f"user_iso_b_{uid_b}@yumsure.app",
        "password": "PasswordB123!",
        "name": "User Beta"
    })
    assert res_b.status_code == 201
    token_b = res_b.json()["access_token"]
    headers_user_b = {"Authorization": f"Bearer {token_b}"}

    # User A performs a scan with their token
    scan_res = await client.get("/api/v1/scanner/8901058852394", headers=headers_user_a)
    assert scan_res.status_code == 200

    # User A checks their history
    hist_a = await client.get("/api/v1/history", headers=headers_user_a)
    assert hist_a.status_code == 200
    items_a = hist_a.json()
    assert len(items_a) > 0
    item_id = items_a[0]["id"]

    # User B checks their history (must be empty or not contain User A's item)
    hist_b = await client.get("/api/v1/history", headers=headers_user_b)
    assert hist_b.status_code == 200
    items_b_ids = [item["id"] for item in hist_b.json()]
    assert item_id not in items_b_ids

    # User B attempts to favorite User A's scan item -> 404 unauthorized
    patch_res = await client.patch(
        f"/api/v1/history/{item_id}/favorite", 
        json={"is_favorite": True}, 
        headers=headers_user_b
    )
    assert patch_res.status_code == 404

    # User B attempts to delete User A's scan item -> must not delete
    del_res = await client.delete(f"/api/v1/history/{item_id}", headers=headers_user_b)
    assert del_res.status_code == 204 # 204 or no-op on non-owned items

    # User A verifies their item is still intact
    hist_a_again = await client.get("/api/v1/history", headers=headers_user_a)
    assert any(item["id"] == item_id for item in hist_a_again.json())
