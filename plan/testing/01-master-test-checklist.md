# Master Test Checklist

## A. Authentication
- [ ] Login đúng
- [ ] Login sai
- [ ] Empty input
- [ ] Session restore
- [ ] Logout
- [ ] Unauthorized access
- [ ] Role restriction

## B. Dashboard
- [ ] Có dữ liệu
- [ ] Student mới
- [ ] Partial failure
- [ ] Empty recommendation
- [ ] Prediction unavailable
- [ ] Loading

## C. Learning
- [ ] Topic list
- [ ] Lesson open
- [ ] Completion
- [ ] Prerequisite lock
- [ ] Next item

## D. Quiz
- [ ] Start
- [ ] Answer
- [ ] Submit
- [ ] Score
- [ ] Correct/incorrect mapping
- [ ] Double submit
- [ ] Network failure
- [ ] Mastery update

## E. Coding – Monaco + Pyodide
- [ ] Pyodide load
- [ ] Valid Python solution
- [ ] Wrong answer
- [ ] Syntax error
- [ ] Runtime error
- [ ] Infinite loop timeout
- [ ] Worker terminate/recreate
- [ ] Empty code
- [ ] Very large source payload
- [ ] Re-submit
- [ ] Test result count
- [ ] Attempt history
- [ ] execution_source = client_pyodide
- [ ] backend trust_level = untrusted_client
- [ ] UI không gọi client result là official secure grading

## F. Mastery
- [ ] No evidence
- [ ] One evidence
- [ ] Repeated success
- [ ] Repeated failure
- [ ] Different skill isolation
- [ ] Confidence update

## G. Adaptive Path
- [ ] Prerequisite unmet
- [ ] Easy recommendation
- [ ] Difficulty increase
- [ ] Difficulty decrease
- [ ] Completed items preserved
- [ ] Reason available

## H. Recommendation
- [ ] Weak skill targeted
- [ ] Correct difficulty
- [ ] No inaccessible resource
- [ ] No excessive duplicate
- [ ] Explanation exists
- [ ] Click/completion tracking

## I. Prediction
- [ ] Enough data
- [ ] Insufficient data
- [ ] Model unavailable
- [ ] Probability bounds
- [ ] Correct model version
- [ ] Actual outcome later linked

## J. XAI
- [ ] Explanation linked to correct prediction
- [ ] Feature labels readable
- [ ] Positive/negative direction correct
- [ ] No absolute claim
- [ ] Actionable suggestion present

## K. Admin
- [ ] Topic CRUD
- [ ] Skill CRUD
- [ ] Quiz CRUD
- [ ] Exercise CRUD
- [ ] Resource CRUD
- [ ] Invalid data blocked
- [ ] Unauthorized student blocked

## L. API
- [ ] Validation
- [ ] 401
- [ ] 403
- [ ] 404
- [ ] 409 where applicable
- [ ] 422/400 invalid payload
- [ ] 500 sanitized
- [ ] Pagination
- [ ] Rate limit if enabled

## M. Database
- [ ] FK
- [ ] Unique
- [ ] Transaction
- [ ] Migration clean DB
- [ ] Migration existing DB
- [ ] Index sanity

## N. Security
- [ ] Password not logged
- [ ] Secret not exposed
- [ ] Auth bypass attempt
- [ ] IDOR check
- [ ] Injection validation
- [ ] XSS output handling
- [ ] Pyodide code runs in Web Worker, not main UI thread
- [ ] Supabase service role key not exposed

## O. UI/UX
- [ ] Correct NextTech colors
- [ ] No unreadable contrast
- [ ] Loading state
- [ ] Empty state
- [ ] Error state
- [ ] Long text
- [ ] Keyboard focus
- [ ] No critical console errors

## P. Research/Data
- [ ] Research ID pseudonymized
- [ ] No direct identifier in ML feature
- [ ] Dataset split documented
- [ ] Leakage check
- [ ] Model metric reproducible
- [ ] Feature version stored
- [ ] Model version stored


## Q. Tech Stack Compliance
- [ ] React/Vite/TypeScript, không có framework FE thứ hai
- [ ] npm lockfile duy nhất
- [ ] FastAPI/Python backend, không có Node backend thứ hai
- [ ] SQLAlchemy + Alembic
- [ ] Supabase Auth/PostgreSQL
- [ ] ML artifact load trong FastAPI
- [ ] Không có AI microservice V1
- [ ] Không có paid LLM dependency cho core feature
