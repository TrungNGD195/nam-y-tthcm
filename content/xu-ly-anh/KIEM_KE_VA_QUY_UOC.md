# Kiểm kê nội dung Xử lý ảnh

- Tổng: 168 câu/bài; 101 lý thuyết, 67 bài tính.
- Giải ngân hàng: 1 điểm 14 câu, 2 điểm 16 câu, 3 điểm 11 bài, 4 điểm 10 bài (gồm 4.8 bổ sung không đánh số).
- Giải bài cô Uyên: 117 mục. 28 câu Lý thuyết.pdf gộp với bản Anh; các bộ chương 3/4/5/6/7 lần lượt 21/12/16/21/19 mục.
- Chương hiển thị theo slide/bộ cô Uyên; chương giáo trình không trùng số nên trích dẫn ghi trang PDF cụ thể.
- Câu 1 đạo đức chưa có ngân hàng riêng; không tự tạo câu hoặc nhận là đã giải đủ phần đạo đức.
- Mỗi bài tính giữ ảnh đề gốc và bản chép văn bản; công thức và quy ước đặt trước thay số.
- Quy tắc kiểm tra: scripts/content/xu-ly-anh/verify.py; dữ kiện chuẩn tại source-prompts.json.

## Những chỗ cần đọc đúng quy ước hoặc đề có lỗi

- **bank-1-2**: Bản đáp án tham khảo nói CMY dùng được mọi màu nhìn thấy, nhưng khẳng định đó không đúng. Giữ định nghĩa phối màu trừ trong giáo trình, không học thuộc nhận định này.
- **bank-2-6**: Bản đáp án ghi nhầm trọng số 2 trong một mặt nạ Prewitt. Phân biệt đúng: Prewitt dùng 1, Sobel dùng 2, Frei–Chen dùng √2 ở vị trí giữa.
- **bank-3-3**: Bản đáp án chi tiết thay nhầm pixel hàng 5 cột 5 từ 1 thành 0 và bỏ mức 7. Lời giải này giữ đúng ma trận của ngân hàng câu hỏi; không chép bảng đếm sai đó.
- **bank-3-10**: Bảng co trong đáp án tham khảo có điểm 1 tại vị trí vốn là 0, ví dụ (4,3), trái với điều kiện fit khi tâm SE là 1. Lời giải tính lại từ đúng ma trận X và kiểm tra ảnh co phải là tập con của X.
- **bank-3-11**: Dùng quy ước fit/hit của slide cho kết quả chính; bổ sung riêng kết quả giãn tập hợp chuẩn vì SE không đối xứng, không tráo hai kết quả.
- **bank-4-1**: Đề yêu cầu cộng hai đáp ứng: giữ phép cộng có dấu ở phần a. Để có độ lớn gradient cần |Gx|+|Gy|. Đề chỉ ghi tâm giữa, chưa nói biên: lời giải công bố đệm 0; phần trong không phụ thuộc cách đệm.
- **bank-4-2**: Đề yêu cầu cộng hai đáp ứng: giữ phép cộng có dấu ở phần a. Để có độ lớn gradient cần |Gx|+|Gy|. Đề chỉ ghi tâm giữa, chưa nói biên: lời giải công bố đệm 0; phần trong không phụ thuộc cách đệm.
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
