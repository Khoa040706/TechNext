# NextTech

## 1. Giới thiệu

**NextTech** là hệ thống **Personal Education – Giáo dục cá nhân hóa** dành cho sinh viên mới học lập trình. Hệ thống ứng dụng trí tuệ nhân tạo và học máy để phát hiện sớm khó khăn trong quá trình học, phân tích năng lực cá nhân và cung cấp hỗ trợ phù hợp theo từng người học.

NextTech tập trung vào ba thành phần chính:

1. **Adaptive Learning – Học tập thích ứng**
2. **Learning Resource Recommendation – Gợi ý tài liệu học theo năng lực**
3. **Student Performance Prediction – Dự đoán kết quả học tập**

Bên cạnh đó, hệ thống sử dụng **Explainable AI (XAI)** để giúp sinh viên hiểu tại sao một dự đoán hoặc khuyến nghị được đưa ra.

## 2. Phạm vi

- Đối tượng: sinh viên mới học lập trình.
- Nội dung: lập trình và thuật toán nền tảng.
- Không giới hạn vào một học phần cụ thể.
- Giai đoạn đầu chuẩn hóa trên một ngôn ngữ lập trình.
- Dữ liệu được khai thác từ bài trắc nghiệm, bài tập lập trình, lịch sử làm bài, kết quả kiểm thử và tiến độ học.

## 3. Mục tiêu sản phẩm

- Giúp người học nhận diện kỹ năng còn yếu.
- Điều chỉnh nội dung và độ khó theo năng lực.
- Gợi ý học liệu phù hợp.
- Dự đoán khả năng hoàn thành bài tiếp theo.
- Cung cấp giải thích rõ ràng cho dự đoán và khuyến nghị.
- Hỗ trợ theo dõi sự tiến bộ theo thời gian.

## 4. Cấu trúc tài liệu

- `context.md`: bối cảnh và nguồn sự thật chung của dự án.
- `AGENTS.md`: quy tắc làm việc cho AI agent.
- `plan/`: kế hoạch triển khai chi tiết FE → BE → AI/Data → Integration → Testing → Release.
- `docs/technical/tech-stack.md`: công nghệ chính thức của NextTech V1.
- `docs/research/`: tài liệu nghiên cứu.
- `docs/analysis/`: phân tích yêu cầu và nghiệp vụ.
- `docs/ai/`: thiết kế các mô-đun AI.
- `docs/data/`: đặc tả dữ liệu và thực nghiệm.
- `docs/technical/`: kiến trúc, API, cơ sở dữ liệu, UI/UX.

## 5. Nguyên tắc chung

- Ưu tiên tính đúng đắn nghiên cứu trước độ phức tạp của mô hình.
- Không dùng dữ liệu tương lai để dự đoán quá khứ.
- Tách rõ dữ liệu huấn luyện, kiểm định và kiểm thử.
- Mọi quyết định AI ảnh hưởng đến người học cần có giải thích ở mức phù hợp.
- Khuyến nghị mang tính hỗ trợ, không thay thế giảng viên.


## 6. Tech Stack V1

- Frontend: React + Vite + TypeScript + Tailwind CSS + shadcn/ui
- Backend: Python + FastAPI + SQLAlchemy + Alembic
- Platform: Supabase PostgreSQL + Auth + Storage
- AI/ML: pandas + NumPy + scikit-learn + SHAP
- Code Runner V1: Pyodide + Web Worker, Python only
- Deploy: Vercel + Render + Supabase

Chi tiết xem `docs/technical/tech-stack.md`.
