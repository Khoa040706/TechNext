import pytest
from app.models.assessment import CodingExercise, Submission, LearningEvidence


def test_create_and_get_coding_exercise(client, instructor_token, student_token):
    # 1. Instructor creates exercise with public and private test cases
    payload = {
        "title": "Sum of Two Numbers",
        "slug": "sum-two-numbers",
        "description_markdown": "Viết hàm `solve(a, b)` trả về tổng hai số.",
        "starter_code": "def solve(a, b):\n    pass\n",
        "difficulty": "easy",
        "is_published": True,
        "test_cases": [
            {"input_data": "1 2", "expected_output": "3", "is_public": True},
            {"input_data": "5 10", "expected_output": "15", "is_public": True},
            {"input_data": "-1 1", "expected_output": "0", "is_public": False}, # Hidden test case
        ],
    }
    create_res = client.post(
        "/api/v1/exercises",
        json=payload,
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert create_res.status_code == 201
    ex_data = create_res.json()["data"]
    exercise_id = ex_data["id"]
    assert len(ex_data["test_cases"]) == 3

    # 2. Student views exercise: ONLY public test cases (is_public=True) should be returned!
    student_res = client.get(
        f"/api/v1/exercises/{exercise_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_res.status_code == 200
    student_ex = student_res.json()["data"]
    assert len(student_ex["test_cases"]) == 2
    for tc in student_ex["test_cases"]:
        assert "is_public" not in tc or tc.get("is_public") is True


def test_coding_submission_valid_and_forced_attributes(client, instructor_token, student_token, db_session):
    # Setup exercise
    create_res = client.post(
        "/api/v1/exercises",
        json={
            "title": "Square Number",
            "slug": "square-number",
            "description_markdown": "Return n^2",
            "is_published": True,
            "test_cases": [{"input_data": "4", "expected_output": "16", "is_public": True}],
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    exercise_id = create_res.json()["data"]["id"]

    # Student submits valid solution telemetry from Pyodide
    sub_payload = {
        "source_code": "def solve(n):\n    return n * n\n",
        "total_tests": 5,
        "passed_tests": 5,
        "failed_tests": 0,
        "compile_error": False,
        "runtime_error": False,
        "time_limit_error": False,
        "execution_time_ms": 124.5,
    }

    res = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json=sub_payload,
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 201
    data = res.json()["data"]

    # Verify attempt_number is 1
    assert data["attempt_number"] == 1
    assert data["status"] == "passed"

    # CRITICAL: Verify forced execution_source and trust_level
    assert data["execution_source"] == "client_pyodide"
    assert data["trust_level"] == "untrusted_client"
    assert "not official grading" in data["note"].lower() or "client-side" in data["note"].lower()

    # Check telemetry
    assert data["test_result"]["passed_tests"] == 5
    assert data["test_result"]["total_tests"] == 5

    # Verify learning evidence in DB
    submission_id = data["id"]
    evidence = db_session.query(LearningEvidence).filter_by(reference_id=submission_id).first()
    assert evidence is not None
    assert evidence.evidence_type == "coding_submission"
    assert evidence.score == 1.0
    assert evidence.success is True


def test_coding_attempt_increment(client, instructor_token, student_token):
    # Setup exercise
    create_res = client.post(
        "/api/v1/exercises",
        json={
            "title": "Factorial",
            "slug": "factorial",
            "description_markdown": "Calculate n!",
            "is_published": True,
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    exercise_id = create_res.json()["data"]["id"]

    # Submission 1 (fails)
    res1 = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json={
            "source_code": "def solve(n): return n",
            "total_tests": 3,
            "passed_tests": 1,
            "failed_tests": 2,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res1.status_code == 201
    assert res1.json()["data"]["attempt_number"] == 1
    assert res1.json()["data"]["status"] == "failed"

    # Submission 2 (runtime error)
    res2 = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json={
            "source_code": "def solve(n): return 1/0",
            "total_tests": 3,
            "passed_tests": 0,
            "failed_tests": 1,
            "runtime_error": True,
            "error_type": "ZeroDivisionError",
            "error_message": "division by zero",
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res2.status_code == 201
    assert res2.json()["data"]["attempt_number"] == 2
    assert res2.json()["data"]["status"] == "runtime_error"

    # Submission 3 (success)
    res3 = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json={
            "source_code": "def solve(n): return 1 if n<=1 else n*solve(n-1)",
            "total_tests": 3,
            "passed_tests": 3,
            "failed_tests": 0,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res3.status_code == 201
    assert res3.json()["data"]["attempt_number"] == 3
    assert res3.json()["data"]["status"] == "passed"


def test_oversized_source_rejected(client, instructor_token, student_token):
    create_res = client.post(
        "/api/v1/exercises",
        json={"title": "Size Test", "slug": "size-test", "description_markdown": "Test exercise description", "is_published": True},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert create_res.status_code == 201
    exercise_id = create_res.json()["data"]["id"]

    # Create oversized code (> 64 KB = 65,536 bytes)
    oversized_code = "# Comment\n" * 8000  # ~80 KB

    res = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json={
            "source_code": oversized_code,
            "total_tests": 1,
            "passed_tests": 1,
            "failed_tests": 0,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    # Should be rejected with 422
    assert res.status_code == 422


def test_invalid_telemetry_rejected(client, instructor_token, student_token):
    create_res = client.post(
        "/api/v1/exercises",
        json={"title": "Telemetry Test", "slug": "telemetry-test", "description_markdown": "Test telemetry description", "is_published": True},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert create_res.status_code == 201
    exercise_id = create_res.json()["data"]["id"]

    # 1. passed + failed > total_tests
    res1 = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json={
            "source_code": "def solve(): pass",
            "total_tests": 5,
            "passed_tests": 4,
            "failed_tests": 3, # 4 + 3 = 7 > 5
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res1.status_code == 422

    # 2. negative test count
    res2 = client.post(
        f"/api/v1/exercises/{exercise_id}/submissions",
        json={
            "source_code": "def solve(): pass",
            "total_tests": -1,
            "passed_tests": 0,
            "failed_tests": 0,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res2.status_code == 422
