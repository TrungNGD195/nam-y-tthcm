# Chỉ lược ý hỏi lý thuyết — 17/11/2026

## Phạm vi và kết quả

Yêu cầu đính chính: chỉ sửa lý thuyết, giữ bài tập. Thay thế bản rút gọn 23 bài tính đã triển khai trước đó.

- Khôi phục đầy đủ mọi yêu cầu của **67 bài tính**, trong đó **46 bài cô Uyên**. Giữ các cải tiến chia câu (a), (b), (c), câu dẫn, công thức, ký hiệu và cách làm. Không còn `editedQuestion`, dữ kiện trung gian cho sẵn hoặc lời giải bị cắt theo cơ chế cũ.
- Giữ đủ **71 câu lý thuyết cô Uyên**, nguyên mã và phân chương. Rà 36 câu: **26 câu giữ các ý mới**, **10 câu giữ dạng tham chiếu** về câu đã hỏi. Câu trùng hoàn toàn vẫn có đề gốc và nút xem câu trả lời đối chiếu; không bịa thêm yêu cầu để lấp số câu.
- Ngân hàng vẫn đủ **51 mục**; toàn môn đủ **168 mục**, gồm 101 lý thuyết và 67 bài tính.
- Đề gốc và các vế đã lược được lưu riêng trong `theoryFocus.sourcePrompt`, không ghi đè `originalText`. `theory-focus-review.json` lưu nội dung lược/giữ, liên kết và hash. Audit bài tính cũ chuyển vào `content/xu-ly-anh/archive/` và không còn áp dụng.
- Câu lý thuyết có lời giải thành đoạn văn, giữ công thức và keyword; các nhận định đúng/sai còn lại giữ đúng nhãn gốc: 4.L8 (d), 6.L9 (a,d,e), 7.L8 (b,c,e,f).
- Tăng revision những câu thay đổi để tiến độ cũ không tự đánh dấu Đã nắm cho nội dung khác.

## Tính chính xác và tài liệu

Đối chiếu các vế với đề nguồn, giáo trình và slide đã được lưu trong workspace. Những lỗi tính toán đã kiểm tra vẫn được sửa: 4.T3 không dùng nhầm dòng toàn 90 của 4.T4; bài Otsu 5.T4 có cực đại tại 3 và 5 nhưng không tại 4, nên không lấy trung bình 4 làm ngưỡng tối ưu. Giữ các sửa lỗi đáp án ngân hàng về RGB–CMY và trọng số mặt nạ.

Xuất lại PDF **263 trang**, **193 ảnh lời giải**, fingerprint `399fc0046cfb`. Ảnh được chụp từ PDF thật; không thay lời giải bài tính bằng HTML.

## Kiểm tra trước công bố

- `npm run check`, `npm test`: đạt, **43/43 kiểm tra**.
- `verify.py`: đạt với toàn bộ 67 lời giải được tuần tự hóa và kiểm tra tính toán độc lập bằng NumPy/SciPy.
- `verify_documents.py`: đạt 67 bài, 263 trang PDF, 193 ảnh, sai khác pixel trung bình tối đa **0**.
- Luồng trình duyệt: chọn câu → chỉ thấy vế mới → mở đề gốc → xem lời giải; câu tham chiếu → mở câu đã hỏi; bài tính → đủ nút các phần và ảnh PDF. Kết quả trình duyệt và công bố được ghi bổ sung sau khi hoàn tất.

Web tĩnh dùng dữ liệu JSON và tài liệu cùng bản build; không có API, đăng nhập hoặc dịch vụ dữ liệu cần cấu hình.

## Công bố và kiểm tra công khai

- Commit `39b43cc`; [GitHub Actions 44060253789](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/44060253789) thành công.
- Web công khai: đối chiếu đủ 67 bài tính, 36 câu lý thuyết đã sửa (gồm 10 tham chiếu), đề gốc và nội dung trả lời khớp dữ liệu; không có lỗi JavaScript hoặc tràn ngang ở màn hình 1366×768.
- Kiểm tra SHA-256 đủ 193 ảnh công khai. Một lượt tải timeout và một ảnh trả HTTP 503; kiểm tra lại với số kết nối thấp hơn đã đạt.
- PDF công khai đủ 263 trang, 13.837.861 byte; SHA-256 `2e2c2202fb8518a77ae0e4c5826bdd04c726f398360197f97724f697704d53b8` khớp bản xuất.
- Đã xem ảnh giao diện câu 4.L3, 4.L4 và bài tính 6.T11; tiến độ Cần ôn giữ qua tải lại trang.
