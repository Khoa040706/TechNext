from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SkillMasteryRead(BaseModel):
    id: str
    student_id: str
    skill_id: str
    skill_name: Optional[str] = None
    skill_slug: Optional[str] = None
    topic_id: Optional[str] = None
    mastery_score: float = Field(..., ge=0.0, le=1.0, description="Điểm thành thạo chuẩn hóa [0.0 - 1.0]")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Độ tin cậy của ước lượng [0.0 - 1.0]")
    evidence_count: int = Field(..., ge=0, description="Số lượng bằng chứng học tập")
    mastery_level: str = Field(..., description="Phân loại: weak (<0.4), developing (0.4-0.7), mastered (>=0.7)")
    version: str = Field(..., description="Phiên bản logic/mô hình tính toán mastery")
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LearningPathItemRead(BaseModel):
    id: str
    item_type: str = Field(..., description="Loại mục học: lesson, coding_exercise, quiz, reinforcement")
    item_id: str = Field(..., description="ID của bài học / bài tập / quiz liên quan")
    title: str = Field(..., description="Tiêu đề mục học")
    order_index: int = Field(..., description="Thứ tự học")
    difficulty: str = Field(..., description="Độ khó gợi ý: easy, medium, hard")
    status: str = Field(default="pending", description="Trạng thái: pending, in_progress, completed")
    reason: Optional[str] = Field(default=None, description="Lý do mục học được đề xuất")

    model_config = ConfigDict(from_attributes=True)


class LearningPathRead(BaseModel):
    id: str
    student_id: str
    status: str = Field(..., description="Trạng thái lộ trình: active, superseded, completed")
    target_skill_id: Optional[str] = Field(default=None, description="ID kỹ năng mục tiêu hiện tại")
    target_skill_name: Optional[str] = Field(default=None, description="Tên kỹ năng mục tiêu")
    recommended_difficulty: str = Field(..., description="Độ khó tổng thể được điều chỉnh")
    reason_for_change: Optional[str] = Field(default=None, description="Giải thích lý do điều chỉnh lộ trình (XAI)")
    version: str = Field(..., description="Phiên bản thuật toán thích ứng")
    items: List[LearningPathItemRead] = Field(default_factory=list, description="Danh sách các mục học trong lộ trình")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
