from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProfileBase(BaseModel):
    display_name: Optional[str] = Field(default=None, max_length=100)
    role: str = Field(default="student", description="student | instructor | admin")


class ProfileCreate(ProfileBase):
    id: str = Field(..., description="ID từ Supabase auth.users")
    email: Optional[str] = Field(default=None, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ProfileUpdate(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    profile_id: str
    research_id: str
    created_at: datetime


class ProfileRead(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    student: Optional[StudentRead] = None


class CurrentUserResponse(BaseModel):
    user_id: str
    email: Optional[str] = None
    role: str
    profile: ProfileRead
    student: Optional[StudentRead] = None
