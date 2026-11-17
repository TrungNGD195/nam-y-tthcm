# Lược ý hỏi lặp trong bài cô Uyên — 17/11/2026

## Kết quả

- Giữ đủ **46 bài tập cô Uyên**, 117 mục cô Uyên và 168 mục toàn môn. Giữ ID/mã bài; không xóa hay gộp cả bài chỉ vì cùng phương pháp.
- Rà theo thứ tự chương và số bài, chỉnh **23 bài** ở cấp ý hỏi. Phần đã luyện chuyển thành kết quả trung gian tính cho đúng dữ kiện của bài hiện tại; các yêu cầu mới và điều kiện khác biệt tiếp tục được hỏi/giải. Bài còn lại giữ đề hiện tại.
- Các ví dụ: 5.T6 cho sẵn histogram/làm trơn để tập trung đếm đỉnh; 6.T2 cho sẵn kết quả Huffman, giữ hòa tần suất và mã cố định; 6.T11 cho sẵn lượng tử, zig-zag, mã DC, giữ DCT 2×2, mã AC, ghép bit và giải nén.
- Đề ôn tập có yêu cầu ở đầu, dữ kiện và kết quả cho sẵn ở dưới, liên kết xem lại phương pháp. Liên kết không khóa bài. Ảnh/bản chép đề gốc giữ đầy đủ trong mục mở riêng.
- Đề ôn tập, lời giải, PDF và bản văn bản dùng chung nội dung biên tập. Bài đổi tăng revision để dấu Đã nắm cũ không tự áp lên yêu cầu mới.

## Đối chiếu và sửa lỗi

- `content/xu-ly-anh/exercise-focus-review.json`: 23 quyết định, các ý lược, trọng tâm giữ lại, bài trước tương ứng và hash của bản gốc/đề ôn tập/lời giải.
- `scripts/content/xu-ly-anh/exercise_focus.py`: biên tập ý hỏi và lựa chọn các bước giải; kết quả cho sẵn lấy từ các phép tính đã được kiểm tra, không lấy ma trận của bài khác thay vào.
- Sửa phần lời giải 4.T3 trước đây còn nhắc nhầm dòng toàn 90: dòng này thuộc 4.T4. Bài 4.T3 hiện đối chiếu đúng hai ảnh kết quả trên dữ kiện của nó; 4.T4 tập trung dòng 90 với θ=100.
- Histogram 5.T4 có cực đại Otsu tại 3 và 5, nhưng f(4) nhỏ hơn cực đại. Chọn 3 hoặc 5; không lấy trung bình 4 một cách máy móc. Tiêu chuẩn cực đại tại giáo trình PDF trang 32 là căn cứ trực tiếp. Cách chọn ngưỡng và hai câu lý thuyết liên quan được làm rõ cùng kiểm thử hồi quy.

## Kiểm tra tại máy

- `npm test`: **45 kiểm thử đạt**, gồm giữ đủ ID, bảo toàn đề gốc, đối chiếu hash, yêu cầu/đáp án khớp, giữ trọng tâm mới, liên kết tới bài trước, revision tự đánh giá và trường hợp Otsu rời nghiệm.
- `npm run build -- --logLevel warn`: TypeScript, validator dữ liệu và build đạt. Vite chỉ cảnh báo kích thước chunk dữ liệu.
- `npm run test:e2e`: **34 kiểm thử đạt**, có luồng đề đã lược ý, dữ kiện cho sẵn, mở đề gốc, xem lại bài trước, đọc lời giải và nhảy đúng câu PDF.
- `verify.py`: toàn bộ kiểm tra độc lập đạt; 67 lời giải khớp bản xuất, thêm hồi quy chọn ngưỡng Otsu đúng cực đại.
- PDF mới **249 trang**, **170 ảnh trang lời giải**, 67 bản văn bản. `verify_documents.py` kiểm tra SHA, vị trí tiêu đề, đủ ký hiệu/cách làm và sai số pixel giữa ảnh/PDF bằng **0**.
- Fingerprint `88fcacd1437e`; SHA-256 PDF `63fe86a23a4dc383f77aaaddf540e06de7ee570a4bc971e1abb7ba217f5bbddb`.
- Đã xem bản chụp desktop và các trang PDF mẫu: yêu cầu còn lại rõ, các phần trung gian cung cấp đủ dữ kiện và bản gốc không lẫn vào đề cần làm.

## Kiểm tra bản public

- Commit triển khai `e9b2f09`, [workflow 44043003755](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/44043003755) thành công cả kiểm tra và triển khai GitHub Pages.
- Đã mở đủ 67 bài, đối chiếu danh sách phần giải và bản văn bản; 23 đề đã chỉnh khớp các yêu cầu mới và vẫn có ảnh đề gốc trong mục mở riêng. Đã đối chiếu SHA-256 đủ 170 PNG tải từ web.
- Lần tải PDF bằng Playwright vượt giới hạn 30 giây sau khi trả HTTP 200. Kiểm tra tiếp bằng Python đọc luồng thành công: **11.813.287 byte**, SHA-256 khớp `63fe86a23a4dc383f77aaaddf540e06de7ee570a4bc971e1abb7ba217f5bbddb`.
- Kiểm tra riêng toàn bộ **23 đề đã chỉnh** cùng hai câu lý thuyết Otsu liên quan hoàn tất lúc 08:23 UTC ngày 17/11/2026: yêu cầu và nhãn từng câu khớp, không có lỗi JavaScript. Đề gốc 5.T6 mở được, ảnh nguồn trả HTTP 200 và tải thành công.
- Kết quả tại workspace: `.analysis/focused-questions-public-review.json`, `.analysis/focus-public-pdf-review.json`; ảnh desktop tại `test-results/focused-exercise-question.png`.
