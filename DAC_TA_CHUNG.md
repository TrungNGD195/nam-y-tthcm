# Đặc tả chung — Nắm ý, ôn tập nhiều môn

Phiên bản 2.10 · 16/11/2026. Chuẩn triển khai hiện tại; bản Tư tưởng Hồ Chí Minh đầu tiên được lưu trong `docs/archive/`.

## 1. Mục tiêu và phạm vi

Một website public, không đăng nhập, ưu tiên máy tính, để ôn nhiều môn. Người dùng vào trang đầu phải biết ngay **chọn môn nào, bấm đâu để học**. Các môn dùng chung khung điều hướng và khối trình bày; chế độ học phù hợp tài liệu: TTHCM trắc nghiệm, Xử lý ảnh tự luận có lời giải. Dữ liệu và tiến độ tách riêng.

| Môn | Mã ổn định | Trạng thái |
| --- | --- | --- |
| Tư tưởng Hồ Chí Minh | `tthcm` | 506 câu, 6 chương, 92 câu số liệu; 8 đề tổng hợp × 60 + 1 đề cuối 26 câu, không lặp giữa các đề |
| Xử lý ảnh | `xu-ly-anh` | 168 câu/bài có lời giải: 51 ngân hàng, 117 bộ cô Uyên |
| Khoa học dữ liệu | `khoa-hoc-du-lieu` | Chờ giáo trình/ngân hàng từ người dùng |

Không tự đoán số chương, tạo câu từ kiến thức chung hoặc dùng ngân hàng giả cho môn chưa có tài liệu. Các chương Xử lý ảnh lấy theo slide và bộ Ôn tập, không theo số chương khác trong giáo trình PTIT.

## 2. Thiết kế giao diện: rõ khối, rõ hành động

### Trang chọn môn

- Tiêu đề trực tiếp: **Hôm nay bạn muốn học môn nào?**
- Ngay bên dưới là ba thẻ môn học trên desktop, không đặt banner lớn che mất các thẻ.
- Mỗi thẻ có icon, tên môn đủ lớn, trạng thái, mô tả tối đa hai ý, số chương/câu nếu có thật.
- Môn sẵn sàng có **một nút Vào học** nổi bật, rộng bằng thẻ. Bài dang dở có liên kết Tiếp tục nhỏ hơn.
- Môn chưa có tài liệu ghi **Chờ tài liệu**; nút học không hoạt động. Liên kết thông tin dẫn đến trang chờ trung thực, không hiện bài hoặc số lượng giả.
- Phần hướng dẫn ba bước và thông tin tiến độ nằm dưới các thẻ, không tranh trọng tâm.

### Bên trong một môn

- Header và bộ chọn môn luôn cho biết đang học môn nào. Sidebar chỉ hiện chương, chuyên đề và công cụ của môn hiện tại; có đường về Tất cả môn học.
- Hành động đầu tiên: Bắt đầu học từ chương đầu tiên. Kế tiếp là lưới thẻ chương, mỗi thẻ ghi rõ **Học chương này**.
- Nội dung một thẻ chương: số chương → tên → mô tả ngắn → số câu/tiến độ nhẹ → hành động học nổi bật. Không bắt người học đoán icon mũi tên.
- Học theo chương là luồng chính; thi thử, ôn sai, keyword và chuyên đề là khối phụ tách rõ.
- Dùng khoảng trắng, viền, màu nền nhẹ và cỡ chữ để phân cấp; không dùng nhiều màu đậm cho các nút cạnh tranh trên cùng thẻ.
- Desktop: sidebar khoảng 248px, vùng nội dung có giới hạn rộng, trang chọn môn 3 cột; màn hình hẹp chuyển một cột, sidebar thu thành menu.
- Màu môn: TTHCM đỏ trầm, Xử lý ảnh xanh lục lam, Khoa học dữ liệu xanh dương. Trạng thái đúng/sai vẫn có chữ và biểu tượng.
- Chữ dùng đơn vị `rem`, nền cỡ 16px: nội dung chính 18–20px, câu hỏi trắc nghiệm desktop 25px, đáp án 18px, menu/nút 16px, nhãn phụ 13–15px. Trên mobile đáp án tối thiểu 16px. Giãn dòng và khoảng cách khối theo cỡ chữ, bảng/công thức tự cuộn trong khối.
- Bảng màu dịu: nền kem xám `#eeede7`, thẻ kem nhạt `#faf9f5`, chữ chính `#29352f`, chữ phụ `#56625b`. Nhấn TTHCM `#764950`, Xử lý ảnh `#35635e`, Khoa học dữ liệu `#4d6181`; dùng nền nhạt đồng tông cho mục đang chọn. Keyword, đúng/sai và gợi ý dùng màu nền trầm nhẹ, chữ đậm đủ rõ.

