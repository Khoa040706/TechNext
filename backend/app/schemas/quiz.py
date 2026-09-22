from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# Option Schemas
class QuestionOptionBase(BaseModel):
    id: str = Field(..., description="ID của lựa chọn, e.g. opt_1")
    text: str = Field(..., description="Nội dung lựa chọn")


class QuestionOptionCreate(QuestionOptionBase):
    is_correct: bool = Field(default=False, description="Đáp án đúng hay sai")


class QuestionOptionRead(QuestionOptionBase):
    """Schema lựa chọn hiển thị cho học sinh (loại bỏ is_correct để chống lộ đề)"""
    pass


class QuestionOptionAdminRead(QuestionOptionBase):
    is_correct: bool = Field(..., description="Đáp án đúng hay sai")


# Question Schemas
class QuestionBase(BaseModel):
    question_text: str = Field(..., min_length=3, description="Nội dung câu hỏi")
    question_type: str = Field(default="multiple_choice", description="Loại câu hỏi: multiple_choice, single_choice")
    difficulty: str = Field(default="easy", description="Độ khó: easy, medium, hard")
    concept_id: Optional[str] = Field(default=None, description="ID của concept liên quan")
    skill_id: Optional[str] = Field(default=None, description="ID của skill đo lường")
    order_index: int = Field(default=0, description="Thứ tự hiển thị")


class QuestionCreate(QuestionBase):
    explanation: Optional[str] = Field(default=None, description="Giải thích đáp án")
    options: List[QuestionOptionCreate] = Field(..., min_length=2, description="Danh sách các lựa chọn")


class QuestionRead(QuestionBase):
    """Schema câu hỏi trả về cho học sinh làm bài: không chứa explanation và is_correct"""
    id: str
    quiz_id: str
    options: List[QuestionOptionRead]

    model_config = ConfigDict(from_attributes=True)


class QuestionAdminRead(QuestionBase):
    id: str
    quiz_id: str
    explanation: Optional[str] = None
    options: List[QuestionOptionAdminRead]

    model_config = ConfigDict(from_attributes=True)


# Quiz Schemas
class QuizBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Tiêu đề quiz")
    description: Optional[str] = Field(default=None, description="Mô tả quiz")
    topic_id: Optional[str] = Field(default=None, description="ID Topic liên quan")
    lesson_id: Optional[str] = Field(default=None, description="ID Lesson liên quan")
    order_index: int = Field(default=0, description="Thứ tự hiển thị")
    is_published: bool = Field(default=True, description="Trạng thái công khai")


class QuizCreate(QuizBase):
    questions: Optional[List[QuestionCreate]] = Field(default=None, description="Danh sách câu hỏi kèm theo")


class QuizRead(QuizBase):
    id: str
    total_questions: int = Field(default=0, description="Tổng số câu hỏi")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuizDetailRead(QuizRead):
    questions: List[QuestionRead] = Field(default_factory=list, description="Danh sách câu hỏi cho học sinh")


class QuizDetailAdminRead(QuizRead):
    questions: List[QuestionAdminRead] = Field(default_factory=list, description="Danh sách câu hỏi cho quản trị")


# Quiz Attempt & Submit Schemas
class QuizAttemptCreateResponse(BaseModel):
    id: str = Field(..., description="ID của lượt làm bài (Attempt ID)")
    quiz_id: str
    student_id: str
    status: str
    started_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionAnswerSubmission(BaseModel):
    question_id: str = Field(..., description="ID câu hỏi")
    selected_option_id: str = Field(..., description="ID đáp án học sinh chọn")
    response_time_seconds: Optional[int] = Field(default=None, ge=0, description="Thời gian phản hồi tính bằng giây")


class QuizSubmitRequest(BaseModel):
    attempt_id: str = Field(..., description="ID lượt làm bài cần nộp")
    answers: List[QuestionAnswerSubmission] = Field(..., description="Danh sách câu trả lời của học sinh")


class QuestionResultDetail(BaseModel):
    question_id: str
    selected_option_id: Optional[str] = None
    is_correct: bool
    correct_option_id: Optional[str] = None
    explanation: Optional[str] = None


class QuizSubmitResponse(BaseModel):
    attempt_id: str
    quiz_id: str
    score: float = Field(..., description="Điểm số đạt được (thang 100)")
    total_questions: int
    correct_answers: int
    status: str
    submitted_at: datetime
    results: List[QuestionResultDetail]
