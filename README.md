# Nắm ý — Ôn tập nhiều môn

**[Vào học trên web](https://trungngd195.github.io/nam-y-tthcm/)** · [Đặc tả chung](DAC_TA_CHUNG.md)

Chọn môn → chọn chương → học ý cốt lõi → luyện câu hỏi → nhớ keyword và ôn sai. Ưu tiên máy tính, nút học rõ ràng, không đăng nhập, không khóa chương hoặc giới hạn lượt.

TTHCM có **45 mục học theo 6 chương, gồm 213 nhóm kiến thức** được đối chiếu từ toàn bộ 506 câu. Mỗi mục có ý cần hiểu, keyword, điểm dễ nhầm, nguồn và danh sách câu liên quan; luyện riêng một ý, một mục hoặc cả chương. [Bảng liên kết từng câu với bài học](content/tthcm/lesson-coverage.json) được tái tạo cùng ngân hàng; thêm câu mà chưa có bài học tương ứng sẽ bị validator chặn.

| Môn | Trạng thái |
| --- | --- |
| Tư tưởng Hồ Chí Minh | 506 câu, 6 chương, 92 câu số liệu; 8 đề × 60 + 1 đề cuối 26 câu, không lặp giữa các đề |
| Xử lý ảnh | 168 câu/bài tự luận có lời giải, chia ngân hàng theo 4 mức điểm và bộ cô Uyên theo chương |
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
  features/solutions/   đọc đề tự luận, công thức, lời giải và tự đánh giá
  shared/               UI, blocks, công thức, styles
  subjects/
    catalog.json        thông tin và cấu hình từng môn
    tthcm/bank.json     câu hỏi, concept, chương và nguồn đã biên tập
    xu-ly-anh/solutions.json  168 đề và lời giải từng bước
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

Mô hình câu có block ảnh, ma trận, bảng, code và công thức TeX. Công thức dùng KaTeX tải khi cần; code chỉ hiển thị, không chạy. Ảnh thuộc `public/subjects/<id>/`. Catalog dùng `learningMode: "solutions"` và `solutions.json` cho bộ bài tự luận; mặc định `quiz` và `bank.json` cho trắc nghiệm. Không chuyển bài tự luận thành câu chọn đáp án giả.

## Nội dung Xử lý ảnh

[Vào môn Xử lý ảnh](https://trungngd195.github.io/nam-y-tthcm/#/mon/xu-ly-anh).

- **giải ngân hàng**: 51 mục — 1 điểm 14, 2 điểm 16, 3 điểm 11, 4 điểm 10 (có một bài bổ sung không đánh số sau 4.8).
- **giải bài cô Uyên**: 117 mục, gộp hai bản lý thuyết Việt–Anh trùng 28 câu; chia theo chương của slide/bộ Ôn tập, ưu tiên chương 3–7.
- Đọc đề → tự làm → mở lời giải → đánh dấu Cần ôn/Đã nắm. Bài tính giữ ảnh đề, có câu dẫn, công thức rồi thay số và kết quả. **101 câu lý thuyết có câu trả lời hoàn chỉnh**, chia theo từng vế đề hỏi, có keyword, công thức, ví dụ hoặc giải thích đúng/sai khi cần. Ngân hàng bám đáp án đã đối chiếu giáo trình/slide; khu cô Uyên theo lý thuyết, cùng cách trình bày. [Bảng đối chiếu từng câu](content/xu-ly-anh/theory-answer-review.json) ghi căn cứ và hash câu hỏi/câu trả lời; ghi chú tại câu các lỗi nguồn như CMY `225` thay vì `255`, mặt nạ Prewitt và phạm vi màu CMY.
- **67 bài tính hiển thị bằng ảnh trang PDF**, tách riêng từng câu (a), (b), (c)…; mỗi bước có công thức, **ký hiệu, cách làm**, thay số và kết quả. Có nút nhảy tới từng câu, PDF tổng hợp gồm đề và lời giải, mục lục dấu trang, ảnh lớn và bản văn bản. Dàn theo đáp án ngân hàng: chữ serif, bảng histogram ngang, ma trận rõ ràng. Lý thuyết đúng/sai tách từng nhận định, đặt câu trả lời ngay dưới nhận định tương ứng.
- Chỉ lược ý hỏi trùng ở **lý thuyết cô Uyên**: giữ đủ 71 câu; 26 câu giữ các vế mới, 10 câu trùng hoàn toàn giữ mã/đề gốc và dẫn đến câu đã hỏi. Câu trả lời viết đầy đủ, làm nổi keyword; đề gốc luôn mở được để đối chiếu. **67 bài tính (46 bài cô Uyên) giữ đủ mọi yêu cầu**, lời giải từng phần và ảnh PDF. [Bảng rà lý thuyết](content/xu-ly-anh/theory-focus-review.json) ghi từng ý lược, ý giữ và câu tham chiếu. Bản rút gọn bài tập trước đó đã được hủy áp dụng.
- Cấu trúc đề theo người học: đạo đức, lý thuyết, hai bài tập chương 3–7. Chưa có bộ câu đạo đức riêng nên chưa biên soạn lời giải phần đó.
- [Kiểm kê và các quy ước/sai sót nguồn](content/xu-ly-anh/KIEM_KE_VA_QUY_UOC.md).

Tái tạo nội dung (ZIP gốc cần có trong `materials/xu-ly-anh` khi chạy ingest):

```sh
pip install -r scripts/content/requirements.txt
pip install Pillow
python scripts/content/xu-ly-anh/ingest.py
python scripts/content/xu-ly-anh/build.py
pip install -r scripts/content/xu-ly-anh/requirements-review.txt
python scripts/content/xu-ly-anh/verify.py
node scripts/content/xu-ly-anh/render-documents.mjs
python scripts/content/xu-ly-anh/rasterize_documents.py
python scripts/content/xu-ly-anh/verify_documents.py
npm run check
```

CI chạy kiểm tra toán độc lập bằng NumPy/SciPy; khi học chỉ cần file web tĩnh, không cần Python, tài khoản hoặc máy chủ API.

## Nội dung TTHCM

[Luyện đề tổng hợp](https://trungngd195.github.io/nam-y-tthcm/#/mon/tthcm/de-tong-hop): **8 đề 60 câu và 1 đề cuối 26 câu**. Cả bộ dùng đúng 506 câu, mỗi câu chỉ thuộc một đề. Rải đều số câu của từng chương giữa các đề chính theo lượng câu thực có. Có thể làm lại, lưu bài dang dở và xem lời giải sau nộp. Điểm bộ 50 câu cũ không gán sang bộ mới; bài cũ đang làm vẫn có thể tiếp tục. Đề mẫu/đề trộn 20 câu vẫn nằm trong khu Thi thử.

506 câu chuẩn từ 755 mục nguồn: 233 mục LMS/quiz/đề mẫu và 522 mục tại 6 link Azota. Sau đợt gộp ban đầu còn 623 câu; đợt rà trùng ý gộp thêm 117 bản trong 96 nhóm, còn 506. [Quyết định gộp](content/tthcm/duplicate-decisions.json) giữ hash đề/lựa chọn/đáp án trước gộp; mọi nguồn và bản chụp gốc vẫn giữ. 4 câu Azota và 11 mục cũ còn mơ hồ chưa dùng để chấm. Mỗi câu có keyword, lời giải ngắn và căn cứ đối chiếu. [Báo cáo nội dung](content/tthcm/BAO_CAO_NOI_DUNG.md) và [quyết định từng mục](content/tthcm/azota/reviewed.json) ghi đầy đủ thay đổi.

| Chương theo giáo trình | Câu kiến thức | Câu số liệu | Tổng |
| --- | ---: | ---: | ---: |
| 1 | 19 | 11 | 30 |
| 2 | 70 | 53 | 123 |
| 3 | 104 | 11 | 115 |
| 4 | 101 | 4 | 105 |
| 5 | 45 | 7 | 52 |
| 6 | 75 | 6 | 81 |

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

Việc học trên web không cần Python hay các PDF gốc. Importer gốc không lấy lại Azota; các snapshot Azota đã kiểm duyệt được lưu tại `content/tthcm/azota/`. Không sửa snapshot rồi tái dùng key vị trí: curator sẽ từ chối khi băm không khớp. Không tăng revision câu nếu chỉ đổi nơi lưu trữ; khi sửa ý nghĩa hoặc đáp án của câu đã phát hành thì tăng revision và phiên bản ngân hàng.

## Tiến độ và tương thích bản cũ

- Mỗi môn lưu riêng tại `nam-y:progress:v2:<id>`; xuất/nhập/xóa chỉ ảnh hưởng môn đang mở.
- TTHCM tự đọc tiến độ v1 khi chưa có bản v2, giữ records, bài dang dở và thứ tự đáp án đã đảo. Bản v1 vẫn được giữ làm dự phòng.
- Nhập tệp sai môn bị từ chối dù có ID câu giống nhau. Không tự đồng bộ giữa các trình duyệt/thiết bị; dùng xuất/nhập JSON để chuyển máy.
- URL cũ như `#/chuong/2` và `#/lam-bai` chuyển về môn TTHCM. Giữ nguyên URL GitHub Pages và repository hiện có để không làm hỏng liên kết đã chia sẻ.
- Tự đánh giá bài tự luận lưu riêng tại `nam-y:solutions:v1:<id>`, không ghi vào kết quả trắc nghiệm và không tự chấm điểm.

## Public

Website tĩnh, deploy bằng `.github/workflows/pages.yml`; các bước check, test, build và browser test phải qua trước khi triển khai. Repository public; Settings → Pages dùng GitHub Actions. Chỉ `dist/` được xuất bản; tài liệu gốc và tệp phân tích không đẩy lên GitHub.

Tham khảo: [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [Vite import theo yêu cầu](https://vite.dev/guide/features.html#glob-import), [KaTeX API](https://katex.org/docs/api.html).
