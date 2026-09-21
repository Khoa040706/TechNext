# Dataset and Experiment Plan

## 1. Pipeline

Raw Events  
→ Validation  
→ Cleaning  
→ Feature Engineering  
→ Dataset Snapshot  
→ Split  
→ Training  
→ Validation  
→ Test  
→ XAI  
→ Report

## 2. Dataset Snapshot

Mỗi experiment phải ghi:
- snapshot date;
- source version;
- number of students;
- number of samples;
- target distribution;
- feature version.

## 3. Split Strategy

Ưu tiên hai lựa chọn:

### Student-wise Split
Dùng khi muốn đánh giá khả năng tổng quát sang student chưa thấy.

### Time-based Split
Dùng khi muốn mô phỏng prediction tương lai.

Không random split vô điều kiện nếu gây leakage từ cùng student/attempt chain.

## 4. Experiment A

**Theory-only vs Practice-only vs Combined**

Mục tiêu: kiểm tra giá trị của việc kết hợp hai nhóm dữ liệu.

## 5. Experiment B

**Baseline vs ML models**

So sánh model đơn giản và model nâng cao.

## 6. Experiment C

**With vs Without personalization**

Nếu điều kiện thực nghiệm cho phép, so sánh hỗ trợ cá nhân hóa và không cá nhân hóa.

## 7. Preprocessing

- missing values;
- categorical encoding;
- scaling khi cần;
- imbalance handling;
- outlier policy.

## 8. Reproducibility

Lưu:
- random seed;
- package versions;
- feature config;
- model hyperparameters;
- split IDs;
- metric outputs.

## 9. Leakage Checklist

- target tương lai có lọt vào feature không?
- mastery có được tính từ chính outcome đang dự đoán không?
- aggregate có dùng record sau thời điểm prediction không?
- scaler có fit trên toàn dataset không?
