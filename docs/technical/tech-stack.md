# Tech Stack – NextTech

> **Status: CHỐT cho NextTech V1**
>
> File này là nguồn sự thật chính thức cho lựa chọn công nghệ.  
> Agent không được tự thay framework, database, ORM, package manager, code runner hoặc nền tảng deploy nếu chưa có yêu cầu thay đổi rõ ràng.

---

## I. Mục tiêu lựa chọn công nghệ

Tech stack của NextTech được chọn theo 6 tiêu chí:

1. **Chi phí ban đầu rất thấp** – ưu tiên free tier và công cụ mã nguồn mở.
2. **Phù hợp NCKH** – dễ kiểm chứng, tái lập thực nghiệm và giải thích mô hình.
3. **Ít service** – tránh microservice sớm và tránh deploy quá nhiều hệ thống.
4. **Agent dễ làm việc** – stack phổ biến, tài liệu nhiều, ít boilerplate.
5. **Phù hợp AI/ML** – backend dùng Python để không phải tách Node backend + Python AI service.
6. **Có đường nâng cấp** – V1 đơn giản nhưng không khóa đường phát triển sau này.

---

## II. Tổng quan stack

```text
Frontend
React + Vite + TypeScript
Tailwind CSS + shadcn/ui
React Router
TanStack Query
Zustand
React Hook Form + Zod
Monaco Editor
Recharts

Authentication
Supabase Auth

Backend
Python 3.12
FastAPI
Pydantic
SQLAlchemy 2.x
Alembic

Database / Storage
Supabase PostgreSQL
Supabase Storage

AI / ML
pandas
NumPy
scikit-learn
SHAP
joblib
Jupyter / Google Colab

Code Execution V1
Python only
Pyodide
Web Worker

Testing
Vitest
React Testing Library
Playwright
Pytest

Deployment
Frontend → Vercel
Backend + loaded ML model → Render
Database/Auth/Storage → Supabase
Model training → Local / Google Colab

Repository / CI
Git + GitHub
npm
GitHub Actions khi cần
```

---

# III. Frontend

## 3.1 Framework

### React + Vite + TypeScript

**Chốt:**
- React
- Vite
- TypeScript

### Lý do

NextTech là web application thiên về:

- dashboard;
- learning workflow;
- quiz;
- code editor;
- skill analytics;
- recommendation;
- prediction;
- admin.

Ứng dụng không cần SSR/SEO phức tạp ở V1, vì vậy không dùng Next.js chỉ để có framework lớn hơn.

### Không dùng ở V1

- Next.js
- Angular
- Vue
- server components
- SSR phức tạp

Chỉ thay khi có yêu cầu sản phẩm thực sự.

---

## 3.2 Styling & UI

### Tailwind CSS + shadcn/ui

Dùng để:

- xây design system nhanh;
- giữ source component trong project;
- dễ tùy biến theo bộ màu NextTech;
- tránh khóa vào component library khó chỉnh.

### Brand tokens

```text
primary:       #FAAA48
secondary:     #FFDDAC
text-primary:  #2F0F03
surface:       #FFFFFF
surface-soft:  #FFF8F0
border-soft:   #F1E2D2
success:       #2E8B57
warning:       #C87500
error:         #B42318
```

UI chi tiết tuân theo:

`docs/technical/ui-ux-spec.md`

---

## 3.3 Routing

### React Router

Routes chính:

```text
/login
/dashboard
/learn
/learn/:topicId
/quiz/:quizId
/exercise/:exerciseId
/skills
/recommendations
/prediction
/admin/*
```

---

## 3.4 Server State

### TanStack Query

Dùng cho:

- API fetching;
- cache;
- invalidation;
- retry;
- loading/error states.

Không dùng Zustand để thay thế server cache.

---

## 3.5 Client State

### Zustand

Chỉ dùng cho state thực sự thuộc client, ví dụ:

- UI preferences;
- editor state cần chia sẻ;
- temporary workflow state.

Không đưa toàn bộ API data vào Zustand.

---

## 3.6 Forms

### React Hook Form + Zod

Dùng cho:

- login/profile;
- quiz/admin forms;
- content management;
- validation phía client.

Backend vẫn phải validation độc lập bằng Pydantic.

---

## 3.7 Code Editor

### Monaco Editor

Dùng cho coding exercise:

- syntax highlighting;
- line numbers;
- editor themes;
- editor experience gần IDE.

Ngôn ngữ V1: **Python**.

---

## 3.8 Charting

### Recharts

Dùng cho:

- mastery;
- progress;
- trend;
- analytics đơn giản.

Không thêm chart library thứ hai nếu Recharts đáp ứng được.

---

# IV. Authentication

## 4.1 Supabase Auth

Frontend sử dụng Supabase client để:

- signup/login nếu chức năng signup được bật;
- restore session;
- logout;
- nhận access token.

Backend FastAPI:

- nhận Bearer token;
- xác minh token Supabase;
- không tự lưu mật khẩu;
- không tự implement password hashing/session system.

