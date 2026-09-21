# Database & API Design – NextTech

## 1. Platform

- Database: Supabase PostgreSQL
- Authentication: Supabase Auth
- Backend access: FastAPI + SQLAlchemy
- Migration: Alembic

`auth.users` do Supabase quản lý. NextTech không lưu password hash trong bảng ứng dụng.

---

## 2. Core Tables

### profiles

```text
id UUID PK → auth.users.id
role
display_name
created_at
updated_at
```

### students
- id
- profile_id
- research_id
- created_at

### topics
### concepts
### skills
### skill_prerequisites
### lessons

### quizzes
### questions
### quiz_attempts
### question_results

### coding_exercises
### test_cases
### submissions
### test_results

`submissions/test_results` V1 phải phân biệt:

```text
execution_source = client_pyodide
trust_level = untrusted_client
```

để không nhầm client-run result với server-authoritative grading.

### learning_resources
### resource_skill_map

### skill_mastery
### learning_paths
### recommendations
### predictions
### explanations

---

## 3. Important Indexes

- student_id + created_at
- skill_id + student_id
- exercise_id + student_id
- prediction student_id + target_type
- recommendation student_id + created_at
- submission student_id + exercise_id + submitted_at

---

## 4. Authentication & Authorization

Frontend đăng nhập qua Supabase Auth.

Protected API:

```http
Authorization: Bearer <supabase_access_token>
```

FastAPI:
1. verify JWT;
2. lấy user id;
3. lookup profile/role;
4. áp authorization rule.

Frontend role check không thay thế backend authorization.

---

## 5. API Principles

- RESTful naming.
- Pydantic request/response validation.
- Consistent error schema.
- Auth required for protected resources.
- Role-based access.
- Date/time dùng ISO 8601.
- API không trả secret/provider key.

---

## 6. Student APIs

```http
GET /api/me
GET /api/dashboard
GET /api/topics
GET /api/topics/{id}
POST /api/quizzes/{id}/submit
POST /api/exercises/{id}/submissions
GET /api/mastery
GET /api/learning-path
GET /api/recommendations
GET /api/predictions/latest
GET /api/predictions/{id}/explanation
```

### Coding submission V1

Client chạy code bằng Pyodide, sau đó gửi submission telemetry.

Backend:
- validate payload;
- lưu source;
- lưu attempt;
- lưu execution_source/trust_level;
- không mặc định coi result client là grading chính thức.

---

## 7. Instructor/Admin APIs

```http
POST /api/admin/topics
POST /api/admin/skills
POST /api/admin/quizzes
POST /api/admin/exercises
POST /api/admin/resources
GET  /api/admin/analytics
```

---

## 8. Prediction Response

```json
{
  "targetType": "next_exercise_success",
  "probability": 0.58,
  "riskBand": "medium",
  "modelVersion": "v1",
  "explanationId": "exp_123"
}
```

---

## 9. Recommendation Response

```json
{
  "resourceId": "res_10",
  "targetSkill": "array_traversal",
  "score": 0.86,
  "reason": "Kỹ năng duyệt mảng hiện còn yếu."
}
```

---

## 10. Audit & Versioning

Không xóa lịch sử prediction/recommendation cần cho nghiên cứu.

Lưu:
- algorithm/model version;
- created_at;
- input/reference cần thiết;
- actual outcome khi có;
- execution source đối với coding result.

---

## 11. Migration Rules

- mọi schema change dùng Alembic;
- không sửa DB production thủ công rồi bỏ qua migration;
- migration được test trên clean DB;
- destructive migration phải có backup/forward-fix plan.
