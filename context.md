# NextTech – Project Context

> Tài liệu này là **nguồn sự thật chung (single source of truth)** của toàn bộ dự án.  
> Mọi AI agent, developer, reviewer và tester phải đọc file này trước khi làm việc.

---

## I. Tổng quan dự án

### 1. Tên hệ thống
**NextTech**

### 2. Định hướng
NextTech là hệ thống **Personal Education – Giáo dục cá nhân hóa** dành cho người mới học lập trình, tập trung vào sinh viên đang học kiến thức lập trình và thuật toán nền tảng.

Hệ thống không chỉ cung cấp bài học và bài tập, mà còn sử dụng **AI/ML** để:

- phát hiện sớm khó khăn học tập;
- ước lượng mức độ thành thạo kỹ năng;
- điều chỉnh lộ trình học;
- gợi ý tài liệu phù hợp;
- dự đoán khả năng hoàn thành bài tiếp theo;
- giải thích vì sao hệ thống đưa ra dự đoán hoặc khuyến nghị.

---

## II. Bài toán nghiên cứu

Sinh viên mới học lập trình thường gặp một hoặc nhiều khó khăn:

- hiểu lý thuyết nhưng không chuyển được sang code;
- làm được bài đơn giản nhưng gặp khó khi tăng độ khó;
- lặp lại cùng một lỗi;
- không biết kỹ năng nào đang yếu;
- không biết nên học lại nội dung nào;
- học theo cùng một lộ trình dù năng lực khác nhau.

NextTech nghiên cứu việc kết hợp **dữ liệu lý thuyết + dữ liệu thực hành** để xác định trạng thái học tập của từng sinh viên và cung cấp hỗ trợ phù hợp.

---

## III. Ba thành phần cốt lõi

### 3.1 Adaptive Learning – Học tập thích ứng

Mục tiêu:

- xây dựng learning path tham khảo;
- điều chỉnh thứ tự nội dung;
- thay đổi độ khó bài tập;
- ưu tiên kỹ năng đang yếu;
- yêu cầu học lại prerequisite khi cần.

Nguồn dữ liệu:

- mastery;
- quiz result;
- coding result;
- progress;
- số lần thử;
- difficulty history.

---

### 3.2 Recommendation System – Gợi ý tài liệu học theo năng lực

Có thể gợi ý:

- tài liệu lý thuyết;
- giải thích thuật toán;
- ví dụ;
- quiz;
- coding exercise;
- practice set.

Khuyến nghị phải có:

- target skill;
- lý do;
- difficulty phù hợp;
- explanation dễ hiểu.

---

### 3.3 Student Performance Prediction – Dự đoán kết quả học tập

Mục tiêu giai đoạn đầu:

- dự đoán khả năng hoàn thành bài tập tiếp theo;
- hoặc dự đoán khả năng đạt yêu cầu ở lần đánh giá tiếp theo.

Candidate features:

- quiz score;
- coding test pass rate;
- compile/runtime errors;
- số lần nộp bài;
- difficulty;
- mastery;
- learning progress;
- historical trend.

---

## IV. Explainable AI – XAI

Prediction không được chỉ hiển thị một con số.

Ví dụ không đủ:

> Khả năng hoàn thành bài tiếp theo: 43%

Ví dụ mong muốn:

> Khả năng hoàn thành bài tiếp theo hiện ở mức thấp hơn bình thường.  
> Các yếu tố ảnh hưởng chính:
> - test pass rate gần đây thấp;
> - nhiều lần retry;
> - mastery ở Arrays chưa ổn định.  
> Gợi ý: ôn Arrays và làm một bài mức Easy trước.

Nguyên tắc:

- không dùng ngôn ngữ tuyệt đối;
- không biến prediction thành kết luận học lực;
- explanation phải phản ánh đúng model;
- explanation cần dẫn đến hành động học cụ thể.

---

## V. Phạm vi nghiên cứu

### Trong phạm vi

- người mới học lập trình;
- lập trình nền tảng;
- thuật toán nền tảng;
- quiz;
- coding exercises;
- skills/concepts;
- adaptive learning;
- recommendation;
- prediction;
- XAI;
- research evaluation.

### Ngoài phạm vi giai đoạn đầu

- nhiều ngôn ngữ lập trình cùng lúc;
- hệ thống chấm điểm chính thức cho nhà trường;
- thay thế giảng viên;
- chatbot tổng quát không liên quan đến mục tiêu nghiên cứu;
- mạng xã hội học tập;
- gamification phức tạp nếu chưa cần;
- microservice hóa không có lý do kỹ thuật.

---

## VI. Đối tượng sử dụng

### Student

- đăng ký / đăng nhập;
- xem dashboard;
- học lesson;
- làm quiz;
- làm coding exercise;
- xem tiến độ;
- xem skill mastery;
- nhận learning path;
- nhận recommendation;
- xem prediction;
- xem XAI explanation.

### Instructor

- quản lý topic;
- quản lý skill;
- quản lý lesson;
- quản lý quiz;
- quản lý coding exercise;
- quản lý learning resources;
- xem analytics tổng hợp.

### Admin

- quản lý user;
- quản lý role;
- cấu hình hệ thống;
- quản lý version model;
- quản lý dữ liệu nghiên cứu ở mức cho phép.

---

## VII. Domain chính

Các entity bắt buộc phải được hiểu thống nhất:

