def test_missing_auth_token_returns_401(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == "AUTHENTICATION_FAILED"
    assert "Thiếu" in data["message"]


def test_malformed_auth_token_returns_401(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.payload"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == "AUTHENTICATION_FAILED"


def test_expired_auth_token_returns_401(client, expired_token):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == "AUTHENTICATION_FAILED"
    assert "hết hạn" in data["message"]


def test_valid_auth_token_returns_user_profile(client, student_token):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user_id"] == "student-123"
    assert data["data"]["role"] == "student"


def test_invalid_signature_returns_401(client):
    from app.core.security import create_access_token_for_test
    wrong_token = create_access_token_for_test(
        user_id="hacker-user",
        secret="completely-wrong-secret-key-that-does-not-match-32c",
    )
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {wrong_token}"},
    )
    assert response.status_code == 401
    assert response.json()["code"] == "AUTHENTICATION_FAILED"


def test_direct_me_endpoint_returns_current_user_profile(client, student_token):
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user_id"] == "student-123"
    assert data["data"]["role"] == "student"
    assert data["data"]["profile"] is not None

