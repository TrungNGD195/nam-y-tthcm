# Ý cốt lõi từ toàn bộ ngân hàng — 15/11/2026

Luồng cần kiểm tra: chọn chương → đọc mục kiến thức/keyword → mở câu liên quan → luyện đúng nhóm câu → chọn đáp án, tải lại và chấm/nộp. Website tĩnh, dữ liệu tải từ module của môn; không có API, backend hoặc thông tin đăng nhập.

## Phạm vi nội dung

- Rà 506 câu chuẩn theo đề và nội dung đáp án, gồm các câu phủ định, điền khuyết và đáp án tổng hợp. Gom thành 45 mục học, dùng 213 concept khác nhau; có 10 trường hợp liên hệ khác chương gốc của concept nên cùng ý xuất hiện ở hơn một chương.
- Giữ nguyên chương của từng câu: 30 / 123 / 115 / 105 / 52 / 81. Không chuyển câu, không sửa đề/lựa chọn/đáp án/revision; đối chiếu bằng Python cho kết quả danh sách `questions` và `chapters` bằng hoàn toàn với bản public trước thay đổi. Phiên bản ngân hàng giữ nguyên để không thay bộ đề và lịch sử.
- Các chương có lần lượt 5 / 9 / 8 / 8 / 7 / 8 mục học; trong mỗi chương, mỗi câu liên kết đúng một mục, có thể mở danh sách để đối chiếu.
- Mở rộng các ý lớn thành các gạch đầu dòng có giải thích: khái niệm, phương pháp, giai đoạn, độc lập, giải phóng dân tộc, CNXH/quá độ, Đảng/Nhà nước, Mặt trận, văn hóa, đạo đức và giáo dục.
- Dùng các trang PTIT và giáo trình được cung cấp, giữ căn cứ nguồn chính thống đã kiểm tra cho tiểu sử/số liệu. Ba chức năng văn hóa dẫn giáo trình Bộ GDĐT 2009 trang PDF 101–102; giáo dục toàn diện và phương châm đối chiếu trang 103, kết hợp PTIT trang 149/164. Không gán ba chức năng văn hóa sang trang PTIT chỉ trình bày vai trò văn hóa.
- `lesson-coverage.json` ghi từng câu, chương, concept, mục, đáp án nội dung và hash. Validator kiểm tra thiếu ý, gán trùng, nguồn/trang hợp lệ và báo khi câu thay đổi mà audit chưa được cập nhật. Hash thể hiện tính nhất quán của dữ liệu, không tự chứng minh độ đúng của diễn giải.

## Kết quả kiểm tra

- `npm run check`, `npm test`: đạt; 34 kiểm tra logic/dữ liệu. Bao gồm 506 liên kết, hash từng câu, nguồn, kiến thức nhiều thành phần, các trường hợp liên hệ, từ chối bỏ sót hoặc gán trùng.
- `npm run build`: đạt; còn cảnh báo kích thước chunk nội dung lớn đã có trước đó.
- 29 kiểm tra trình duyệt đạt: các chương hiển thị toàn bộ câu đúng chương; mục lục bằng bàn phím, mở/thu gọn, giữ trạng thái mở khi đổi số câu, luyện theo mục, chọn đáp án và chấm sau reload, luyện một câu liên hệ, màn hình điện thoại không tràn ngang.
- Browser QA tại local: 6 chương có đúng 45 mục, 506 ID không lặp; luyện mục Nhà nước với đúng 18 câu, lưu/chấm/nộp đạt. Không lỗi JavaScript hoặc phản hồi tài nguyên lỗi.
- Đã xem ảnh tại 1366×768: mục lục, khung luyện và chữ nội dung rõ, keyword nổi bật; chưa coi việc mở một mục hoặc trả lời đúng một câu là đã nắm hết mọi câu trong mục.