## 4.2 Authorization

Role ứng dụng:

```text
student
instructor
admin
```

Role/business profile được quản lý ở database ứng dụng.

Backend là nơi quyết định authorization cho protected API.

Frontend chỉ dùng role để điều khiển UX, không được xem là security boundary.

---

# V. Backend

## 5.1 Runtime

### Python 3.12

Lý do:

- tương thích tốt với hệ sinh thái ML;
- FastAPI ổn định;
- scikit-learn/SHAP/pandas hỗ trợ tốt;
- giảm rủi ro dependency so với dùng runtime quá mới.

Version patch phải được pin trong môi trường thực tế.

---

## 5.2 API Framework

### FastAPI

Dùng cho:

- REST API;
- dependency injection;
- authentication dependency;
- OpenAPI;
- request validation;
- service integration.

---

## 5.3 Validation

### Pydantic

Tất cả request/response quan trọng phải có schema rõ ràng.

Không nhận dictionary tự do cho core domain nếu có thể định nghĩa model.

---

## 5.4 ORM

### SQLAlchemy 2.x

Dùng cho:

- persistence;
- query;
- transaction;
- mapping domain/database.

### Migration

**Alembic**

Mọi schema change phải có migration.

---

## 5.5 Backend structure gợi ý

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── ai/
│   └── main.py
├── migrations/
├── tests/
└── pyproject.toml / requirements.lock
```

Không bắt buộc đúng tên folder nếu repository hiện tại đã có cấu trúc hợp lý; không refactor chỉ để giống sơ đồ.

---

# VI. Database & Platform

## 6.1 Supabase PostgreSQL

Database chính: **PostgreSQL trên Supabase**.

Phù hợp với quan hệ:

```text
Student
→ Attempts
→ Quiz / Exercise
→ Evidence
→ Skill Mastery
→ Recommendation / Prediction
```

Không chọn Firebase/Firestore cho V1 vì domain có nhiều quan hệ và cần query phục vụ phân tích/nghiên cứu.

---

## 6.2 Auth schema

`auth.users` do Supabase quản lý.

Ứng dụng nên có bảng như:

```text
profiles
students
```

để lưu dữ liệu nghiệp vụ.

Không tạo bảng password riêng.

---

## 6.3 Storage

### Supabase Storage

Chỉ dùng khi cần:

- ảnh học liệu;
- file học liệu;
- asset người quản trị upload.

Không lưu model artifact lớn vào database row.

---

# VII. AI / Machine Learning

## 7.1 Data Processing

- pandas
- NumPy

## 7.2 ML

### scikit-learn

Baseline:

- Majority baseline
- Rule baseline
- Logistic Regression

Candidate:

- Decision Tree
- Random Forest
- Gradient Boosting

### Optional

XGBoost/LightGBM chỉ thêm khi:

- baseline đã có;
- dataset đủ;
- có lý do thực nghiệm.

Không thêm chỉ vì muốn model "mạnh hơn".

---

## 7.3 Model Artifact

### joblib

Artifact phải đi kèm metadata:

- model version;
- feature version;
- training date;
- experiment ID;
- metric;
- expected feature order/schema.

---

## 7.4 Model Serving V1

**Không tách AI thành service riêng.**

FastAPI load model artifact khi ứng dụng khởi động hoặc qua model registry nội bộ.

```text
Frontend
   ↓
FastAPI
   ├── Domain Logic
   ├── Recommendation
   ├── Feature Builder
   ├── Loaded ML Model
   └── XAI
          ↓
      PostgreSQL
```

Mục tiêu: chỉ cần một backend deployment.

---

# VIII. Explainable AI

## SHAP

SHAP là lựa chọn chính cho local/global explanation khi phù hợp với model.

Nếu model đơn giản có explanation tự nhiên hơn, có thể dùng:

- coefficient;
- tree contribution;
- feature importance.

Không bắt buộc mọi model phải dùng SHAP nếu phương pháp khác trung thực và dễ kiểm chứng hơn.

---

# IX. Code Execution V1

## 9.1 Chốt: Pyodide + Web Worker

Giai đoạn đầu chỉ hỗ trợ **Python**.

Execution flow:

```text
Monaco Editor
      ↓
Web Worker
      ↓
Pyodide
      ↓
Run user Python code
      ↓
Public/Test feedback
      ↓
