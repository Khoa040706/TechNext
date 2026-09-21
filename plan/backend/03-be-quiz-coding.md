# BE-03 – Quiz & Coding APIs

## Quiz
- [ ] Get quiz
- [ ] Start attempt
- [ ] Submit answers
- [ ] Grade
- [ ] Save question results
- [ ] Create evidence
- [ ] Prevent invalid double-submit

## Coding Exercise V1

Code execution diễn ra ở frontend bằng Pyodide/Web Worker.

Backend chịu trách nhiệm:
- [ ] Get exercise
- [ ] Accept coding submission payload
- [ ] Validate source length / payload
- [ ] Save source code hoặc reference theo policy
- [ ] Save attempt number
- [ ] Save reported test telemetry
- [ ] Save Python error type/message phù hợp
- [ ] Save execution time
- [ ] Force `execution_source=client_pyodide`
- [ ] Force `trust_level=untrusted_client`
- [ ] Create learning evidence theo policy đã chốt
- [ ] Không mô tả result client như secure official grading

## V1 Security / Integrity
- [ ] Backend không execute submitted code
- [ ] Payload size limit
- [ ] Sanitize/log safely
- [ ] Không tin field trust_level từ client; backend tự set
- [ ] Controlled-research limitation documented

## Future V2 – NOT IMPLEMENT NOW
Server-side isolated runner chỉ làm khi plan được cập nhật chính thức.

## Tests
- [ ] Quiz grading
- [ ] Quiz invalid payload
- [ ] Coding submission valid
- [ ] Oversized source rejected
- [ ] Invalid telemetry rejected
- [ ] execution_source forced by backend
- [ ] trust_level forced by backend
- [ ] Attempt increment
