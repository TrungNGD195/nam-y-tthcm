# Kết quả kiểm tra bản đầu

Ngày: 13/11/2026. Bản dữ liệu: `2026.11.13.1`.

## Đã đạt tại máy

- TypeScript và kiểm tra nội dung: 215 câu chuẩn, đủ quyết định cho 233 mục nguồn, đề mẫu 20 câu, 11 mục chưa dùng để chấm không lọt vào đề.
- 11 kiểm thử engine: chấm theo ID sau đảo đáp án; không ghi nhận lặp khi tải lại/nộp lại; gợi ý và đánh dấu; bỏ qua; đề trộn đủ 6 chương có số liệu; bộ lọc; đề mẫu; khôi phục dữ liệu; tìm kiếm tiếng Việt; luyện lại đúng nhóm câu của lượt trước.
- 10 kiểm thử Chrome headless: luyện và ôn sai; Enter/giữ phím; thi không lộ đáp án, giữ deadline sau reload và tự nộp; tìm keyword; xuất/nhập và JSON lỗi; storage bị chặn; điều hướng và reload ở 1366×768, 1920×1080, 390×844 và 683×384.
- Build production thành công; JavaScript khoảng 72 KB gzip, CSS khoảng 7 KB gzip. Không có backend hay yêu cầu API key.

## Giới hạn cần giữ rõ

- Bộ Tổng hợp và Bonus chưa được nhập toàn bộ; xem báo cáo nội dung cho phạm vi chính xác. Không nhận các câu còn mâu thuẫn là đã có đáp án chắc chắn.
- Kiểm thử trình duyệt tại máy dùng Chrome; chưa xác nhận riêng Safari và Firefox.
- Kích thước 683×384 kiểm tra trường hợp vùng nhìn hẹp; không thay thế việc kiểm tra mức phóng to bằng giao diện thật của mọi trình duyệt.
- Thống kê học tập lưu riêng theo trình duyệt. Xuất/nhập JSON dùng để chuyển máy, không có đồng bộ tài khoản.

Workflow GitHub Pages tiếp tục chạy cùng các kiểm tra engine, nội dung và trình duyệt trước khi công khai bản build.

## Bản public

- Website: https://trungngd195.github.io/nam-y-tthcm/
- Repository: https://github.com/TrungNGD195/nam-y-tthcm
- Workflow build và deploy đã thành công: https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43464845102
- Đã mở URL public bằng Chrome headless: HTTP 200, đủ 6 chương; chọn chương → bắt đầu luyện → chọn đúng → xem lời giải → reload giữ nguyên kết quả. Không ghi nhận lỗi JavaScript hoặc HTTP trong lượt kiểm tra.
