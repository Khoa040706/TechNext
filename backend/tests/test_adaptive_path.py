import pytest
from app.services.adaptive_service import AdaptiveService, PREREQUISITE_MASTERY_THRESHOLD


def test_difficulty_up_down_rules():
    assert AdaptiveService.adjust_difficulty(0.0) == "easy"
    assert AdaptiveService.adjust_difficulty(0.39) == "easy"
    assert AdaptiveService.adjust_difficulty(0.40) == "medium"
    assert AdaptiveService.adjust_difficulty(0.69) == "medium"
    assert AdaptiveService.adjust_difficulty(0.70) == "hard"
    assert AdaptiveService.adjust_difficulty(1.0) == "hard"


def test_cold_start_empty_evidence_learning_path(client, student_token):
    res = client.get(
        "/api/v1/learning-path",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert res.status_code == 200
    path = res.json()["data"]
    assert path["status"] == "active"
    assert path["recommended_difficulty"] == "easy"
    assert "chào mừng" in path["reason_for_change"].lower() or "khởi đầu" in path["reason_for_change"].lower()


def test_prerequisite_block_in_adaptive_path(client, instructor_token, student_token):
    # 1. Create topic
    t_res = client.post(
        "/api/v1/topics",
        json={"title": "Prereq Topic", "slug": "prereq-topic", "order_index": 10},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    t_id = t_res.json()["data"]["id"]

    # 2. Create Skill Base and Skill Advanced
    s_base = client.post(
        "/api/v1/skills",
        json={"name": "Base Skill", "slug": "base-skill", "topic_id": t_id},
        headers={"Authorization": f"Bearer {instructor_token}"},
    ).json()["data"]["id"]

    s_adv = client.post(
        "/api/v1/skills",
        json={"name": "Advanced Skill", "slug": "adv-skill", "topic_id": t_id},
        headers={"Authorization": f"Bearer {instructor_token}"},
    ).json()["data"]["id"]

    # 3. Add Base Skill as prerequisite to Advanced Skill
    prereq_res = client.post(
        f"/api/v1/skills/{s_adv}/prerequisites",
        json={"prerequisite_skill_id": s_base},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    assert prereq_res.status_code == 200

    # 4. Generate learning path: Base Skill has mastery 0.0 (< 0.60 threshold)
    # The path must block progression to Advanced Skill and target Base Skill!
    path_res = client.get(
        f"/api/v1/learning-path?target_skill_id={s_adv}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert path_res.status_code == 200
    path = path_res.json()["data"]

    # Verify path is directed to Base Skill
    assert path["target_skill_id"] == s_base
    assert "tiên quyết" in path["reason_for_change"].lower()


def test_reinforcement_selected_when_skill_weak(client, instructor_token, student_token):
    # Setup skill and exercise
    t_res = client.post(
        "/api/v1/topics",
        json={"title": "Reinforce Topic", "slug": "reinforce-topic", "order_index": 20},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    t_id = t_res.json()["data"]["id"]

    s_res = client.post(
        "/api/v1/skills",
        json={"name": "Strings Skill", "slug": "strings-skill", "topic_id": t_id},
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    s_id = s_res.json()["data"]["id"]

    ex_res = client.post(
        "/api/v1/exercises",
        json={
            "title": "String Reversal",
            "slug": "str-rev-test",
            "description_markdown": "Test reverse string",
            "skill_id": s_id,
            "topic_id": t_id,
            "is_published": True,
        },
        headers={"Authorization": f"Bearer {instructor_token}"},
    )
    ex_id = ex_res.json()["data"]["id"]

    # Student fails exercise repeatedly
    for _ in range(3):
        client.post(
            f"/api/v1/exercises/{ex_id}/submissions",
            json={"source_code": "error", "total_tests": 2, "passed_tests": 0, "failed_tests": 2},
            headers={"Authorization": f"Bearer {student_token}"},
        )

    # Check that learning path triggers reinforcement for the weak skill
    path_res = client.get(
        "/api/v1/learning-path",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert path_res.status_code == 200
    path = path_res.json()["data"]
    assert path["recommended_difficulty"] == "easy"
    assert "củng cố" in path["reason_for_change"].lower() or "yếu" in path["reason_for_change"].lower()
