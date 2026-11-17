# Kiểm kê nội dung Xử lý ảnh

- Tổng: 168 câu/bài; 101 lý thuyết, 67 bài tính.
- Giải ngân hàng: 1 điểm 14 câu, 2 điểm 16 câu, 3 điểm 11 bài, 4 điểm 10 bài (gồm 4.8 bổ sung không đánh số).
- Giải bài cô Uyên: 117 mục. 28 câu Lý thuyết.pdf gộp với bản Anh; các bộ chương 3/4/5/6/7 lần lượt 21/12/16/21/19 mục.
- Chương hiển thị theo slide/bộ cô Uyên; chương giáo trình không trùng số nên trích dẫn ghi trang PDF cụ thể.
- Câu 1 đạo đức chưa có ngân hàng riêng; không tự tạo câu hoặc nhận là đã giải đủ phần đạo đức.
- Mỗi bài tính giữ ảnh đề gốc và bản chép văn bản; công thức và quy ước đặt trước thay số.
- Quy tắc kiểm tra: scripts/content/xu-ly-anh/verify.py; dữ kiện chuẩn tại source-prompts.json.

## Những chỗ cần đọc đúng quy ước hoặc đề có lỗi

- **bank-1-2**: Đáp án tham khảo ghi CMY sử dụng được mọi màu trong phổ nhìn thấy. Nhận định này không đúng; câu trả lời giữ mô hình phối màu trừ và phạm vi màu hữu hạn theo lý thuyết.
- **bank-2-2**: Đáp án tham khảo trang PDF 10 ghi nhầm 225−R, 225−G, 225−B. Với RGB 8 bit, công thức đúng là 255−R, 255−G, 255−B, phù hợp phép lấy phần bù trong giáo trình.
- **bank-2-6**: Đáp án tham khảo có mặt nạ Prewitt ghi trọng số giữa là 2. Phân biệt theo lý thuyết: Prewitt dùng 1, Sobel dùng 2, Frei–Chen dùng √2; độ lớn gradient không phải tổng có dấu Gx+Gy.
- **bank-3-3**: Bản đáp án chi tiết thay nhầm pixel hàng 5 cột 5 từ 1 thành 0 và bỏ mức 7. Lời giải này giữ đúng ma trận của ngân hàng câu hỏi; không chép bảng đếm sai đó.
- **bank-3-10**: Bảng co trong đáp án tham khảo có điểm 1 tại vị trí vốn là 0, ví dụ (4,3), trái với điều kiện fit khi tâm SE là 1. Lời giải tính lại từ đúng ma trận X và kiểm tra ảnh co phải là tập con của X.
- **bank-3-11**: Dùng quy ước fit/hit của slide cho kết quả chính; bổ sung riêng kết quả giãn tập hợp chuẩn vì SE không đối xứng, không tráo hai kết quả.
- **bank-4-1**: Đề yêu cầu cộng hai đáp ứng: giữ phép cộng có dấu ở phần a. Để có độ lớn gradient cần |Gx|+|Gy|. Đề chỉ ghi tâm giữa, chưa nói biên: lời giải công bố đệm 0; phần trong không phụ thuộc cách đệm.
- **bank-4-2**: Đề yêu cầu cộng hai đáp ứng: giữ phép cộng có dấu ở phần a. Để có độ lớn gradient cần |Gx|+|Gy|. Đề chỉ ghi tâm giữa, chưa nói biên: lời giải công bố đệm 0; phần trong không phụ thuộc cách đệm.
- **bank-4-3**:  Đề gốc đánh nhãn a hai lần; lời giải gọi yêu cầu xử lý ảnh thứ hai là câu (b), giữ nguyên dữ kiện và thứ tự.
- **bank-4-4**:  Đề gốc đánh nhãn a hai lần; lời giải gọi yêu cầu xử lý ảnh thứ hai là câu (b), giữ nguyên dữ kiện và thứ tự.
- **bank-4-7**: Giữ đúng số liệu trong ngân hàng đề. Bản đáp án gọi một bài khác là 4.8 và còn thay 250 thành 120; không dùng bảng tính đó cho dữ kiện này. Ngân hàng không nêu quy ước phân vị rời rạc: dùng mức cuối không vượt p% như cách làm đáp án; xem thêm quy ước đạt p% ở bài cô Uyên chương 5.
- **bank-4-8**: Giữ đúng số liệu trong ngân hàng đề. Bản đáp án gọi một bài khác là 4.8 và còn thay 250 thành 120; không dùng bảng tính đó cho dữ kiện này. Ngân hàng không nêu quy ước phân vị rời rạc: dùng mức cuối không vượt p% như cách làm đáp án; xem thêm quy ước đạt p% ở bài cô Uyên chương 5.
- **bank-4-8-bs**: Giữ đúng số liệu trong ngân hàng đề. Bản đáp án gọi một bài khác là 4.8 và còn thay 250 thành 120; không dùng bảng tính đó cho dữ kiện này. Ngân hàng không nêu quy ước phân vị rời rạc: dùng mức cuối không vượt p% như cách làm đáp án; xem thêm quy ước đạt p% ở bài cô Uyên chương 5.
- **uyen-3-T10**: Công thức f(g) trong PDF bị dàn trang dễ đọc nhầm. Dùng công thức giáo trình trang PDF 32: t/(N−t) nhân bình phương chênh trung bình, không chia cho bình phương đó.
- **uyen-3-T11**: Chương 3 quy định phân vị cuối không vượt p%; khác quy ước đầu tiên đạt p% của chương 5. Kết quả được tính theo từng đề, không trộn quy ước.
- **uyen-4-T3**: Câu 4.T3 phần b nói dòng 2 toàn 90 nhưng ma trận cho dòng 2 là 143,27,5,251,33,76. Giữ đúng ma trận; dòng toàn 90 nằm ở 4.T4. Không thay dữ kiện để khớp câu nhận xét.
- **uyen-6-T2**: Đề nhắc ký hiệu C, D nhưng chưa gán chữ cho mẫu khối. Lời giải dùng chuỗi 4 bit nhận diện khối để tránh gán nhầm; hòa tần suất đổi mã nhưng không đổi tổng số bit tối ưu.