Submission telemetry → FastAPI
```

## 9.2 Lý do

- không cần server code runner riêng;
- giảm chi phí CPU backend;
- không chạy code sinh viên trong FastAPI process;
- dễ demo;
- phù hợp prototype/NCKH.

## 9.3 Timeout

Main thread không được chạy code trực tiếp.

Worker phải có timeout. Khi vượt timeout:

- terminate worker;
- tạo worker mới;
- báo timeout cho UI.

## 9.4 Giới hạn quan trọng

Kết quả chạy ở browser là **client-generated** và không được xem là grading có tính bảo mật cao.

V1 phù hợp:

- học tập;
- feedback;
- prototype;
- controlled research.

Không phù hợp làm:

- thi chính thức;
- chấm điểm chống gian lận;
- hidden tests bảo mật cao.

Backend phải có field hoặc metadata để phân biệt kết quả:

```text
execution_source = client_pyodide
trust_level = untrusted_client
```

Nếu nghiên cứu cần kết quả có độ tin cậy cao hơn, phải dùng controlled experiment hoặc nâng cấp runner.

## 9.5 Hướng nâng cấp V2

Chỉ khi cần:

```text
Server-side isolated runner
→ container/sandbox
→ CPU / memory / time limits
→ hidden tests
```

Không xây hệ thống này trong V1 nếu chưa có yêu cầu.

---

# X. Testing Stack

## Frontend Unit/Component

- Vitest
- React Testing Library

## End-to-End

- Playwright

## Backend

- Pytest
- FastAPI TestClient/httpx phù hợp implementation

## AI

- Pytest cho feature functions;
- notebook/script experiment riêng;
- metric report có thể tái lập.

---

# XI. Deployment

## 11.1 Frontend

### Vercel

Deploy React/Vite static frontend.

---

## 11.2 Backend

### Render

Deploy một FastAPI service chứa:

- API;
- business logic;
- recommendation baseline;
- loaded ML model;
- XAI.

Free/low-cost tier có thể có giới hạn hoặc sleep; đây là chấp nhận được cho prototype. Không thiết kế kiến trúc dựa vào giả định free tier sẽ tồn tại mãi.

---

## 11.3 Database/Auth/Storage

### Supabase

Dùng một project giai đoạn đầu.

---

## 11.4 Model Training

Không train model trên web server V1.

Training:

```text
Supabase export/query
      ↓
Local / Jupyter / Google Colab
      ↓
Experiment
      ↓
Evaluation
      ↓
model.joblib + metadata
      ↓
Backend deployment
```

---

# XII. Repository & Package Management

## Frontend

Package manager: **npm**

Chỉ dùng một lockfile:

```text
package-lock.json
```

Không trộn npm + pnpm + yarn.

## Backend

Dependency phải được pin bằng một cơ chế nhất quán của project.

Có thể dùng:

- `pyproject.toml` + lock tool; hoặc
- requirements lock.

Agent không tự đổi dependency manager giữa project.

## Git

- Git
- GitHub

CI có thể dùng GitHub Actions khi bắt đầu cần automation.

---

# XIII. Environment Variables

## Frontend

Ví dụ:

```text
VITE_API_BASE_URL=
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

Chỉ public-safe config mới được dùng với `VITE_*`.

Không đưa service role key vào frontend.

## Backend

Ví dụ:

```text
DATABASE_URL=
SUPABASE_URL=
SUPABASE_JWKS_URL=
SUPABASE_JWT_AUDIENCE=
SUPABASE_SERVICE_ROLE_KEY=   # chỉ khi thật sự cần
CORS_ORIGINS=
MODEL_PATH=
MODEL_VERSION=
```

Secret không commit vào Git.

---

# XIV. Những công nghệ KHÔNG cần ở V1

Không tự thêm:

- Kubernetes
- microservices
- Kafka
- Redis nếu chưa có use case rõ
- Celery nếu chưa có job cần thiết
- GraphQL
- vector database
- LLM API cho chức năng lõi
- Firebase/Firestore
- Node/Express backend thứ hai
- server-side code runner
- nhiều database
- nhiều frontend state libraries

Mục tiêu là **một hệ thống nghiên cứu hoạt động được**, không phải chứng minh số lượng công nghệ.

---

# XV. Version Policy

Không hard-code version trong tài liệu nếu không cần.

Khi khởi tạo repository:

1. chọn stable compatible version;
2. pin trong lockfile/config;
3. commit lockfile;
4. CI/deploy dùng cùng runtime;
5. không tự nâng major version trong một task feature.

Python V1 được định hướng **3.12.x** để ưu tiên tương thích ML.

---

# XVI. Chi phí

Mục tiêu V1:

- dùng open-source library;
- dùng free/low-cost hosting;
- không dùng paid LLM API;
- không cần GPU server;
- không cần code execution server;
- chỉ nâng gói khi giới hạn thực tế ảnh hưởng nghiên cứu/demo.

Chi phí nhà cung cấp có thể thay đổi theo thời gian; quyết định nâng cấp phải dựa trên usage thật.

---

# XVII. Tech Stack Change Rule

Muốn thay một thành phần cấp nền tảng, phải:

1. nêu lý do;
2. xác định tài liệu/code bị ảnh hưởng;
3. đánh giá migration cost;
4. cập nhật `tech-stack.md`;
5. cập nhật `context.md` nếu thay đổi kiến trúc lớn;
6. cập nhật plan liên quan;
7. chỉ sau đó mới implement.

Agent không được tự đổi stack để "tiện hơn".
