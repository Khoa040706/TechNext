# BE-03 – Quiz & Coding APIs

## Quiz
- [x] Get quiz
- [x] Start attempt
- [x] Submit answers
- [x] Grade
- [x] Save question results
- [x] Create evidence
- [x] Prevent invalid double-submit

## Coding Exercise V1

Code execution diễn ra ở frontend bằng Pyodide/Web Worker.

Backend chịu trách nhiệm:
- [x] Get exercise
- [x] Accept coding submission payload
- [x] Validate source length / payload
- [x] Save source code hoặc reference theo policy
- [x] Save attempt number
- [x] Save reported test telemetry
- [x] Save Python error type/message phù hợp
- [x] Save execution time
- [x] Force `execution_source=client_pyodide`
- [x] Force `trust_level=untrusted_client`
- [x] Create learning evidence theo policy đã chốt
- [x] Không mô tả result client như secure official grading

## V1 Security / Integrity
- [x] Backend không execute submitted code
- [x] Payload size limit
- [x] Sanitize/log safely
- [x] Không tin field trust_level từ client; backend tự set
- [x] Controlled-research limitation documented

## Future V2 – NOT IMPLEMENT NOW
Server-side isolated runner chỉ làm khi plan được cập nhật chính thức.

## Tests
- [x] Quiz grading
- [x] Quiz invalid payload
- [x] Coding submission valid
- [x] Oversized source rejected
- [x] Invalid telemetry rejected
- [x] execution_source forced by backend
- [x] trust_level forced by backend
- [x] Attempt increment
