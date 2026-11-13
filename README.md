# Nắm ý — Ôn thi Tư tưởng Hồ Chí Minh

Web ôn trắc nghiệm ưu tiên laptop và desktop, không cần đăng nhập. Học ý cốt lõi, luyện câu ngân hàng, ghi nhớ keyword và ôn lại câu còn yếu.

**Vào học:** [trungngd195.github.io/nam-y-tthcm](https://trungngd195.github.io/nam-y-tthcm/)

## Chạy tại máy

Cần Node.js 22.18 trở lên (bản 22 LTS hoặc bản LTS mới hơn tương thích).

```sh
npm ci
npm run dev
```

Mở địa chỉ Local mà Vite in ra, thường là `http://127.0.0.1:5173`.

```sh
npm run check     # TypeScript và cấu trúc/nội dung ngân hàng
npm test          # Engine chấm bài, chọn đề, tiến độ
npm run build    # Tạo website tĩnh trong dist/
npm run preview  # Xem bản đã build
```

Kiểm thử bằng trình duyệt:

```sh
npx playwright install chromium
npm run build
npm run test:e2e
```

Có thể dùng Chrome đã cài thay cho trình duyệt tải về. Trong PowerShell:

```powershell
$env:PLAYWRIGHT_CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
npm run test:e2e
```

## Luồng học

- **6 chương:** đọc kiến thức cốt lõi, luyện 10/20/tất cả câu; tùy chọn kèm số liệu.
- **Con số cần nhớ:** lọc mốc thời gian, Đại hội/hội nghị, số lượng nội dung.
- **Luyện từng câu:** chọn rồi kiểm tra, hiện giải thích ngắn, keyword và nguồn. Phím 1–4 chọn đáp án, Enter kiểm tra rồi đi tiếp bằng lần nhấn riêng.
- **Thi thử:** đề mẫu thầy Cường đủ 20 câu và đề trộn 20 câu. Không hiện đáp án trước khi nộp; thời gian tùy chọn, tải lại không làm tăng thời gian.
- **Cần ôn:** câu sai, bỏ qua, dùng gợi ý hoặc tự đánh dấu. Đúng nhờ gợi ý không tính là trả lời đúng độc lập.
- **Sổ keyword:** tìm có dấu/không dấu, tự nhớ rồi mở ý chính.
- **Tiến độ:** tự lưu trong trình duyệt; có xuất/nhập JSON để chuyển máy. Không có máy chủ thu thập tiến độ.

## Phạm vi nội dung

Hiện có **215 câu chuẩn**, từ **233 mục** của LMS, quiz cô Khánh và đề mẫu. **11 mục** chưa dùng để chấm vì thiếu lựa chọn hợp lệ, mơ hồ hoặc mâu thuẫn. Đề mẫu giữ đủ 20 mục theo thứ tự câu gốc 3–22; những câu trùng dùng chung ID và giữ đủ nguồn.

Mỗi câu có đáp án theo mã phương án, keyword, giải thích ngắn, trang và số câu nguồn, căn cứ đối chiếu. Căn cứ là diễn giải tài liệu, không phải trích nguyên văn. Việc đảo đáp án có kiểm soát: câu phụ thuộc A/B giữ thứ tự. Các câu trả lời ngắn được chuyển đổi có ghi chú riêng.

Xem [báo cáo nội dung](content/BAO_CAO_NOI_DUNG.md) để biết từng mục chưa dùng và tình trạng nguồn bổ sung. Bộ Tổng hợp và Bonus chưa được nhập toàn bộ; không tính các mục chưa nhập vào số câu sẵn sàng. Đây là tài liệu ôn tập theo nguồn trong môn, không phải đề thi chính thức hay dự đoán đề.

## Đặc tả và cấu trúc

- [Đặc tả chung](DAC_TA_CHUNG.md): chuẩn triển khai, trạng thái, hành vi và nghiệm thu.
- [Bản đề xuất ban đầu](DE_XUAT_WEB_ON_THI.md): kết quả khảo sát và lựa chọn thiết kế.
- `src/data/bank.json`: dữ liệu công khai đã biên tập.
- `content/raw-questions.json`: các mục gốc được trích từ ba ngân hàng chính.
- `content/editorial-decisions.json`: quyết định biên tập của từng mục.
- `scripts/curate_content.py`: quy tắc và nội dung biên tập có thể tái tạo dữ liệu.
- `src/engine.ts`: chọn câu, đảo phương án, chấm bài và ôn lại.
- `src/storage.ts`: kiểm tra dữ liệu và lưu/khôi phục tiến độ.
- `src/main.ts`, `src/ui.ts`, `src/style.css`: giao diện, điều hướng và thao tác.
- `tests/`: kiểm thử engine và trình duyệt.

Muốn trích xuất lại nguồn tại máy: đặt các tài liệu gốc vào `Theory_and_questionbank/`, cài `pip install -r scripts/requirements.txt`, chạy `python scripts/import_sources.py` rồi `python scripts/curate_content.py`. Kiểm tra lại nội dung trước khi công khai. CI và việc chạy web bình thường không cần Python hoặc các PDF gốc.

Khi sửa đáp án hoặc ý nghĩa câu đã phát hành, tăng `revision` của câu và phiên bản ngân hàng. Tiến độ từ revision cũ không tính là bằng chứng đã nắm đúng kiến thức mới.

## Public trên GitHub Pages

1. Tạo repository **public**, đưa mã nguồn lên nhánh `main`.
2. Vào **Settings → Pages → Build and deployment → Source → GitHub Actions**.
3. Workflow `.github/workflows/pages.yml` kiểm tra dữ liệu, chạy test, build và kiểm tra trình duyệt trước khi triển khai.
4. Mở URL được workflow trả về. Hash route và tài nguyên tương đối hỗ trợ đường dẫn dạng `https://<tài-khoản>.github.io/<repository>/`.

Chỉ thư mục `dist/` được xuất bản. PDF/ZIP gốc, `.analysis/`, `node_modules/`, dữ liệu tiến độ và tệp môi trường được loại khỏi Git/bản triển khai.

Tham khảo: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [workflow Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [Vite static deployment](https://vite.dev/guide/static-deploy.html#github-pages).
