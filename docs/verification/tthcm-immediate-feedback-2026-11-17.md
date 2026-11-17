# TTHCM — hiện đáp án ngay sau khi chọn

## Hành vi

Áp dụng cho đề tổng hợp 60 câu (và đề cuối 26 câu), đề mẫu và đề trộn của TTHCM. Chọn phương án là chấm ngay, tô đúng/sai và hiện đáp án đúng, giải thích, keyword cùng nguồn đối chiếu. Không cần nút Kiểm tra hoặc nộp cả đề để biết đáp án. Người học tự bấm Câu tiếp để có thời gian đọc giải thích.

Câu đã chấm giữ nguyên lựa chọn; quay lại vẫn xem được đáp án. Mỗi câu chỉ ghi vào tiến độ một lần trong một lượt, kể cả tải lại hay nộp bài. Thứ tự và số câu, cách rải chương, lịch sử và deadline hiện có được giữ.

## Dữ liệu và bài cũ

- Cấu hình môn `examFeedback: immediate`; chính sách được lưu trong session để khôi phục an toàn qua tải lại và xuất/nhập tiến độ. Mặc định của môn chưa cấu hình vẫn là xem sau nộp.
- Khi tiếp tục hoặc nhập bài TTHCM cũ, chấm những lựa chọn đã lưu một lần, giữ ID lượt, thứ tự câu/đáp án, vị trí và deadline.
- Gợi ý của luyện chương giữ luồng hiện có. Đề có thời gian vẫn tự nộp một lần khi đến deadline.

## Kiểm tra

- `npm run check`, `npm test`: đạt **46/46** kiểm tra, gồm chấm đúng/sai theo ID phương án, không chấm lại, khôi phục bài cũ và kiểm tra dữ liệu nhập.
- Playwright: đạt **35/35** kiểm tra. Đã kiểm tra đề tổng hợp (đúng, sai, bàn phím, quay lại, tải lại, nộp, điểm lịch sử), đề mẫu tự nộp đúng deadline và bài cũ chuyển sang phản hồi ngay.
- Build đạt. Phần hiển thị nhãn đổi thành Luyện đề cho lượt có phản hồi ngay.

Luồng kiểm tra: chọn đề → chọn phương án → hiện đáp án và giải thích → lưu tiến độ → tải lại/quay lại vẫn giữ kết quả → nộp không tăng số lượt chấm. Đây là web tĩnh, không có API hoặc dữ liệu máy chủ cần cấu hình.
