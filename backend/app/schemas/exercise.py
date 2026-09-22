from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator


# Test Case Schemas
class TestCaseBase(BaseModel):
    input_data: str = Field(..., description="Dữ liệu đầu vào của test case")
    expected_output: str = Field(..., description="Kết quả kỳ vọng đầu ra")
    order_index: int = Field(default=0, description="Thứ tự test case")


class TestCaseCreate(TestCaseBase):
    is_public: bool = Field(default=True, description="Test case công khai cho trình duyệt Pyodide chạy")


class TestCaseRead(TestCaseBase):
    """Test case công khai trả về cho học sinh để chạy Pyodide worker"""
    id: str
    exercise_id: str

    model_config = ConfigDict(from_attributes=True)


class TestCaseAdminRead(TestCaseBase):
    id: str
    exercise_id: str
    is_public: bool

    model_config = ConfigDict(from_attributes=True)


# Coding Exercise Schemas
class CodingExerciseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Tiêu đề bài tập coding")
    slug: str = Field(..., min_length=2, max_length=150, description="Đường dẫn tĩnh duy nhất")
    description_markdown: str = Field(..., min_length=5, description="Mô tả đề bài định dạng Markdown")
    starter_code: Optional[str] = Field(default=None, description="Mã khởi tạo sẵn (Python)")
    difficulty: str = Field(default="easy", description="Độ khó: easy, medium, hard")
    time_limit_ms: int = Field(default=5000, ge=500, le=30000, description="Thời gian tối đa thực thi (ms)")
    skill_id: Optional[str] = Field(default=None, description="ID Kỹ năng đo lường")
    topic_id: Optional[str] = Field(default=None, description="ID Chủ đề liên quan")
    lesson_id: Optional[str] = Field(default=None, description="ID Bài học liên quan")
    order_index: int = Field(default=0, description="Thứ tự hiển thị")
    is_published: bool = Field(default=True, description="Trạng thái công khai")


class CodingExerciseCreate(CodingExerciseBase):
    test_cases: Optional[List[TestCaseCreate]] = Field(default=None, description="Danh sách test cases kèm theo")


class CodingExerciseRead(CodingExerciseBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CodingExerciseDetailRead(CodingExerciseRead):
    test_cases: List[TestCaseRead] = Field(default_factory=list, description="Danh sách test cases công khai")


class CodingExerciseDetailAdminRead(CodingExerciseRead):
    test_cases: List[TestCaseAdminRead] = Field(default_factory=list, description="Toàn bộ test cases cho quản trị")


# Submission & Telemetry Schemas
class CodingSubmissionCreate(BaseModel):
    source_code: str = Field(..., min_length=1, max_length=65536, description="Mã nguồn nộp bài (tối đa 64 KB)")
    total_tests: int = Field(ge=0, description="Tổng số test cases thực thi")
    passed_tests: int = Field(ge=0, description="Số test cases vượt qua")
    failed_tests: int = Field(ge=0, description="Số test cases thất bại")
    compile_error: bool = Field(default=False, description="Lỗi cú pháp / biên dịch Python")
    runtime_error: bool = Field(default=False, description="Lỗi ngoại lệ khi thực thi")
    time_limit_error: bool = Field(default=False, description="Vượt quá thời gian chạy worker")
    error_type: Optional[str] = Field(default=None, max_length=100, description="Loại lỗi (e.g. ZeroDivisionError)")
    error_message: Optional[str] = Field(default=None, max_length=2000, description="Thông điệp lỗi đã rút gọn")
    execution_time_ms: Optional[float] = Field(default=None, ge=0, description="Thời gian thực thi mili-giây")

    @model_validator(mode="after")
    def validate_test_counts(self):
        if self.passed_tests + self.failed_tests > self.total_tests:
            raise ValueError("Tổng số test passed và failed không được vượt quá total_tests")
        return self


class TestResultRead(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    compile_error: bool
    runtime_error: bool
    time_limit_error: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class CodingSubmissionResponse(BaseModel):
    id: str
    exercise_id: str
    student_id: str
    attempt_number: int
    status: str
    execution_source: str = Field(default="client_pyodide", description="Nguồn thực thi code")
    trust_level: str = Field(default="untrusted_client", description="Mức độ tin cậy của kết quả")
    submitted_at: datetime
    test_result: TestResultRead
    note: str = Field(
        default="Kết quả được sinh bởi client-side Pyodide Worker và không được coi là secure official grading.",
        description="Ghi chú về tính xác thực của grading V1",
    )

    model_config = ConfigDict(from_attributes=True)
