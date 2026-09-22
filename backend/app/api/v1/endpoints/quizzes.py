import math
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles, get_current_student
from app.db.session import get_db
from app.schemas.auth import UserPayload
from app.models.user import Student
from app.schemas.common import ResponseWrapper, PaginatedResponse, PaginationMeta
from app.schemas.quiz import (
    QuizCreate,
    QuizRead,
    QuizDetailRead,
    QuizDetailAdminRead,
    QuestionRead,
    QuestionAdminRead,
    QuestionOptionRead,
    QuestionOptionAdminRead,
    QuizAttemptCreateResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
)
from app.repositories.quiz_repo import QuizRepository
from app.services.quiz_service import QuizService
from app.core.errors import NotFoundError

router = APIRouter()


@router.get("", response_model=ResponseWrapper[PaginatedResponse[QuizRead]])
def list_quizzes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    topic_id: Optional[str] = Query(default=None),
    lesson_id: Optional[str] = Query(default=None),
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các bài quiz. Học viên chỉ xem được quiz đã xuất bản."""
    is_published = True if current_user.role == "student" else None
    skip = (page - 1) * page_size

    quizzes, total = QuizRepository.get_quizzes(
        db, skip=skip, limit=page_size, topic_id=topic_id, lesson_id=lesson_id, is_published=is_published
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    items = []
    for q in quizzes:
        item = QuizRead(
            id=q.id,
            title=q.title,
            description=q.description,
            topic_id=q.topic_id,
            lesson_id=q.lesson_id,
            order_index=q.order_index,
            is_published=q.is_published,
            total_questions=len(q.questions),
            created_at=q.created_at,
            updated_at=q.updated_at,
        )
        items.append(item)

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


@router.get("/{quiz_id}", response_model=ResponseWrapper[dict])
def get_quiz_detail(
    quiz_id: str,
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy chi tiết một bài quiz và danh sách câu hỏi.
    Nếu người dùng là học viên: ẩn trường is_correct trong options và explanation để chống lộ đáp án."""
    quiz = QuizRepository.get_quiz(db, quiz_id)
    if not quiz:
        raise NotFoundError(f"Không tìm thấy quiz với id '{quiz_id}'")

    if current_user.role == "student" and not quiz.is_published:
        raise NotFoundError(f"Không tìm thấy quiz với id '{quiz_id}'")

    if current_user.role in ["instructor", "admin"]:
        # Trả về đầy đủ đáp án đúng cho giảng viên / admin
        questions_admin = [
            QuestionAdminRead(
                id=q.id,
                quiz_id=q.quiz_id,
                concept_id=q.concept_id,
                skill_id=q.skill_id,
                question_text=q.question_text,
                question_type=q.question_type,
                difficulty=q.difficulty,
                order_index=q.order_index,
                explanation=q.explanation,
                options=[QuestionOptionAdminRead(**opt) for opt in q.options],
            )
            for q in quiz.questions
        ]
        detail_admin = QuizDetailAdminRead(
            id=quiz.id,
            title=quiz.title,
            description=quiz.description,
            topic_id=quiz.topic_id,
            lesson_id=quiz.lesson_id,
            order_index=quiz.order_index,
            is_published=quiz.is_published,
            total_questions=len(quiz.questions),
            created_at=quiz.created_at,
            updated_at=quiz.updated_at,
            questions=questions_admin,
        )
        return ResponseWrapper(data=detail_admin.model_dump(mode="json"))

    # Đối với student: loại bỏ is_correct và explanation
    questions_student = [
        QuestionRead(
            id=q.id,
            quiz_id=q.quiz_id,
            concept_id=q.concept_id,
            skill_id=q.skill_id,
            question_text=q.question_text,
            question_type=q.question_type,
            difficulty=q.difficulty,
            order_index=q.order_index,
            options=[QuestionOptionRead(id=opt["id"], text=opt["text"]) for opt in q.options],
        )
        for q in quiz.questions
    ]
    detail_student = QuizDetailRead(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        topic_id=quiz.topic_id,
        lesson_id=quiz.lesson_id,
        order_index=quiz.order_index,
        is_published=quiz.is_published,
        total_questions=len(quiz.questions),
        created_at=quiz.created_at,
        updated_at=quiz.updated_at,
        questions=questions_student,
    )
    return ResponseWrapper(data=detail_student.model_dump(mode="json"))


@router.post("/{quiz_id}/attempts", response_model=ResponseWrapper[QuizAttemptCreateResponse], status_code=status.HTTP_201_CREATED)
def start_quiz_attempt(
    quiz_id: str,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Khởi tạo một lượt làm bài mới (Attempt) cho học viên."""
    attempt = QuizService.start_attempt(db, student_id=student.id, quiz_id=quiz_id)
    return ResponseWrapper(data=QuizAttemptCreateResponse.model_validate(attempt))


@router.post("/{quiz_id}/submit", response_model=ResponseWrapper[QuizSubmitResponse])
def submit_quiz(
    quiz_id: str,
    submit_in: QuizSubmitRequest,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Nộp bài quiz, chấm điểm tự động và ghi nhận evidence học tập."""
    result = QuizService.submit_quiz(
        db,
        student_id=student.id,
        quiz_id=quiz_id,
        submit_in=submit_in,
    )
    return ResponseWrapper(data=result)


@router.post("", response_model=ResponseWrapper[QuizDetailAdminRead], status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_in: QuizCreate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Tạo mới bài quiz kèm danh sách câu hỏi (Dành cho Giảng viên / Quản trị viên)."""
    quiz = QuizRepository.create_quiz(db, quiz_in)
    questions_admin = [
        QuestionAdminRead(
            id=q.id,
            quiz_id=q.quiz_id,
            concept_id=q.concept_id,
            skill_id=q.skill_id,
            question_text=q.question_text,
            question_type=q.question_type,
            difficulty=q.difficulty,
            order_index=q.order_index,
            explanation=q.explanation,
            options=[QuestionOptionAdminRead(**opt) for opt in q.options],
        )
        for q in quiz.questions
    ]
    detail = QuizDetailAdminRead(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        topic_id=quiz.topic_id,
        lesson_id=quiz.lesson_id,
        order_index=quiz.order_index,
        is_published=quiz.is_published,
        total_questions=len(quiz.questions),
        created_at=quiz.created_at,
        updated_at=quiz.updated_at,
        questions=questions_admin,
    )
    return ResponseWrapper(data=detail)
