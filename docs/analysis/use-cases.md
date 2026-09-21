# Use Cases – NextTech

## Actor: Student

### UC-01 Register / Login
**Mục tiêu:** truy cập hệ thống.

### UC-02 View Learning Dashboard
**Mục tiêu:** xem tổng quan tiến độ, kỹ năng yếu, gợi ý và dự đoán.

### UC-03 Study Learning Content
**Main flow**
1. Student mở topic.
2. Hệ thống tải nội dung.
3. Student hoàn thành lesson.
4. Hệ thống ghi progress.

### UC-04 Take Quiz
1. Student bắt đầu quiz.
2. Hệ thống hiển thị câu hỏi.
3. Student gửi đáp án.
4. Hệ thống chấm.
5. Hệ thống cập nhật concept evidence.
6. Hệ thống cập nhật mastery.

### UC-05 Submit Coding Exercise
1. Student đọc đề.
2. Student viết code.
3. Student submit.
4. Hệ thống chạy test.
5. Hệ thống lưu test result/error.
6. Hệ thống cập nhật skill evidence.

### UC-06 View Skill Analysis
Student xem mastery, lịch sử và kỹ năng cần củng cố.

### UC-07 Get Adaptive Learning Path
Hệ thống chọn nội dung tiếp theo dựa trên prerequisite, mastery, progress và difficulty.

### UC-08 Get Recommended Resources
Hệ thống đề xuất tài liệu phù hợp với weakness và mục tiêu hiện tại.

### UC-09 View Performance Prediction
Hệ thống hiển thị khả năng hoàn thành đánh giá/bài tập tiếp theo.

### UC-10 View XAI Explanation
Student xem các yếu tố có ảnh hưởng chính đến prediction.

## Actor: Instructor

### UC-11 Manage Topics and Skills
### UC-12 Manage Quizzes
### UC-13 Manage Coding Exercises
### UC-14 Manage Learning Resources
### UC-15 View Aggregate Learning Analytics

## Actor: Admin

### UC-16 Manage Users
### UC-17 Manage Roles
### UC-18 Manage System Configuration
### UC-19 Manage Model Deployment Metadata

## Luồng tích hợp chính

Quiz/Coding Result  
→ Evidence  
→ Mastery Update  
→ Prediction Update  
→ Weakness Detection  
→ Recommendation  
→ Adaptive Path Update