## Danh mục và vị trí nguồn

| ID | Câu/bài | Khu vực | Chương | Trang PDF đề |
|---|---|---|---|---|
| bank-1-1 | 1.1 | bank | 4 | bank: 2 |
| bank-1-2 | 1.2 | bank | 4 | bank: 2 |
| bank-1-3 | 1.3 | bank | 4 | bank: 2 |
| bank-1-4 | 1.4 | bank | 2 | bank: 2 |
| bank-1-5 | 1.5 | bank | 4 | bank: 2 |
| bank-1-6 | 1.6 | bank | 4 | bank: 2 |
| bank-1-7 | 1.7 | bank | 4 | bank: 2 |
| bank-1-8 | 1.8 | bank | 3 | bank: 2 |
| bank-1-9 | 1.9 | bank | 3 | bank: 2 |
| bank-1-10 | 1.10 | bank | 3 | bank: 2 |
| bank-1-11 | 1.11 | bank | 3 | bank: 2 |
| bank-1-12 | 1.12 | bank | 5 | bank: 2 |
| bank-1-13 | 1.13 | bank | 5 | bank: 2 |
| bank-1-14 | 1.14 | bank | 6 | bank: 2 |
| bank-2-1 | 2.1 | bank | 4 | bank: 3 |
| bank-2-2 | 2.2 | bank | 4 | bank: 3 |
| bank-2-3 | 2.3 | bank | 2 | bank: 3 |
| bank-2-4 | 2.4 | bank | 3 | bank: 3 |
| bank-2-5 | 2.5 | bank | 5 | bank: 3 |
| bank-2-6 | 2.6 | bank | 5 | bank: 3 |
| bank-2-7 | 2.7 | bank | 5 | bank: 3 |
| bank-2-8 | 2.8 | bank | 3 | bank: 3 |
| bank-2-9 | 2.9 | bank | 3 | bank: 3 |
| bank-2-10 | 2.10 | bank | 5 | bank: 3 |
| bank-2-11 | 2.11 | bank | 8 | bank: 3 |
| bank-2-12 | 2.12 | bank | 8 | bank: 3 |
| bank-2-13 | 2.13 | bank | 8 | bank: 3 |
| bank-2-14 | 2.14 | bank | 8 | bank: 3 |
| bank-2-15 | 2.15 | bank | 6 | bank: 3 |
| bank-2-16 | 2.16 | bank | 6 | bank: 3 |
| bank-3-1 | 3.1 | bank | 3 | bank: 4 |
| bank-3-2 | 3.2 | bank | 3 | bank: 4 |
| bank-3-3 | 3.3 | bank | 3 | bank: 4 |
| bank-3-4 | 3.4 | bank | 3 | bank: 4 |
| bank-3-5 | 3.5 | bank | 3 | bank: 5 |
| bank-3-6 | 3.6 | bank | 4 | bank: 5 |
| bank-3-7 | 3.7 | bank | 4 | bank: 5 |
| bank-3-8 | 3.8 | bank | 6 | bank: 5 |
| bank-3-9 | 3.9 | bank | 6 | bank: 6 |
| bank-3-10 | 3.10 | bank | 7 | bank: 6 |
| bank-3-11 | 3.11 | bank | 7 | bank: 6 |
| bank-4-1 | 4.1 | bank | 5 | bank: 7 |
| bank-4-2 | 4.2 | bank | 5 | bank: 7 |
| bank-4-3 | 4.3 | bank | 5 | bank: 8 |
| bank-4-4 | 4.4 | bank | 5 | bank: 8 |
| bank-4-5 | 4.5 | bank | 3 | bank: 9 |
| bank-4-6 | 4.6 | bank | 3 | bank: 9 |
| bank-4-7 | 4.7 | bank | 3 | bank: 9,10 |
| bank-4-8 | 4.8 | bank | 3 | bank: 10 |
| bank-4-8-bs | 4.8-bs | bank | 3 | bank: 10 |
| bank-4-9 | 4.9 | bank | 6 | bank: 11 |
| uyen-5-L1 | 5.L1 | uyen | 5 | uyen-5: 1 |
| uyen-5-L2 | 5.L2 | uyen | 5 | uyen-5: 1 |
| uyen-5-L3 | 5.L3 | uyen | 5 | uyen-5: 1 |
| uyen-5-L4 | 5.L4 | uyen | 5 | uyen-5: 1 |
| uyen-5-L5 | 5.L5 | uyen | 5 | uyen-5: 1 |
| uyen-5-L6 | 5.L6 | uyen | 5 | uyen-5: 1 |
| uyen-5-L7 | 5.L7 | uyen | 5 | uyen-5: 2 |
| uyen-5-L8 | 5.L8 | uyen | 5 | uyen-5: 2 |
| uyen-5-L9 | 5.L9 | uyen | 5 | uyen-5: 2 |
| uyen-5-T1 | 5.T1 | uyen | 5 | uyen-5: 2 |
| uyen-5-T2 | 5.T2 | uyen | 5 | uyen-5: 2,3 |
| uyen-5-T3 | 5.T3 | uyen | 5 | uyen-5: 3 |
| uyen-5-T4 | 5.T4 | uyen | 5 | uyen-5: 3,4 |
| uyen-5-T5 | 5.T5 | uyen | 5 | uyen-5: 4 |
| uyen-5-T6 | 5.T6 | uyen | 5 | uyen-5: 4,5 |
| uyen-5-T7 | 5.T7 | uyen | 5 | uyen-5: 5 |
| uyen-lt-1-1 | 1.1 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-1-2 | 1.2 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-1-3 | 1.3 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-1-4 | 1.4 | uyen | 2 | uyen-theory: 1 |
| uyen-lt-1-5 | 1.5 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-1-6 | 1.6 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-1-7 | 1.7 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-1-8 | 1.8 | uyen | 3 | uyen-theory: 1 |
| uyen-lt-1-9 | 1.9 | uyen | 3 | uyen-theory: 1 |
| uyen-lt-1-10 | 1.10 | uyen | 3 | uyen-theory: 1 |
| uyen-lt-1-11 | 1.11 | uyen | 3 | uyen-theory: 1 |
| uyen-lt-1-12 | 1.12 | uyen | 5 | uyen-theory: 1 |
| uyen-lt-2-1 | 2.1 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-2-2 | 2.2 | uyen | 4 | uyen-theory: 1 |
| uyen-lt-2-3 | 2.3 | uyen | 2 | uyen-theory: 1 |
| uyen-lt-2-4 | 2.4 | uyen | 3 | uyen-theory: 1 |
| uyen-lt-2-5 | 2.5 | uyen | 5 | uyen-theory: 1 |
| uyen-lt-2-6 | 2.6 | uyen | 5 | uyen-theory: 1 |
| uyen-lt-2-7 | 2.7 | uyen | 5 | uyen-theory: 1 |
| uyen-lt-2-8 | 2.8 | uyen | 3 | uyen-theory: 2 |
| uyen-lt-2-9 | 2.9 | uyen | 3 | uyen-theory: 2 |
| uyen-lt-2-10 | 2.10 | uyen | 5 | uyen-theory: 2 |
| uyen-lt-2-11 | 2.11 | uyen | 8 | uyen-theory: 2 |
| uyen-lt-2-12 | 2.12 | uyen | 8 | uyen-theory: 2 |
| uyen-lt-2-13 | 2.13 | uyen | 8 | uyen-theory: 2 |
| uyen-lt-2-14 | 2.14 | uyen | 8 | uyen-theory: 2 |
| uyen-lt-2-15 | 2.15 | uyen | 6 | uyen-theory: 2 |
| uyen-lt-2-16 | 2.16 | uyen | 6 | uyen-theory: 2 |
| uyen-3-L1 | 3.L1 | uyen | 3 | uyen-3: 1 |
| uyen-3-L2 | 3.L2 | uyen | 3 | uyen-3: 1 |
| uyen-3-L3 | 3.L3 | uyen | 3 | uyen-3: 1 |
| uyen-3-L4 | 3.L4 | uyen | 3 | uyen-3: 1 |
| uyen-3-L5 | 3.L5 | uyen | 3 | uyen-3: 1 |
| uyen-3-L6 | 3.L6 | uyen | 3 | uyen-3: 1 |
| uyen-3-L7 | 3.L7 | uyen | 3 | uyen-3: 1 |
| uyen-3-L8 | 3.L8 | uyen | 3 | uyen-3: 1 |
| uyen-3-L9 | 3.L9 | uyen | 3 | uyen-3: 1 |
| uyen-3-T1 | 3.T1 | uyen | 3 | uyen-3: 1 |
| uyen-3-T2 | 3.T2 | uyen | 3 | uyen-3: 1 |
| uyen-3-T3 | 3.T3 | uyen | 3 | uyen-3: 1,2 |
| uyen-3-T4 | 3.T4 | uyen | 3 | uyen-3: 2 |
| uyen-3-T5 | 3.T5 | uyen | 3 | uyen-3: 2 |
| uyen-3-T6 | 3.T6 | uyen | 3 | uyen-3: 2 |
| uyen-3-T7 | 3.T7 | uyen | 3 | uyen-3: 3 |
| uyen-3-T8 | 3.T8 | uyen | 3 | uyen-3: 3 |
| uyen-3-T9 | 3.T9 | uyen | 3 | uyen-3: 3 |
| uyen-3-T10 | 3.T10 | uyen | 3 | uyen-3: 3 |
| uyen-3-T11 | 3.T11 | uyen | 3 | uyen-3: 3,4 |
| uyen-3-T12 | 3.T12 | uyen | 3 | uyen-3: 4 |
| uyen-4-L1 | 4.L1 | uyen | 4 | uyen-4: 1 |
| uyen-4-L2 | 4.L2 | uyen | 4 | uyen-4: 1 |
| uyen-4-L3 | 4.L3 | uyen | 4 | uyen-4: 1 |
| uyen-4-L4 | 4.L4 | uyen | 4 | uyen-4: 1 |
| uyen-4-L5 | 4.L5 | uyen | 4 | uyen-4: 1 |
| uyen-4-L6 | 4.L6 | uyen | 4 | uyen-4: 1 |
| uyen-4-L7 | 4.L7 | uyen | 4 | uyen-4: 1 |
| uyen-4-L8 | 4.L8 | uyen | 4 | uyen-4: 1 |
| uyen-4-T1 | 4.T1 | uyen | 4 | uyen-4: 1 |
| uyen-4-T2 | 4.T2 | uyen | 4 | uyen-4: 2 |
| uyen-4-T3 | 4.T3 | uyen | 4 | uyen-4: 2 |
| uyen-4-T4 | 4.T4 | uyen | 4 | uyen-4: 2 |
| uyen-7-L1 | 7.L1 | uyen | 7 | uyen-7: 1 |
| uyen-7-L2 | 7.L2 | uyen | 7 | uyen-7: 1 |
| uyen-7-L3 | 7.L3 | uyen | 7 | uyen-7: 1 |
| uyen-7-L4 | 7.L4 | uyen | 7 | uyen-7: 1 |
| uyen-7-L5 | 7.L5 | uyen | 7 | uyen-7: 1 |
| uyen-7-L6 | 7.L6 | uyen | 7 | uyen-7: 1 |
| uyen-7-L7 | 7.L7 | uyen | 7 | uyen-7: 1 |
| uyen-7-L8 | 7.L8 | uyen | 7 | uyen-7: 1,2 |
| uyen-7-T1 | 7.T1 | uyen | 7 | uyen-7: 2 |
| uyen-7-T2 | 7.T2 | uyen | 7 | uyen-7: 2 |
| uyen-7-T3 | 7.T3 | uyen | 7 | uyen-7: 3 |
| uyen-7-T4 | 7.T4 | uyen | 7 | uyen-7: 3 |
| uyen-7-T5 | 7.T5 | uyen | 7 | uyen-7: 3,4 |
| uyen-7-T6 | 7.T6 | uyen | 7 | uyen-7: 4 |
| uyen-7-T7 | 7.T7 | uyen | 7 | uyen-7: 4 |
| uyen-7-T8 | 7.T8 | uyen | 7 | uyen-7: 4,5 |
| uyen-7-T9 | 7.T9 | uyen | 7 | uyen-7: 5 |
| uyen-7-T10 | 7.T10 | uyen | 7 | uyen-7: 5,6 |
| uyen-7-T11 | 7.T11 | uyen | 7 | uyen-7: 6 |
| uyen-6-L1 | 6.L1 | uyen | 6 | uyen-6: 1 |
| uyen-6-L2 | 6.L2 | uyen | 6 | uyen-6: 1 |
| uyen-6-L3 | 6.L3 | uyen | 6 | uyen-6: 1 |
| uyen-6-L4 | 6.L4 | uyen | 6 | uyen-6: 1 |
| uyen-6-L5 | 6.L5 | uyen | 6 | uyen-6: 1 |
| uyen-6-L6 | 6.L6 | uyen | 6 | uyen-6: 1 |
| uyen-6-L7 | 6.L7 | uyen | 6 | uyen-6: 1 |
| uyen-6-L8 | 6.L8 | uyen | 6 | uyen-6: 1 |
| uyen-6-L9 | 6.L9 | uyen | 6 | uyen-6: 1,2 |
| uyen-6-T1 | 6.T1 | uyen | 6 | uyen-6: 2 |
| uyen-6-T2 | 6.T2 | uyen | 6 | uyen-6: 2 |
| uyen-6-T3 | 6.T3 | uyen | 6 | uyen-6: 2,3 |
| uyen-6-T4 | 6.T4 | uyen | 6 | uyen-6: 3 |
| uyen-6-T5 | 6.T5 | uyen | 6 | uyen-6: 3,4 |
| uyen-6-T6 | 6.T6 | uyen | 6 | uyen-6: 4 |
| uyen-6-T7 | 6.T7 | uyen | 6 | uyen-6: 4 |
| uyen-6-T8 | 6.T8 | uyen | 6 | uyen-6: 4,5 |
| uyen-6-T9 | 6.T9 | uyen | 6 | uyen-6: 5,6 |
| uyen-6-T10 | 6.T10 | uyen | 6 | uyen-6: 6 |
| uyen-6-T11 | 6.T11 | uyen | 6 | uyen-6: 6,7 |
| uyen-6-T12 | 6.T12 | uyen | 6 | uyen-6: 7 |

