from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.db.session import get_db
from app.models.user import Student
from app.schemas.common import ResponseWrapper
from app.schemas.mastery import LearningPathRead, LearningPathItemRead
from app.services.adaptive_service import AdaptiveService

router = APIRouter()


@router.get("", response_model=ResponseWrapper[LearningPathRead])
def get_my_learning_path(
    target_skill_id: Optional[str] = Query(default=None, description="Yêu cầu kiểm tra hoặc định hướng kỹ năng mục tiêu"),
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Lấy lộ trình học tập thích ứng hiện tại của học viên (kèm theo lý do XAI và độ khó động)."""
    path = AdaptiveService.get_or_create_active_path(
        db, student_id=student.id, target_skill_id=target_skill_id
    )

    items = [
        LearningPathItemRead(
            id=item.id,
            item_type=item.item_type,
            item_id=item.item_id,
            title=item.title,
            order_index=item.order_index,
            difficulty=item.difficulty,
            status=item.status,
            reason=item.reason,
        )
        for item in path.items
    ]

    path_data = LearningPathRead(
        id=path.id,
        student_id=path.student_id,
        status=path.status,
        target_skill_id=path.target_skill_id,
        target_skill_name=path.target_skill.name if path.target_skill else None,
        recommended_difficulty=path.recommended_difficulty,
        reason_for_change=path.reason_for_change,
        version=path.version,
        items=items,
        created_at=path.created_at,
        updated_at=path.updated_at,
    )
    return ResponseWrapper(data=path_data)
