# Domain Model – NextTech

## 1. Student

Thuộc tính chính:
- id
- profile
- enrollment status
- current learning state

Quan hệ:
- có nhiều attempts;
- có mastery theo skill;
- có recommendations;
- có predictions.

## 2. Topic

Nhóm nội dung lớn, ví dụ:
- Variables
- Conditionals
- Loops
- Arrays
- Functions
- Recursion
- Basic Data Structures

## 3. Concept

Khái niệm nhỏ hơn trong topic.

Ví dụ:
`Loop` → for loop, while loop, loop invariant cơ bản.

## 4. Skill

Năng lực có thể quan sát/ước lượng.

Ví dụ:
- hiểu điều kiện;
- viết vòng lặp;
- duyệt mảng;
- phân tích độ phức tạp cơ bản;
- debug lỗi logic.

## 5. Learning Objective

Mục tiêu cụ thể có thể đo được.

## 6. Quiz / Question

Question gắn với:
- concept;
- skill;
- difficulty.

## 7. Coding Exercise

Gắn với:
- skill;
- prerequisite;
- difficulty;
- test cases.

## 8. Submission

Một lần nộp code:
- source/code reference;
- timestamp;
- status;
- attempt number.

## 9. Test Result

- passed count;
- failed count;
- error type;
- execution metadata.

## 10. Learning Resource

Có thể là:
- theory note;
- algorithm explanation;
- example;
- video/link;
- practice task.

## 11. Skill Mastery

Biểu diễn trạng thái năng lực:
- mastery score;
- confidence;
- evidence count;
- updated_at.

## 12. Learning Path

Danh sách item được ưu tiên theo:
- prerequisite;
- mastery;
- current goal;
- difficulty.

## 13. Recommendation

- resource;
- reason;
- target skill;
- score;
- model/rule version.

## 14. Prediction

- target;
- probability/score;
- outcome horizon;
- model version;
- generated_at.

## 15. Explanation

- related prediction/recommendation;
- top factors;
- human-readable message;
- explanation method.

## 16. Quan hệ cốt lõi

Student  
→ Attempt  
→ Quiz/Coding Exercise  
→ Evidence  
→ Skill Mastery  
→ Prediction  
→ Recommendation  
→ Learning Path
