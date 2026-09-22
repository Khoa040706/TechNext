import pytest
from app.models.assessment import Quiz, QuizAttempt, LearningEvidence


def test_create_and_get_quiz(client, instructor_token, student_token):
    # 1. Instructor creates quiz
    payload = {
        "title": "Python Basics Quiz",
        "description": "Kiểm tra kiến thức cơ bản về biến và kiểu dữ liệu",
        "is_published": True,
        "questions": [
            {
                "question_text": "Trong Python, cú pháp nào dùng để in ra màn hình?",
                "question_type": "single_choice",
                "difficulty": "easy",
                "explanation": "Hàm print() được dùng để in ra console trong Python",
                "options": [
                    {"id": "opt_1", "text": "print('hello')", "is_correct": True},
                    {"id": "opt_2", "text": "echo 'hello'", "is_correct": False},
                    {"id": "opt_3", "text": "console.log('hello')", "is_correct": False},
                ],
            },
            {
                "question_text": "Kiểu dữ liệu của [1, 2, 3] trong Python là gì?",
                "question_type": "single_choice",
                "difficulty": "easy",
                "explanation": "Dấu ngoặc vuông biểu thị danh sách (list)",
                "options": [
                    {"id": "opt_a", "text": "dict", "is_correct": False},
                    {"id": "opt_b", "text": "list", "is_correct": True},
                    {"id": "opt_c", "text": "tuple", "is_correct": False},
                ],
            },
        ],
    }

    create_res = client.post(
        "/api/v1/quizzes",
        json=payload,
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert create_res.status_code == 201
    quiz_data = create_res.json()["data"]
    quiz_id = quiz_data["id"]
    assert len(quiz_data["questions"]) == 2
    # Instructor can see is_correct and explanation
    assert "is_correct" in quiz_data["questions"][0]["options"][0]
    assert quiz_data["questions"][0]["explanation"] is not None

    # 2. Student views quiz detail (Answers and explanations must be hidden)
    get_res = client.get(
        f"/api/v1/quizzes/{quiz_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert get_res.status_code == 200
    student_quiz = get_res.json()["data"]
    assert student_quiz["id"] == quiz_id
    assert len(student_quiz["questions"]) == 2

    # Anti-leak check: is_correct and explanation must NOT exist for student
    for q in student_quiz["questions"]:
        assert "explanation" not in q or q.get("explanation") is None
        for opt in q["options"]:
            assert "is_correct" not in opt


def test_quiz_grading_and_evidence(client, instructor_token, student_token, db_session):
    # Setup quiz
    payload = {
        "title": "Loop Control Quiz",
        "description": "Kiểm tra vòng lặp",
        "is_published": True,
        "questions": [
            {
                "question_text": "Từ khóa nào dùng để thoát khỏi vòng lặp?",
                "difficulty": "easy",
                "explanation": "Từ khóa break kết thúc vòng lặp ngay lập tức",
                "options": [
                    {"id": "q1_opt1", "text": "exit", "is_correct": False},
                    {"id": "q1_opt2", "text": "break", "is_correct": True},
                ],
            },
            {
                "question_text": "Từ khóa nào dùng để bỏ qua lần lặp hiện tại?",
                "difficulty": "easy",
                "explanation": "Từ khóa continue chuyển sang bước lặp tiếp theo",
                "options": [
                    {"id": "q2_opt1", "text": "continue", "is_correct": True},
                    {"id": "q2_opt2", "text": "pass", "is_correct": False},
                ],
            },
        ],
    }
    create_res = client.post(
        "/api/v1/quizzes",
        json=payload,
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    quiz_id = create_res.json()["data"]["id"]

    # 1. Student starts attempt
    attempt_res = client.post(
        f"/api/v1/quizzes/{quiz_id}/attempts",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert attempt_res.status_code == 201
    attempt_id = attempt_res.json()["data"]["id"]
    assert attempt_res.json()["data"]["status"] == "in_progress"

    # 2. Student submits answers: 1 correct (break), 1 incorrect (pass)
    submit_payload = {
        "attempt_id": attempt_id,
        "answers": [
            {"question_id": create_res.json()["data"]["questions"][0]["id"], "selected_option_id": "q1_opt2", "response_time_seconds": 15},
            {"question_id": create_res.json()["data"]["questions"][1]["id"], "selected_option_id": "q2_opt2", "response_time_seconds": 20},
        ],
    }

    submit_res = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit",
        json=submit_payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert submit_res.status_code == 200
    res_data = submit_res.json()["data"]
    assert res_data["score"] == 50.0
    assert res_data["correct_answers"] == 1
    assert res_data["total_questions"] == 2
    assert res_data["status"] == "completed"

    # Results detail verification
    results = res_data["results"]
    assert len(results) == 2
    assert results[0]["is_correct"] is True
    assert results[0]["correct_option_id"] == "q1_opt2"
    assert results[1]["is_correct"] is False
    assert results[1]["correct_option_id"] == "q2_opt1"

    # 3. Verify Learning Evidence created in DB
    evidence = db_session.query(LearningEvidence).filter_by(reference_id=attempt_id).first()
    assert evidence is not None
    assert evidence.evidence_type == "quiz_attempt"
    assert evidence.score == 0.5


def test_quiz_prevent_double_submit(client, instructor_token, student_token):
    # Setup quiz
    create_res = client.post(
        "/api/v1/quizzes",
        json={
            "title": "Double Submit Test",
            "is_published": True,
            "questions": [
                {
                    "question_text": "1 + 1 = ?",
                    "options": [
                        {"id": "o1", "text": "2", "is_correct": True},
                        {"id": "o2", "text": "3", "is_correct": False},
                    ],
                }
            ],
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    quiz_id = create_res.json()["data"]["id"]
    q_id = create_res.json()["data"]["questions"][0]["id"]

    # Start attempt
    att_res = client.post(
        f"/api/v1/quizzes/{quiz_id}/attempts",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    attempt_id = att_res.json()["data"]["id"]

    # Submit first time -> 200 OK
    submit_payload = {
        "attempt_id": attempt_id,
        "answers": [{"question_id": q_id, "selected_option_id": "o1"}],
    }
    sub_1 = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit",
        json=submit_payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert sub_1.status_code == 200

    # Submit second time on same attempt -> 409 Conflict
    sub_2 = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit",
        json=submit_payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert sub_2.status_code == 409
    assert sub_2.json()["code"] == "CONFLICT_ERROR"


def test_quiz_invalid_payload(client, instructor_token, student_token):
    # Setup quiz
    create_res = client.post(
        "/api/v1/quizzes",
        json={
            "title": "Invalid Payload Test",
            "is_published": True,
            "questions": [
                {
                    "question_text": "Test question?",
                    "options": [
                        {"id": "opt1", "text": "Option 1", "is_correct": True},
                        {"id": "opt2", "text": "Option 2", "is_correct": False},
                    ],
                }
            ],
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    quiz_id = create_res.json()["data"]["id"]

    att_res = client.post(
        f"/api/v1/quizzes/{quiz_id}/attempts",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    attempt_id = att_res.json()["data"]["id"]

    # 1. Submitting nonexistent question_id -> 422
    bad_payload = {
        "attempt_id": attempt_id,
        "answers": [{"question_id": "nonexistent-question-id", "selected_option_id": "opt1"}],
    }
    res = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit",
        json=bad_payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 422

    # 2. Missing attempt_id in request -> 422
    res_missing = client.post(
        f"/api/v1/quizzes/{quiz_id}/submit",
        json={"answers": []},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res_missing.status_code == 422


def test_student_cannot_create_quiz(client, student_token):
    res = client.post(
        "/api/v1/quizzes",
        json={"title": "Unauthorized Quiz", "is_published": True},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 403
