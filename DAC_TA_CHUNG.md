# Đặc tả chung — Nắm ý | Ôn thi Tư tưởng Hồ Chí Minh

Phiên bản 1.0 · 13/11/2026. Tài liệu này là chuẩn triển khai; kế thừa nội dung học tập của `DE_XUAT_WEB_ON_THI.md` và ưu tiên sử dụng trên máy tính đã được người dùng chốt.

## 1. Mục tiêu và phạm vi

Giúp người bắt đầu từ số 0 nắm ý cốt lõi, luyện trắc nghiệm sát ngân hàng, nhận diện keyword và ôn phần còn yếu. Website công khai, không đăng nhập, không giới hạn lượt, không khóa chương. Triển khai web tĩnh trên GitHub Pages; dữ liệu học của mỗi người nằm trong trình duyệt.

Bản đầu hoàn thành các luồng: tổng quan → chọn chương/chuyên đề → kiến thức cốt lõi → luyện → phản hồi → kết quả → ôn sai; thi thử 20 câu; sổ keyword; tiếp tục bài đang làm; xuất/nhập tiến độ. Không có bảng xếp hạng, tài khoản, thanh toán hoặc chatbot.

## 2. Tổ chức nội dung

6 chương theo giáo trình 2019: (1) Nhập môn; (2) Cơ sở, quá trình hình thành và phát triển; (3) Độc lập dân tộc và CNXH; (4) Đảng và Nhà nước; (5) Đại đoàn kết; (6) Văn hóa, đạo đức, con người.

Câu đòi nhớ ngày, năm, giai đoạn, Đại hội/hội nghị hoặc số lượng nội dung có nhãn `date`, `congress` hoặc `count`, thuộc chuyên đề Con số cần nhớ. Mặc định bộ chương không gồm câu số liệu; tùy chọn đưa số liệu trở lại bộ chương. Cùng một câu luôn dùng cùng ID và tiến độ, dù đi từ bộ nào.

Ưu tiên nhập đầy đủ các mục của LMS (95), Quiz cô Khánh (118 mục nhận diện) và đề mẫu thầy Cường (20). Mỗi mục phải có kết quả: xuất bản, gộp với câu chuẩn, hoặc chờ kiểm chứng với lý do. Bộ Tổng hợp và Bonus là nguồn bổ sung, không tự động coi các mục của chúng là đã kiểm duyệt. Báo cáo biên tập ghi rõ độ phủ và phần chưa nhập; UI chỉ đếm câu thực sự đủ điều kiện.

### Quy tắc kiểm duyệt

- Giữ đề và lựa chọn gốc; chỉ sửa lỗi định dạng/chính tả không đổi nghĩa, có ghi chú khi sửa nội dung.
- Đáp án dựa trên đối chiếu tài liệu, không suy từ chữ A hay vị trí đánh dấu. Lưu trích đoạn/căn cứ và trang cho từng nhóm kiến thức.
- Câu thiếu, nhiều đáp án hợp lý, không có phương án hợp lệ hoặc mâu thuẫn chưa giải quyết không dùng để chấm điểm.
- LMS chương 6 câu 7 về vai trò văn hóa phải được giữ riêng do đáp án đánh dấu mâu thuẫn với giáo trình trang in 115 / PDF 117 và slide chương 6 trang 12.
- Câu trả lời ngắn chỉ chuyển thành trắc nghiệm nếu phương án nhiễu có căn cứ trong môn; ghi nhãn chuyển đổi và giữ bản gốc trong dữ liệu biên tập.
- Câu trùng hoàn toàn gộp nguồn. Câu khác phạm vi, từ phủ định hoặc lựa chọn không gộp chỉ vì cùng keyword.
- Giải thích 1–2 câu, keyword 1–3 cụm, tối đa một ghi chú dễ nhầm; câu đếm số phải liệt kê các ý được đếm. Nguồn hiện ở phần mở rộng.

## 3. Giao diện và điều hướng

Tên sản phẩm: **Nắm ý**. Phụ đề: **Ôn thi Tư tưởng Hồ Chí Minh**. Ngôn ngữ: tiếng Việt.

