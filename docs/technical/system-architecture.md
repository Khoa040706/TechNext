# System Architecture – NextTech

> Kiến trúc V1 phải phù hợp `docs/technical/tech-stack.md`.

## 1. Logical Architecture

```text
┌───────────────────────────────────────────────────────────┐
│                     React / Vite Web                      │
│                                                           │
│  UI + TanStack Query + Zustand                           │
│  Monaco Editor                                            │
│       │                                                   │
│       └── Web Worker → Pyodide → Python execution V1      │
└───────────────────────┬───────────────────────────────────┘
                        │
             REST API / Bearer JWT
                        │
                ┌───────▼────────┐
                │    FastAPI     │
                │                │
                │ Domain Logic   │
                │ Mastery        │
                │ Recommendation │
                │ Feature Build  │
                │ ML Prediction  │
                │ XAI            │
                └───────┬────────┘
                        │ SQLAlchemy
                ┌───────▼──────────────┐
                │ Supabase PostgreSQL  │
                │ + Auth + Storage     │
                └──────────────────────┘
```

## 2. Frontend Responsibilities

Stack:
- React;
- Vite;
- TypeScript;
- Tailwind CSS;
- shadcn/ui;
- React Router;
- TanStack Query;
- Zustand.

Responsibilities:
- authentication UI/session integration với Supabase;
- dashboard;
- learning content;
- quiz;
- coding exercise;
- recommendation view;
- prediction/XAI view;
- admin UI;
- Pyodide code execution V1.

Frontend không quyết định business rule cốt lõi.

## 3. Authentication Flow

```text
React
  ↓
Supabase Auth
  ↓
Access Token
  ↓
FastAPI Authorization Header
  ↓
JWT verification
  ↓
App role/profile lookup
```

FastAPI không tự quản lý password.

## 4. Backend Responsibilities

Stack:
- Python 3.12;
- FastAPI;
- Pydantic;
- SQLAlchemy;
- Alembic.

Responsibilities:
- authorization;
- content management;
- attempts/submissions persistence;
- mastery;
- adaptive path;
- recommendation;
- prediction;
- XAI;
- logging;
- model metadata;
- research data integrity.

## 5. AI Layer V1

AI **không tách thành deployment riêng**.

Modules nằm trong backend codebase:
- feature generation;
- mastery;
- recommendation;
- prediction;
- explanation.

Model artifact được load vào FastAPI.

Training diễn ra offline bằng:
- local Python/Jupyter;
- Google Colab.

## 6. Code Runner V1

### Architecture

```text
Monaco
  ↓
Dedicated Web Worker
  ↓
Pyodide
  ↓
Python code
  ↓
Result / error / test feedback
```

### Constraints

- Python only ở V1.
- Không chạy code student trong FastAPI process.
- Worker phải timeout và terminate được.
- Browser result được xem là client-generated telemetry.
- Không dùng V1 runner cho grading chính thức có yêu cầu chống gian lận.

Khi submit, backend có thể lưu:
- source code;
- attempt;
- reported test result;
- execution source;
- trust level.

## 7. Data Layer

Supabase PostgreSQL lưu:
- learning content;
- quiz/coding attempts;
- evidence;
- mastery;
- recommendation;
- prediction;
- explanation;
- research metadata.

Supabase Storage chỉ dùng cho file/asset cần thiết.

## 8. Integration Principle

Mọi AI result cần:
- input snapshot/reference;
- model/rule version;
- output;
- timestamp;
- explanation reference.

Mọi client code execution result dùng cho nghiên cứu phải biết nguồn/trust level.

## 9. Deployment

```text
React/Vite → Vercel
FastAPI + ML artifact → Render
PostgreSQL/Auth/Storage → Supabase
Training → Local / Colab
```

## 10. Scalability

V1 ưu tiên đơn giản:
- một frontend;
- một backend;
- một managed database platform.

Chỉ tách AI service, queue, Redis hoặc server-side runner khi có nhu cầu đo được.
