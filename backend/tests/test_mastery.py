import pytest
from app.models.content import Topic, Skill
from app.models.assessment import CodingExercise, Quiz
from app.models.mastery import SkillMastery
from app.services.mastery_service import MasteryService, MASTERY_LOGIC_VERSION
from app.core.security import create_access_token_for_test


def test_empty_evidence_mastery(client):
    fresh_student_token = create_access_token_for_test(user_id="student-fresh-empty", role="student")
    res = client.get(
        "/api/v1/mastery",
        headers={"Authorization": f"Bearer {fresh_student_token}"},
    )
    assert res.status_code == 200
    data = res.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 0


def test_mastery_increases_after_success(client, instructor_token, student_token, db_session):
    # 1. Create topic & skill
    topic_res = client.post(
        "/api/v1/topics",
        json={"title": "Mastery Topic", "slug": "mastery-topic", "order_index": 1},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    topic_id = topic_res.json()["data"]["id"]

    skill_res = client.post(
        "/api/v1/skills",
        json={"name": "Variables Skill", "slug": "vars-skill", "topic_id": topic_id},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    skill_id = skill_res.json()["data"]["id"]

    # 2. Create coding exercise for this skill
    ex_res = client.post(
        "/api/v1/exercises",
        json={
            "title": "Variable Assignment",
            "slug": "var-assign-test",
            "description_markdown": "Test exercise description",
            "skill_id": skill_id,
            "topic_id": topic_id,
            "is_published": True,
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    ex_id = ex_res.json()["data"]["id"]

    # 3. Student submits successful coding exercise
    sub_res = client.post(
        f"/api/v1/exercises/{ex_id}/submissions",
        json={
            "source_code": "x = 10",
            "total_tests": 4,
            "passed_tests": 4,
            "failed_tests": 0,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert sub_res.status_code == 201

    # 4. Check mastery endpoint
    mastery_res = client.get(
        "/api/v1/mastery",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert mastery_res.status_code == 200
    masteries = mastery_res.json()["data"]
    assert len(masteries) >= 1
    m = next(item for item in masteries if item["skill_id"] == skill_id)
    assert m["mastery_score"] == 1.0
    assert m["evidence_count"] == 1
    assert m["confidence"] == 0.2  # 1 / 5.0
    assert m["version"] == MASTERY_LOGIC_VERSION


def test_mastery_decreases_after_repeated_failure(client, instructor_token, student_token):
    # Setup topic & skill
    t_res = client.post(
        "/api/v1/topics",
        json={"title": "Failure Topic", "slug": "failure-topic", "order_index": 2},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    topic_id = t_res.json()["data"]["id"]

    s_res = client.post(
        "/api/v1/skills",
        json={"name": "Recursion Skill", "slug": "recursion-skill", "topic_id": topic_id},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    skill_id = s_res.json()["data"]["id"]

    ex_res = client.post(
        "/api/v1/exercises",
        json={
            "title": "Recursion Challenge",
            "slug": "recursion-test",
            "description_markdown": "Test recursion description",
            "skill_id": skill_id,
            "is_published": True,
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    ex_id = ex_res.json()["data"]["id"]

    # 1. First submission succeeds (pass rate = 1.0)
    client.post(
        f"/api/v1/exercises/{ex_id}/submissions",
        json={"source_code": "pass", "total_tests": 3, "passed_tests": 3, "failed_tests": 0},
        headers={"Authorization": f"Bearer {student_token}"},
    )

    # 2. Three consecutive failures
    for _ in range(3):
        client.post(
            f"/api/v1/exercises/{ex_id}/submissions",
            json={"source_code": "fail", "total_tests": 3, "passed_tests": 0, "failed_tests": 3},
            headers={"Authorization": f"Bearer {student_token}"},
        )

    # 3. Check mastery: should be pulled down by failures and recency
    m_res = client.get(
        f"/api/v1/mastery?skill_id={skill_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert m_res.status_code == 200
    m_data = m_res.json()["data"][0]
    assert m_data["evidence_count"] == 4
    assert m_data["mastery_score"] < 0.4  # Pulled down into weak level
    assert m_data["mastery_level"] == "weak"
