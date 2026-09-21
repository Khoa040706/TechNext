import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.schemas.auth import UserPayload
from app.schemas.common import ResponseWrapper, PaginatedResponse, PaginationMeta
from app.schemas.content import (
    SkillCreate,
    SkillUpdate,
    SkillRead,
    SkillPrerequisiteAdd,
    PrerequisiteItem,
)
from app.repositories.content_repo import ContentRepository
from app.services.content_service import ContentService
from app.core.errors import NotFoundError

router = APIRouter()


@router.get("", response_model=ResponseWrapper[PaginatedResponse[SkillRead]])
def list_skills(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy danh sách các kỹ năng (Skills)."""
    skip = (page - 1) * page_size
    skills, total = ContentRepository.get_skills(db, skip=skip, limit=page_size)
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    items = []
    for s in skills:
        items.append(SkillRead.model_validate(s))

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


@router.get("/{skill_id}", response_model=ResponseWrapper[SkillRead])
def get_skill_detail(
    skill_id: str,
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lấy chi tiết kỹ năng và danh sách các kỹ năng tiên quyết."""
    skill = ContentRepository.get_skill_by_id(db, skill_id)
    if not skill:
        raise NotFoundError(f"Không tìm thấy kỹ năng '{skill_id}'")

    return ResponseWrapper(data=SkillRead.model_validate(skill))


@router.post("", response_model=ResponseWrapper[SkillRead])
def create_skill(
    payload: SkillCreate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Tạo kỹ năng mới. Yêu cầu quyền instructor hoặc admin."""
    created = ContentService.create_skill(
        db,
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        difficulty=payload.difficulty,
        concept_id=payload.concept_id,
        topic_id=payload.topic_id,
    )
    return ResponseWrapper(data=SkillRead.model_validate(created))


@router.put("/{skill_id}", response_model=ResponseWrapper[SkillRead])
def update_skill(
    skill_id: str,
    payload: SkillUpdate,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Cập nhật thông tin kỹ năng. Yêu cầu quyền instructor hoặc admin."""
    skill = ContentRepository.get_skill_by_id(db, skill_id)
    if not skill:
        raise NotFoundError(f"Không tìm thấy kỹ năng '{skill_id}'")

    if payload.name is not None:
        skill.name = payload.name
    if payload.description is not None:
        skill.description = payload.description
    if payload.difficulty is not None:
        skill.difficulty = payload.difficulty

    updated = ContentRepository.update_skill(db, skill)
    return ResponseWrapper(data=SkillRead.model_validate(updated))


@router.delete("/{skill_id}", response_model=ResponseWrapper[dict])
def delete_skill(
    skill_id: str,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Xóa kỹ năng khỏi hệ thống. Yêu cầu quyền instructor hoặc admin."""
    skill = ContentRepository.get_skill_by_id(db, skill_id)
    if not skill:
        raise NotFoundError(f"Không tìm thấy kỹ năng '{skill_id}'")

    ContentRepository.delete_skill(db, skill)
    return ResponseWrapper(data={"deleted": True, "skill_id": skill_id})


@router.post("/{skill_id}/prerequisites", response_model=ResponseWrapper[SkillRead])
def add_prerequisite(
    skill_id: str,
    payload: SkillPrerequisiteAdd,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Thêm quan hệ điều kiện tiên quyết (Prerequisite). Có kiểm tra ngăn chặn chu trình (Cycle Prevention)."""
    updated_skill = ContentService.add_skill_prerequisite(
        db,
        skill_id=skill_id,
        prereq_id=payload.prerequisite_skill_id,
    )
    return ResponseWrapper(data=SkillRead.model_validate(updated_skill))


@router.delete("/{skill_id}/prerequisites/{prereq_id}", response_model=ResponseWrapper[dict])
def remove_prerequisite(
    skill_id: str,
    prereq_id: str,
    current_user: UserPayload = Depends(require_roles(["instructor", "admin"])),
    db: Session = Depends(get_db),
):
    """Xóa quan hệ điều kiện tiên quyết giữa hai kỹ năng."""
    removed = ContentRepository.remove_prerequisite(db, skill_id=skill_id, prereq_id=prereq_id)
    if not removed:
        raise NotFoundError(f"Không tìm thấy mối quan hệ tiên quyết giữa '{skill_id}' và '{prereq_id}'")

    return ResponseWrapper(data={"removed": True, "skill_id": skill_id, "prerequisite_skill_id": prereq_id})
