from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.assessment import Quiz, QuizAttempt
from app.schemas.quiz import QuizSubmitRequest, QuizSubmitResponse, QuestionResultDetail
from app.repositories.quiz_repo import QuizRepository
from app.core.errors import NotFoundError, ValidationError, ConflictError, PermissionDeniedError
from app.core.logging import logger


class QuizService:
    @staticmethod
    def start_attempt(db: Session, student_id: str, quiz_id: str) -> QuizAttempt:
        quiz = QuizRepository.get_quiz(db, quiz_id)
        if not quiz:
            raise NotFoundError(f"Không tìm thấy quiz với id '{quiz_id}'")
        if not quiz.is_published:
            raise ValidationError("Bài quiz này chưa được xuất bản")

        attempt = QuizRepository.create_attempt(db, student_id=student_id, quiz_id=quiz_id)
        logger.info(f"Student '{student_id}' bắt đầu attempt '{attempt.id}' cho Quiz '{quiz_id}'")
        return attempt

    @staticmethod
    def submit_quiz(
        db: Session,
        student_id: str,
        quiz_id: str,
        submit_in: QuizSubmitRequest,
    ) -> QuizSubmitResponse:
        quiz = QuizRepository.get_quiz(db, quiz_id)
        if not quiz:
            raise NotFoundError(f"Không tìm thấy quiz với id '{quiz_id}'")

        attempt = QuizRepository.get_attempt(db, submit_in.attempt_id)
        if not attempt:
            raise NotFoundError(f"Không tìm thấy lượt làm bài '{submit_in.attempt_id}'")

        if attempt.student_id != student_id:
            raise PermissionDeniedError("Lượt làm bài này không thuộc về bạn")

        if attempt.quiz_id != quiz_id:
            raise ValidationError("Lượt làm bài không khớp với bài quiz được yêu cầu")

        # Prevent double-submit
        if attempt.status == "completed":
            raise ConflictError("Lượt làm bài này đã hoàn thành và được nộp trước đó. Không thể nộp lại.")

        question_map = {q.id: q for q in quiz.questions}
        if not question_map:
            raise ValidationError("Bài quiz hiện chưa có câu hỏi nào để chấm điểm")

        # Map student answers
        answers_dict = {ans.question_id: ans for ans in submit_in.answers}

        # Check for invalid question ids
        for q_id in answers_dict:
            if q_id not in question_map:
                raise ValidationError(f"Câu hỏi id '{q_id}' không thuộc bài quiz này")

        results_detail: List[QuestionResultDetail] = []
        db_results_data: List[Dict[str, Any]] = []
        correct_count = 0

        for q in quiz.questions:
            correct_opt = next((opt for opt in q.options if opt.get("is_correct")), None)
            correct_opt_id = correct_opt.get("id") if correct_opt else None

            ans = answers_dict.get(q.id)
            selected_opt_id = ans.selected_option_id if ans else None
            is_correct = (selected_opt_id is not None and selected_opt_id == correct_opt_id)

            if is_correct:
                correct_count += 1

            results_detail.append(
                QuestionResultDetail(
                    question_id=q.id,
                    selected_option_id=selected_opt_id,
                    is_correct=is_correct,
                    correct_option_id=correct_opt_id,
                    explanation=q.explanation,
                )
            )

            db_results_data.append({
                "question_id": q.id,
                "concept_id": q.concept_id,
                "skill_id": q.skill_id,
                "selected_option_id": selected_opt_id,
                "is_correct": is_correct,
                "response_time_seconds": ans.response_time_seconds if ans else None,
            })

        total_questions = len(quiz.questions)
        score = round((correct_count / total_questions) * 100.0, 2)

        # Save submission and question results
        updated_attempt = QuizRepository.save_quiz_submission(
            db,
            attempt=attempt,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_count,
            results_data=db_results_data,
        )

        # Create Learning Evidence
        primary_skill_id = next((q.skill_id for q in quiz.questions if q.skill_id), None)
        QuizRepository.create_learning_evidence(
            db,
            student_id=student_id,
            skill_id=primary_skill_id,
            evidence_type="quiz_attempt",
            reference_id=updated_attempt.id,
            score=round(score / 100.0, 4),
            success=(score >= 70.0),
            metadata_json={
                "quiz_id": quiz_id,
                "score": score,
                "total_questions": total_questions,
                "correct_answers": correct_count,
            },
        )

        # Trigger Internal Mastery & Adaptive Hooks
        from app.services.mastery_service import MasteryService
        from app.services.adaptive_service import AdaptiveService
        MasteryService.recompute_mastery(db, student_id=student_id, skill_id=primary_skill_id)
        AdaptiveService.generate_or_update_learning_path(db, student_id=student_id)

        logger.info(
            f"Student '{student_id}' hoàn thành quiz '{quiz_id}', điểm: {score}/100 ({correct_count}/{total_questions})"
        )

        return QuizSubmitResponse(
            attempt_id=updated_attempt.id,
            quiz_id=quiz_id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_count,
            status=updated_attempt.status,
            submitted_at=updated_attempt.submitted_at,
            results=results_detail,
        )