- Desktop: thanh bên 248px, vùng nội dung tối đa khoảng 1120px; tổng khung không kéo văn bản câu hỏi dài quá khoảng 820px.
- Kiểm tra chính ở 1366×768 và 1920×1080. Dưới 900px thu thanh bên thành menu; dưới 640px dùng một cột. Phóng to 200% vẫn thao tác được, không mất nội dung.
- Màu: nền giấy `#f7f6f2`, thẻ trắng, chữ `#262b2b`, đỏ trầm `#853e44`; màu phụ xanh lá cho đúng và cam cho cần ôn. Không chỉ dùng màu để truyền trạng thái.
- Font hệ thống hỗ trợ đầy đủ tiếng Việt; câu hỏi 20–24px trên desktop, nội dung thường 15–17px, line-height tối thiểu 1.55. Điều khiển có vùng bấm từ 44px.
- Sidebar: Tổng quan, 6 chương, Con số cần nhớ, Thi thử, Cần ôn, Sổ keyword. Hiển thị mục đang mở và số câu cần ôn.
- Header: đường dẫn ngắn, tên khu vực, nút mở thông tin nguồn/tiến độ. Không đặt thông số kỹ thuật trong luồng học.
- Mọi nút có focus rõ; dialog dùng phần tử `dialog`, giữ focus bên trong và trả focus về nút mở. Tiến độ và phản hồi có nhãn cho trình đọc màn hình.

### Các route (hash, hoạt động dưới đường dẫn repository)

| Route | Nội dung |
| --- | --- |
| `#/` | Tổng quan |
| `#/chuong/1` … `#/chuong/6` | Kiến thức cốt lõi, cấu hình lượt luyện theo chương |
| `#/con-so` | Chuyên đề số liệu, bộ lọc |
| `#/thi-thu` | Chọn đề mẫu hoặc đề trộn 20 câu |
| `#/can-on` | Câu sai, chưa chắc, đánh dấu |
| `#/keyword` | Tra cứu và tự nhớ keyword |
| `#/lam-bai` | Lượt đang làm; không có lượt thì về tổng quan |
| `#/ket-qua` | Kết quả lượt gần nhất; không có kết quả thì về tổng quan |
| `#/nguon` | Nguồn tài liệu, phạm vi, báo cáo nội dung, quản lý tiến độ |

Route không hợp lệ có đường quay về tổng quan. Back/Forward phải thay đổi đúng màn hình, không tự ghi thêm lượt trả lời.

## 4. Chi tiết từng màn hình

### Tổng quan

Chào ngắn, nút Bắt đầu ôn; thẻ tiếp tục lượt đang làm nếu có; các số thực tế: câu sẵn sàng, câu đã gặp, câu cần ôn. Lưới 6 chương, mỗi thẻ gồm số chương, tiêu đề, mô tả, độ phủ và số câu. Thẻ chuyên đề con số và thi thử. Gợi ý học chương 1 chỉ là tùy chọn.

### Chương / chuyên đề

Đầu trang có mô tả, số câu thực tế và nút luyện. Các nhóm ý cốt lõi trình bày ngắn, keyword có thể che/hiện. Chọn 10 / 20 / tất cả câu; nếu ít hơn lấy số thực tế. Chọn ưu tiên chưa gặp hoặc ngẫu nhiên. Bộ số liệu có bộ lọc Tất cả / Mốc thời gian / Đại hội / Số lượng. Bộ chương có checkbox kèm câu số liệu.

### Lượt luyện

Trạng thái câu: `unanswered → selected → checked`. Chọn đáp án không tự chấm; Kiểm tra chỉ hoạt động khi đã chọn. Sau chấm không đổi lựa chọn. Câu đã chấm hiện đáp án đúng, phần giải thích có keyword nổi bật, ghi chú dễ nhầm và nguồn. Câu tiếp chỉ chuyển sau thao tác riêng, không tự chuyển.

Phím `1–4` chọn phương án đang hiển thị, Enter chấm hoặc đi tiếp tùy trạng thái. Bỏ qua sự kiện lặp do giữ phím. Không kích hoạt phím tắt khi focus trong input/select/textarea hoặc dialog. Các nút và radio vẫn thao tác chuẩn bằng Tab/Space.