## Câu trả lời lý thuyết hoàn chỉnh — 16/11/2026

- 101 câu lý thuyết được trả lời thành đoạn văn theo từng vế đề hỏi, không phải dàn ý hoặc lời nhắc viết bài.
- 30 câu ngân hàng: 27 câu có mục đáp án phù hợp để đối chiếu; 1.12–1.14 không có mục tương ứng trong PDF đáp án nên dùng giáo trình. Mục 1.11 của ngân hàng bao gồm nội dung cả 1.11 và 1.12 trong đáp án; không ghép theo số câu một cách máy móc.
- 71 câu cô Uyên: theo giáo trình/slide, trình bày cùng lối định nghĩa → giải thích/các bước → công thức, ví dụ, so sánh khi đề hỏi.
- Ghi rõ lỗi 225 thay vì 255 ở đáp án đổi RGB 8 bit sang CMY; sửa phát biểu gamut CMY và nhầm trọng số Prewitt, không chép theo phần sai.
- Canny: tài liệu mô tả vai trò quan trọng của bước 4 và 5, không đưa xếp hạng tuyệt đối một bước duy nhất. Câu trả lời giải thích trực tiếp vai trò làm mảnh và liên kết bằng hai ngưỡng.
- `theory-answer-review.json` lưu đủ 101 ID, căn cứ, trang đáp án, các vế trả lời và hash để theo dõi nội dung.
- 67 bài tính chia riêng từng câu (a), (b), (c) theo đề; công thức kèm ký hiệu, cách làm và thay số. PDF/ảnh được xuất lại từ bản trình bày mới, hash từng bài kiểm tra tính tương thích.
- scripts/content/xu-ly-anh/worked_parts.py lưu ánh xạ ý hỏi và cách giải thích ký hiệu. Công thức, bảng và ma trận tính từ calculations.py/exercises.py, tiếp tục được kiểm tra độc lập bằng NumPy/SciPy.

