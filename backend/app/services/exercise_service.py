from sqlalchemy.orm import Session
from app.models.assessment import Submission
from app.schemas.exercise import CodingSubmissionCreate, CodingSubmissionResponse, TestResultRead
from app.repositories.exercise_repo import ExerciseRepository
from app.core.errors import NotFoundError, ValidationError
from app.core.logging import logger


class ExerciseService:
    @staticmethod
    def submit_coding_exercise(
        db: Session,
        student_id: str,
        exercise_id: str,
        payload: CodingSubmissionCreate,
    ) -> CodingSubmissionResponse:
        exercise = ExerciseRepository.get_exercise(db, exercise_id)
        if not exercise:
            raise NotFoundError(f"Không tìm thấy bài tập coding với id '{exercise_id}'")
        if not exercise.is_published:
            raise ValidationError("Bài tập coding này chưa được xuất bản")

        # Extra validation on source code
        if not payload.source_code.strip():
            raise ValidationError("Mã nguồn nộp bài không được để trống")

        if len(payload.source_code) > 65536:
            raise ValidationError("Mã nguồn nộp bài vượt quá kích thước cho phép (tối đa 64 KB)")

        # Validate telemetry counts
        if payload.total_tests < 0 or payload.passed_tests < 0 or payload.failed_tests < 0:
            raise ValidationError("Số lượng test cases trong telemetry không hợp lệ")

        if payload.passed_tests + payload.failed_tests > payload.total_tests:
            raise ValidationError("Tổng số test passed và failed vượt quá total_tests")

        # Determine attempt number
        existing_attempts = ExerciseRepository.get_submission_count(db, student_id, exercise_id)
        attempt_number = existing_attempts + 1

        # Determine submission status
        if payload.compile_error:
            status = "compile_error"
        elif payload.time_limit_error:
            status = "time_limit_exceeded"
        elif payload.runtime_error:
            status = "runtime_error"
        elif payload.total_tests > 0 and payload.passed_tests == payload.total_tests:
            status = "passed"
        else:
            status = "failed"

        # Sanitize error message to prevent excessively large payload
        sanitized_error_message = payload.error_message[:2000] if payload.error_message else None

        telemetry_data = {
            "total_tests": payload.total_tests,
            "passed_tests": payload.passed_tests,
            "failed_tests": payload.failed_tests,
            "compile_error": payload.compile_error,
            "runtime_error": payload.runtime_error,
            "time_limit_error": payload.time_limit_error,
            "error_type": payload.error_type,
            "error_message": sanitized_error_message,
            "execution_time_ms": payload.execution_time_ms,
        }

        # NOTE: Backend enforces execution_source="client_pyodide" and trust_level="untrusted_client"
        submission = ExerciseRepository.create_submission(
            db,
            student_id=student_id,
            exercise_id=exercise_id,
            attempt_number=attempt_number,
            source_code=payload.source_code,
            status=status,
            telemetry=telemetry_data,
        )

        # Create Learning Evidence
        pass_rate = round(payload.passed_tests / payload.total_tests, 4) if payload.total_tests > 0 else 0.0
        is_success = (status == "passed")

        ExerciseRepository.create_learning_evidence(
            db,
            student_id=student_id,
            skill_id=exercise.skill_id,
            evidence_type="coding_submission",
            reference_id=submission.id,
            score=pass_rate,
            success=is_success,
            metadata_json={
                "exercise_id": exercise_id,
                "attempt_number": attempt_number,
                "status": status,
                "passed_tests": payload.passed_tests,
                "total_tests": payload.total_tests,
                "execution_time_ms": payload.execution_time_ms,
            },
        )

        # Trigger Internal Mastery & Adaptive Hooks
        from app.services.mastery_service import MasteryService
        from app.services.adaptive_service import AdaptiveService
        MasteryService.recompute_mastery(db, student_id=student_id, skill_id=exercise.skill_id)
        AdaptiveService.generate_or_update_learning_path(db, student_id=student_id)

        logger.info(
            f"Student '{student_id}' nộp bài '{exercise.slug}', lần {attempt_number}: status={status} "
            f"({payload.passed_tests}/{payload.total_tests} passed, source={submission.execution_source}, "
            f"trust={submission.trust_level})"
        )

        return CodingSubmissionResponse(
            id=submission.id,
            exercise_id=exercise_id,
            student_id=student_id,
            attempt_number=submission.attempt_number,
            status=submission.status,
            execution_source=submission.execution_source,
            trust_level=submission.trust_level,
            submitted_at=submission.submitted_at,
            test_result=TestResultRead.model_validate(submission.test_result),
        )
