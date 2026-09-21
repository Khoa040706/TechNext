def test_admin_accesses_admin_endpoint_success(client, admin_token):
    response = client.get(
        "/api/v1/auth/admin-check",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["authorized"] is True
    assert data["data"]["admin_id"] == "admin-789"


def test_student_rejected_from_admin_endpoint_returns_403(client, student_token):
    response = client.get(
        "/api/v1/auth/admin-check",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["code"] == "PERMISSION_DENIED"
    assert "Yêu cầu một trong các quyền" in data["message"]


def test_instructor_rejected_from_admin_endpoint_returns_403(client, instructor_token):
    response = client.get(
        "/api/v1/auth/admin-check",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["code"] == "PERMISSION_DENIED"