Luồng chính: **Chọn môn → Chọn chương → Đọc ý chính / bắt đầu luyện → Xem lời giải → Ôn phần chưa chắc**. Không khóa chương, không giới hạn lượt.

## 3. Tổ chức nội dung theo môn

Catalog chỉ chứa metadata và cấu hình: tên, mã, màu, icon, trạng thái, số câu/chương thực tế, độ dài đề trộn, tên đề mẫu và chuyên đề.

Ngân hàng của mỗi môn chứa `subjectId`, phiên bản, chương, concept, câu đã kiểm duyệt, nguồn, thứ tự đề mẫu và audit các mục nguồn. Chỉ tải ngân hàng khi người học mở môn đó; trang chọn môn không phải tải toàn bộ câu của các môn.

- Chương là dữ liệu động; không cố định 6, cho phép các môn có số chương khác hoặc số thứ tự không liền nhau.
- Chuyên đề do từng môn cấu hình. Mốc thời gian/Đại hội chỉ thuộc cấu hình TTHCM; không ép áp dụng cho Xử lý ảnh/Khoa học dữ liệu.
- Câu có ID ổn định trong môn; cùng một ID của hai môn khác nhau không dùng chung tiến độ.
- Giữ cách hỏi, từ phủ định và đáp án nguồn khi hợp lệ; câu chuyển từ trả lời ngắn có ghi nhận. Mục mâu thuẫn/mơ hồ không vào bài chấm.
- Giải thích 1–2 câu, keyword 1–3 cụm, điểm dễ nhầm và trang/nguồn đối chiếu. Không thêm kiến thức ngoài phạm vi.
- TTHCM có audit đủ 755 mục: 233 mục cũ và 522 mục từ 6 đề Azota. 15 mục chưa dùng để chấm (11 cũ, 4 mới); gộp câu trùng nhưng giữ mọi nguồn. Phân chương theo nội dung giáo trình, không suy ra chương từ thứ tự câu nguồn.
- Ưu tiên giáo trình 2019 và bài giảng PTIT; số liệu thiếu/mâu thuẫn tra nguồn chính thống, gắn URL hoặc trang cụ thể. Không dùng key Azota để quyết định đáp án.
- Lưu nguyên câu/lựa chọn gốc tách khỏi bản sửa, có băm khóa thứ tự đã duyệt. Câu có hai đáp án đúng phải sửa có ghi chú hoặc giữ ngoài bài chấm. File Word lưu đủ 522 câu gốc, đáp án đối chiếu và các trường hợp cần sửa/chờ xác minh.
- Các câu cũ sửa ý nghĩa phải tăng revision, để kết quả ghi nhớ cũ không chứng nhận nội dung đã đổi. Nguồn trực tuyến hiển thị liên kết, số câu/mục đúng loại, không giả làm trang PDF.
- Đã rà thêm câu trùng ý: gộp 117 bản trong 96 nhóm, từ 623 xuống 506 câu. Chỉ gộp các cặp đã đọc đề/lựa chọn/đáp án, có quyết định và hash tại `content/tthcm/duplicate-decisions.json`; giữ toàn bộ nguồn, không gộp chỉ vì cùng concept/đáp án. Giữ riêng câu khác giai đoạn, chủ thể, phủ định hoặc đoạn trích.

### Ý cốt lõi TTHCM được đối chiếu từ toàn bộ ngân hàng

