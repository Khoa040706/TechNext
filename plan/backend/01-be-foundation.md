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
- [x] FastAPI app
- [x] Route/controller layer
- [x] Service/domain layer
- [x] Repository/data layer
- [x] Pydantic validation layer
- [x] Supabase JWT auth dependency
- [x] Role authorization dependency
- [x] Error middleware
- [x] Logging
- [x] Config/env handling
- [x] SQLAlchemy session management
- [x] Alembic initialized

## API standards
- [x] Consistent JSON response
- [x] Error code
- [x] Error message
- [x] Validation details
- [x] Request ID nếu dùng
- [x] Pagination standard
- [x] ISO 8601 timestamps

## Security
- [x] Không tự lưu password
- [x] Verify Supabase bearer token
- [x] Role authorization ở backend
- [x] Input validation
- [x] Secret via environment
- [x] CORS policy
- [x] Rate limit cho sensitive endpoints nếu phù hợp
- [x] Service role key không xuất hiện ở frontend

## Tests
- [x] Health endpoint
- [x] Validation unit test
- [x] JWT auth dependency test
- [x] Role authorization test
- [x] Global error handling
- [x] DB session test
