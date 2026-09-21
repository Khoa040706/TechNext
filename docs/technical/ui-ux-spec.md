# UI/UX Specification – NextTech

> Implementation UI V1: React + Vite + TypeScript + Tailwind CSS + shadcn/ui. Xem `tech-stack.md`.

## 1. Brand Direction

NextTech hướng đến:
- beginner-friendly;
- warm;
- modern;
- technology-oriented;
- không tạo cảm giác căng thẳng như dashboard kỹ thuật nặng nề.

## 2. Logo

Đã chốt: **Concept 04**

Biểu tượng mang cảm giác:
- chuyển động;
- tiến lên;
- công nghệ;
- khám phá.

## 3. Color System

### Primary – Romantic Orange
`#FAAA48`

Dùng cho:
- CTA;
- progress highlight;
- active state;
- icon quan trọng.

### Secondary – Peach Glow
`#FFDDAC`

Dùng cho:
- secondary surface;
- highlight nhẹ;
- tag;
- learning card.

### Dark – Chocolate Melange
`#2F0F03`

Dùng cho:
- heading;
- primary text;
- dark accent;
- code-related visual accent khi phù hợp.

### Background
Nền chính nên là trắng hoặc off-white rất nhẹ để giữ độ sạch.

## 4. Typography

Ưu tiên sans-serif dễ đọc:
- Inter
- Manrope
- Plus Jakarta Sans

Code:
- JetBrains Mono
- Fira Code

## 5. Layout

Desktop dashboard:
- left sidebar;
- top header;
- main learning area;
- optional right insight panel.

Learning screen:
- content;
- progress;
- quick recommendation;
- next action rõ ràng.

## 6. Core Screens

- Login/Register
- Onboarding
- Dashboard
- Topic/Lesson
- Quiz
- Coding Exercise
- Skill Analysis
- Learning Path
- Recommendation
- Prediction & XAI
- Admin Content Management

## 7. Coding UI

Code editor V1 sử dụng **Monaco Editor**.

Python code được chạy bằng **Pyodide trong Web Worker**, không chạy trên main thread.

Code editor nên dùng nền tối riêng biệt để:
- giảm mỏi mắt;
- tạo cảm giác IDE quen thuộc;
- tách rõ vùng code khỏi nội dung học.

Không bắt buộc toàn website phải dark mode.

## 8. AI Presentation

Prediction không dùng màu đỏ như cảnh báo tuyệt đối trừ khi thật cần.

Nên hiển thị:
- probability hoặc range;
- explanation;
- recommended action.

Ví dụ:
"Bạn có thể gặp khó khăn ở bài tiếp theo. Hãy ôn Arrays trong 10 phút trước khi thử."

## 9. Accessibility

- contrast đạt mức đọc tốt;
- không chỉ dùng màu để biểu thị trạng thái;
- font body không quá nhỏ;
- button có state rõ;
- keyboard navigation cho luồng học quan trọng.

## 10. Design Tokens gợi ý

```text
primary: #FAAA48
secondary: #FFDDAC
text-primary: #2F0F03
surface: #FFFFFF
surface-soft: #FFF8F0
border-soft: #F1E2D2
success: #2E8B57
warning: #C87500
error: #B42318
```
