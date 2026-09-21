# Explainable AI Design

## 1. Mục tiêu

Giúp người học và người nghiên cứu hiểu những yếu tố ảnh hưởng đến prediction.

## 2. Hai mức explanation

### Global
Cho biết model nói chung dựa nhiều vào feature nào.

### Local
Giải thích một prediction cụ thể của một student tại một thời điểm.

## 3. Candidate Methods

Tùy model:
- feature coefficients;
- tree feature importance;
- SHAP;
- local contribution methods.

## 4. Student-facing Explanation

Không đưa trực tiếp biểu đồ kỹ thuật khó hiểu nếu không cần.

Ví dụ:

**Khả năng hoàn thành bài tiếp theo: 58%**

Yếu tố làm giảm:
- test pass rate gần đây thấp;
- nhiều lần retry;
- mastery Arrays chưa ổn định.

Yếu tố tích cực:
- quiz Loop tốt;
- tiến độ học đều.

## 5. Actionable Explanation

Mỗi explanation nên dẫn đến hành động:
- ôn concept;
- xem resource;
- làm easy practice;
- thử lại bài.

## 6. Uncertainty

Không dùng ngôn ngữ tuyệt đối:
- Tránh: "Bạn sẽ thất bại."
- Dùng: "Dữ liệu hiện tại cho thấy nguy cơ gặp khó khăn cao hơn ở bài tiếp theo."

## 7. Technical Logging

Lưu:
- model version;
- explanation method;
- top features;
- contribution;
- timestamp.

## 8. Validation

Kiểm tra:
- fidelity;
- stability;
- comprehensibility;
- usefulness;
- consistency với model.


## 9. Implementation V1

Ưu tiên SHAP cho local/global explanation khi phù hợp model. Với Logistic Regression hoặc tree model đơn giản, có thể dùng explanation tự nhiên hơn nếu vẫn trung thực với model.

Không dùng LLM để bịa hoặc suy diễn feature contribution.
