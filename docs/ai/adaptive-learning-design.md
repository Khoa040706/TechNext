# Adaptive Learning Design

## 1. Mục tiêu

Điều chỉnh nội dung và độ khó theo trạng thái hiện tại của từng sinh viên.

## 2. Input

- current mastery;
- prerequisite completion;
- quiz results;
- coding results;
- recent attempts;
- difficulty history;
- current progress.

## 3. Output

- next recommended concept;
- next exercise difficulty;
- reinforcement item;
- review requirement;
- learning path order.

## 4. Mastery Model – phiên bản đầu

Mỗi skill có:
- mastery score: 0–1;
- confidence;
- evidence count.

Evidence có thể có trọng số:
- quiz đúng;
- coding test pass;
- complete exercise;
- repeated failure;
- recent success.

## 5. Rule-based Baseline

Ví dụ:
- mastery < 0.4 → ôn lý thuyết + easy practice;
- 0.4 ≤ mastery < 0.7 → medium practice;
- mastery ≥ 0.7 → next concept hoặc harder exercise.

Threshold chỉ là cấu hình ban đầu và phải được đánh giá thực nghiệm.

## 6. Prerequisite

Không đề xuất concept B nếu prerequisite A chưa đạt threshold tối thiểu, trừ khi mục tiêu là diagnostic assessment.

## 7. Difficulty Adjustment

Tăng difficulty khi:
- nhiều lần thành công gần đây;
- ít hint;
- test pass rate cao.

Giảm/reinforce khi:
- nhiều failed attempts;
- lỗi cùng skill lặp lại;
- thời gian giải bất thường;
- mastery giảm.

## 8. Path Update Trigger

Cập nhật sau:
- quiz;
- coding submission quan trọng;
- completion lesson;
- instructor override.

## 9. Explainability

Hệ thống nên nói:
"Bạn được gợi ý ôn Arrays vì mastery hiện tại thấp và hai bài gần nhất còn lỗi ở thao tác duyệt mảng."

Không nên chỉ nói:
"AI recommends Arrays."
