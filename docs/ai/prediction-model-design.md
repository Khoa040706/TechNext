# Prediction Model Design

## 1. Prediction Goal

Dự đoán khả năng sinh viên:
- hoàn thành bài tập tiếp theo; hoặc
- đạt yêu cầu ở lần đánh giá tiếp theo.

Giai đoạn đầu nên chọn **một target chính** để tránh làm loãng nghiên cứu.

## 2. Candidate Features

### Theory
- quiz score;
- concept accuracy;
- recent quiz trend.

### Practice
- test pass rate;
- compile errors;
- runtime errors;
- failed attempts;
- submission count.

### Progress
- completed items;
- recent activity;
- current difficulty;
- skill mastery.

### Historical
- previous success rate;
- rolling average;
- trend.

## 3. Feature Rules

Feature phải:
- tồn tại tại thời điểm dự đoán;
- có định nghĩa trong data specification;
- không chứa target leakage;
- có version.

## 4. Baseline Models

- majority baseline;
- simple threshold;
- logistic regression.

## 5. Candidate Models

- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost/LightGBM nếu môi trường phù hợp
- Neural Network chỉ khi dataset đủ lớn

## 6. Selection Criteria

Không chỉ chọn model có metric cao nhất. Cần cân bằng:
- performance;
- calibration;
- explainability;
- inference cost;
- stability.

## 7. Output Contract

Ví dụ:
- outcome_type;
- probability;
- risk_band;
- model_version;
- prediction_time;
- explanation_id.

## 8. Risk Bands

Ví dụ:
- Low risk
- Medium risk
- High risk

Threshold phải được định nghĩa từ validation set, không tự chọn tùy ý.

## 9. Monitoring

Theo dõi:
- data drift;
- performance drift;
- class distribution;
- missing feature rate;
- calibration.


## 10. Implementation Stack V1

- Python 3.12
- pandas / NumPy
- scikit-learn
- joblib
- SHAP khi phù hợp

Model được train offline và load vào FastAPI; không tách AI microservice ở V1.
