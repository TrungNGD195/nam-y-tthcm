# Luyện đề tổng hợp TTHCM — 14/11/2026

Luồng: tổng quan/sidebar → chọn một trong 19 đề → làm 50 câu → lưu/tải lại → nộp → xem điểm, đáp án và keyword → làm lại hoặc chọn đề khác. Website tĩnh, dùng đúng ngân hàng 623 câu hiện có; không cần tài khoản/API.

- Mỗi đề 50 ID khác nhau, mỗi chương 8 hoặc 9 câu. Tổng 950 vị trí bao phủ đúng 623 ID của ngân hàng, gồm toàn bộ câu số liệu.
- 19 là số đề ít nhất để giữ 8–9 câu/chương và bao phủ chương 2 có 163 câu: 18×9 = 162 chưa đủ. Chương ít câu được tái sử dụng; số lần dùng các câu trong cùng chương chênh tối đa 1.
- Đề sinh ổn định từ phiên bản ngân hàng, không thay thành phần khi làm lại hoặc đổi tiến độ. Không sửa nội dung/đáp án câu hỏi.
- 30 core tests đạt: bao phủ, phân bố, không trùng trong đề, tái lập, công bằng khi dùng lại, chương không liên tiếp, lưu/khôi phục và từ chối bộ ID hỏng. Giữ các kiểm tra trắc nghiệm và bộ tự luận trước đó.
- 25 browser tests đạt: ba kiểm tra mới bao gồm chọn đề, 50 nút điều hướng, giữ kín lời giải trước nộp, giữ lựa chọn/deadline sau reload, chấm 50 câu, làm lại cùng bộ, tiếp tục/thay bài dang dở, mobile không tràn ngang. Các luồng TTHCM 20 câu và Xử lý ảnh đều qua.
- Ảnh giao diện: `test-results/comprehensive-desktop.png` (không đưa thư mục tạm vào Git).
- Bản build qua TypeScript và validator nội dung. Cảnh báo chunk dữ liệu lớn đã có từ ngân hàng, dữ liệu môn vẫn tải theo môn đang mở.

## Sau phát hành

- Bản `52b35f6` triển khai thành công: [GitHub Actions](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43596465894).
- Đã mở trực tiếp cả 19 đề tại [trang public](https://trungngd195.github.io/nam-y-tthcm/#/mon/tthcm/de-tong-hop): mỗi đề 50 ID khác nhau, 6 chương đều 8–9 câu, hợp các đề đúng 623 ID ngân hàng. Đã kiểm tra chọn đáp án, reload, nộp và đủ 50 mục kết quả trên public; không có pageerror hoặc tài nguyên cùng website trả HTTP lỗi.
