import uuid
from datetime import datetime, timezone
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.assessment import (
    CodingExercise,
    TestCase,
    Submission,
    TestResult,
    LearningEvidence,
)
from app.schemas.exercise import CodingExerciseCreate


class ExerciseRepository:
    @staticmethod
    def get_exercise(db: Session, exercise_id: str) -> Optional[CodingExercise]:
        stmt = select(CodingExercise).where(CodingExercise.id == exercise_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_exercise_by_slug(db: Session, slug: str) -> Optional[CodingExercise]:
        stmt = select(CodingExercise).where(CodingExercise.slug == slug)
        return db.scalars(stmt).first()

    @staticmethod
    def get_exercises(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        topic_id: Optional[str] = None,
        skill_id: Optional[str] = None,
        is_published: Optional[bool] = None,
    ) -> Tuple[List[CodingExercise], int]:
        stmt = select(CodingExercise)
        count_stmt = select(func.count(CodingExercise.id))

        if topic_id:
            stmt = stmt.where(CodingExercise.topic_id == topic_id)
            count_stmt = count_stmt.where(CodingExercise.topic_id == topic_id)
        if skill_id:
            stmt = stmt.where(CodingExercise.skill_id == skill_id)
            count_stmt = count_stmt.where(CodingExercise.skill_id == skill_id)
        if is_published is not None:
            stmt = stmt.where(CodingExercise.is_published == is_published)
            count_stmt = count_stmt.where(CodingExercise.is_published == is_published)

        total = db.scalar(count_stmt) or 0
        stmt = stmt.order_by(CodingExercise.order_index, CodingExercise.created_at.desc()).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total

    @staticmethod
    def create_exercise(db: Session, exercise_in: CodingExerciseCreate) -> CodingExercise:
        exercise = CodingExercise(
            id=str(uuid.uuid4()),
            title=exercise_in.title,
            slug=exercise_in.slug,
            description_markdown=exercise_in.description_markdown,
            starter_code=exercise_in.starter_code,
            difficulty=exercise_in.difficulty,
            time_limit_ms=exercise_in.time_limit_ms,
            skill_id=exercise_in.skill_id,
            topic_id=exercise_in.topic_id,
            lesson_id=exercise_in.lesson_id,
            order_index=exercise_in.order_index,
            is_published=exercise_in.is_published,
        )
        db.add(exercise)
        db.flush()

        if exercise_in.test_cases:
            for idx, tc_in in enumerate(exercise_in.test_cases):
                test_case = TestCase(
                    id=str(uuid.uuid4()),
                    exercise_id=exercise.id,
                    input_data=tc_in.input_data,
                    expected_output=tc_in.expected_output,
                    is_public=tc_in.is_public,
                    order_index=tc_in.order_index if tc_in.order_index != 0 else idx,
                )
                db.add(test_case)

        db.commit()
        db.refresh(exercise)
        return exercise

    @staticmethod
    def get_submission_count(db: Session, student_id: str, exercise_id: str) -> int:
        stmt = select(func.count(Submission.id)).where(
            Submission.student_id == student_id,
            Submission.exercise_id == exercise_id,
        )
        return db.scalar(stmt) or 0

    @staticmethod
    def create_submission(
        db: Session,
        student_id: str,
        exercise_id: str,
        attempt_number: int,
        source_code: str,
        status: str,
        telemetry: Dict[str, Any],
    ) -> Submission:
        # NOTE: Backend enforces execution_source and trust_level!
        submission = Submission(
            id=str(uuid.uuid4()),
            student_id=student_id,
            exercise_id=exercise_id,
            attempt_number=attempt_number,
            source_code=source_code,
            status=status,
            execution_source="client_pyodide",
            trust_level="untrusted_client",
            submitted_at=datetime.now(timezone.utc),
        )
        db.add(submission)
        db.flush()

        test_result = TestResult(
            id=str(uuid.uuid4()),
            submission_id=submission.id,
            total_tests=telemetry.get("total_tests", 0),
            passed_tests=telemetry.get("passed_tests", 0),
            failed_tests=telemetry.get("failed_tests", 0),
            compile_error=telemetry.get("compile_error", False),
            runtime_error=telemetry.get("runtime_error", False),
            time_limit_error=telemetry.get("time_limit_error", False),
            error_type=telemetry.get("error_type"),
            error_message=telemetry.get("error_message"),
            execution_time_ms=telemetry.get("execution_time_ms"),
        )
        db.add(test_result)

        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def create_learning_evidence(
        db: Session,
        student_id: str,
        skill_id: Optional[str],
        evidence_type: str,
        reference_id: str,
        score: Optional[float],
        success: bool,
        metadata_json: Optional[Dict[str, Any]] = None,
    ) -> LearningEvidence:
        evidence = LearningEvidence(
            id=str(uuid.uuid4()),
            student_id=student_id,
            skill_id=skill_id,
            evidence_type=evidence_type,
            reference_id=reference_id,
            score=score,
            success=success,
            metadata_json=metadata_json,
            created_at=datetime.now(timezone.utc),
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        return evidence
