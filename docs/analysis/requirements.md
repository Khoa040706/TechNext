# System Requirements – NextTech

## 1. Actors

### Student
Người học chính.

### Instructor
Quản lý học liệu, bài tập và theo dõi tiến độ.

### Admin
Quản trị hệ thống, người dùng, cấu hình và dữ liệu.

## 2. Functional Requirements

### FR-01 Authentication
- Đăng ký/đăng nhập.
- Quản lý phiên.
- Phân quyền.

### FR-02 Student Profile
- Xem profile.
- Xem tiến độ.
- Xem skill mastery.

### FR-03 Learning Content
- Xem topic.
- Xem lesson.
- Xem learning objective.
- Theo dõi trạng thái hoàn thành.

### FR-04 Quiz
- Làm quiz.
- Gửi đáp án.
- Chấm điểm.
- Mapping lỗi với concept/skill.

### FR-05 Coding Exercise
- Xem đề.
- Viết/nộp code.
- Chạy test cases.
- Lưu attempt.
- Hiển thị kết quả.

### FR-06 Skill Analysis
- Tính mastery.
- Xác định skill mạnh/yếu.
- Hiển thị lịch sử.

### FR-07 Adaptive Path
- Tạo learning path.
- Cập nhật path sau hoạt động học.
- Điều chỉnh difficulty.

### FR-08 Recommendation
- Gợi ý learning resources.
- Gợi ý practice.
- Lưu explanation cho gợi ý.

### FR-09 Prediction
- Dự đoán outcome tiếp theo.
- Lưu probability.
- Lưu model version.
- Lưu explanation.

### FR-10 Dashboard
- Progress.
- Weak skills.
- Recommendations.
- Prediction summary.
- Recent activities.

### FR-11 Admin/Instructor
- CRUD topic/skill.
- CRUD quiz.
- CRUD coding exercise.
- CRUD resource.
- Xem thống kê tổng hợp.

## 3. Non-functional Requirements

### NFR-01 Usability
Giao diện phải phù hợp người mới học.

### NFR-02 Performance
Các trang chính nên phản hồi nhanh, prediction không được làm khóa UI.

### NFR-03 Reliability
Submission và kết quả phải có trạng thái rõ ràng.

### NFR-04 Security
Phân quyền, validation, bảo vệ dữ liệu cá nhân.

### NFR-05 Explainability
Mọi prediction hiển thị cho student phải có explanation phù hợp.

### NFR-06 Reproducibility
Model version, feature version và experiment config cần truy vết được.

## 4. Constraints

- Giai đoạn đầu một ngôn ngữ lập trình.
- Hạ tầng ưu tiên chi phí thấp.
- Dataset ban đầu có thể nhỏ.
- Không phụ thuộc vào mô hình quá lớn để hệ thống hoạt động cơ bản.

## 5. Business Rules

- Bài tập có thể gắn nhiều skill.
- Một skill có thể có prerequisite.
- Mastery thay đổi theo evidence mới.
- Recommendation phải gắn lý do.
- Prediction không trực tiếp quyết định điểm học phần.
