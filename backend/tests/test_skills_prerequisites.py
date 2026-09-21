def test_create_skill_and_duplicate_slug_rejection(client, instructor_token):
    # Create skill 1
    res = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "name": "Biến và kiểu dữ liệu",
            "slug": "variables-data-types",
            "difficulty": "easy",
            "description": "Khai báo biến trong Python",
        },
    )
    assert res.status_code == 200
    assert res.json()["data"]["slug"] == "variables-data-types"

    # Duplicate slug returns 422
    dup_res = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "name": "Kiểu dữ liệu trùng slug",
            "slug": "variables-data-types",
            "difficulty": "medium",
        },
    )
    assert dup_res.status_code == 422
    assert dup_res.json()["code"] == "VALIDATION_ERROR"


def test_self_prerequisite_rejected(client, instructor_token):
    res = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Vòng lặp", "slug": "loops", "difficulty": "easy"},
    )
    skill_id = res.json()["data"]["id"]

    # Try setting skill as its own prerequisite
    prereq_res = client.post(
        f"/api/v1/skills/{skill_id}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": skill_id},
    )
    assert prereq_res.status_code == 422
    assert "chính nó" in prereq_res.json()["message"]


def test_direct_cycle_prevention(client, instructor_token):
    # Skill A and Skill B
    res_a = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng A", "slug": "skill-a", "difficulty": "easy"},
    )
    res_b = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng B", "slug": "skill-b", "difficulty": "medium"},
    )
    id_a = res_a.json()["data"]["id"]
    id_b = res_b.json()["data"]["id"]

    # A requires B: valid
    res_ab = client.post(
        f"/api/v1/skills/{id_a}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_b},
    )
    assert res_ab.status_code == 200

    # Now attempt B requires A: should detect cycle and reject
    res_ba = client.post(
        f"/api/v1/skills/{id_b}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_a},
    )
    assert res_ba.status_code == 422
    data = res_ba.json()
    assert data["code"] == "PREREQUISITE_CYCLE_DETECTED"
    assert "chu trình" in data["message"].lower()


def test_multi_node_cycle_prevention(client, instructor_token):
    # Nodes X -> Y -> Z (X requires Y, Y requires Z)
    res_x = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng X", "slug": "skill-x", "difficulty": "easy"},
    )
    res_y = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng Y", "slug": "skill-y", "difficulty": "medium"},
    )
    res_z = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng Z", "slug": "skill-z", "difficulty": "hard"},
    )
    id_x = res_x.json()["data"]["id"]
    id_y = res_y.json()["data"]["id"]
    id_z = res_z.json()["data"]["id"]

    # X requires Y
    res_xy = client.post(
        f"/api/v1/skills/{id_x}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_y},
    )
    assert res_xy.status_code == 200

    # Y requires Z
    res_yz = client.post(
        f"/api/v1/skills/{id_y}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_z},
    )
    assert res_yz.status_code == 200

    # Now attempt Z requires X -> Cycle X -> Y -> Z -> X!
    res_zx = client.post(
        f"/api/v1/skills/{id_z}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_x},
    )
    assert res_zx.status_code == 422
    assert res_zx.json()["code"] == "PREREQUISITE_CYCLE_DETECTED"


def test_remove_prerequisite(client, instructor_token):
    res_p = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng P", "slug": "skill-p", "difficulty": "easy"},
    )
    res_q = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng Q", "slug": "skill-q", "difficulty": "easy"},
    )
    id_p = res_p.json()["data"]["id"]
    id_q = res_q.json()["data"]["id"]

    # Add prerequisite P requires Q
    client.post(
        f"/api/v1/skills/{id_p}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_q},
    )

    # Remove prerequisite
    del_res = client.delete(
        f"/api/v1/skills/{id_p}/prerequisites/{id_q}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert del_res.status_code == 200
    assert del_res.json()["data"]["removed"] is True

    # Now Q requiring P is safe and should NOT cycle
    res_qp = client.post(
        f"/api/v1/skills/{id_q}/prerequisites",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"prerequisite_skill_id": id_p},
    )
    assert res_qp.status_code == 200


def test_skill_update_and_delete(client, instructor_token):
    res = client.post(
        "/api/v1/skills",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng sửa xóa", "slug": "skill-edit-delete", "difficulty": "easy"},
    )
    skill_id = res.json()["data"]["id"]

    # Update
    update_res = client.put(
        f"/api/v1/skills/{skill_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"name": "Kỹ năng đã sửa", "difficulty": "hard"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["name"] == "Kỹ năng đã sửa"
    assert update_res.json()["data"]["difficulty"] == "hard"

    # Delete
    del_res = client.delete(
        f"/api/v1/skills/{skill_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert del_res.status_code == 200
    assert del_res.json()["data"]["deleted"] is True

    # Confirm 404
    get_res = client.get(
        f"/api/v1/skills/{skill_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert get_res.status_code == 404


def test_skill_detail_and_pagination(client, student_token):
    res = client.get(
        "/api/v1/skills?page=1&page_size=3",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert "items" in data
    assert "pagination" in data
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 3

