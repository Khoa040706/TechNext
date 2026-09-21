from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.schemas.auth import UserPayload
from app.schemas.common import ResponseWrapper
from app.schemas.content import LessonCreate, LessonUpdate, LessonRead
from app.repositories.content_repo import ContentRepository
from app.services.content_service import ContentService
from app.models.content import Lesson
from app.core.errors import NotFoundError

router = APIRouter()


@router.get("", response_model=ResponseWrapper[List[LessonRead]])
def list_lessons(
    topic_id: str = Query(..., description="ID của chủ đề"),
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các bài học thuộc một chủ đề. Học viên chỉ xem được bài đã xuất bản (is_published=True)."""
    only_published = current_user.role == "student"
    lessons = ContentRepository.get_lessons_by_topic(db, topic_id=topic_id, only_published=only_published)
    return ResponseWrapper(data=[LessonRead.model_validate(l) for l in lessons])


@router.get("/{lesson_id}", response_model=ResponseWrapper[LessonRead])
def get_lesson_detail(
    lesson_id: str,
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy nội dung chi tiết của một bài học. Áp dụng quy tắc truy cập: Học viên không được xem bài bản nháp (draft)."""
    lesson = ContentService.get_lesson(db, lesson_id=lesson_id, user_role=current_user.role)
    return ResponseWrapper(data=LessonRead.model_validate(lesson))


@router.post("", response_model=ResponseWrapper[LessonRead])
def create_lesson(
    payload: LessonCreate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Tạo bài học mới. Yêu cầu quyền instructor hoặc admin."""
    topic = ContentRepository.get_topic_by_id(db, payload.topic_id)
    if not topic:
        raise NotFoundError(f"Không tìm thấy chủ đề '{payload.topic_id}'")

    lesson = Lesson(
        topic_id=payload.topic_id,
        title=payload.title,
        slug=payload.slug,
        content_markdown=payload.content_markdown,
        order_index=payload.order_index,
        is_published=payload.is_published,
    )
    created = ContentRepository.create_lesson(db, lesson)
    return ResponseWrapper(data=LessonRead.model_validate(created))


@router.put("/{lesson_id}", response_model=ResponseWrapper[LessonRead])
def update_lesson(
    lesson_id: str,
    payload: LessonUpdate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Cập nhật bài học hoặc thay đổi trạng thái xuất bản (publish state). Yêu cầu quyền instructor hoặc admin."""
    lesson = ContentRepository.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise NotFoundError(f"Không tìm thấy bài học '{lesson_id}'")

    if payload.title is not None:
        lesson.title = payload.title
    if payload.slug is not None:
        lesson.slug = payload.slug
    if payload.content_markdown is not None:
        lesson.content_markdown = payload.content_markdown
    if payload.order_index is not None:
        lesson.order_index = payload.order_index
    if payload.is_published is not None:
        lesson.is_published = payload.is_published

    updated = ContentRepository.update_lesson(db, lesson)
    return ResponseWrapper(data=LessonRead.model_validate(updated))


@router.delete("/{lesson_id}", response_model=ResponseWrapper[dict])
def delete_lesson(
    lesson_id: str,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Xóa bài học khỏi hệ thống. Yêu cầu quyền instructor hoặc admin."""
    lesson = ContentRepository.get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise NotFoundError(f"Không tìm thấy bài học '{lesson_id}'")

    ContentRepository.delete_lesson(db, lesson)
    return ResponseWrapper(data={"deleted": True, "lesson_id": lesson_id})
