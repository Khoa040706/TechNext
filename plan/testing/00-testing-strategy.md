# Testing Strategy – NextTech

## 1. Stack

Frontend:
- Vitest
- React Testing Library
- Playwright

Backend:
- Pytest

AI:
- Pytest + reproducible experiment scripts/notebooks

## 2. Test pyramid

### Unit
- domain logic;
- validators;
- mastery rules;
- recommendation score;
- feature functions;
- frontend components/utilities.

### Integration
- FastAPI + PostgreSQL;
- FastAPI + loaded ML artifact;
- FE + FastAPI;
- Supabase Auth token → FastAPI authorization;
- Pyodide worker → submission telemetry.

### E2E

Critical student flow:

```text
login
→ learn
→ quiz
→ run Python
→ submit
→ mastery
→ recommendation
→ prediction
```

## 3. Test environments

- local/dev;
- test database;
- staging trước release.

Không dùng production data chưa được xử lý để test tùy tiện.

## 4. Code Runner Testing

V1 runner là client-side.

Phải test:
- worker không block main UI;
- normal run;
- syntax/runtime error;
- infinite loop timeout;
- worker terminate/recreate;
- repeated runs;
- payload submission;
- backend gắn `trust_level=untrusted_client`.

Không test V1 như một server sandbox vì backend không execute code.

## 5. Severity

### Critical
- mất dữ liệu;
- auth bypass;
- secret/service key leak;
- hệ thống không sử dụng được.

### High
- flow chính không hoàn thành;
- quiz grading sai;
- mastery/prediction/recommendation mapping sai nghiêm trọng;
- backend coi client result là trusted grading.

### Medium
- chức năng phụ lỗi;
- edge state lỗi.

### Low
- cosmetic;
- copy;
- spacing.

## 6. Release gate

- Critical = 0
- High = 0
- automated critical tests pass
- migration pass
- smoke test pass
