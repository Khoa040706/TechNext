import uuid
from datetime import datetime, timezone
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.assessment import Quiz, Question, QuizAttempt, QuestionResult, LearningEvidence
from app.schemas.quiz import QuizCreate


class QuizRepository:
    @staticmethod
    def get_quiz(db: Session, quiz_id: str) -> Optional[Quiz]:
        stmt = select(Quiz).where(Quiz.id == quiz_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_quizzes(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        topic_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        is_published: Optional[bool] = None,
    ) -> Tuple[List[Quiz], int]:
        stmt = select(Quiz)
        count_stmt = select(func.count(Quiz.id))

        if topic_id:
            stmt = stmt.where(Quiz.topic_id == topic_id)
            count_stmt = count_stmt.where(Quiz.topic_id == topic_id)
        if lesson_id:
            stmt = stmt.where(Quiz.lesson_id == lesson_id)
            count_stmt = count_stmt.where(Quiz.lesson_id == lesson_id)
        if is_published is not None:
            stmt = stmt.where(Quiz.is_published == is_published)
            count_stmt = count_stmt.where(Quiz.is_published == is_published)

        total = db.scalar(count_stmt) or 0
        stmt = stmt.order_by(Quiz.order_index, Quiz.created_at.desc()).offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())
        return items, total

    @staticmethod
    def create_quiz(db: Session, quiz_in: QuizCreate) -> Quiz:
        quiz = Quiz(
            id=str(uuid.uuid4()),
            title=quiz_in.title,
            description=quiz_in.description,
            topic_id=quiz_in.topic_id,
            lesson_id=quiz_in.lesson_id,
            order_index=quiz_in.order_index,
            is_published=quiz_in.is_published,
        )
        db.add(quiz)
        db.flush()

        if quiz_in.questions:
            for idx, q_in in enumerate(quiz_in.questions):
                options_data = [opt.model_dump() for opt in q_in.options]
                question = Question(
                    id=str(uuid.uuid4()),
                    quiz_id=quiz.id,
                    concept_id=q_in.concept_id,
                    skill_id=q_in.skill_id,
                    question_text=q_in.question_text,
                    question_type=q_in.question_type,
                    difficulty=q_in.difficulty,
                    order_index=q_in.order_index if q_in.order_index != 0 else idx,
                    explanation=q_in.explanation,
                    options=options_data,
                )
                db.add(question)

        db.commit()
        db.refresh(quiz)
        return quiz

    @staticmethod
    def get_attempt(db: Session, attempt_id: str) -> Optional[QuizAttempt]:
        stmt = select(QuizAttempt).where(QuizAttempt.id == attempt_id)
        return db.scalars(stmt).first()

    @staticmethod
    def create_attempt(db: Session, student_id: str, quiz_id: str) -> QuizAttempt:
        attempt = QuizAttempt(
            id=str(uuid.uuid4()),
            student_id=student_id,
            quiz_id=quiz_id,
            status="in_progress",
            started_at=datetime.now(timezone.utc),
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    @staticmethod
    def save_quiz_submission(
        db: Session,
        attempt: QuizAttempt,
        score: float,
        total_questions: int,
        correct_answers: int,
        results_data: List[Dict[str, Any]],
    ) -> QuizAttempt:
        attempt.score = score
        attempt.total_questions = total_questions
        attempt.correct_answers = correct_answers
        attempt.status = "completed"
        attempt.submitted_at = datetime.now(timezone.utc)

        for res in results_data:
            q_res = QuestionResult(
                id=str(uuid.uuid4()),
                attempt_id=attempt.id,
                question_id=res["question_id"],
                concept_id=res.get("concept_id"),
                skill_id=res.get("skill_id"),
                selected_option_id=res.get("selected_option_id"),
                is_correct=res["is_correct"],
                response_time_seconds=res.get("response_time_seconds"),
            )
            db.add(q_res)

        db.commit()
        db.refresh(attempt)
        return attempt

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