Gợi ý cho xem keyword; đánh dấu lượt đã được hỗ trợ. Bỏ qua ghi nhận là cần ôn. Đánh dấu để ôn độc lập với đáp án. Cho xem lưới điều hướng câu và quay về câu trước; xem lại câu đã chấm không tăng thống kê.

Nút Lưu và thoát giữ lượt, trở về tổng quan. Khi bắt đầu lượt khác trong lúc có bài dang dở, dialog cho Tiếp tục bài cũ / Thay bằng bài mới / Hủy. Thay bài không xóa lịch sử đã ghi nhận.

### Thi thử

Đề mẫu giữ thứ tự 20 mục số 3–22 sau khi kiểm chứng; đề trộn lấy đúng 20 câu duy nhất, phân bổ vòng qua 6 chương, có cả số liệu; hạn chế cùng concept khi còn lựa chọn khác. Ghi rõ đề trộn để luyện, không nhận là ma trận thi thật.

Không hiển thị gợi ý, đáp án hoặc giải thích trước khi nộp. Có thể sửa lựa chọn, đi trước/sau và đánh dấu. Nộp mở dialog ghi số câu còn trống. Đồng hồ tùy chọn 15 / 20 / 30 phút do người học chọn, mặc định không giới hạn. Hết giờ tự nộp; tải lại dùng `deadline` đã lưu, không cộng lại thời gian. Không tự lưu thống kê đúng/sai trước khi nộp; thao tác nộp phải idempotent.

### Kết quả

Hiển thị đúng/tổng, điểm thang 10, câu sai, bỏ qua, dùng gợi ý và thời gian. Lượt luyện có gợi ý tách khỏi số đúng độc lập. Danh sách lọc Tất cả / Sai–bỏ qua / Dùng gợi ý, mở được lời giải từng câu. Nút Làm lại câu cần ôn, Luyện lại bộ này, Về tổng quan. Nếu mọi câu đúng và không gợi ý/đánh dấu thì hiện trạng thái hoàn thành thay vì nút ôn sai trống.

### Cần ôn / sổ keyword

Cần ôn gồm câu trả lời sai hoặc bỏ qua ở lần gần nhất, câu dùng gợi ý chưa có lần đúng độc lập sau đó, và câu tự đánh dấu. Một câu đúng độc lập ở lượt mới xóa trạng thái sai/gợi ý, không tự bỏ dấu thủ công. Trạng thái trống có đường đi đến các chương.

Sổ keyword tìm không phân biệt dấu, chữ hoa hay `đ/d`, lọc chương hoặc số liệu; thẻ có cụm gợi nhớ, ý cần nhớ, dễ nhầm và nguồn. Tự kiểm tra bằng che/hiện; việc lật thẻ không tự coi là đã làm đúng câu hỏi.

## 5. Dữ liệu và các bất biến

```ts
type Question = {
  id: string; revision: number; chapter: 1|2|3|4|5|6;
  topic: string; conceptId: string; tags: ('date'|'congress'|'count')[];
  prompt: string; options: {id: string; text: string}[];
  correctOptionId: string; shufflePolicy: 'safe'|'fixed';
  originType: 'original'|'converted'; explanation: string;
  keywords: string[]; confusionNote?: string;
  sources: {sourceId: string; pdfPage: number; originalNumber: number; group?: string}[];
  theoryReferences: {sourceId: string; pdfPage: number; section: string; evidence: string}[];
  editorialNote?: string; reviewStatus: 'verified';
}
```

