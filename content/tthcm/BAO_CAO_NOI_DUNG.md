# Báo cáo nội dung

**506 câu chuẩn** trên web; 92 câu thuộc chuyên đề con số. Đề mẫu vẫn đủ 20 câu.

Đã gộp thêm 117 bản hỏi trùng ý trong 96 nhóm, từ 623 xuống 506 câu. Quyết định có hash đề/lựa chọn tại `duplicate-decisions.json`; giữ nguyên snapshot và đáp án đối chiếu từng mục nguồn.

## Sáu đề Azota

| Đề | Mục gốc | Thêm câu | Gộp trùng | Chờ xác minh |
| --- | ---: | ---: | ---: | ---: |
| [e9lwce](https://azota.vn/de-thi/e9lwce) | 71 | 54 | 17 | 0 |
| [rnaeqk](https://azota.vn/de-thi/rnaeqk) | 148 | 109 | 38 | 1 |
| [ela4jq](https://azota.vn/de-thi/ela4jq) | 88 | 63 | 22 | 3 |
| [ijqzcg](https://azota.vn/de-thi/ijqzcg) | 44 | 32 | 12 | 0 |
| [3eggrt](https://azota.vn/de-thi/3eggrt) | 76 | 56 | 20 | 0 |
| [n6fnzo](https://azota.vn/de-thi/n6fnzo) | 95 | 2 | 93 | 0 |

Tổng cộng **522 mục gốc**: 316 câu thêm, 202 lượt gộp, 4 câu chờ. 233 mục nguồn ban đầu vẫn có đủ audit; 11 mục cũ còn giữ ngoài bài chấm.

## Quy tắc đáp án

- Ưu tiên giáo trình 2019 và bài giảng PTIT được cung cấp; không sao chép đáp án Azota.
- Giáo trình Bộ GDĐT bản cũ chỉ đối chiếu phần mở rộng, không thay khung giai đoạn hiện hành.
- Số liệu thiếu/mâu thuẫn đối chiếu Bảo tàng Hồ Chí Minh, tác phẩm gốc, Văn phòng Chủ tịch nước, Tư liệu Văn kiện Đảng và Báo Nhân Dân. Mỗi câu có vị trí/căn cứ đối chiếu.
- Bản chụp câu hỏi, thứ tự lựa chọn gốc tách khỏi bản biên tập. Chữ A–D chỉ đúng với đúng snapshot; không dùng chữ cái để suy đáp án giữa các lượt Azota.
- Sửa mốc chống thuế thành 4/1908; mốc Hội nghị TW8 thành 5/1941; giai đoạn hình thành nội dung cơ bản theo giáo trình là 1920–1930.
- Không coi lựa chọn “có vẻ đúng nhất” là đủ khi có hai phương án cùng đúng: sửa có ghi chú hoặc giữ ngoài bài chấm.
- Đã đọc lại 215 câu cũ; tăng revision cho câu thay ý nghĩa để kết quả cũ không tiếp tục chứng nhận một câu đã sửa.

## Các câu chờ xác minh

- **azota-rnaeqk-018**: Câu hỏi đánh giá “thành tựu nổi bật nhất” nhưng không nêu giai đoạn, văn kiện hay tiêu chí. Không áp một lựa chọn thành kết luận của giáo trình.
- **azota-ela4jq-027**: “Nguy cơ lớn nhất” không có phạm vi, thời điểm và trích dẫn đủ rõ; các lựa chọn chồng lấn. Không ép chọn khi chưa xác định được luận điểm nguồn.
- **azota-ela4jq-039**: Việc xếp luận điểm vào “vị thế/phương thức/năng lực cầm quyền” không có căn cứ phân loại đủ rõ trong giáo trình; chưa dùng để chấm.
- **azota-ela4jq-085**: Câu hỏi về hệ tư tưởng và phương thức sản xuất của giai cấp nông dân thuộc nội dung lý luận rộng hơn; chưa có đoạn giáo trình môn này đối chiếu trực tiếp để chấm.

## Dữ liệu kiểm tra

- `azota/<code>.json`: bản gốc 522 câu và lựa chọn.
- `azota/reviewed.json`: quyết định từng mục, đáp án nội dung, keyword, bản biên tập, nguồn đối chiếu và băm snapshot.
- `azota/official-sources.json`: URL nguồn chính thống và tài liệu bổ sung.
- `scripts/content/tthcm/azota_editorial.py`: lựa chọn thủ công và lý do sửa.

## Nguồn bổ sung cũ

- combined: Đã khảo sát; chưa nhập toàn bộ vì cần đối chiếu phiên bản kiến thức và bảng đáp án.
- bonus: Dùng chọn lọc để đối chiếu câu trong đề mẫu; chưa nhập toàn bộ các câu tiểu sử và phần bổ sung.
- timeline: Đã khảo sát, dùng hỗ trợ rà mốc; chưa chuyển thành bộ câu hỏi mới.
