# Đề tổng hợp TTHCM 60 câu — 16/11/2026

- Đổi `comprehensiveExamSize` của TTHCM từ 50 thành 60. Bộ 506 câu được chia thành **8 đề 60 câu và 1 đề cuối 26 câu**; mỗi câu xuất hiện đúng một lần trên cả bộ.
- Giữ phân bổ đều từng chương giữa tám đề chính: chênh tối đa một câu cùng chương giữa hai đề. Đề cuối có đủ sáu chương.
- Nội dung hiển thị lấy số câu từ cấu hình, bỏ câu nhắc cứng “đủ 50”. README và đặc tả cập nhật theo bộ đề mới.
- `paperKey` chứa kích thước đề để tránh gán điểm/bài dang dở của bộ 50 câu cũ lên đề mới. Lịch sử và bài cũ vẫn giữ; bài cũ có thể tiếp tục, chọn đề mới hỏi trước khi thay bài đang làm.

## Kiểm tra

- `npm test`: 40 kiểm thử đạt, gồm đủ 506 ID duy nhất, phân bố chương, đề 60 câu lưu/khôi phục và phân biệt khóa lịch sử cũ/mới.
- `npm run build -- --logLevel warn`: TypeScript, kiểm tra nội dung và build đạt.
- `npx playwright test tests/browser/comprehensive.spec.ts`: 4 kiểm thử đạt trên Chrome, gồm làm đề 60 câu, chọn câu cuối, chấm điểm, tải lại, lưu/tiếp tục, đề cuối 26 câu trên mobile và chuyển tiếp bài 50 câu cũ.

## Bản public

- Commit `f74f172`, [workflow 43814631287](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43814631287) hoàn tất thành công, gồm toàn bộ kiểm thử và triển khai GitHub Pages.
- Kiểm tra trực tiếp lúc 06:09 UTC ngày 16/11/2026: mở đủ chín đề, số câu lần lượt `60/60/60/60/60/60/60/60/26`; tổng 506 ID duy nhất, khớp toàn bộ ngân hàng.
- Kiểm tra phân bố chương trên các đề thực tế: chênh tối đa một câu cùng chương giữa tám đề chính; đề cuối đủ sáu chương. Không có lỗi JavaScript.
- Ảnh chụp desktop lưu tại `.analysis/tthcm-60-public.png` trong workspace.
