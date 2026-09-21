def test_student_cannot_create_lesson(client, student_token, instructor_token):
    # Setup topic
    topic_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Hàm và Module", "slug": "functions-modules"},
    )
    topic_id = topic_res.json()["data"]["id"]

    # Student attempts creation
    create_res = client.post(
        "/api/v1/lessons",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "topic_id": topic_id,
            "title": "Định nghĩa hàm",
            "slug": "defining-functions",
            "content_markdown": "# Cách viết hàm def trong Python\nNội dung chi tiết bài học.",
            "is_published": False,
        },
    )
    assert create_res.status_code == 403
    assert create_res.json()["code"] == "PERMISSION_DENIED"


def test_lesson_publish_visibility_and_access_rules(client, instructor_token, student_token):
    # Create topic
    topic_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Lập trình hướng đối tượng", "slug": "oop-python"},
    )
    topic_id = topic_res.json()["data"]["id"]

    # Create published lesson
    pub_res = client.post(
        "/api/v1/lessons",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "topic_id": topic_id,
            "title": "Class và Object",
            "slug": "class-and-object",
            "content_markdown": "# Lớp và đối tượng\nKhái niệm lập trình hướng đối tượng căn bản.",
            "is_published": True,
            "order_index": 1,
        },
    )
    assert pub_res.status_code == 200
    pub_id = pub_res.json()["data"]["id"]

    # Create draft lesson (unpublished)
    draft_res = client.post(
        "/api/v1/lessons",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "topic_id": topic_id,
            "title": "Đa hình trong OOP",
            "slug": "polymorphism-draft",
            "content_markdown": "# Đa hình (Bản thảo chưa duyệt)\nNội dung đang soạn thảo.",
            "is_published": False,
            "order_index": 2,
        },
    )
    assert draft_res.status_code == 200
    draft_id = draft_res.json()["data"]["id"]

    # 1. Student lists lessons by topic: only sees 1 published lesson
    student_list = client.get(
        f"/api/v1/lessons?topic_id={topic_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_list.status_code == 200
    student_lessons = student_list.json()["data"]
    assert len(student_lessons) == 1
    assert student_lessons[0]["id"] == pub_id

    # 2. Instructor lists lessons by topic: sees both 2 lessons
    instructor_list = client.get(
        f"/api/v1/lessons?topic_id={topic_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert instructor_list.status_code == 200
    assert len(instructor_list.json()["data"]) == 2

    # 3. Student attempts to access draft lesson directly: gets 404
    student_get_draft = client.get(
        f"/api/v1/lessons/{draft_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_get_draft.status_code == 404

    # 4. Instructor accesses draft lesson: gets 200
    instructor_get_draft = client.get(
        f"/api/v1/lessons/{draft_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert instructor_get_draft.status_code == 200
    assert instructor_get_draft.json()["data"]["id"] == draft_id

    # 5. Instructor publishes the draft lesson
    update_res = client.put(
        f"/api/v1/lessons/{draft_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"is_published": True},
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["is_published"] is True

    # 6. Now student can access it
    student_get_published = client.get(
        f"/api/v1/lessons/{draft_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_get_published.status_code == 200
    assert student_get_published.json()["data"]["title"] == "Đa hình trong OOP"


def test_delete_lesson(client, instructor_token):
    # Setup topic & lesson
    topic_res = client.post(
        "/api/v1/topics",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={"title": "Chủ đề xóa bài", "slug": "delete-topic-test"},
    )
    topic_id = topic_res.json()["data"]["id"]

    lesson_res = client.post(
        "/api/v1/lessons",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "topic_id": topic_id,
            "title": "Bài học cần xóa",
            "slug": "lesson-to-delete",
            "content_markdown": "# Bài học tạm\nSẽ xóa ngay.",
            "is_published": True,
        },
    )
    lesson_id = lesson_res.json()["data"]["id"]

    # Delete lesson
    del_res = client.delete(
        f"/api/v1/lessons/{lesson_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert del_res.status_code == 200
    assert del_res.json()["data"]["deleted"] is True

    # Confirm 404
    get_res = client.get(
        f"/api/v1/lessons/{lesson_id}",
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert get_res.status_code == 404
