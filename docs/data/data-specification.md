# Data Specification – NextTech

## 1. Nguyên tắc

Chỉ thu dữ liệu cần thiết cho:
- vận hành hệ thống;
- personalization;
- nghiên cứu.

## 2. Student

- student_id
- pseudonymous_research_id
- created_at

Không dùng thông tin nhận diện trực tiếp làm feature ML.

## 3. Skill

- skill_id
- name
- parent_skill_id
- prerequisite_skill_id
- difficulty_level

## 4. Quiz Attempt

- quiz_attempt_id
- student_id
- quiz_id
- started_at
- submitted_at
- score
- total_questions

## 5. Question Result

- question_id
- concept_id
- skill_id
- correct
- response_time

## 6. Coding Submission

- submission_id
- student_id
- exercise_id
- attempt_number
- submitted_at
- status

## 7. Test Result

- total_tests
- passed_tests
- failed_tests
- compile_error
- runtime_error
- time_limit_error
- execution_time
- execution_source (`client_pyodide` ở V1)
- trust_level (`untrusted_client` ở V1)

**Lưu ý:** kết quả Pyodide từ browser không được coi là server-authoritative grading. Khi dùng làm dữ liệu nghiên cứu phải ghi rõ nguồn và giới hạn này.

## 8. Learning Progress

- topic_id
- lesson_id
- completion_state
- completed_at
- estimated_time
- actual_time nếu thu thập hợp lệ

## 9. Mastery

- student_id
- skill_id
- mastery_score
- confidence
- evidence_count
- version
- updated_at

## 10. Recommendation

- recommendation_id
- resource_id
- target_skill_id
- score
- reason_code
- algorithm_version
- created_at
- clicked_at
- completed_at

## 11. Prediction

- prediction_id
- student_id
- target_type
- target_reference
- probability
- risk_band
- model_version
- created_at
- actual_outcome khi có

## 12. Feature Dataset

Ví dụ:
- quiz_avg_last_n
- quiz_trend
- coding_pass_rate_last_n
- failed_attempts_last_n
- compile_error_rate
- runtime_error_rate
- mastery_target_skill
- current_difficulty
- recent_activity_count

Mọi feature phải có:
- công thức;
- source table;
- window;
- missing strategy;
- version.
