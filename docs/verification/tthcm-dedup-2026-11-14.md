# Gộp câu trùng và bỏ lặp giữa các đề — 14/11/2026

Yêu cầu đã xác nhận: bỏ cả câu trùng nội dung trong ngân hàng và việc một câu xuất hiện ở nhiều đề tổng hợp; cho phép đề cuối ít hơn 50 câu và không ép mỗi chương 8–9 câu/đề.

- Đọc 44 nhóm trùng đề và các cặp gần nghĩa; chỉ gộp các nhóm đã đối chiếu ý hỏi, đáp án và lựa chọn. Giữ riêng các câu khác giai đoạn, phủ định, đối tượng, đoạn trích hoặc nội dung kiểm tra, dù gần giống chữ hoặc cùng đáp án.
- Gộp 117 bản trong 96 nhóm, từ 623 xuống **506 câu**. Quyết định giữ/gộp, đề/đáp án trước gộp và hash khóa mỗi mục tại `content/tthcm/duplicate-decisions.json`. Snapshot 522 câu Azota không sửa; audit đủ 755 mục nguồn và mọi trích dẫn được giữ trong bản đại diện.
- Số câu chương 1–6: **30 / 123 / 115 / 105 / 52 / 81**; 92 câu số liệu. Đề mẫu gốc vẫn đủ 20 ID, không thay câu hoặc thứ tự nguồn.
- Bộ đề tổng hợp: **10×50 + 6 = 506** vị trí, hợp ID đúng 506, không có ID nào xuất hiện hai lần trong cả bộ. Các đề chính phân bổ từng chương chênh tối đa 1 câu giữa các đề; đề cuối 6 câu có một câu mỗi chương.
- Đề sinh ổn định theo phiên bản; `paperKey` mới phân biệt kết quả/bài dang dở của bộ cũ với bộ mới cùng số đề. Điểm lịch sử cũ vẫn là lịch sử, không gán làm điểm đề mới.
- Tiến độ ID được gộp chuyển về ID chuẩn khi đọc/nhập: giữ bản ghi gần nhất, hợp bookmark, không cộng lượt để thổi số câu đã gặp. Bài có ID/lựa chọn không còn phù hợp được báo, không chấm lại theo phương án của câu khác.
- Curator chạy lại tạo cùng hash ngân hàng, không đưa các câu đã gộp trở lại. Word gốc vẫn đủ 522 đề/2088 lựa chọn, phần giới thiệu cập nhật số câu web 506.
- **31 core tests và 25 browser tests đạt**. Bao gồm nguồn/băm đáp án sau gộp, alias migration, không mất khác biệt giữa câu gần nhau, không trùng trong/toàn bộ đề, đề cuối 6 câu, reload, điểm và lựa chọn, thay/tiếp tục bài, mobile, TTHCM và Xử lý ảnh.
- `npm run build` đạt, validator kiểm tra alias, nguồn và công thức. Dữ liệu kiểm tra tạm lưu trong `.analysis/`, không công bố.
