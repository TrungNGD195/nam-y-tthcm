# Bài tập Xử lý ảnh dạng trang PDF — 15/11/2026

Luồng cần kiểm tra: chọn bộ/chương → đọc đề gốc → mở lời giải → đọc ảnh trang PDF → mở ảnh lớn hoặc tải PDF → tự đánh dấu cần ôn/đã nắm. Website tĩnh, không có backend hoặc đăng nhập.

## Phạm vi và trình bày

- Chuyển cả 67 bài tính: 21 bài ngân hàng (11 bài 3 điểm, 10 bài 4 điểm) và 46 bài cô Uyên theo chương 3–7. 101 câu lý thuyết giữ chữ/keyword để ôn nhanh.
- Đọc mẫu đáp án ngân hàng ở các trang PDF 21–22 (histogram), 29 (khuếch tán lỗi), 32 (Huffman). Dàn lại từ nội dung đã biên tập, không dùng ảnh đáp án nguồn làm đáp án đúng mặc định.
- PDF A4 dùng chữ serif 13,5pt, công thức vector KaTeX, bảng histogram ngang, ma trận có ngoặc và chú thích, đặt cạnh nhau để so sánh. Bảng dài có tiêu đề cột lặp, không cắt giữa dòng.
- Đánh số bước thay vì tự gán a/b/c theo số bước: ví dụ JPEG 2×2 có bước giải đồng thời hai ý của đề; tránh khiến người đọc hiểu nhầm thứ tự ý hỏi.
- Một PDF tổng hợp có đủ đề và lời giải, dấu trang theo bộ/chương/bài. Web hiển thị ảnh raster từ đúng những trang lời giải của PDF, giữ đề gốc riêng ở phía trên.
- Mỗi trang có ảnh lớn; có liên kết mở đúng trang PDF, tải toàn bộ và bản văn bản hỗ trợ đọc/tìm kiếm. Ảnh tải dần, định kích thước để giảm nhảy trang; tự đánh giá và hai khu vực học được giữ.

## Tính đúng và nguồn

- Giữ công thức tổng quát sau câu dẫn và trước thay số. Viết rõ ví dụ gộp histogram: h′(4)=h(0)+h(8)=4+1=5; đối chiếu bảng nguồn tại trang PDF 22.
- Kiểm tra độc lập bằng NumPy/SciPy: nhân chập/tương quan, co/giãn, histogram, DCT; giải mã ngược Huffman và LZW. Bổ sung kiểm tra tiêu chuẩn Otsu bằng phương sai hai lớp, trung bình lớp đẳng liệu, tích chập làm trơn và giải mã ngược RUN/value.
- Kiểm tra toàn bộ 67 bộ `steps` xuất bản bằng kết quả tính đã kiểm tra, tránh chỉ kiểm tra hàm tính rồi vô tình dùng bảng kết quả cũ trên web.
- Các sai sót/quy ước đã nhận diện ở đáp án nguồn vẫn được nêu tại đúng bài, gồm Prewitt/Sobel, ảnh co là tập con của ảnh gốc, giãn với SE bất đối xứng và các công thức cân bằng/ngưỡng theo bộ bài.
- Huffman dùng tên N1, N2,… cho các nút ghép để tránh bảng chuỗi tuple dài; bảng vẫn định nghĩa đầy đủ hai con và trọng số từng nút. Không thay thứ tự ghép hoặc chuỗi mã.

## Pipeline và kiểm tra

1. `build.py` tạo nội dung từ snapshot và lời giải đã biên tập; `verify.py` kiểm tra số học và nội dung xuất bản.
2. `render-documents.mjs` in PDF thật bằng Chromium, chờ font/ảnh; kiểm tra tràn công thức, chia dòng khi cần.
3. `rasterize_documents.py` ghép PDF, tạo dấu trang, xác định trang bắt đầu lời giải, kiểm tra ký tự/bounds và raster PNG không mất dữ liệu ở 168dpi. Manifest ghi hash nội dung và SHA256 từng ảnh/PDF.
4. Validator chặn ảnh cũ khi sửa nội dung, thiếu trang, gán trùng ảnh, sai trang PDF hoặc đường dẫn không thuộc môn.
5. `verify_documents.py` kiểm tra PDF/ảnh trên đĩa, render lại từng trang PDF và so pixel với ảnh hiển thị, yêu cầu giống hoàn toàn. Kiểm tra ảnh và kiểm tra đáp án là hai bước riêng.

## Kết quả kiểm tra nội dung và tài liệu

- Một PDF 192 trang, gồm đề và lời giải 67 bài; 122 ảnh PNG trang lời giải. Tổng tài liệu/ảnh/bản văn bản khoảng 30,8MB; chỉ tải ảnh bài đang mở, PDF tải khi người học chọn.
- `verify.py` đạt: 28 đối chiếu tương quan, 173 hình thái, 24 histogram, 2 DCT, 4 LZW round-trip, 5 Otsu, 8 đẳng liệu, 16 làm trơn, 3 AC round-trip và 67 bộ lời giải xuất bản khớp kết quả kiểm tra.
- `verify_documents.py` đạt cho toàn bộ 122 ảnh, sai khác pixel lớn nhất **0** so với trang PDF được render lại. SHA256 PDF và các ảnh khớp manifest. Khóa PyMuPDF 1.28.2/Pillow 12.3.0 theo môi trường xuất ảnh để tránh thay bộ raster giữa các lần kiểm tra.
- 37 kiểm tra logic/dữ liệu đạt; gồm giữ câu dẫn/công thức/thay số/kết luận trong tài liệu, bảng histogram ngang, tên nút Huffman và từ chối ảnh cũ/thiếu/gán trùng/sai trang.
- TypeScript, validator và build đạt. Đã xem ảnh tại 1366×768: histogram, Huffman, JPEG 2×2 và làm đầy hai vùng; công thức, ma trận, bảng có cỡ chữ rõ và không tràn khung.

- Browser QA trên bản local: mở đủ 67 bài, có đúng 122 ảnh lời giải, không còn các khối HTML/KaTeX lời giải bài tính. Tải và đối chiếu SHA256 tất cả 122 PNG cùng PDF; tự đánh dấu rồi reload vẫn giữ đúng trạng thái. Không có lỗi JavaScript.

## Xác nhận phát hành

- Commit `9e8b325` được triển khai GitHub Pages thành công qua [GitHub Actions](https://github.com/TrungNGD195/nam-y-tthcm/actions/runs/43726838733): check, 37 core tests, kiểm tra số học, kiểm tra PDF/PNG và toàn bộ 30 browser tests đều đạt.
- Lượt browser local đầu có hai ca vượt giới hạn 30 giây khi chạy song song với QA toàn bộ tài liệu; 28 ca còn lại đạt. Chạy riêng lại đúng hai ca đó đều đạt, không thay mã để che lỗi hay tăng timeout.
- Trên bản public, browser QA mở đủ 67 bài, đối chiếu đúng 122 ảnh và tải/kiểm tra SHA256 toàn bộ ảnh cùng PDF 192 trang. Giữ đánh dấu sau reload, không lỗi JavaScript. PDF public: `subjects/xu-ly-anh/answer-pages/xu-ly-anh-67-bai-giai-4dc7c820fd81.pdf`.
