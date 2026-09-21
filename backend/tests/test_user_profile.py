from app.core.security import create_access_token_for_test
from app.models.user import Profile, Student


def test_get_current_user_profile_and_auto_provisioning(client):
    token = create_access_token_for_test(
        user_id="new-student-001",
        email="student001@example.com",
        role="student",
    )
    response = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    data = res_data["data"]
    assert data["user_id"] == "new-student-001"
    assert data["email"] == "student001@example.com"
    assert data["role"] == "student"
    assert data["profile"]["display_name"] == "student001"
    assert data["profile"]["is_active"] is True
    assert data["student"] is not None
    assert data["student"]["research_id"].startswith("stu_")


def test_update_current_user_display_name(client):
    token = create_access_token_for_test(
        user_id="student-update-name",
        email="update@example.com",
        role="student",
    )
    # First provision
    client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})

    # Update display_name
    update_res = client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"display_name": "Nguyen Van A"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["display_name"] == "Nguyen Van A"

    # Verify updated in get
    get_res = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert get_res.json()["data"]["profile"]["display_name"] == "Nguyen Van A"


def test_disabled_user_returns_401(client, db_session):
    token = create_access_token_for_test(
        user_id="disabled-user-001",
        email="disabled@example.com",
        role="student",
    )
    # First access creates the profile
    client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})

    # Manually disable the profile in DB
    profile = db_session.get(Profile, "disabled-user-001")
    assert profile is not None
    profile.is_active = False
    db_session.commit()

    # Next access should fail with 401
    res = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
    data = res.json()
    assert data["code"] == "AUTHENTICATION_FAILED"
    assert "vô hiệu hóa" in data["message"]


def test_db_role_takes_precedence_over_token_claim(client, db_session):
    # Token claims student, but DB profile is updated to instructor
    token = create_access_token_for_test(
        user_id="promoted-user-001",
        email="promoted@example.com",
        role="student",
    )
    client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})

    # Promote to instructor in DB
    profile = db_session.get(Profile, "promoted-user-001")
    profile.role = "instructor"
    db_session.commit()

    # Access endpoint requiring instructor role
    res = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["data"]["role"] == "instructor"
