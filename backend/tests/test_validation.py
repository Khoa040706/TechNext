def test_valid_input_passes(client):
    payload = {"title": "Biến và Kiểu dữ liệu", "score": 95}
    response = client.post("/api/v1/auth/test-validation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Biến và Kiểu dữ liệu"
    assert data["data"]["score"] == 95


def test_invalid_input_returns_422_with_standard_error(client):
    # score out of range (> 100) and title too short (< 3)
    payload = {"title": "A", "score": 150}
    response = client.post("/api/v1/auth/test-validation", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["code"] == "VALIDATION_ERROR"
    assert "details" in data
    assert "errors" in data["details"]
    assert len(data["details"]["errors"]) >= 2
    assert "X-Request-ID" in response.headers
    assert data["request_id"] == response.headers["X-Request-ID"]
