from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.db.session import get_db
from app.models.user import Student
from app.schemas.common import ResponseWrapper
from app.schemas.mastery import SkillMasteryRead
from app.services.mastery_service import MasteryService

router = APIRouter()


@router.get("", response_model=ResponseWrapper[List[SkillMasteryRead]])
def get_my_mastery(
    skill_id: Optional[str] = Query(default=None, description="Lọc theo ID kỹ năng cụ thể"),
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Lấy danh sách điểm thành thạo kỹ năng (Skill Mastery) của học viên hiện tại."""
    masteries = MasteryService.get_student_mastery_list(
        db, student_id=student.id, skill_id=skill_id
    )
    items = [SkillMasteryRead.model_validate(m) for m in masteries]
    return ResponseWrapper(data=items)