- ID phương án ổn định, không lấy vị trí hiển thị làm đáp án. Lượt lưu cả thứ tự câu và thứ tự phương án để tải lại không đổi đề.
- Câu tham chiếu A/B, “trên”, hoặc nội dung phụ thuộc vị trí dùng `fixed`; chỉ đảo khi không đổi nghĩa. “Cả ba đáp án” ở câu LMS có thể chuẩn hóa thành “Cả ba phương án còn lại” và ghi nhận biên tập.
- Mỗi câu có 2–4 lựa chọn không rỗng, một đáp án hợp lệ, ít nhất một nguồn câu hỏi và một căn cứ lý thuyết. Không phát hành câu pending/disputed.
- Dữ liệu biên tập tách khỏi JSON dùng trên web. Có báo cáo mọi mục ngân hàng chính và tình trạng các nguồn bổ sung.
- Mỗi chương có ít nhất 5 nhóm ý cốt lõi có căn cứ. Bộ đếm độ phủ lấy `conceptId` duy nhất, không lấy số lượt làm.

## 6. Lưu tiến độ

Khóa có phiên bản `nam-y:progress:v1`; payload gồm phiên bản schema/ngân hàng, bản ghi theo ID và revision câu, lượt dang dở, kết quả gần nhất và lịch sử lượt tối đa 50 mục. Thống kê gồm số lần gặp, đúng độc lập/sai, thời điểm gần nhất, kết quả gần nhất và đánh dấu.

JSON sai hoặc dữ liệu cũ không làm crash; dữ liệu revision cũ của câu không tính là kiến thức đã nắm trong phiên bản mới. Lượt không hợp lệ bị bỏ, thông báo ngắn. Nếu localStorage không ghi được, tiếp tục học bằng bộ nhớ và báo chưa lưu. Cho xuất JSON, nhập JSON có kiểm tra cấu trúc/kích thước, và xóa tiến độ sau xác nhận. Không gửi dữ liệu cá nhân lên máy chủ.

## 7. Cấu trúc mã và triển khai

Vite + TypeScript + CSS, không backend; module dữ liệu, engine chọn/chấm, storage, view và event tách biệt. Tài nguyên cùng origin, không yêu cầu API key hay dịch vụ trả phí. Dùng `base: './'` và hash route để chạy trên GitHub Pages của repository bất kỳ.

Lệnh: `npm install`, `npm run dev`, `npm run check`, `npm test`, `npm run build`, `npm run preview`. Build ra `dist/`. Workflow GitHub Actions chạy kiểm tra dữ liệu, typecheck, test, build rồi deploy Pages. Không commit `.analysis`, file nguồn PDF/ZIP, node_modules, dist, thông tin xác thực hoặc dữ liệu tiến độ.

Repository chưa có tên/remote hoặc công cụ không tạo được repository: hoàn thiện và kiểm tra mã tại workspace, chuẩn bị workflow và hướng dẫn public; không tự đẩy vào repository khác không liên quan. Chỉ ghi URL đã thực sự triển khai thành công.

## 8. Kiểm thử và nghiệm thu

1. Nội dung: mọi mục của ngân hàng chính có trạng thái, không có câu thiếu phương án/nguồn/keyword; câu tranh chấp không lọt vào đề. Cặp ngày/sự kiện và số lượng được đối chiếu đúng phiên bản.
2. Engine: đảo đáp án vẫn chấm đúng; câu fixed giữ nguyên; chọn 20 câu không trùng; bộ số liệu và chương không đếm đôi; quay lại/khôi phục/nộp lặp không tăng thống kê.
3. Luyện: chọn → kiểm tra → lời giải → câu tiếp → kết quả → luyện sai hoạt động bằng chuột và phím; dùng gợi ý không tính đúng độc lập.
4. Thi: không lộ đáp án trước nộp; câu bỏ trống được đếm; thời gian hết tự nộp, reload không reset; chấm một lần.
5. Tiến độ: reload/tiếp tục, phiên bản câu, JSON hỏng, storage bị chặn, xuất/nhập hợp lệ và dữ liệu không hợp lệ.
6. Browser: desktop và điện thoại, menu/dialog/focus, back/forward, không lỗi console hoặc asset 404; 200% zoom vẫn dùng được.
7. GitHub Pages: build tĩnh, tài nguyên đường dẫn tương đối, reload hash route; CI có kiểm tra trước deploy.

Tình trạng triển khai và kết quả kiểm tra thực tế ghi trong README/báo cáo kiểm tra; không biến điều chưa kiểm tra thành tiêu chí đã đạt.
