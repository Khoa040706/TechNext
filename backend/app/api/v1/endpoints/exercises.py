import math
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles, get_current_student
from app.db.session import get_db
from app.schemas.auth import UserPayload
from app.models.user import Student
from app.schemas.common import ResponseWrapper, PaginatedResponse, PaginationMeta
from app.schemas.exercise import (
    CodingExerciseCreate,
    CodingExerciseRead,
    CodingExerciseDetailRead,
    CodingExerciseDetailAdminRead,
    TestCaseRead,
    TestCaseAdminRead,
    CodingSubmissionCreate,
    CodingSubmissionResponse,
)
from app.repositories.exercise_repo import ExerciseRepository
from app.services.exercise_service import ExerciseService
from app.core.errors import NotFoundError, ValidationError

router = APIRouter()


@router.get("", response_model=ResponseWrapper[PaginatedResponse[CodingExerciseRead]])
def list_exercises(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    topic_id: Optional[str] = Query(default=None),
    skill_id: Optional[str] = Query(default=None),
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các bài tập lập trình. Học viên chỉ xem được bài tập đã xuất bản."""
    is_published = True if current_user.role == "student" else None
    skip = (page - 1) * page_size

    exercises, total = ExerciseRepository.get_exercises(
        db, skip=skip, limit=page_size, topic_id=topic_id, skill_id=skill_id, is_published=is_published
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    items = [CodingExerciseRead.model_validate(e) for e in exercises]

    return ResponseWrapper(
        data=PaginatedResponse(
            items=items,
            pagination=PaginationMeta(
                page=page,
                page_size=page_size,
                total_items=total,
                total_pages=total_pages,
            ),
        )
    )


@router.get("/{exercise_id}", response_model=ResponseWrapper[dict])
def get_exercise_detail(
    exercise_id: str,
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy chi tiết một bài tập coding.
    Nếu người dùng là học viên: chỉ trả về các test cases công khai (is_public=True) để chạy trong Pyodide worker."""
    exercise = ExerciseRepository.get_exercise(db, exercise_id)
    if not exercise:
        raise NotFoundError(f"Không tìm thấy bài tập coding với id '{exercise_id}'")

    if current_user.role == "student" and not exercise.is_published:
        raise NotFoundError(f"Không tìm thấy bài tập coding với id '{exercise_id}'")

    if current_user.role in ["instructor", "admin"]:
        admin_test_cases = [TestCaseAdminRead.model_validate(tc) for tc in exercise.test_cases]
        admin_detail = CodingExerciseDetailAdminRead(
            id=exercise.id,
            title=exercise.title,
            slug=exercise.slug,
            description_markdown=exercise.description_markdown,
            starter_code=exercise.starter_code,
            difficulty=exercise.difficulty,
            time_limit_ms=exercise.time_limit_ms,
            skill_id=exercise.skill_id,
            topic_id=exercise.topic_id,
            lesson_id=exercise.lesson_id,
            order_index=exercise.order_index,
            is_published=exercise.is_published,
            created_at=exercise.created_at,
            updated_at=exercise.updated_at,
            test_cases=admin_test_cases,
        )
        return ResponseWrapper(data=admin_detail.model_dump(mode="json"))

    # Đối với học viên: chỉ lấy test cases công khai
    public_test_cases = [
        TestCaseRead.model_validate(tc) for tc in exercise.test_cases if tc.is_public
    ]
    student_detail = CodingExerciseDetailRead(
        id=exercise.id,
        title=exercise.title,
        slug=exercise.slug,
        description_markdown=exercise.description_markdown,
        starter_code=exercise.starter_code,
        difficulty=exercise.difficulty,
        time_limit_ms=exercise.time_limit_ms,
        skill_id=exercise.skill_id,
        topic_id=exercise.topic_id,
        lesson_id=exercise.lesson_id,
        order_index=exercise.order_index,
        is_published=exercise.is_published,
        created_at=exercise.created_at,
        updated_at=exercise.updated_at,
        test_cases=public_test_cases,
    )
    return ResponseWrapper(data=student_detail.model_dump(mode="json"))


@router.post("/{exercise_id}/submissions", response_model=ResponseWrapper[CodingSubmissionResponse], status_code=status.HTTP_201_CREATED)
def submit_coding_exercise(
    exercise_id: str,
    submission_in: CodingSubmissionCreate,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Tiếp nhận nộp bài tập coding V1 từ trình duyệt (Pyodide Worker).
    Lưu ý:
    - Backend không thực thi mã nguồn submitted.
    - execution_source luôn được gán cứng là 'client_pyodide'.
    - trust_level luôn được gán cứng là 'untrusted_client'.
    - Sinh learning_evidence cho hệ thống học tập thích ứng."""
    result = ExerciseService.submit_coding_exercise(
        db,
        student_id=student.id,
        exercise_id=exercise_id,
        payload=submission_in,
    )
    return ResponseWrapper(data=result)


@router.post("", response_model=ResponseWrapper[CodingExerciseDetailAdminRead], status_code=status.HTTP_201_CREATED)
def create_exercise(
    exercise_in: CodingExerciseCreate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Tạo mới bài tập coding kèm test cases (Dành cho Giảng viên / Quản trị viên)."""
    # Check duplicate slug
    existing = ExerciseRepository.get_exercise_by_slug(db, exercise_in.slug)
    if existing:
        raise ValidationError(f"Đường dẫn slug '{exercise_in.slug}' đã tồn tại trong hệ thống")

    exercise = ExerciseRepository.create_exercise(db, exercise_in)
    admin_test_cases = [TestCaseAdminRead.model_validate(tc) for tc in exercise.test_cases]
    detail = CodingExerciseDetailAdminRead(
        id=exercise.id,
        title=exercise.title,
        slug=exercise.slug,
        description_markdown=exercise.description_markdown,
        starter_code=exercise.starter_code,
        difficulty=exercise.difficulty,
        time_limit_ms=exercise.time_limit_ms,
        skill_id=exercise.skill_id,
        topic_id=exercise.topic_id,
        lesson_id=exercise.lesson_id,
        order_index=exercise.order_index,
        is_published=exercise.is_published,
        created_at=exercise.created_at,
        updated_at=exercise.updated_at,
        test_cases=admin_test_cases,
    )
    return ResponseWrapper(data=detail)