- Xét đủ 506 câu chuẩn và các lựa chọn/đáp án; gom theo ý kiến thức, đối chiếu giáo trình 2019, bài giảng PTIT và nguồn bổ sung đã xác minh. Không chỉ lấy những concept từng được gắn `core`.
- Bài học có 45 mục trong 6 chương, bao phủ 213 concept khác nhau. Một concept được nhắc tại hai chương khi ngân hàng có câu liên hệ; giữ nguyên chương và ID của từng câu, không chuyển câu để làm đẹp mục lục.
- Mỗi mục có tổng quan; mỗi ý có diễn giải, keyword, điểm dễ nhầm, căn cứ và danh sách câu liên quan. Nội dung nhiều thành phần như đặc trưng CNXH, ba kiểu nhà nước và chuẩn mực đạo đức được giải thích từng ý, không chỉ liệt kê tên.
- Có mục lục bấm mở đúng mục, mở tất cả/thu gọn, luyện từng ý/từng mục/từng câu. Nút luyện mục lấy đúng các câu trong chương, gồm cả câu số liệu. Thiết lập luyện toàn chương vẫn cho chọn kèm chuyên đề riêng.
- Bảng `content/tthcm/lesson-coverage.json` lưu mỗi câu, chương, concept, mục học, nội dung đáp án và hash. Validator từ chối câu thiếu bài học tương ứng, gán trùng trong một chương hoặc nguồn không hợp lệ.
- Nội dung bài học có phiên bản riêng; không đổi phiên bản ngân hàng, ID, lựa chọn, revision hay đáp án chỉ vì mở rộng bài học. Bộ đề tổng hợp và tiến độ cũ giữ nguyên.

### Nội dung kỹ thuật cho hai môn mới

Mô hình câu hỏi chuẩn bị các block tùy chọn cho đề, lựa chọn và giải thích:

- `image`: ảnh thuộc thư mục asset của đúng môn, có alt/caption; không dùng ảnh tham chiếu ngoài hoặc ảnh từ môn khác.
- `matrix`: ma trận hai chiều chữ/số, số cột nhất quán.
- `table`: tiêu đề cột, hàng dữ liệu và chú thích; cuộn ngang trong khối khi cần.
- `code`: đoạn mã được escape, chỉ hiển thị, không tự chạy.
- `formula`: TeX hiển thị bằng KaTeX tải khi cần; không cho thực thi nội dung HTML từ biểu thức.

Các block này chỉ đưa vào khi có tài liệu đối chiếu. Chế độ `quiz` hỗ trợ một đáp án với 2–4 lựa chọn nguồn; chế độ `solutions` hỗ trợ đề tự luận, nhiều ý hỏi và lời giải từng bước. Không tự tạo lựa chọn trắc nghiệm cho bài tự luận.

### Xử lý ảnh: hai khu vực học riêng

