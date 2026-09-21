from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.api.deps import get_current_user, require_roles
from app.schemas.auth import UserPayload
from app.schemas.common import ResponseWrapper

router = APIRouter()


class SampleValidationModel(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    score: int = Field(..., ge=0, le=100)


@router.get("/me", response_model=ResponseWrapper[UserPayload])
def get_me(current_user: UserPayload = Depends(get_current_user)):
    """Trả về thông tin người dùng hiện tại sau khi xác thực Bearer token"""
    return ResponseWrapper(data=current_user)


@router.get("/admin-check", response_model=ResponseWrapper[dict])
def admin_only_check(admin_user: UserPayload = Depends(require_roles(["admin"]))):
    """Endpoint chỉ cho phép vai trò Admin truy cập"""
    return ResponseWrapper(data={"authorized": True, "admin_id": admin_user.user_id})


@router.post("/test-validation", response_model=ResponseWrapper[SampleValidationModel])
def test_validation(payload: SampleValidationModel):
    """Endpoint thử nghiệm kiểm tra validation của Pydantic"""
    return ResponseWrapper(data=payload)
