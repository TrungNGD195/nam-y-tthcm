# Xử lý ảnh — biên tập nội dung

Đã biên soạn 168 câu/bài từ hai ZIP được bổ sung ngày 14/11/2026. Đây là bộ tự luận, dùng `src/subjects/xu-ly-anh/solutions.json`, không tạo ngân hàng trắc nghiệm giả.

`source-prompts.json` giữ đề, vị trí nguồn, ảnh đề và SHA-256 tài liệu. [Kiểm kê và quy ước](KIEM_KE_VA_QUY_UOC.md) ghi đủ từng mục cùng những lỗi/mâu thuẫn nguồn cần lưu ý. 28 câu lý thuyết tiếng Anh trùng bản Việt, chỉ tính một lần.

Scripts biên tập ở `scripts/content/xu-ly-anh/`: `ingest.py` đọc ZIP và tạo ảnh đề; `theory.py` viết dàn ý; `exercises.py` giải bài; `calculations.py` thực hiện phép tính; `build.py` xuất JSON; `verify.py` kiểm tra độc lập bằng NumPy/SciPy và giải mã ngược.

Chương theo slide và bộ cô Uyên; giáo trình PTIT khác số chương nên đối chiếu bằng trang PDF. Không tự thêm câu đạo đức khi chưa có tài liệu tương ứng.