- Giữ đúng tên **giải ngân hàng** và **giải bài cô Uyên** trên trang môn, sidebar và nút vào học. Hai khối lớn trên desktop, nút vào học nằm ngay vùng nhìn đầu ở 1366×768.
- **giải ngân hàng** dùng ZIP Xử lý ảnh: phần 1 điểm 14 câu, 2 điểm 16 câu, 3 điểm 11 bài, 4 điểm 10 bài. Giữ cả bài bổ sung không đánh số sau 4.8, mã `4.8-bs`.
- **giải bài cô Uyên** dùng ZIP Ôn tập: 117 mục, gộp 28 câu lý thuyết Việt–Anh trùng nhau. Theo chương: 2 có 2, 3 có 28, 4 có 20, 5 có 21, 6 có 23, 7 có 19, 8 có 4. Chương 3–7 hiển thị trước; 2 và 8 là lý thuyết bổ sung có thật trong bộ này.
- Mẫu đề người dùng cung cấp: câu 1 đạo đức, câu 2 lý thuyết, câu 3–4 bài tập chương 3–7. Không coi bốn mức điểm của ngân hàng cũ là bốn vị trí của đề hiện tại. Chưa có bộ câu đạo đức riêng: báo rõ, không tự viết câu giả định.
- Luồng: chọn khu → chọn phần/chương → danh sách có tìm kiếm keyword và lọc lý thuyết/bài tính → đọc đề → tự làm → mở/ẩn lời giải → tự đánh dấu **Cần ôn** hoặc **Đã nắm**. Bấm lại để bỏ đánh dấu. Không chấm điểm tự động phần tự luận, không khóa chương, không giới hạn lượt.
- Lý thuyết: 101 câu trả lời hoàn chỉnh theo từng vế đề hỏi, làm nổi bật keyword; có công thức, ví dụ, kết luận và giải thích đúng/sai hoặc lệnh MATLAB khi đề yêu cầu. Không dùng dàn ý hướng dẫn người học tự viết thay cho câu trả lời. Khu ngân hàng bám đáp án sau khi kiểm tra bằng giáo trình/slide: 27/30 câu lý thuyết có mục tương ứng trong đáp án; ba câu 1.12–1.14 dùng lý thuyết vì đáp án không có mục tương ứng nội dung. Khu cô Uyên có 71 câu lý thuyết viết theo giáo trình/slide, trình bày cùng cách trả lời của khu ngân hàng. Sai sót nguồn phải sửa và ghi chú ngay tại câu; không chép nguyên đáp án sai.
- 67 bài tính được dàn thành PDF trước rồi raster ảnh trang để hiển thị trên web; không dựng lại lời giải bài tính thành các khối HTML/công thức ở trang học. Tách riêng từng câu (a), (b), (c)… theo đề; trong mỗi câu đánh số bước lại từ 1. Mỗi bước theo **câu dẫn ngắn → công thức → giải thích ký hiệu → cách làm → thay số/thực hiện → kết quả**. Các nhận xét không tính toán có giải thích trực tiếp. Mỗi bài được kiểm tra hash nội dung riêng; thay đổi lý thuyết không bắt buộc tạo lại PDF của bài tính không thay đổi.
- PDF theo cách trình bày đáp án ngân hàng: chữ serif đen trên giấy trắng, bảng histogram ngang, ma trận có ngoặc và chú thích, đặt cạnh nhau khi so sánh. Đánh số bước, không tự gán chữ a/b/c cho bước làm khi một bước trả lời nhiều ý của đề.
- Có một PDF tổng hợp đủ đề và lời giải 67 bài, dấu trang theo bộ/chương/bài. Trang học giữ đề gốc riêng, chỉ hiển thị ảnh những trang lời giải; nút từng câu nhảy tới đúng trang và vị trí tiêu đề trong ảnh, liên kết mở PDF tại đúng trang, tải cả bộ, mở ảnh lớn và bản văn bản hỗ trợ đọc/tìm kiếm. Ảnh tải dần, có kích thước và alt; không làm trang tràn ngang. Lý thuyết đúng/sai tách từng nhận định ở cả đề và câu trả lời, không đặt toàn bộ (a)–(g) trong một đoạn.
- Manifest `documents.json` ghi hash nội dung từng bài, trang PDF tương ứng, kích thước và SHA256 từng ảnh/PDF. Không phát hành khi bài đã sửa mà ảnh chưa tạo lại hoặc thiếu trang. Kiểm tra ảnh bằng render lại đúng trang PDF và so pixel; kiểm tra tính toán riêng với NumPy/SciPy, không coi ảnh đẹp là bằng chứng đáp án đúng.
- Giữ hình đề gốc và bản chép văn bản cho 67 bài tính. Mỗi mục có nguồn đề, trang PDF và nguồn lý thuyết/đáp án tham khảo.
- Công bố quy ước: đệm 0, đặt tâm và không lật mặt nạ theo bộ bài; sai số đầu dòng bằng 0; hai công thức cân bằng histogram; hai cách lấy phân vị ở chương 3/5; SE phản xạ khi phân biệt giãn chuẩn và hit B. Sai dữ kiện/đáp án có ghi chú tại đúng bài.
- Kiểm tra phép tính độc lập bằng NumPy/SciPy và giải mã ngược Huffman/LZW. Kiểm kê đủ 168 mục và kiểm tra công thức KaTeX trước phát hành.

## 4. Route và tương thích

