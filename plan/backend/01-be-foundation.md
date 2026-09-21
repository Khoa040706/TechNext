# BE-01 – Backend Foundation

## Stack bắt buộc

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- Supabase PostgreSQL
- Supabase Auth JWT verification
- Pytest

Không tạo Node/Express backend thứ hai.

## Architecture
- [ ] FastAPI app
- [ ] Route/controller layer
- [ ] Service/domain layer
- [ ] Repository/data layer
- [ ] Pydantic validation layer
- [ ] Supabase JWT auth dependency
- [ ] Role authorization dependency
- [ ] Error middleware
- [ ] Logging
- [ ] Config/env handling
- [ ] SQLAlchemy session management
- [ ] Alembic initialized

## API standards
- [ ] Consistent JSON response
- [ ] Error code
- [ ] Error message
- [ ] Validation details
- [ ] Request ID nếu dùng
- [ ] Pagination standard
- [ ] ISO 8601 timestamps

## Security
- [ ] Không tự lưu password
- [ ] Verify Supabase bearer token
- [ ] Role authorization ở backend
- [ ] Input validation
- [ ] Secret via environment
- [ ] CORS policy
- [ ] Rate limit cho sensitive endpoints nếu phù hợp
- [ ] Service role key không xuất hiện ở frontend

## Tests
- [ ] Health endpoint
- [ ] Validation unit test
- [ ] JWT auth dependency test
- [ ] Role authorization test
- [ ] Global error handling
- [ ] DB session test
