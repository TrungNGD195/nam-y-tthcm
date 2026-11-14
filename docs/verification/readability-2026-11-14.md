# Cỡ chữ và màu sắc — 14/11/2026

Luồng kiểm tra: trang chọn môn → TTHCM / đề tổng hợp / làm trắc nghiệm; Xử lý ảnh → chọn bộ → mở lời giải có công thức. Website tĩnh, không đổi dữ liệu câu hỏi hoặc quy tắc chấm.

- Chuyển cỡ chữ CSS và các cỡ inline của trang học sang rem. Cỡ đo thực ở viewport 1366×768: body 18px, menu 16px, mô tả môn 18px, câu hỏi 25px, phương án 18px, lời giải Xử lý ảnh 18px.
- Nền chính `#eeede7`; thẻ `#faf9f5`; màu nhấn đỏ/xanh giảm độ rực. Chữ phụ trước đây nhạt đổi sang `#56625b`; keyword/gợi ý có nền dịu và chữ tối. Màu focus theo màu nhấn môn.
- Tỷ lệ tương phản tính từ sRGB: chữ chính/thẻ 12,12:1; chữ phụ/thẻ 6,05:1; chữ trắng/nút TTHCM 7,40:1; chữ trắng/nút Xử lý ảnh 6,78:1; keyword TTHCM 6,30:1. Đây là các cặp đã kiểm tra, không tuyên bố đo toàn bộ mọi thành phần.
- Các nút Vào học trên trang chọn môn ở khoảng y=691, nằm trong màn hình desktop cao 768px; hai nút chọn bộ Xử lý ảnh ở khoảng y=558. Các trang đã đo không tràn ngang; ma trận/công thức giữ vùng cuộn riêng.
- Điều chỉnh khoảng cách menu, thẻ đề và khối thông tin để cân đối với chữ lớn hơn. Giữ cả bố cục mobile và chế độ màn hình thấp/zoom.
- `npm run build` đạt; 25 browser tests đạt, gồm desktop 1366/1920, mobile 390 và màn hình 683×384. Đã xem ảnh chụp thật của trang chọn môn, chọn đề và làm bài.

Ảnh và số đo tại `.analysis/readability-*.png` và `.analysis/readability-metrics.json` trong workspace; tệp kiểm tra tạm không đưa vào Git.

Sau phát hành: bản `1f166ba` qua [GitHub Actions](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43598747305). Đã đo trực tiếp trên Pages: body/mô tả 18px, câu hỏi 25px, phương án 18px, lời giải 18px; nền `rgb(238,237,231)`, màu nhấn Xử lý ảnh `#35635e`. Không có pageerror hoặc tràn ngang trong luồng public đã kiểm tra.
