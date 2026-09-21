from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class UserPayload(BaseModel):
    user_id: str = Field(..., description="ID định danh người dùng từ Supabase auth.users")
    email: Optional[str] = Field(default=None, description="Email người dùng")
    role: str = Field(default="student", description="Vai trò: student | instructor | admin")
    app_metadata: Dict[str, Any] = Field(default_factory=dict)
    user_metadata: Dict[str, Any] = Field(default_factory=dict)
