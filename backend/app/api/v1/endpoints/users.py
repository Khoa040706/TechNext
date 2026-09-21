from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_profile
from app.db.session import get_db
from app.schemas.auth import UserPayload
from app.schemas.user import CurrentUserResponse, ProfileRead, ProfileUpdate
from app.schemas.common import ResponseWrapper
from app.repositories.user_repo import UserRepository
from app.models.user import Profile

router = APIRouter()


@router.get("/me", response_model=ResponseWrapper[CurrentUserResponse])
def get_my_profile(
    current_user: UserPayload = Depends(get_current_user),
    profile: Profile = Depends(get_current_profile),
):
    """Lấy thông tin người dùng hiện tại, bao gồm Profile và mã ẩn danh Student (nếu là học viên)."""
    response_data = CurrentUserResponse(
        user_id=current_user.user_id,
        email=profile.email,
        role=profile.role,
        profile=ProfileRead.model_validate(profile),
        student=profile.student,
    )
    return ResponseWrapper(data=response_data)


@router.put("/me", response_model=ResponseWrapper[ProfileRead])
def update_my_profile(
    payload: ProfileUpdate,
    profile: Profile = Depends(get_current_profile),
    db: Session = Depends(get_db),
):
    """Cập nhật thông tin hiển thị (display_name) của người dùng hiện tại."""
    updated = UserRepository.update_profile(db, profile, display_name=payload.display_name)
    return ResponseWrapper(data=ProfileRead.model_validate(updated))
