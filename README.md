# Nắm ý — Ôn tập nhiều môn

**[Vào học trên web](https://trungngd195.github.io/nam-y-tthcm/)** · [Đặc tả chung](DAC_TA_CHUNG.md)

Chọn môn → chọn chương → học ý cốt lõi → luyện câu hỏi → nhớ keyword và ôn sai. Ưu tiên máy tính, nút học rõ ràng, không đăng nhập, không khóa chương hoặc giới hạn lượt.

| Môn | Trạng thái |
| --- | --- |
| Tư tưởng Hồ Chí Minh | 623 câu, 6 chương, 110 câu số liệu; đề mẫu 20 câu |
| Xử lý ảnh | Chờ giáo trình và ngân hàng, chưa tạo câu hoặc chia chương |
| Khoa học dữ liệu | Chờ giáo trình và ngân hàng, chưa tạo câu hoặc chia chương |

## Chạy và kiểm tra

Cần Node.js 22.18 trở lên hoặc bản LTS tương thích.

```sh
npm ci
npm run dev
```

Mở URL Local mà Vite in ra, thường là `http://127.0.0.1:5173`.

```sh
npm run check    # TypeScript, catalog, ngân hàng của từng môn
npm test         # Engine, lưu tiến độ, migration, routing, scientific blocks
npm run build    # Build tĩnh ra dist/
npm run preview  # Xem bản build
```

Kiểm tra trình duyệt sau khi build:

```sh
npx playwright install chromium
npm run test:e2e
```

Hoặc dùng Chrome đã cài, trong PowerShell:

```powershell
$env:PLAYWRIGHT_CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
npm run test:e2e
```

## Cấu trúc dự án

```text
src/
  app/                  router, đăng ký và tải môn, vòng đời ứng dụng
  core/                 engine, kiểu dữ liệu, tiến độ, migration
  features/subjects/    trang chọn môn, trang chờ tài liệu
  features/study/       luồng học chung, không nhân bản theo môn
  shared/               UI, blocks, công thức, styles
  subjects/
    catalog.json        thông tin và cấu hình từng môn
    tthcm/bank.json     câu hỏi, concept, chương và nguồn đã biên tập
materials/<id>/         tài liệu gốc riêng từng môn, không public file gốc
content/<id>/           trích xuất, audit và quyết định biên tập theo môn
public/subjects/<id>/   ảnh, sơ đồ dùng trong câu hỏi đã kiểm duyệt
scripts/content/       validator chung và importer/curator riêng từng môn
scripts/deploy/        công cụ GitHub Pages
tests/core/            kiểm thử logic
tests/browser/         kiểm thử thao tác và bố cục
docs/archive/          tài liệu TTHCM v1
docs/verification/     kết quả kiểm tra
```

Các thư mục mã môn dùng thống nhất: `tthcm`, `xu-ly-anh`, `khoa-hoc-du-lieu`.

## Bổ sung hai môn mới

Đặt tài liệu vào:

- `materials/xu-ly-anh/`
- `materials/khoa-hoc-du-lieu/`

Sau khi có tài liệu: đọc phạm vi, xác định chương và ngân hàng, lưu dữ liệu biên tập trong `content/<id>/`; chỉ xuất câu đủ căn cứ sang `src/subjects/<id>/bank.json`. Đăng ký metadata, số câu/chương thực tế và chuyên đề trong catalog, rồi chuyển trạng thái sang `ready` sau khi kiểm tra.

Không sao chép khung 6 chương hoặc chuyên đề Đại hội của TTHCM sang môn khác. Engine chọn đề lấy chương từ dữ liệu thực, mỗi môn có thể có độ dài đề mẫu/đề trộn khác nhau. Trang chọn môn chỉ tải metadata; mở môn nào mới tải ngân hàng môn đó.

Mô hình câu chuẩn bị block ảnh, ma trận, bảng, code và công thức TeX cho đề, lựa chọn, giải thích. Công thức dùng KaTeX tải khi cần; code chỉ hiển thị, không chạy. Ảnh phải nằm trong `public/subjects/<id>/`, có alt và tham chiếu từ đúng môn. Chưa có tài liệu thì không xuất bản câu minh họa giả. Bản hiện tại chấm trắc nghiệm một đáp án đúng với 2–4 lựa chọn.

## Nội dung TTHCM

623 câu chuẩn từ 755 mục nguồn: 233 mục LMS/quiz/đề mẫu và 522 mục tại 6 link Azota. Thêm 408 câu, gộp 110 lượt trùng; 4 câu Azota và 11 mục cũ còn mơ hồ chưa dùng để chấm. Đã đọc lại 215 câu cũ, sửa câu mơ hồ và mốc chống thuế theo nguồn Bảo tàng; 23 câu tăng revision. Mỗi câu có keyword, lời giải ngắn và căn cứ đối chiếu. [Báo cáo nội dung](content/tthcm/BAO_CAO_NOI_DUNG.md) và [quyết định từng mục](content/tthcm/azota/reviewed.json) ghi đầy đủ thay đổi.

| Chương theo giáo trình | Câu kiến thức | Câu số liệu | Tổng |
| --- | ---: | ---: | ---: |
| 1 | 21 | 12 | 33 |
| 2 | 95 | 68 | 163 |
| 3 | 128 | 11 | 139 |
| 4 | 121 | 4 | 125 |
| 5 | 58 | 8 | 66 |
| 6 | 90 | 7 | 97 |

Phân chương theo nội dung giáo trình; tên chương của đề Azota vẫn lưu trong nguồn gốc. Câu số liệu nằm trong chuyên đề riêng, tùy chọn đưa vào lượt luyện chương. Các snapshot giữ nguyên câu hỏi/thứ tự lựa chọn trong lần lấy, có băm chống thay nhầm thứ tự đáp án. Đáp án do đối chiếu tài liệu, không dùng key chấm Azota. Khi hai lựa chọn cùng đúng hoặc câu nguồn sai, bản trên web được sửa có ghi chú hoặc giữ ngoài bài chấm.

File Word đầy đủ đặt tại `TTHCM_AZOTA_522_CAU_HOI_VA_DAP_AN.docx` trong workspace (không đẩy bản Word lên GitHub). Tái tạo sau khi biên tập:

```sh
python scripts/content/tthcm/curate_content.py
python scripts/content/tthcm/export_azota_docx.py
```

Tài liệu cũ đã chuyển từ `Theory_and_questionbank/` vào `materials/tthcm/`. Để tái tạo tại máy:

```sh
pip install -r scripts/content/requirements.txt
python scripts/content/tthcm/import_sources.py
python scripts/content/tthcm/curate_content.py
npm run check
```

CI và việc học trên web không cần Python hay các PDF gốc. Importer gốc không lấy lại Azota; các snapshot Azota đã kiểm duyệt được lưu tại `content/tthcm/azota/`. Không sửa snapshot rồi tái dùng key vị trí: curator sẽ từ chối khi băm không khớp. Không tăng revision câu nếu chỉ đổi nơi lưu trữ; khi sửa ý nghĩa hoặc đáp án của câu đã phát hành thì tăng revision và phiên bản ngân hàng.

## Tiến độ và tương thích bản cũ

- Mỗi môn lưu riêng tại `nam-y:progress:v2:<id>`; xuất/nhập/xóa chỉ ảnh hưởng môn đang mở.
- TTHCM tự đọc tiến độ v1 khi chưa có bản v2, giữ records, bài dang dở và thứ tự đáp án đã đảo. Bản v1 vẫn được giữ làm dự phòng.
- Nhập tệp sai môn bị từ chối dù có ID câu giống nhau. Không tự đồng bộ giữa các trình duyệt/thiết bị; dùng xuất/nhập JSON để chuyển máy.
- URL cũ như `#/chuong/2` và `#/lam-bai` chuyển về môn TTHCM. Giữ nguyên URL GitHub Pages và repository hiện có để không làm hỏng liên kết đã chia sẻ.

## Public

Website tĩnh, deploy bằng `.github/workflows/pages.yml`; các bước check, test, build và browser test phải qua trước khi triển khai. Repository public; Settings → Pages dùng GitHub Actions. Chỉ `dist/` được xuất bản; tài liệu gốc và tệp phân tích không đẩy lên GitHub.

Tham khảo: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [Vite import theo yêu cầu](https://vite.dev/guide/features.html#glob-import), [KaTeX API](https://katex.org/docs/api.html).
