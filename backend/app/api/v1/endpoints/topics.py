import math
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.schemas.auth import UserPayload
from app.schemas.common import ResponseWrapper, PaginatedResponse, PaginationMeta
from app.schemas.content import (
    TopicCreate,
    TopicUpdate,
    TopicRead,
    TopicDetailRead,
    ConceptBase,
    ConceptRead,
    LessonRead,
)
from app.repositories.content_repo import ContentRepository
from app.services.content_service import ContentService
from app.models.content import Topic, Concept
from app.core.errors import NotFoundError, ValidationError

router = APIRouter()


@router.get("", response_model=ResponseWrapper[PaginatedResponse[TopicRead]])
def list_topics(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    include_archived: bool = Query(default=False),
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các chủ đề (Topics) học tập. Học viên chỉ xem được chủ đề chưa lưu trữ."""
    # Student cannot view archived topics
    effective_archived = False if current_user.role == "student" else include_archived
    skip = (page - 1) * page_size

    topics, total = ContentRepository.get_topics(
        db, skip=skip, limit=page_size, include_archived=effective_archived
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return ResponseWrapper(
        data=PaginatedResponse(
            items=[TopicRead.model_validate(t) for t in topics],
            pagination=PaginationMeta(
                page=page,
                page_size=page_size,
                total_items=total,
                total_pages=total_pages,
            ),
        )
    )


@router.get("/{topic_id}", response_model=ResponseWrapper[TopicDetailRead])
def get_topic_detail(
    topic_id: str,
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy chi tiết chủ đề kèm danh sách Concepts và Lessons.
    Học viên chỉ thấy các bài học đã xuất bản (is_published=True)."""
    topic = ContentRepository.get_topic_by_id(db, topic_id)
    if not topic:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_id}'")

    if current_user.role == "student" and topic.is_archived:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_id}'")

    concepts = ContentRepository.get_concepts_by_topic(db, topic_id)
    only_published = current_user.role == "student"
    lessons = ContentRepository.get_lessons_by_topic(db, topic_id, only_published=only_published)

    detail_data = TopicDetailRead(
        id=topic.id,
        title=topic.title,
        slug=topic.slug,
        description=topic.description,
        order_index=topic.order_index,
        is_archived=topic.is_archived,
        created_at=topic.created_at,
        updated_at=topic.updated_at,
        concepts=[ConceptRead.model_validate(c) for c in concepts],
        lessons=[LessonRead.model_validate(l) for l in lessons],
    )
    return ResponseWrapper(data=detail_data)


@router.post("", response_model=ResponseWrapper[TopicRead])
def create_topic(
    payload: TopicCreate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Tạo chủ đề mới. Yêu cầu quyền instructor hoặc admin."""
    created = ContentService.create_topic(
        db,
        title=payload.title,
        slug=payload.slug,
        description=payload.description,
        order_index=payload.order_index,
    )
    return ResponseWrapper(data=TopicRead.model_validate(created))


@router.put("/{topic_id}", response_model=ResponseWrapper[TopicRead])
def update_topic(
    topic_id: str,
    payload: TopicUpdate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Cập nhật thông tin chủ đề. Yêu cầu quyền instructor hoặc admin."""
    topic = ContentRepository.get_topic_by_id(db, topic_id)
    if not topic:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_id}'")

    if payload.title is not None:
        topic.title = payload.title
    if payload.description is not None:
        topic.description = payload.description
    if payload.order_index is not None:
        topic.order_index = payload.order_index
    if payload.is_archived is not None:
        topic.is_archived = payload.is_archived

    updated = ContentRepository.update_topic(db, topic)
    return ResponseWrapper(data=TopicRead.model_validate(updated))


@router.delete("/{topic_id}", response_model=ResponseWrapper[dict])
def delete_topic(
    topic_id: str,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Xóa chủ đề khỏi hệ thống. Yêu cầu quyền instructor hoặc admin."""
    topic = ContentRepository.get_topic_by_id(db, topic_id)
    if not topic:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_id}'")

    ContentRepository.delete_topic(db, topic)
    return ResponseWrapper(data={"deleted": True, "topic_id": topic_id})


@router.post("/{topic_id}/concepts", response_model=ResponseWrapper[ConceptRead])
def create_concept_for_topic(
    topic_id: str,
    payload: ConceptBase,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Tạo Concept thuộc một Topic. Yêu cầu quyền instructor hoặc admin."""
    topic = ContentRepository.get_topic_by_id(db, topic_id)
    if not topic:
        raise NotFoundError(f"Không tìm thấy chủ đề '{topic_id}'")

    concept = Concept(
        topic_id=topic_id,
        title=payload.title,
        description=payload.description,
        order_index=payload.order_index,
    )
    created = ContentRepository.create_concept(db, concept)
    return ResponseWrapper(data=ConceptRead.model_validate(created))
