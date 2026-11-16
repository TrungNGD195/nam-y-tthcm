# Xử lý ảnh: từng câu và từng bước — 16/11/2026

## Thay đổi

- Biên tập lại cách trình bày **67 bài tập**, gồm **177 phần, 239 bước và 187 công thức**. Tách theo nhãn (a), (b), (c)… của đề; đánh số bước lại từ 1 trong mỗi câu. Các bài không đánh chữ có phần giải theo phép tính, không tự giả định nhãn nguồn.
- Mỗi bước tính có câu dẫn, công thức, giải thích ký hiệu tại chỗ, cách thực hiện, thay số và kết quả. Các câu nhận xét trả lời trực tiếp. Ví dụ nhân mặt nạ ghi đủ tích tại một pixel; JPEG tách lượng tử hóa, zig-zag, mã DC, mã AC, chuỗi bit và giải nén. Câu giải nén tách tiếp giải lượng tử, DCT ngược, RMS với bốn sai lệch cụ thể.
- Giữ nguyên đề gốc của 67 bài, nội dung 101 câu lý thuyết và toàn bộ **124 ma trận kết quả** trong bản trước. Thêm giải thích và các ma trận trung gian cần thiết, không thay các giá trị đã kiểm tra. Ngân hàng 4.3–4.4 đánh a hai lần: lời giải ghi câu thứ hai là (b), có ghi chú tại bài.
- Lý thuyết đúng/sai tách từng nhận định ở đề; khi mở lời giải, nhắc lại đúng nhận định phía trên kết luận và giải thích.
- PDF tổng hợp **263 trang**, xuất **193 ảnh trang lời giải** cùng 67 bản văn bản. Mỗi câu có nút nhảy đúng trang và vị trí tiêu đề trong ảnh. Công thức/bảng/ma trận bài tập tiếp tục được hiển thị từ ảnh PDF.

## Tệp và cách tái tạo

- `scripts/content/xu-ly-anh/worked_parts.py`: ánh xạ ý hỏi, giải thích ký hiệu và thao tác. Dữ liệu tính từ `calculations.py`/`exercises.py`.
- `node scripts/content/xu-ly-anh/render-documents.mjs`: in PDF thật bằng Chromium.
- `python -X utf8 scripts/content/xu-ly-anh/rasterize_documents.py`: gộp PDF, xuất ảnh, bản văn bản và tọa độ từng câu.
- Manifest tại `src/subjects/xu-ly-anh/documents.json`; fingerprint `1fb3f2ad77a4`.
- PDF: `public/subjects/xu-ly-anh/answer-pages/xu-ly-anh-67-bai-giai-1fb3f2ad77a4.pdf`; SHA-256 `95827f8364823ccc3565f2a33fd75cd8c572f6f4d849cfa021e5a4e8b44e51b4`.

## Kiểm tra

- TypeScript, validator nội dung và build đạt. Validator chặn công thức thiếu giải thích ký hiệu, bước thiếu cách làm hoặc tiêu đề câu và bản PDF không tương thích.
- **41 kiểm thử logic đạt**, gồm đủ nhãn a–g của JPEG, thứ tự công thức/ký hiệu/cách làm/thay số và giữ đầy đủ nội dung trong bản in.
- **33 kiểm thử trình duyệt đạt**. Sau lần bổ sung ví dụ JPEG cuối, kiểm thử nhảy tới từng câu và bản văn bản được chạy lại thành công; CI chạy lại toàn bộ khi triển khai.
- `verify.py`: các phép tính tương quan, hình thái, histogram, DCT, LZW, Otsu, ISODATA, làm trơn, AC đều qua đối chiếu độc lập và khớp 67 lời giải xuất bản.
- `verify_documents.py`: 67 bài, 263 trang, **193 ảnh khớp PDF với sai số pixel 0**; xác nhận đủ phần “Ký hiệu”, “Cách làm” và đúng vị trí tiêu đề từng câu.
- So sánh với bản trước: 101 câu lý thuyết không đổi dữ liệu; 67 đề gốc và 124 ma trận giữ nguyên. Đã xem ảnh trang PDF và ảnh chụp trên desktop để rà bố cục.

## Bản public

- Commit `93975f4`, [workflow 43892044797](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43892044797) hoàn tất thành công cả kiểm tra và triển khai.
- Đã mở đủ **67 bài trên GitHub Pages**, đối chiếu số trang, danh sách từng câu và bản văn bản; đủ phần “Ký hiệu”, “Cách làm” tương ứng mỗi công thức/bước.
- Tải và kiểm tra SHA-256 toàn bộ **193 ảnh và PDF 263 trang** từ bản public: khớp manifest, không có lỗi JavaScript.
- Lúc 15:05 UTC ngày 16/11/2026, kiểm tra nút câu (g) của bài JPEG 6.T11: cuộn đúng vị trí tiêu đề trong ảnh. Câu lý thuyết 7.L8 có đủ bảy nhận định riêng và bảy phần trả lời tương ứng.
- Ảnh chụp public tại `.analysis/subpart-navigation-public.png`; kết quả đủ 67 bài tại `.analysis/document-solutions-live-qa.json` trong workspace.
