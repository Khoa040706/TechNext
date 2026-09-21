# Research Methodology – NextTech

## 1. Thiết kế nghiên cứu

NextTech sử dụng hướng nghiên cứu thực nghiệm kết hợp phát triển hệ thống.

Quy trình:

1. Xác định câu hỏi nghiên cứu.
2. Thiết kế hệ thống.
3. Thu thập dữ liệu.
4. Tiền xử lý.
5. Xây baseline.
6. Huấn luyện mô hình.
7. Đánh giá.
8. Tích hợp mô hình.
9. Đánh giá hỗ trợ cá nhân hóa.
10. Phân tích hạn chế.

## 2. Đơn vị phân tích

Có thể gồm:
- student;
- student-topic;
- student-skill;
- attempt;
- exercise;
- assessment window.

Phải chốt một đơn vị rõ cho mỗi experiment.

## 3. Nguồn dữ liệu

- Quiz answers.
- Quiz score.
- Coding submissions.
- Test-case results.
- Error types.
- Attempts.
- Time/progress.
- Difficulty.
- Skill mapping.
- Previous learning outcomes.

## 4. Tiền xử lý

- Loại record hỏng.
- Chuẩn hóa timestamp.
- Chuẩn hóa difficulty.
- Mapping bài tập → skill.
- Mapping question → concept.
- Tạo rolling/history features.
- Xử lý missing values.
- Kiểm tra outlier.

## 5. Thiết kế train/test

Ưu tiên split theo thời gian hoặc theo student tùy câu hỏi nghiên cứu.

Không được:
- để thông tin từ lần đánh giá tương lai xuất hiện trong feature;
- tạo feature trên toàn dataset trước khi split nếu có nguy cơ leakage;
- tune model trên test set.

## 6. Baseline

Ví dụ:
- majority class;
- simple threshold;
- logistic regression;
- rule based score.

Model phức tạp chỉ có ý nghĩa khi vượt baseline một cách có kiểm chứng.

## 7. So sánh mô hình

Ứng viên:
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting / XGBoost
- Neural Network khi dataset đủ lớn

Chọn model dựa trên:
- metric;
- độ ổn định;
- khả năng giải thích;
- chi phí triển khai.

## 8. XAI

- Global: feature importance.
- Local: SHAP hoặc phương pháp tương đương phù hợp model.
- Chuyển feature kỹ thuật thành explanation cho sinh viên.

## 9. Đánh giá khuyến nghị

- relevance;
- coverage;
- diversity khi cần;
- acceptance/use rate;
- learning gain sau recommendation.

## 10. Đạo đức và quyền riêng tư

- Pseudonymize student ID.
- Chỉ thu dữ liệu cần thiết.
- Không dùng dữ liệu ngoài mục tiêu nghiên cứu nếu chưa được phép.
- Không trình bày prediction như quyết định chính thức.


## 11. Research Implementation Environment

Implementation V1 dùng Python 3.12 với pandas/NumPy/scikit-learn; SHAP được dùng khi phù hợp cho XAI. Training thực hiện offline/local/Colab để giữ experiment tái lập và không phụ thuộc web server.
