import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.mastery import SkillMastery, LearningPath, LearningPathItem
from app.models.assessment import LearningEvidence


class MasteryRepository:
    @staticmethod
    def get_skill_mastery(db: Session, student_id: str, skill_id: str) -> Optional[SkillMastery]:
        stmt = select(SkillMastery).where(
            SkillMastery.student_id == student_id,
            SkillMastery.skill_id == skill_id,
        )
        return db.scalars(stmt).first()

    @staticmethod
    def get_student_masteries(
        db: Session, student_id: str, skill_id: Optional[str] = None
    ) -> List[SkillMastery]:
        stmt = select(SkillMastery).where(SkillMastery.student_id == student_id)
        if skill_id:
            stmt = stmt.where(SkillMastery.skill_id == skill_id)
        stmt = stmt.order_by(SkillMastery.mastery_score.asc())
        return list(db.scalars(stmt).all())

    @staticmethod
    def upsert_skill_mastery(
        db: Session,
        student_id: str,
        skill_id: str,
        mastery_score: float,
        confidence: float,
        evidence_count: int,
        version: str = "v1.0-rule-baseline",
    ) -> SkillMastery:
        mastery = MasteryRepository.get_skill_mastery(db, student_id, skill_id)
        if not mastery:
            mastery = SkillMastery(
                id=str(uuid.uuid4()),
                student_id=student_id,
                skill_id=skill_id,
                mastery_score=mastery_score,
                confidence=confidence,
                evidence_count=evidence_count,
                version=version,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(mastery)
        else:
            mastery.mastery_score = mastery_score
            mastery.confidence = confidence
            mastery.evidence_count = evidence_count
            mastery.version = version
            mastery.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(mastery)
        return mastery

    @staticmethod
    def get_evidences_for_skill(
        db: Session, student_id: str, skill_id: str, limit: int = 10
    ) -> List[LearningEvidence]:
        stmt = (
            select(LearningEvidence)
            .where(
                LearningEvidence.student_id == student_id,
                LearningEvidence.skill_id == skill_id,
            )
            .order_by(LearningEvidence.created_at.desc())
            .limit(limit)
        )
        # Return chronological order for time-weighted processing
        evidences = list(db.scalars(stmt).all())
        evidences.reverse()
        return evidences

    @staticmethod
    def get_active_learning_path(db: Session, student_id: str) -> Optional[LearningPath]:
        stmt = (
            select(LearningPath)
            .where(
                LearningPath.student_id == student_id,
                LearningPath.status == "active",
            )
            .order_by(LearningPath.created_at.desc())
        )
        return db.scalars(stmt).first()

    @staticmethod
    def supersede_active_paths(db: Session, student_id: str) -> None:
        stmt = select(LearningPath).where(
            LearningPath.student_id == student_id,
            LearningPath.status == "active",
        )
        active_paths = db.scalars(stmt).all()
        for p in active_paths:
            p.status = "superseded"
            p.updated_at = datetime.now(timezone.utc)
        db.flush()

    @staticmethod
    def create_learning_path(
        db: Session,
        student_id: str,
        target_skill_id: Optional[str],
        recommended_difficulty: str,
        reason_for_change: str,
        items_data: List[Dict[str, Any]],
        version: str = "v1.0-rule-baseline",
    ) -> LearningPath:
        MasteryRepository.supersede_active_paths(db, student_id)

        path = LearningPath(
            id=str(uuid.uuid4()),
            student_id=student_id,
            status="active",
            target_skill_id=target_skill_id,
            recommended_difficulty=recommended_difficulty,
            reason_for_change=reason_for_change,
            version=version,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(path)
        db.flush()

        for idx, item in enumerate(items_data):
            path_item = LearningPathItem(
                id=str(uuid.uuid4()),
                path_id=path.id,
                item_type=item["item_type"],
                item_id=item["item_id"],
                title=item["title"],
                order_index=item.get("order_index", idx),
                difficulty=item.get("difficulty", "easy"),
                status=item.get("status", "pending"),
                reason=item.get("reason"),
            )
            db.add(path_item)

        db.commit()
        db.refresh(path)
        return path
