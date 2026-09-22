from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.mastery import SkillMastery
from app.models.assessment import LearningEvidence
from app.repositories.mastery_repo import MasteryRepository
from app.core.logging import logger

MASTERY_LOGIC_VERSION = "v1.0-rule-baseline"
EVIDENCE_WEIGHTS = {
    "coding_submission": 0.6,
    "quiz_attempt": 0.4,
}


class MasteryService:
    @staticmethod
    def calculate_mastery(evidences: List[LearningEvidence]) -> tuple[float, float, int]:
        """Tính toán mastery score và confidence dựa trên danh sách evidence (đã sort theo thời gian tăng dần).
        Trả về tuple: (mastery_score, confidence, evidence_count)."""
        if not evidences:
            return 0.0, 0.0, 0

        count = len(evidences)
        weighted_sum = 0.0
        weight_total = 0.0

        for i, ev in enumerate(evidences):
            # Recency factor: các evidence gần đây nhất có trọng số cao hơn (tăng dần từ 0.5 đến 1.0)
            recency_factor = 0.5 + 0.5 * ((i + 1) / count)
            type_weight = EVIDENCE_WEIGHTS.get(ev.evidence_type, 0.5)
            effective_weight = type_weight * recency_factor

            # Điểm của evidence (mặc định 0.0 nếu None)
            score = ev.score if ev.score is not None else (1.0 if ev.success else 0.0)
            weighted_sum += score * effective_weight
            weight_total += effective_weight

        raw_mastery = (weighted_sum / weight_total) if weight_total > 0 else 0.0

        # Phạt giảm điểm nếu các lần gần nhất liên tục thất bại
        recent_window = evidences[-3:] if count >= 3 else evidences
        all_recent_failed = all((not e.success or (e.score is not None and e.score < 0.5)) for e in recent_window)
        if all_recent_failed and count >= 2:
            raw_mastery = max(0.0, raw_mastery * 0.8)

        # Giới hạn chuẩn hóa [0.0 - 1.0]
        final_mastery = round(max(0.0, min(1.0, raw_mastery)), 4)

        # Confidence tăng dần theo số lượng bằng chứng (đạt 1.0 khi có từ 5 bằng chứng trở lên)
        confidence = round(min(1.0, count / 5.0), 4)

        return final_mastery, confidence, count

    @staticmethod
    def get_mastery_level(score: float) -> str:
        if score < 0.4:
            return "weak"
        elif score < 0.7:
            return "developing"
        return "mastered"

    @staticmethod
    def recompute_mastery(
        db: Session, student_id: str, skill_id: Optional[str]
    ) -> Optional[SkillMastery]:
        if not skill_id:
            return None

        # Lấy tối đa 10 evidences gần nhất
        evidences = MasteryRepository.get_evidences_for_skill(
            db, student_id=student_id, skill_id=skill_id, limit=10
        )

        score, confidence, count = MasteryService.calculate_mastery(evidences)

        mastery = MasteryRepository.upsert_skill_mastery(
            db,
            student_id=student_id,
            skill_id=skill_id,
            mastery_score=score,
            confidence=confidence,
            evidence_count=count,
            version=MASTERY_LOGIC_VERSION,
        )

        level = MasteryService.get_mastery_level(score)
        logger.info(
            f"Tái tính toán Mastery: student='{student_id}', skill='{skill_id}' => "
            f"score={score}, confidence={confidence}, count={count}, level='{level}' (v={MASTERY_LOGIC_VERSION})"
        )
        return mastery

    @staticmethod
    def get_student_mastery_list(
        db: Session, student_id: str, skill_id: Optional[str] = None
    ) -> List[dict]:
        masteries = MasteryRepository.get_student_masteries(db, student_id, skill_id)
        result = []
        for m in masteries:
            result.append({
                "id": m.id,
                "student_id": m.student_id,
                "skill_id": m.skill_id,
                "skill_name": m.skill.name if m.skill else None,
                "skill_slug": m.skill.slug if m.skill else None,
                "topic_id": m.skill.topic_id if m.skill else None,
                "mastery_score": m.mastery_score,
                "confidence": m.confidence,
                "evidence_count": m.evidence_count,
                "mastery_level": MasteryService.get_mastery_level(m.mastery_score),
                "version": m.version,
                "updated_at": m.updated_at,
            })
        return result
