def test_student_cannot_create_topic(client, student_token):
    res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "title": "Cấu trúc dữ liệu",
            "slug": "data-structures",
            "description": "Các cấu trúc dữ liệu cơ bản",
        },
    )
    assert res.status_code == 403
    assert res.json()["code"] == "PERMISSION_DENIED"


def test_instructor_can_create_topic_and_read(client, instructor_token, student_token):
    # Instructor creates topic
    create_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "title": "Nhập môn Python",
            "slug": "python-intro",
            "description": "Lập trình Python căn bản cho người mới",
            "order_index": 1,
        },
    )
    assert create_res.status_code == 200
    created = create_res.json()["data"]
    topic_id = created["id"]
    assert created["title"] == "Nhập môn Python"
    assert created["slug"] == "python-intro"

    # Duplicate slug returns 422 ValidationError
    dup_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "title": "Nhập môn Python 2",
            "slug": "python-intro",
        },
    )
    assert dup_res.status_code == 422
    assert dup_res.json()["code"] == "VALIDATION_ERROR"

    # Student can read topic detail
    detail_res = client.get(
        f"/api/v1/topics/{topic_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert detail_res.status_code == 200
    assert detail_res.json()["data"]["id"] == topic_id


def test_topic_update_and_archive_visibility(client, instructor_token, student_token):
    # Create topic
    create_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Toán rời rạc", "slug": "discrete-math"},
    )
    topic_id = create_res.json()["data"]["id"]

    # Update description and archive
    update_res = client.put(
        f"/api/v1/topics/{topic_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"description": "Lý thuyết đồ thị và tổ hợp", "is_archived": True},
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["is_archived"] is True

    # Student cannot view archived topic
    student_get = client.get(
        f"/api/v1/topics/{topic_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_get.status_code == 404

    # Instructor CAN view archived topic
    instructor_get = client.get(
        f"/api/v1/topics/{topic_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert instructor_get.status_code == 200


def test_create_concept_for_topic(client, instructor_token):
    # Create topic
    create_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Thuật toán tìm kiếm", "slug": "search-algorithms"},
    )
    topic_id = create_res.json()["data"]["id"]

    # Create concept
    concept_res = client.post(
        f"/api/v1/topics/{topic_id}/concepts",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "title": "Tìm kiếm nhị phân",
            "description": "Thuật toán tìm kiếm trên mảng đã sắp xếp O(log N)",
            "order_index": 1,
        },
    )
    assert concept_res.status_code == 200
    concept_data = concept_res.json()["data"]
    assert concept_data["topic_id"] == topic_id
    assert concept_data["title"] == "Tìm kiếm nhị phân"


def test_delete_topic(client, instructor_token):
    create_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Chủ đề tạm thời", "slug": "temp-topic"},
    )
    topic_id = create_res.json()["data"]["id"]

    del_res = client.delete(
        f"/api/v1/topics/{topic_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert del_res.status_code == 200
    assert del_res.json()["data"]["deleted"] is True

    # Check 404 after deletion
    get_res = client.get(
        f"/api/v1/topics/{topic_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert get_res.status_code == 404


def test_list_topics_pagination(client, student_token):
    res = client.get(
        "/api/v1/topics?page=1&page_size=2",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert "items" in data
    assert "pagination" in data
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["page_size"] == 2

