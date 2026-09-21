# Prompt 02 – Start Next Plan

Bắt đầu triển khai NextTech theo kế hoạch đã có trong thư mục `plan/`.

QUY TẮC BẮT BUỘC:

1. Đọc lại:
   - `context.md`
   - `AGENTS.md`
   - `docs/technical/tech-stack.md`
   - `plan/00-overview.md`

2. Xác định PLAN ĐẦU TIÊN chưa hoàn thành theo đúng thứ tự trong `plan/`.

3. Đọc trực tiếp file plan đó và thực hiện các task/checklist bên trong.

4. KHÔNG tạo bất kỳ implementation plan mới nào.
   - Không tạo `implementation-plan.md`
   - Không tạo `IMPLEMENTATION_PLAN.md`
   - Không tạo `todo.md`
   - Không tạo plan phụ
   - Không viết lại kế hoạch sang file khác

Thư mục `plan/` HIỆN TẠI chính là implementation plan chính thức của dự án.

5. KHÔNG tự thay tech stack.
   - `docs/technical/tech-stack.md` là nguồn sự thật cho công nghệ.
   - Không tự đổi React/Vite sang Next.js.
   - Không tự đổi FastAPI sang Node/Express.
   - Không tự đổi Supabase/PostgreSQL sang Firebase.
   - Không tự thêm AI microservice, vector DB, Redis, LLM API hoặc server-side code runner nếu plan không yêu cầu.

6. Trước khi sửa code, đọc kỹ source code liên quan đến task đó.

7. Implement trực tiếp theo checklist trong plan.
   - Không thêm tính năng ngoài scope.
   - Không refactor phần không liên quan.
   - Không tự thay đổi API/schema/domain nếu plan không yêu cầu.
   - Tuân thủ UI trong `docs/technical/ui-ux-spec.md`.

8. Trong quá trình làm, cập nhật checklist của CHÍNH file plan đang thực hiện:
   - `[ ]` → `[x]` chỉ khi task thực sự hoàn thành và đã kiểm tra.
   - Không tick task chưa hoàn thành.

9. Sau khi implement xong plan hiện tại:
   - chạy các test/check tương ứng;
   - kiểm tra build/runtime;
   - kiểm tra console nếu là Frontend;
   - kiểm tra API/data integrity nếu là Backend.

10. Nếu task hiện tại là TEST/REVIEW ONLY:
   - KHÔNG sửa code;
   - chỉ ghi bug theo format trong `plan/testing/bug-report-template.md`.

11. Chỉ thực hiện MỘT file plan trong lượt này.
KHÔNG tự động chuyển sang plan tiếp theo sau khi hoàn thành.

Cuối cùng báo cáo đúng format:

PLAN:
STATUS:

FILES CHANGED:
- ...

COMPLETED:
- ...

TESTS RUN:
- ...

RESULT:
- ...

REMAINING:
- ...

ISSUES/RISKS:
- ...

NEXT PLAN:
- ...

Sau báo cáo thì DỪNG để tôi kiểm tra.
