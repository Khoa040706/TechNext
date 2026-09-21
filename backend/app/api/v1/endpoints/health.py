from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import ResponseWrapper

router = APIRouter()


@router.get("/health")
def check_health():
    """Endpoint kiểm tra tính sẵn sàng của hệ thống NextTech Backend"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
