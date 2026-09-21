# NextTech – Master Plan

## 1. Mục tiêu

Thư mục `plan/` chia toàn bộ NextTech thành các phase có thể giao trực tiếp cho agent.

## 2. Thứ tự thực hiện

```text
Phase 00 Foundation
   ↓
Phase 01 Frontend Foundation
   ↓
Phase 02 Backend Foundation
   ↓
Phase 03 Core Learning FE + BE
   ↓
Phase 04 Data Collection
   ↓
Phase 05 Adaptive Learning
   ↓
Phase 06 Recommendation
   ↓
Phase 07 Prediction + XAI
   ↓
Phase 08 Integration
   ↓
Phase 09 Testing
   ↓
Phase 10 Release
```

FE và BE có thể chạy song song sau khi:
- domain đã chốt;
- API contract đã chốt;
- mock response đã có.

## 3. Nguyên tắc

- Mỗi file plan có checklist riêng.
- Không đánh dấu Done chỉ vì UI "trông xong".
- Không test thủ công thay cho toàn bộ automated tests.
- Không sửa code trong task kiểm thử thuần.
- Bug phải ghi vào `plan/testing/bug-report-template.md`.

## 4. Gate

### Gate A – Foundation
Requirements + domain + tech stack + API skeleton được chốt.

### Gate B – Core Product
Student có thể:
- login;
- học;
- làm quiz;
- submit code;
- xem progress.

### Gate C – Personalization
Mastery + recommendation + adaptive path chạy end-to-end.

### Gate D – AI
Prediction + XAI có model version và metric thật.

### Gate E – Release
Critical/High bug = 0.


## 5. Tech Stack Authority

Mọi phase implementation phải tuân thủ:

`docs/technical/tech-stack.md`

Plan không được tự thay framework hoặc tạo một stack mới.
