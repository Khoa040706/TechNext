from typing import List, Callable
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_supabase_token
from app.core.errors import AuthenticationError, PermissionDeniedError
from app.schemas.auth import UserPayload
from app.db.session import get_db

security_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    auth_header: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> UserPayload:
    """Dependency lấy thông tin User từ Bearer token của Supabase Auth"""
    if not auth_header:
        raise AuthenticationError("Thiếu Authorization Bearer token")
    
    token = auth_header.credentials
    return decode_supabase_token(token)


def require_roles(allowed_roles: List[str]) -> Callable[[UserPayload], UserPayload]:
    """Dependency factory kiểm tra quyền người dùng ở tầng backend"""
    def role_checker(current_user: UserPayload = Depends(get_current_user)) -> UserPayload:
        if current_user.role not in allowed_roles:
            raise PermissionDeniedError(
                f"Yêu cầu một trong các quyền: {', '.join(allowed_roles)}. Quyền hiện tại: '{current_user.role}'"
            )
        return current_user
    
    return role_checker