## Chỉ lược ý hỏi lý thuyết — 17/11/2026

- Khôi phục đầy đủ mọi ý hỏi của 67 bài tính, trong đó có 46 bài cô Uyên. Bản PDF và ảnh lời giải trả lời đủ từng câu.
- Giữ đủ 71 câu lý thuyết cô Uyên; 36 câu được rà ý hỏi lặp, gồm 10 câu tham chiếu về nội dung đã hỏi.
- Câu trùng một phần chỉ hỏi các ý mới; câu trùng hoàn toàn giữ mã, đề gốc và câu trả lời đối chiếu, dẫn đến câu đã có. Không thêm kiến thức ngoài đề.
- theory-focus-review.json lưu ý lược, ý giữ, liên kết câu trước và hash. Audit rút gọn bài tính cũ chuyển vào archive và không còn áp dụng.
- Giữ các sửa lỗi đã kiểm tra: 4.T3 không dùng nhầm dòng toàn 90 của 4.T4; 5.T4 chọn cực đại Otsu 3 hoặc 5, không lấy 4.

| Câu | Nội dung đã hỏi | Phần giữ lại |
|---|---|---|
| 5.L1 | uyen-lt-1-12: Biên và phát hiện trực tiếp; uyen-lt-2-6: Mặt nạ và cách tạo ảnh biên | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 5.L2 | uyen-lt-2-5: Nguyên lý đạo hàm và mặt nạ ngang | Mặt nạ chuyển vị theo hướng dọc; xấp xỉ độ lớn gradient |
| 5.L3 | uyen-lt-2-6: Ba loại mặt nạ và các bước tạo biên | So sánh trọng số và tác dụng của Sobel |
| 5.L5 | uyen-lt-2-7: Các bước Canny và vai trò các bước then chốt | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 5.L7 | uyen-3-L8: So sánh tham số, điều kiện và trường hợp nhiều ngưỡng | Trình tự thực hiện và công thức Otsu; lặp ISODATA và dừng |
| 5.L8 | uyen-lt-2-8: Khái niệm và điều kiện đối xứng nền; uyen-3-L6: Các bước và tỷ lệ tích lũy; uyen-lt-2-9: Tam giác và trường hợp không phù hợp | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 5.L9 | uyen-lt-2-10: Ý tưởng và tiêu chuẩn của tách/hợp vùng | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 1.6 | uyen-lt-1-5: Halftone và lý do dùng trong in ấn | Vai trò khuếch tán lỗi; so với tách ngưỡng |
| 1.7 | uyen-lt-1-6: Khái niệm, vai trò và khác biệt với tách ngưỡng | Một chiều/hai chiều; vệt giả theo hướng quét |
| 2.1 | uyen-lt-1-2: Nguyên lý CMY và khác biệt với RGB | Trường hợp sử dụng |
| 2.2 | uyen-lt-1-2: CMY và khác biệt RGB; uyen-lt-2-1: Ứng dụng phối màu trừ | Phép chuyển RGB→CMY, hai miền giá trị |
| 2.3 | uyen-lt-1-4: So sánh raster với vector | Cách lưu hình học vector; lý do raster vẫn cần thiết |
| 2.6 | uyen-lt-2-5: Nguyên lý dùng đạo hàm | Ba cặp mặt nạ và hậu xử lý đáp ứng |
| 3.L1 | uyen-lt-1-8: Tăng/giảm sáng bằng toán tử điểm | Âm bản, log, gamma |
| 3.L2 | uyen-lt-1-9: Khái niệm và mục đích cân bằng histogram | Cân bằng lý tưởng và giới hạn rời rạc |
| 3.L3 | uyen-lt-1-10: Toán tử không gian và ý tưởng cửa sổ di chuyển | Đệm 0, lặp rìa, phản xạ, bỏ biên |
| 3.L4 | uyen-lt-1-11: Khái niệm, mục đích và mô hình nhiễu rời rạc | Mô hình liên tục; các loại nhiễu |
| 3.L5 | uyen-lt-2-4: So sánh trung vị, trung bình, k gần nhất và trường hợp sử dụng | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 3.L6 | uyen-lt-2-8: Khái niệm và giả thiết nền phù hợp | Các bước; ảnh hưởng của p% |
| 3.L7 | uyen-lt-2-9: Ý tưởng tam giác và trường hợp không phù hợp | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 3.L8 | uyen-lt-2-8: Đối xứng nền; uyen-lt-2-9: Tam giác | Otsu và ISODATA: điều kiện, khởi tạo, lựa chọn và nhiều nghiệm |
| 3.L9 | uyen-lt-2-4: Trung bình số học, trung vị và k gần nhất | Tăng cường/khôi phục; hai miền; các bộ lọc nhiễu còn lại |
| 4.L1 | uyen-lt-1-2: Phân biệt RGB và CMY; uyen-lt-2-1: Trường hợp sử dụng hai nguyên lý phối màu | Ví dụ phối hai màu |
| 4.L2 | uyen-lt-1-1: Khái niệm và tên các mô hình màu; uyen-lt-1-3: Ý nghĩa các thành phần HSV/HSL; uyen-lt-2-1: Ứng dụng RGB và CMY | Ứng dụng HSV/HSL trong thao tác màu |
| 4.L3 | uyen-lt-1-2: So sánh CMY với RGB | Lý do thực tế dùng thêm mực đen K |
| 4.L4 | uyen-lt-1-3: Lý do phát triển HSV/HSL và ý nghĩa từng chữ cái | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 4.L5 | uyen-lt-1-4: Raster/vector và trường hợp sử dụng; uyen-lt-2-3: Vector và lý do vẫn dùng raster | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 4.L6 | uyen-lt-1-5: Mục đích và ý tưởng halftone | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 4.L7 | uyen-lt-1-6: Khuếch tán lỗi so với tách ngưỡng; uyen-lt-1-7: Một chiều, hai chiều và nhược điểm được khắc phục | Tham chiếu câu đã hỏi; giữ nguyên bản để đối chiếu |
| 4.L8 | uyen-lt-1-2: CMY là phối màu trừ; uyen-lt-1-4: Phóng to raster/vector; uyen-lt-1-5: Cảm nhận cường độ trung bình trong halftone | Nhận định (d): số mức xám sau lượng tử hóa |
| 7.L8 | uyen-7-L3: Mở không luôn trả ảnh gốc; tác dụng nối khe của đóng; uyen-7-L6: Vì sao phải giao với Aᶜ khi làm đầy | (b) điều kiện bao hàm co/giãn; (c) lũy đẳng; (e) SE bất đối xứng; (f) đối ngẫu |
| 6.L1 | uyen-lt-2-15: Khái niệm RLC và khi nào dữ liệu nở | Ví dụ có số bit cụ thể |
| 6.L2 | uyen-lt-2-16: Mục đích DCT và bước lượng tử gây tổn thất | Sai số số học thực tế và tính khả nghịch lý thuyết |
| 6.L5 | uyen-6-L3: Tần suất và việc gửi bảng mã trong Huffman tĩnh | Các bước; mã tiền tố; chia khối; mất đồng bộ vì lỗi bit |
| 6.L7 | uyen-lt-2-16: Lượng tử hóa không khôi phục chính xác; uyen-6-L2: Sai số và tổn thất trong JPEG | Cấu trúc và chức năng các khối mã hóa |
| 6.L9 | uyen-6-L3: LZW tự tái tạo từ điển; uyen-lt-2-16: DCT khả nghịch và lượng tử hóa gây mất mát | (a) entropy/Huffman; (d) DCT/DFT và blocking; (e) bước lượng tử theo tần số |
