from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth_check,
    users,
    topics,
    skills,
    lessons,
    quizzes,
    exercises,
    mastery,
    learning_path,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth_check.router, prefix="/auth", tags=["Auth Check"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(users.router, tags=["Users"])  # Provides /api/v1/me
api_router.include_router(topics.router, prefix="/topics", tags=["Topics"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["Coding Exercises"])
api_router.include_router(mastery.router, prefix="/mastery", tags=["Mastery"])
api_router.include_router(learning_path.router, prefix="/learning-path", tags=["Learning Path"])
