# AGENTS.md – NextTech Agent Operating Rules

> Mọi agent phải tuân thủ file này.  
> Không được bỏ qua chỉ vì task có vẻ nhỏ.

---

## I. Vai trò agent

### 1. Frontend Agent
Có thể dùng Antigravity hoặc agent frontend tương đương.

Trách nhiệm:
- UI;
- component;
- page;
- state;
- API integration;
- form validation phía client;
- loading/empty/error state;
- accessibility;
- responsive behavior theo scope;
- frontend tests.

Không được:
- tự sửa DB schema;
- tự đổi API contract;
- tự tạo business rule mới.

### 2. Backend Agent
Có thể dùng Codex hoặc agent backend tương đương.

Trách nhiệm:
- API;
- authentication/authorization;
- domain logic;
- persistence;
- validation;
- data integrity;
- AI service integration;
- backend tests.

Không được:
- tự thay đổi UX đã chốt;
- tự đổi semantic của field mà không cập nhật contract.

### 3. AI/Data Agent
Trách nhiệm:
- dataset;
- feature engineering;
- baseline;
- model;
- evaluation;
- XAI;
- reproducibility.

Không được:
- dùng dữ liệu không tồn tại tại thời điểm prediction;
- báo cáo metric không được tạo từ experiment thật.

### 4. Test/Review Agent
Trách nhiệm:
- kiểm thử theo plan;
- không sửa code nếu task là "test only";
- ghi bug rõ owner;
- ghi expected/actual;
- cung cấp reproduction steps.

---

## II. Thứ tự đọc bắt buộc

Trước mỗi task:

1. `context.md`
2. `AGENTS.md`
3. `docs/technical/tech-stack.md`
4. `plan/00-overview.md`
5. file plan đúng phase/task
6. tài liệu chuyên môn liên quan
7. code hiện tại của khu vực cần sửa

Không được sửa code chỉ từ prompt mà không đọc code liên quan.

---

## III. Quy tắc lập kế hoạch

Trước khi implement:

- xác định mục tiêu;
- xác định file dự kiến sửa;
- xác định dependency;
- xác định API/schema liên quan;
- xác định test cần chạy;
- xác định tiêu chí Done.

Nếu task lớn, chia thành checkpoint nhỏ.

---

## IV. Quy tắc sửa code

- sửa nhỏ nhất có thể;
- không refactor ngoài phạm vi;
- không rename hàng loạt khi không cần;
- không đổi format repository vô lý;
- không thêm dependency nếu giải pháp hiện có đủ;
- không thay framework/database/ORM/package manager/code runner trái với `docs/technical/tech-stack.md`;
- không tự thêm Next.js, Firebase, Node backend, Redis, vector DB, LLM API hoặc microservice nếu plan không yêu cầu;
- không xóa code "có vẻ thừa" nếu chưa xác minh;
- giữ backward compatibility nếu task chưa cho phép breaking change.

---

## V. Quy tắc Frontend

### UI
- dùng token trong `ui-ux-spec.md`;
- giữ màu NextTech;
- component có hierarchy rõ;
- tránh visual noise.

### State
Mỗi màn hình gọi API phải xử lý:
- loading;
- success;
- empty;
- error;
- retry nếu phù hợp.

### Form
- client validation;
- server error mapping;
- không chỉ dựa vào client validation.

### AI Result
Prediction/recommendation UI phải có:
- kết quả;
- lý do;
- next action;
- trạng thái không chắc chắn phù hợp.

---

## VI. Quy tắc Backend

### API
- request validation;
- normalized response;
- status code đúng;
- authorization;
- error handling.

### Domain Logic
- controller/route mỏng;
- business logic ở service/domain layer;
- tránh duplicate logic.

### Database
- dùng PostgreSQL/Supabase theo `tech-stack.md`;
- schema change phải có Alembic migration;
- index cho query quan trọng;
- transaction cho luồng cần atomicity;
- không tạo password table riêng;
- authentication do Supabase Auth quản lý;
- không lưu secret/plain password.

---

## VII. Quy tắc AI/Data

- implementation V1 dùng Python + pandas/NumPy/scikit-learn/SHAP;
- AI model được load trong FastAPI V1, không tự tách AI microservice;
- baseline trước model nâng cao;
- split dữ liệu trước bước có nguy cơ leakage;
- log feature version;
- log model version;
- log metric;
- lưu seed/config;
- không dùng test set để tune;
- prediction API phải version được.

---

## VIII. Quy tắc Test

### Test-only task
Khi prompt nói **test/review only**:
- KHÔNG sửa code;
- KHÔNG auto-fix;
- ghi lỗi vào report;
- gắn owner: FE / BE / AI / Data / Integration.

### Bug report bắt buộc có
- Test ID;
- title;
- severity;
- precondition;
- steps;
- expected;
- actual;
- owner;
- evidence;
- status.

---

## IX. Quy tắc giao việc FE ↔ BE

### FE cần BE
FE phải ghi rõ:
- endpoint;
- request;
- response mong muốn;
- error case;
- field bắt buộc.

### BE bàn giao FE
BE phải cung cấp:
- API contract;
- auth requirement;
- sample request;
- sample response;
- known errors;
- test status.

Không giao bằng câu kiểu:
> "API xong rồi, FE tự xem code."

---

## X. Handoff format

Mỗi agent khi hoàn thành phải trả về:

```text
TASK:
STATUS:

FILES CHANGED:
- ...

IMPLEMENTED:
- ...

TESTS RUN:
- ...

RESULT:
- ...

NOT DONE / RISKS:
- ...

NEXT OWNER:
- FE / BE / AI / TEST
```

---

## XI. Commit rules

Commit theo nhóm logic, ví dụ:

```text
feat(fe): add learning dashboard
feat(be): add quiz submission API
feat(ai): add baseline prediction pipeline
test(integration): cover quiz submission flow
docs: update API contract
fix(fe): handle empty recommendation state
```

Không gom nhiều phase không liên quan vào một commit lớn nếu tránh được.

---

## XII. Definition of Done

Task chỉ Done khi:

- code chạy;
- test cần thiết pass;
- checklist task hoàn tất;
- không còn TODO quan trọng chưa báo;
- documentation cập nhật;
- handoff rõ ràng.

---

## XIII. Khi có mâu thuẫn

Ưu tiên:

1. `context.md`
2. `docs/technical/tech-stack.md` đối với quyết định công nghệ
3. requirement/domain/API docs
4. plan task
5. code hiện tại
6. suy đoán của agent

Nếu vẫn mâu thuẫn: dừng thay đổi phá vỡ hệ thống và báo cáo.
