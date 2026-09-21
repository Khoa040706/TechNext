# Evaluation Framework – NextTech

## 1. Mục tiêu

Đánh giá NextTech theo bốn lớp:
1. prediction;
2. recommendation;
3. adaptive learning;
4. user-facing explanation.

## 2. Prediction Metrics

### Classification
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC khi phù hợp
- PR-AUC khi dữ liệu mất cân bằng

### Probability Quality
- Brier Score
- Calibration curve

### Regression nếu dùng
- MAE
- RMSE
- R²

## 3. Recommendation Metrics

Offline:
- Precision@K
- Recall@K
- Hit Rate@K
- Coverage

User-level:
- tỷ lệ click/use;
- tỷ lệ hoàn thành tài liệu;
- mức hữu ích tự báo cáo;
- improvement sau recommendation.

## 4. Adaptive Learning

Có thể đo:
- tỷ lệ hoàn thành lộ trình;
- thời gian đạt mastery;
- số lần retry;
- learning gain;
- performance trên bài mới.

## 5. XAI

Đánh giá:
- fidelity: explanation có phản ánh model không;
- comprehensibility: người học có hiểu không;
- usefulness: người học có biết nên làm gì tiếp theo không;
- stability: input gần nhau có explanation quá khác nhau không.

## 6. So sánh

Tối thiểu:
- baseline vs proposed model;
- theory-only vs practice-only vs combined data;
- non-personalized vs personalized recommendation khi có thể.

## 7. Báo cáo uncertainty

- confidence interval nếu phù hợp;
- số lượng mẫu;
- class distribution;
- limitation;
- external validity.

## 8. Điều kiện không được kết luận quá mức

Không được kết luận "AI cải thiện việc học" chỉ từ F1-score. Muốn nói về hiệu quả học cần có outcome học tập tương ứng.