| Route | Nội dung |
| --- | --- |
| `#/` | Chọn môn |
| `#/mon/<id>` | Tổng quan môn hoặc trạng thái chờ tài liệu |
| `#/mon/<id>/chuong/<n>` | Chương của môn |
| `#/mon/<id>/<chuyen-de>` | Chuyên đề được cấu hình cho môn |
| `#/mon/<id>/thi-thu` | Thi thử trong đúng môn |
| `#/mon/tthcm/de-tong-hop` | 8 đề 60 câu và 1 đề cuối 26 câu; mỗi câu thuộc đúng một đề |
| `#/mon/<id>/can-on` | Câu cần ôn của môn |
| `#/mon/<id>/keyword` | Sổ keyword của môn |
| `#/mon/<id>/lam-bai` | Bài đang làm của môn |
| `#/mon/<id>/ket-qua` | Kết quả gần nhất của môn |
| `#/mon/<id>/nguon` | Nguồn và quản lý tiến độ môn |
| `#/mon/xu-ly-anh/ngan-hang[/<1-4>]` | Giải ngân hàng, chọn mức điểm |
| `#/mon/xu-ly-anh/co-uyen[/chuong/<n>]` | Giải bài cô Uyên, chọn chương |
| `#/mon/xu-ly-anh/bai/<id>` | Đề tự luận và lời giải từng bước |

URL cũ như `#/chuong/2`, `#/lam-bai` tự chuyển về route tương ứng của TTHCM bằng replace, không tạo vòng Back. Giữ nguyên địa chỉ GitHub Pages hiện tại để các liên kết đã chia sẻ vẫn dùng được.

## 5. Luồng làm bài

### Luyện đề tổng hợp TTHCM

- Khu riêng **Luyện đề tổng hợp**, có nút vào từ tổng quan môn và sidebar. Hiển thị toàn bộ 9 đề, không khóa thứ tự.
- Mỗi đề chính có 60 câu theo yêu cầu mới: 8 đề đúng 60 câu và 1 đề cuối 26 câu. Toàn bộ 506 câu, gồm 92 câu số liệu, xuất hiện đúng một lần trong cả bộ. Không lấy lại câu cũ để lấp đề cuối.
- Số câu từng chương sau gộp là 30/123/115/105/52/81. Rải câu của mỗi chương đều giữa các đề chính: số câu cùng chương ở các đề 60 câu chênh tối đa 1. Đề cuối 26 câu vẫn có đủ sáu chương, phân bổ theo lượng câu thực có.
- Trộn ổn định từng chương, chia theo hạn mức không quay vòng rồi trộn thứ tự trong đề. Thành phần đề tái lập theo phiên bản ngân hàng, không phụ thuộc tiến độ. Mã bộ đề gồm cả số câu mỗi đề để không hiển thị điểm/bài dang dở của bộ cũ lên đề mới trùng số thứ tự. Bài 50 câu cũ đang làm vẫn có thể tiếp tục; chọn đề mới sẽ hỏi trước khi thay bài dang dở.
- Thẻ đề ghi phân bố từng chương, số câu đã gặp và kết quả nộp gần nhất còn trong lịch sử. Thời gian tùy chọn, mặc định không giới hạn. Làm theo chế độ thi, đáp án/keyword/lời giải hiện sau nộp.
- Lưu lựa chọn, thứ tự đáp án và deadline trong bài dang dở. Tải lại, chuyển môn, làm lại cùng đề và ôn riêng câu sai dùng luồng sẵn có; không mất bài cũ nếu hủy thao tác chọn đề khác.
- Dữ liệu lượt dùng `Deck.kind = comprehensive`, `questionIds`, `paperKey`, số câu thực tế và tên đề. Nhập/lưu lại phải giữ đủ bộ ID đúng thứ tự, không chấp nhận ID trùng hoặc bộ đề không khớp lượt.
- Giữ đề mẫu và đề trộn 20 câu trong khu Thi thử hiện có.

Với chế độ trắc nghiệm, giữ luồng v1: chọn đáp án → Kiểm tra → lời giải → Câu tiếp. Phím 1–4 và Enter có thao tác tách riêng; giữ phím không chuyển liên tiếp. Đáp án lưu theo mã, thứ tự đã đảo lưu theo lượt. Câu tham chiếu A/B giữ thứ tự.

Thi thử trộn theo các chương thực có của môn, không trộn môn; đề mẫu chỉ hiện khi có danh sách câu hợp lệ từ nguồn. Thời gian tùy chọn, deadline không reset khi tải lại. Gợi ý không tính đúng độc lập; bài thi không lộ đáp án trước nộp.

Chuyển môn tự giữ bài đang làm, gỡ listener/timer của màn hình cũ để không chấm lặp hoặc tự chuyển trang của môn khác. Deadline bài có thời gian vẫn theo đồng hồ thực; khi quay lại bài đã hết giờ, chấm và lưu một lần.

