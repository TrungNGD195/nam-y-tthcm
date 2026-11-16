# Câu trả lời lý thuyết Xử lý ảnh — 16/11/2026

## Phạm vi và căn cứ

Đã viết lại 101 câu lý thuyết thành câu trả lời hoàn chỉnh theo từng vế đề hỏi, thay cho dàn ý và lời hướng dẫn viết bài. Keyword vẫn được tô nổi bật; công thức, ví dụ, kết luận đúng/sai kèm lý do và MATLAB xuất hiện khi câu hỏi yêu cầu. Nội dung biên tập tại `scripts/content/xu-ly-anh/theory_answers.py`, ánh xạ đề tại `theory.py`.

- **Ngân hàng:** 30 câu lý thuyết, 27 câu có mục đáp án phù hợp nội dung. Đối chiếu với giáo trình và slide trước khi dùng. Ngân hàng 1.11 gồm nhiễu và biên trực tiếp, tương ứng hai mục 1.11–1.12 trong đáp án. Ba câu ngân hàng 1.12–1.14 không có mục tương ứng nội dung trong đáp án; dùng giáo trình, không gán trang đáp án chỉ vì trùng số.
- **Cô Uyên:** 71 câu lý thuyết dựa trên giáo trình/slide, cùng cách trình bày trả lời trực tiếp như ngân hàng.
- Sửa và ghi chú ngay tại câu các lỗi đáp án: CMY không bao trùm mọi màu nhìn thấy; chuyển RGB 8 bit dùng **255**, không phải 225; Prewitt có trọng số giữa **1**, Sobel **2**, Frei–Chen **√2**.
- Giữ các biến thể lọc có ngưỡng θ trong giáo trình. Câu Canny giải thích vai trò của bước loại cực đại và hai ngưỡng; tài liệu không xác định một bước quan trọng nhất tuyệt đối. Tỷ lệ nén không tổn thất 2–10 có căn cứ tại slide nén ảnh tiếng Anh trang 17; không gán một khoảng tỷ lệ phổ quát cho nén có tổn thất.
- Giữ nguyên toàn bộ 67 bản ghi bài tính và các PDF/PNG đã xuất. Kiểm tra sự tương thích PDF dựa trên hash từng bài tính, độc lập với thay đổi phiên bản lý thuyết.

`content/xu-ly-anh/theory-answer-review.json` lưu 101 ID, căn cứ, trang đáp án, các phần trả lời, hash đề và hash câu trả lời.

## Kiểm tra tại máy

- `npm test`: 40 kiểm thử đạt, gồm đối chiếu hash, ánh xạ nguồn đáp án, các vế hỏi cụ thể và bảo vệ PDF khi nội dung bài tính thay đổi.
- `npm run build -- --logLevel warn`: đạt TypeScript, validator nội dung và build. Vite báo cảnh báo kích thước chunk dữ liệu, không chặn build.
- `npm run test:e2e`: 31 kiểm thử trình duyệt đạt trên Chrome. Kiểm tra câu trả lời đầy đủ, công thức, lỗi nguồn, đúng/sai, MATLAB, chức năng ôn và PDF bài tính.
- `python -X utf8 scripts/content/xu-ly-anh/verify.py`: đạt toàn bộ kiểm tra tính toán độc lập và khớp 67 lời giải đã xuất.
- So sánh dữ liệu với bản trước: 67/67 bản ghi bài tính giống hoàn toàn; manifest PDF và thư mục ảnh lời giải không thay đổi.
- Đã xem ảnh chụp toàn trang câu CMY ở desktop 1366 px: đoạn trả lời, tiêu đề từng phần, công thức, keyword và ghi chú nguồn hiển thị rõ.

## Kiểm tra bản public

- Commit triển khai: `deae60d`. [Workflow 43813323857](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43813323857) hoàn tất thành công cả build và deploy, gồm kiểm tra tính toán, PDF, trình duyệt.
- Lúc 05:57 UTC ngày 16/11/2026, đã truy cập đủ **101 câu lý thuyết trên GitHub Pages**, mở lời giải và so sánh từng đoạn với dữ liệu đã biên tập: khớp toàn bộ.
- **59 khối công thức** hiển thị thành công, không có KaTeX error hoặc lỗi JavaScript. Ảnh chụp lưu tại `.analysis/theory-bank-2-2.png` và `.analysis/theory-uyen-6-L9.png` ở máy làm việc.
- [Mở câu CMY có ghi chú sửa đáp án nguồn](https://trungngd195.github.io/nam-y-tthcm/#/mon/xu-ly-anh/bai/bank-2-2).
