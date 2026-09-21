from typing import Optional, Dict, Any
from datetime import datetime, timezone, timedelta
import jwt
from app.core.config import settings
from app.core.errors import AuthenticationError
from app.schemas.auth import UserPayload


DEFAULT_DEV_SECRET = "nexttech-super-secure-jwt-secret-for-dev-32chars"


def decode_supabase_token(token: str) -> UserPayload:
    """
    Xác minh và giải mã Supabase JWT token.
    Hỗ trợ verify secret, expiration và audience.
    """
    if not token:
        raise AuthenticationError("Thiếu mã xác thực (Token required)")

    try:
        secret = settings.SUPABASE_JWT_SECRET or DEFAULT_DEV_SECRET
        
        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_aud": bool(settings.SUPABASE_JWT_AUDIENCE),
        }

        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256", "RS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE if options["verify_aud"] else None,
            options=options,
        )

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Token không chứa thông tin user_id (sub)")

        # Role can come from app_metadata or user_metadata or default to student
        app_metadata = payload.get("app_metadata", {})
        user_metadata = payload.get("user_metadata", {})
        role = app_metadata.get("role") or user_metadata.get("role") or payload.get("role") or "student"

        return UserPayload(
            user_id=str(user_id),
            email=payload.get("email"),
            role=role,
            app_metadata=app_metadata,
            user_metadata=user_metadata,
        )

    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Mã xác thực đã hết hạn (Token expired)")
    except jwt.InvalidAudienceError:
        raise AuthenticationError("Audience của token không hợp lệ (Invalid audience)")
    except jwt.PyJWTError as e:
        raise AuthenticationError(f"Mã xác thực không hợp lệ: {str(e)}")
    except Exception as e:
        raise AuthenticationError(f"Lỗi xử lý xác thực: {str(e)}")


def create_access_token_for_test(
    user_id: str,
    role: str = "student",
    email: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
    secret: Optional[str] = None,
) -> str:
    """Tạo mock JWT token phục vụ kiểm thử đơn vị & integration tests"""
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(hours=1))
    
    payload = {
        "sub": user_id,
        "email": email or f"{user_id}@nexttech.edu.vn",
        "role": role,
        "aud": settings.SUPABASE_JWT_AUDIENCE,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "app_metadata": {"role": role},
        "user_metadata": {"role": role},
    }
    
    key = secret or settings.SUPABASE_JWT_SECRET or DEFAULT_DEV_SECRET
    return jwt.encode(payload, key, algorithm="HS256")
