from fastapi import APIRouter
from app.api.v1.endpoints import health, auth_check

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth_check.router, prefix="/auth", tags=["Auth Check"])
