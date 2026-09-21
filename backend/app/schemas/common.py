from typing import Generic, TypeVar, Optional, Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Mã lỗi hệ thống chuẩn hóa, e.g. AUTH_ERROR, NOT_FOUND")
    message: str = Field(..., description="Thông báo lỗi dễ hiểu cho client")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Chi tiết lỗi (validation, fields)")
    request_id: Optional[str] = Field(default=None, description="Request ID để truy vết log")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Thời điểm lỗi ISO 8601")


class ResponseWrapper(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    page: int = Field(ge=1, description="Trang hiện tại (1-indexed)")
    page_size: int = Field(ge=1, le=100, description="Số lượng mục mỗi trang")
    total_items: int = Field(ge=0, description="Tổng số mục")
    total_pages: int = Field(ge=0, description="Tổng số trang")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: PaginationMeta