- User
- Student
- Topic
- Concept
- Skill
- LearningObjective
- Lesson
- Quiz
- Question
- QuizAttempt
- CodingExercise
- Submission
- TestCase
- TestResult
- LearningResource
- SkillMastery
- LearningPath
- Recommendation
- Prediction
- Explanation

---

## VIII. Luồng nghiệp vụ lõi

```text
Student học / làm quiz / nộp code
        ↓
Hệ thống tạo learning evidence
        ↓
Cập nhật Skill Mastery
        ↓
Phát hiện weak skills
        ↓
Cập nhật Prediction
        ↓
Sinh Recommendation
        ↓
Điều chỉnh Learning Path
        ↓
Student thực hiện hoạt động tiếp theo
```

---

## IX. Nguyên tắc dữ liệu

- không dùng dữ liệu tương lai để dự đoán quá khứ;
- tránh target leakage;
- student ID dùng cho nghiên cứu phải được pseudonymize;
- không dùng thông tin nhận diện trực tiếp làm feature;
- mọi feature phải có định nghĩa;
- mọi dataset experiment phải version được;
- train/validation/test phải tách rõ.

---

## X. Nguyên tắc AI/ML

1. Luôn có baseline.
2. Không giả số liệu thực nghiệm.
3. Không chọn model chỉ vì phức tạp.
4. Model phải được đánh giá bằng metric phù hợp.
5. Nếu output là xác suất, cần quan tâm calibration.
6. XAI phải bám model thật.
7. Kết quả AI chỉ mang tính hỗ trợ học tập.

---

## XI. UI/UX đã chốt

### Brand
- Tên: **NextTech**
- Logo: **Concept 04**

### Màu
- Romantic Orange: `#FAAA48`
- Peach Glow: `#FFDDAC`
- Chocolate Melange: `#2F0F03`

### Hướng thiết kế
- thân thiện với beginner;
- hiện đại;
- ấm áp;
- ít gây áp lực;
- code editor có thể dùng nền tối riêng;
- không biến toàn bộ hệ thống thành giao diện hacker.

---

## XII. Tech Stack đã chốt cho V1

Nguồn chi tiết: `docs/technical/tech-stack.md`

### Frontend
- React + Vite + TypeScript
- Tailwind CSS + shadcn/ui
- React Router
- TanStack Query
- Zustand
- React Hook Form + Zod
- Monaco Editor
- Recharts

### Authentication / Platform
- Supabase Auth
- Supabase PostgreSQL
- Supabase Storage

### Backend
- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic

### AI / ML
- pandas
- NumPy
- scikit-learn
- SHAP
- joblib
- Jupyter / Google Colab cho training

### Code Execution V1
- Python only
- Pyodide
- Web Worker
- client-generated execution result không được xem là grading bảo mật cao

### Testing
- Vitest
- React Testing Library
- Playwright
- Pytest

### Deployment
- Frontend: Vercel
- Backend + loaded ML model: Render
- Database/Auth/Storage: Supabase
- Training: local / Google Colab

### Nguyên tắc
- không tách AI service ở V1;
- không dùng Firebase/Firestore;
- không dùng Node backend thứ hai;
- không thêm LLM API cho core research;
- không xây server-side code runner ở V1 nếu chưa có yêu cầu mới;
- agent không được tự thay stack.

---

## XIII. Ưu tiên phát triển

Thứ tự ưu tiên:

1. Core learning flow chạy được.
2. Dữ liệu được thu đúng.
3. Mastery có logic rõ.
4. Recommendation baseline.
5. Prediction baseline.
6. XAI.
7. Tối ưu UI.
8. Nâng cấp model.

Không đảo thứ tự để làm AI trước khi có dữ liệu hợp lệ.

---

## XIV. Definition of Done cấp dự án

Một feature chỉ được xem là hoàn thành khi:

- yêu cầu đã được implement;
- validation hoạt động;
- empty/loading/error state có xử lý;
- test liên quan đã chạy;
- không phá luồng hiện tại;
- tài liệu được cập nhật nếu behavior thay đổi;
- checklist task được tick;
- có evidence hoặc log test phù hợp.

---

## XV. Tài liệu cần đọc theo task

### Frontend
1. `context.md`
2. `AGENTS.md`
3. `docs/technical/tech-stack.md`
4. `docs/technical/ui-ux-spec.md`
5. `docs/analysis/requirements.md`
6. file task trong `plan/frontend/`

### Backend
1. `context.md`
2. `AGENTS.md`
3. `docs/technical/tech-stack.md`
4. `docs/analysis/domain-model.md`
5. `docs/technical/database-api-design.md`
6. file task trong `plan/backend/`

### AI/Data
1. `context.md`
2. `AGENTS.md`
3. `docs/technical/tech-stack.md`
4. `docs/ai/*`
5. `docs/data/*`
6. file task trong `plan/ai-data/`

### Testing
1. `context.md`
2. `AGENTS.md`
3. `plan/testing/*`
4. tài liệu của feature đang test

---

## XVI. Quy tắc thay đổi context

Chỉ cập nhật file này khi có thay đổi cấp dự án như:

- đổi phạm vi;
- đổi mục tiêu nghiên cứu;
- thêm/bỏ module lớn;
- đổi domain chính;
- đổi brand;
- thay đổi nguyên tắc dữ liệu/AI.

Không dùng file này để ghi task nhỏ hoặc bug.