## 6. Tiến độ và chuyển đổi dữ liệu

- Khóa mới: `nam-y:progress:v2:<subjectId>`; payload có schema version 2 và subjectId.
- Mỗi môn có records, bài dang dở, kết quả, đánh dấu và lịch sử riêng. Xuất/nhập/reset chỉ ảnh hưởng môn đang mở.
- Khi lần đầu mở TTHCM mà chưa có khóa mới, đọc khóa v1, kiểm tra câu và revision, chuyển đầy đủ records/lượt/danh sách phương án/kết quả/lịch sử sang v2.
- Giữ nguyên khóa v1 làm bản dự phòng; lần sau ưu tiên v2, không nhập đè lại v1. Không chuyển v1 sang môn khác.
- Tệp nhập sai môn bị từ chối dù ID câu trùng. Dữ liệu hỏng hoặc storage bị chặn không làm web ngừng học.
- Concept, câu và revision cũ không được dùng để thổi phồng độ phủ ở phiên bản mới.
- Câu gộp có alias về ID chuẩn và revision trước gộp. Đọc/nhập tiến độ chuyển các bản ghi tương đương về một ID, giữ trạng thái gần nhất và hợp dấu bookmark, không cộng dồn để thổi số lượt. Bài dang dở có ID/phương án không còn hợp lệ được báo thay vì chấm theo câu khác.
- Chế độ lời giải lưu tự đánh giá tại `nam-y:solutions:v1:<subjectId>`, gồm ID, revision và trạng thái. Revision khác loại bỏ đánh dấu cũ. Storage hỏng/bị chặn vẫn đọc được bài, báo nếu không lưu được đánh dấu.

## 7. Cấu trúc thư mục

```text
src/
  app/                  # router, catalog loader, vòng đời ứng dụng
  core/                 # types, chọn đề, chấm, tiến độ và migration
  features/
    subjects/           # màn hình chọn môn, môn chờ tài liệu
    study/              # luồng học dùng chung cho các môn
    solutions/          # đọc đề tự luận, lời giải, tìm kiếm, tự đánh giá
  shared/               # UI, block hiển thị, công thức, CSS
  subjects/
    catalog.json        # đăng ký môn và cấu hình
    tthcm/bank.json     # ngân hàng công khai của TTHCM
    xu-ly-anh/solutions.json # đề gốc, lời giải từng bước và nguồn
materials/              # tài liệu gốc riêng theo môn, không public file gốc
  tthcm/
  xu-ly-anh/
  khoa-hoc-du-lieu/
content/                # trích xuất, quyết định biên tập, audit theo môn
  tthcm/
  xu-ly-anh/
  khoa-hoc-du-lieu/
public/subjects/<id>/   # ảnh/sơ đồ đã được chọn để đưa vào câu hỏi
scripts/
  content/              # kiểm tra chung; importer/curator trong thư mục từng môn
  deploy/               # công cụ GitHub Pages
tests/
  core/                 # engine, isolation, migration, routes, block dữ liệu
  browser/              # thao tác và bố cục thực tế
docs/
  archive/              # đề xuất và đặc tả TTHCM v1
  verification/         # kết quả kiểm tra từng đợt
```

Không nhân bản giao diện theo từng môn, không dùng ba file main. Catalog chọn `learningMode` (`quiz` mặc định hoặc `solutions`) rồi tải dữ liệu/controller tương ứng khi mở môn; các môn cùng chế độ dùng chung controller.

## 8. Kiểm tra và phát hành

Giữ các kiểm thử v1; bổ sung kiểm thử trang chọn môn/nút học nằm trong vùng nhìn đầu, trạng thái chờ trung thực, tải ngân hàng theo môn, đổi môn không mất/chấm lặp, v1 migration, import sai môn, số chương không cố định và block khoa học.

CI kiểm tra catalog, dữ liệu của mọi môn ready, phép tính Xử lý ảnh và browser test; trạng thái awaiting không được khai số chương/câu giả. ZIP/PDF gốc trong materials và tệp tạm không vào Git/bản build. Chỉ ảnh đề được chọn, bản chép, lời giải và nguồn được công bố cùng web.
