# Recommendation System Design

## 1. Mục tiêu

Gợi ý học liệu có liên quan trực tiếp đến nhu cầu hiện tại của sinh viên.

## 2. Item Types

- Theory
- Algorithm explanation
- Worked example
- Coding exercise
- Quiz
- Practice set

## 3. Metadata của Resource

- target skill;
- target concept;
- difficulty;
- format;
- estimated time;
- prerequisite;
- language;
- quality status.

## 4. User Context

- weak skills;
- current topic;
- mastery;
- recent errors;
- preferred/used resource history;
- current difficulty.

## 5. Baseline – Rule Based

Score ví dụ:

`score = skill_match + difficulty_match + prerequisite_match + freshness - repetition_penalty`

## 6. Content-based

Biểu diễn resource bằng metadata và tính mức phù hợp với student profile.

## 7. Hybrid – giai đoạn sau

Có thể kết hợp:
- content score;
- student behavior;
- population interaction signal.

Chỉ dùng collaborative signal khi lượng dữ liệu đủ.

## 8. Recommendation Explanation

Mỗi recommendation phải có:
- target skill;
- reason code;
- human-readable reason.

Ví dụ:
"Đề xuất vì bạn còn yếu ở recursion base case và bài này tập trung đúng kỹ năng đó."

## 9. Guardrails

- Không gợi ý tài liệu quá khó so với prerequisite.
- Hạn chế lặp cùng resource.
- Đảm bảo có lựa chọn thực hành sau tài liệu lý thuyết.
- Không dùng popularity làm tiêu chí duy nhất.

## 10. Evaluation

- Precision@K
- Recall@K
- Coverage
- Usage rate
- Completion rate
- Learning gain
