from typing import Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.common import ErrorResponse


class AppException(Exception):
    """Base application exception for NextTech API"""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class AuthenticationError(AppException):
    def __init__(self, message: str = "Xác thực không thành công", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="AUTHENTICATION_FAILED",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class PermissionDeniedError(AppException):
    def __init__(self, message: str = "Không có quyền truy cập tài nguyên này", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="PERMISSION_DENIED",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class NotFoundError(AppException):
    def __init__(self, message: str = "Không tìm thấy tài nguyên yêu cầu", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ValidationError(AppException):
    def __init__(self, message: str = "Dữ liệu không hợp lệ", code: str = "VALIDATION_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=code,
            status_code=422,
            details=details,
        )


class ConflictError(AppException):
    def __init__(self, message: str = "Xung đột dữ liệu", code: str = "CONFLICT_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_409_CONFLICT,
            details=details,
        )


def get_request_id(request: Request) -> Optional[str]:
    return getattr(request.state, "request_id", None) or request.headers.get("X-Request-ID")


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    payload = ErrorResponse(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        request_id=get_request_id(request),
        timestamp=datetime.now(timezone.utc),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump(mode="json"))


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err.get("loc", []))
        errors.append({
            "field": loc,
            "message": err.get("msg"),
            "type": err.get("type"),
        })

    payload = ErrorResponse(
        code="VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ",
        details={"errors": errors},
        request_id=get_request_id(request),
        timestamp=datetime.now(timezone.utc),
    )
    return JSONResponse(status_code=422, content=payload.model_dump(mode="json"))


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    payload = ErrorResponse(
        code="HTTP_ERROR",
        message=str(exc.detail),
        details=None,
        request_id=get_request_id(request),
        timestamp=datetime.now(timezone.utc),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump(mode="json"))


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    payload = ErrorResponse(
        code="INTERNAL_SERVER_ERROR",
        message="Hệ thống gặp sự cố không mong muốn. Vui lòng thử lại sau.",
        details={"raw_error": str(exc)} if getattr(request.app.state, "debug", False) else None,
        request_id=get_request_id(request),
        timestamp=datetime.now(timezone.utc),
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump(mode="json"))
