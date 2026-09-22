from typing import List, Callable
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_supabase_token
from app.core.errors import AuthenticationError, PermissionDeniedError
from app.schemas.auth import UserPayload
from app.db.session import get_db
from app.repositories.user_repo import UserRepository
from app.models.user import Profile, Student

security_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    auth_header: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> UserPayload:
    """Dependency lấy thông tin User từ Bearer token của Supabase Auth,
    tự động provisioning profile/student trong DB và kiểm tra trạng thái active."""
    if not auth_header:
        raise AuthenticationError("Thiếu Authorization Bearer token")
    
    token = auth_header.credentials
    user_payload = decode_supabase_token(token)

    # Profile provisioning & lookup
    profile = UserRepository.get_or_create_profile(
        db,
        profile_id=user_payload.user_id,
        email=user_payload.email,
        role=user_payload.role,
    )

    if not profile.is_active:
        raise AuthenticationError("Tài khoản đã bị vô hiệu hóa hoặc không hợp lệ")

    # DB role takes precedence
    user_payload.role = profile.role
    return user_payload


def get_current_profile(
    current_user: UserPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Profile:
    profile = UserRepository.get_profile(db, current_user.user_id)
    if not profile:
        raise AuthenticationError("Không tìm thấy hồ sơ người dùng trong hệ thống")
    return profile


def require_roles(allowed_roles: List[str]) -> Callable[[UserPayload], UserPayload]:
    """Dependency factory kiểm tra quyền người dùng ở tầng backend"""
    def role_checker(current_user: UserPayload = Depends(get_current_user)) -> UserPayload:
        if current_user.role not in allowed_roles:
            raise PermissionDeniedError(
                f"Yêu cầu một trong các quyền: {', '.join(allowed_roles)}. Quyền hiện tại: '{current_user.role}'"
            )
        return current_user
    
    return role_checker


def get_current_student(
    current_user: UserPayload = Depends(require_roles(["student"])),
    db: Session = Depends(get_db),
) -> Student:
    """Dependency lấy thực thể Student tương ứng với student user hiện tại"""
    student = UserRepository.ensure_student_for_profile(db, current_user.user_id)
    return student


