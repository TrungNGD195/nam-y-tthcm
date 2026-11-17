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

## C?ng b? v? ki?m tra c?ng khai

- Commit tri?n khai: `39b43cc`; [GitHub Actions 44060253789](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/44060253789) ho?n t?t th?nh c?ng, g?m ki?m tra n?i dung, ph?p t?nh, PDF, build v? 34 b?i ki?m tra tr?nh duy?t tr?n Linux.
- [Web c?ng khai](https://trungngd195.github.io/nam-y-tthcm/): ??i chi?u ?? **67 b?i t?nh** (?nh ?? g?c, b?n ch?p, c?c ph?n l?i gi?i, c?ng th?c v? c?ch l?m), **36 c?u l? thuy?t ?? s?a** (g?m 10 tham chi?u), m? ???c ?? g?c v? n?i dung tr? l?i kh?p d? li?u; kh?ng c? l?i JavaScript hay tr?n ngang ? m?n h?nh 1366?768.
- Ki?m tra SHA-256 ?? **193 ?nh** c?ng khai. M?t l??t t?i ?nh b? timeout v? m?t ?nh tr? HTTP 503; t?i l?i v?i s? k?t n?i ??ng th?i th?p h?n ?? ??t, kh?ng thay ??i n?i dung ?? n? l?i m?ng.
- T?i ???c PDF c?ng khai **13.837.861 byte**, ?? 263 trang, SHA-256 `2e2c2202fb8518a77ae0e4c5826bdd04c726f398360197f97724f697704d53b8` kh?p ch?nh x?c b?n xu?t.
- ?? xem ?nh ch?p giao di?n c?u 4.L3 (ch? h?i l? do th?m m?c K), 4.L4 (tham chi?u HSV/HSL), v? b?i t?nh 6.T11 (c?c c?u a?g gi? ??y ??).

| Lu?ng | K?t qu? | B?ng ch?ng |
|---|---|---|
| Ch?n c?u ? d? li?u | ??t | To?n b? ID gi? nguy?n; 168 m?c |
| L? thuy?t ? ph?n m?i / tham chi?u | ??t | 36 c?u c?ng khai ??ng prompt, ??p ?n v? li?n k?t |
| ?? g?c ? ??i chi?u | ??t | N?i dung g?c gi? nguy?n v? m? ???c |
| B?i t?nh ? PDF / ?nh / b?n v?n b?n | ??t | 67 b?i ?? ph?n, 193 hash ?nh v? hash PDF kh?p |
| Ti?n ?? h?c ? t?i l?i | ??t | L?u d?u C?n ?n qua reload, l?i gi?i v?n thu g?n khi m? l?i |
