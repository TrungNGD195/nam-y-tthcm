"""Editorial decisions for the local question banks. No generated external facts."""
from pathlib import Path
import copy
import json
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
RAW = json.loads((ROOT / "content/tthcm/raw-questions.json").read_text(encoding="utf-8"))
BY_ID = {q["id"]: q for q in RAW}
concepts = {}
reviews = {}

def concept(key, chapter, title, summary, keywords, page, *, source="ptit", confusion="", core=False):
    concepts[key] = {"id": key, "chapter": chapter, "title": title, "summary": summary,
                     "keywords": keywords.split("|"), "confusionNote": confusion, "core": core,
                     "references": [{"sourceId": source, "pdfPage": page, "section": title, "evidence": summary}]}

# References are paraphrases of the identified sections, not verbatim quotations.
concept("definition",1,"Khái niệm và ba nội hàm","Khái niệm nêu bản chất khoa học, cách mạng và nội dung; cơ sở hình thành; ý nghĩa, giá trị. Quá trình hoặc thời gian hình thành không phải một nội hàm của khái niệm.","bản chất|cơ sở hình thành|ý nghĩa",9,core=True)
concept("value-definition",1,"Tài sản tinh thần","Tư tưởng Hồ Chí Minh là tài sản tinh thần vô cùng to lớn và quý giá của Đảng và dân tộc ta.","tài sản tinh thần|Đảng và dân tộc",9,core=True)
concept("meaning",1,"Ba ý nghĩa học tập","Học môn này giúp nâng cao tư duy lý luận; giáo dục, thực hành đạo đức cách mạng và bồi dưỡng lòng yêu nước; rèn luyện phương pháp, phong cách công tác.","tư duy lý luận|đạo đức cách mạng|phương pháp, phong cách",16,core=True)
concept("method",1,"Phương pháp luận","Nghiên cứu phải thống nhất tính Đảng và tính khoa học, lý luận và thực tiễn; có quan điểm lịch sử cụ thể, toàn diện và hệ thống, kế thừa và phát triển.","tính Đảng và tính khoa học|lý luận và thực tiễn|lịch sử cụ thể",11,core=True)
concept("foundation",1,"Nền tảng tư tưởng","Chủ nghĩa Mác–Lênin cùng với tư tưởng Hồ Chí Minh là nền tảng tư tưởng, kim chỉ nam cho hành động của Đảng. Phương án đầy đủ phải có cả hai.","Mác–Lênin cùng với|nền tảng tư tưởng|kim chỉ nam",8,core=True)
concept("congress2",1,"Đại hội II — 1951","Đại hội II năm 1951 yêu cầu học tập đường lối chính trị, tác phong và đạo đức cách mạng của Hồ Chủ tịch.","Đại hội II|1951|đường lối chính trị",6,confusion="Học tập một cách có hệ thống tư tưởng, đạo đức, tác phong → Đại hội V (1982).")
concept("eulogy",1,"Điếu văn — 1969","Điếu văn năm 1969 khẳng định dân tộc, nhân dân và non sông đất nước đã sinh ra Hồ Chủ tịch, người anh hùng dân tộc vĩ đại.","1969|anh hùng dân tộc vĩ đại",7)
concept("congress4",1,"Đại hội IV — 1976","Đại hội IV năm 1976 khẳng định những thắng lợi của cách mạng gắn liền với tên tuổi Hồ Chí Minh, người chiến sĩ lỗi lạc của phong trào cộng sản và công nhân quốc tế.","Đại hội IV|1976|chiến sĩ lỗi lạc",7)
concept("congress5",1,"Đại hội V — 1982","Đại hội V năm 1982 yêu cầu tổ chức học tập một cách có hệ thống tư tưởng, đạo đức, tác phong của Chủ tịch Hồ Chí Minh trong toàn Đảng.","Đại hội V|1982|một cách có hệ thống",7,confusion="Đại hội II (1951) nhấn mạnh học tập đường lối chính trị, tác phong và đạo đức.")
concept("congress6",1,"Đại hội VI — 1986","Đại hội VI năm 1986 yêu cầu nắm vững bản chất cách mạng và khoa học của chủ nghĩa Mác–Lênin, kế thừa di sản quý báu về tư tưởng và lý luận cách mạng của Hồ Chí Minh.","Đại hội VI|1986|bản chất cách mạng và khoa học",7)
concept("congress7",1,"Đại hội VII — 1991","Đại hội VII năm 1991 khẳng định Đảng lấy chủ nghĩa Mác–Lênin và tư tưởng Hồ Chí Minh làm nền tảng tư tưởng và kim chỉ nam cho hành động.","Đại hội VII|1991|nền tảng tư tưởng",8,confusion="Khái niệm đầy đủ được dùng trong giáo trình → Đại hội XI (2011).")
concept("congress11",1,"Đại hội XI — 2011","Giáo trình 2019 trình bày khái niệm tư tưởng Hồ Chí Minh theo văn kiện Đại hội XI năm 2011.","Đại hội XI|2011|khái niệm",9,confusion="Đại hội IX (2001) đã nêu định nghĩa; cần đọc đúng câu hỏi về khái niệm đầy đủ đang học.")

concept("practical",2,"Phân biệt thực tiễn và lý luận","Thực tiễn gồm xã hội Việt Nam và thế giới cuối thế kỷ XIX, đầu thế kỷ XX. Lý luận gồm truyền thống tốt đẹp của dân tộc, tinh hoa văn hóa nhân loại và chủ nghĩa Mác–Lênin.","thực tiễn|cuối thế kỷ XIX|đầu thế kỷ XX",18,core=True,confusion="Tình hình xã hội là cơ sở thực tiễn; truyền thống, tinh hoa văn hóa, Mác–Lênin thuộc cơ sở lý luận.")
concept("theoretical",2,"Ba nguồn lý luận","Ba nguồn lý luận là giá trị truyền thống tốt đẹp của dân tộc, tinh hoa văn hóa nhân loại và chủ nghĩa Mác–Lênin. Trong đó chủ nghĩa Mác–Lênin có vai trò quyết định.","truyền thống dân tộc|tinh hoa văn hóa|Mác–Lênin",22,core=True)
concept("eastern",2,"Tinh hoa phương Đông","Ba học thuyết phương Đông được nhấn mạnh là Nho giáo, Phật giáo và Lão giáo; Hồ Chí Minh tiếp thu có chọn lọc, phát triển sáng tạo.","Nho giáo|Phật giáo|Lão giáo",23,core=True)
concept("confucius",2,"Khổng Tử — tu dưỡng cá nhân","Ưu điểm lớn nhất của học thuyết Khổng Tử được ngân hàng hỏi là sự tu dưỡng đạo đức cá nhân; Nho giáo còn có ảnh hưởng về nhân trị, đức trị.","Khổng Tử|tu dưỡng đạo đức cá nhân|nhân trị, đức trị",8,source="summary",core=True,confusion="Giêsu → lòng nhân ái cao cả; chủ nghĩa Mác → phương pháp làm việc biện chứng.")
concept("jesus",2,"Giêsu — lòng nhân ái","Ưu điểm lớn nhất của tôn giáo Giêsu là lòng nhân ái cao cả. Không nhầm với sự tu dưỡng đạo đức cá nhân của Khổng Tử.","Giêsu|lòng nhân ái cao cả",3,source="lms")
concept("buddhism",2,"Phật giáo — từ bi và bình đẳng","Hồ Chí Minh tiếp thu tư tưởng từ bi, vị tha, yêu thương con người, cứu khổ cứu nạn, sống giản dị và tinh thần bình đẳng của Phật giáo.","Phật giáo|từ bi|bình đẳng",23,core=True)
concept("marx-method",2,"Ưu điểm của chủ nghĩa Mác","Câu hỏi về ưu điểm lớn nhất của chủ nghĩa Mác–Lênin chọn phương pháp làm việc biện chứng.","ưu điểm lớn nhất|phương pháp làm việc biện chứng",9,source="summary",confusion="Câu hỏi về tiền đề lý luận giữ vai trò quyết định → chủ nghĩa Mác–Lênin; đây là câu hỏi khác.")
concept("tam-dan",2,"Chủ nghĩa Tam dân","Tam dân của Tôn Trung Sơn gồm dân tộc độc lập, dân quyền tự do, dân sinh hạnh phúc; có ảnh hưởng đến quan điểm độc lập gắn với tự do, hạnh phúc của nhân dân.","dân tộc độc lập|dân quyền tự do|dân sinh hạnh phúc",25,core=True)
concept("subjective",2,"Nhân tố chủ quan","Nhân tố chủ quan gồm lý tưởng, hoài bão cứu nước; tư duy độc lập, sáng tạo, khả năng tiếp thu tinh hoa; phẩm chất và hoạt động thực tiễn phong phú của Hồ Chí Minh.","lý tưởng|tư duy độc lập|thực tiễn phong phú",27,core=True)
concept("phases",2,"Năm giai đoạn hình thành","Theo khung đang học: trước 1911 — yêu nước; 1911–1920 — tìm con đường vô sản; 1920–1930 — nội dung cơ bản; 1930–1941 — vượt thử thách; 1941–1969 — tiếp tục phát triển.","5 giai đoạn|1920–1930|1941–1969",28)
concept("phase1",2,"Trước 1911 — yêu nước","Trước năm 1911 là thời kỳ hình thành tư tưởng yêu nước và chí hướng tìm đường cứu nước mới.","trước 1911|yêu nước|chí hướng",28)
concept("phase2",2,"1911–1920 — tìm đường","Giai đoạn 1911–1920 hình thành tư tưởng cứu nước, giải phóng dân tộc Việt Nam theo con đường cách mạng vô sản.","1911–1920|con đường cách mạng vô sản",30)
concept("phase3",2,"1920–1930 — nội dung cơ bản","Giai đoạn 1920–1930 hình thành những nội dung cơ bản của tư tưởng về cách mạng Việt Nam, gắn với chuẩn bị và thành lập Đảng.","1920–1930|nội dung cơ bản",31)
concept("phase4",2,"1930–1941 — vượt thử thách","Giai đoạn 1930–1941 là thời kỳ vượt qua thử thách, giữ vững đường lối và phương pháp cách mạng Việt Nam đúng đắn, sáng tạo.","1930–1941|vượt qua thử thách|giữ vững đường lối",33)
concept("leech",2,"Con đỉa hai vòi","Hồ Chí Minh dùng hình tượng con đỉa có hai vòi để chỉ chủ nghĩa tư bản bóc lột ở chính quốc và thuộc địa.","chủ nghĩa tư bản|con đỉa có hai vòi",49)
concept("versailles",2,"Yêu sách — Vécxây 1919","Ngày 18/6/1919, Nguyễn Ái Quốc gửi bản Yêu sách của nhân dân An Nam đến Hội nghị Vécxây; bản yêu sách gồm tám điểm.","18/6/1919|Vécxây|Yêu sách",30)
concept("lenin-theses",2,"Luận cương — tháng 7/1920","Tháng 7/1920, Nguyễn Ái Quốc đọc Sơ thảo lần thứ nhất những luận cương về vấn đề dân tộc và thuộc địa của Lênin, tìm thấy con đường cách mạng vô sản.","7/1920|Luận cương|Lênin",30)
concept("vo-san",3,"Con đường cách mạng vô sản","Cách mạng giải phóng dân tộc muốn thắng lợi phải đi theo con đường cách mạng vô sản.","giải phóng dân tộc|cách mạng vô sản",46,core=True)
concept("duong-kach-menh",2,"Đường Kách mệnh","Đường Kách mệnh tập hợp các bài giảng huấn luyện cán bộ, chuẩn bị về chính trị, tư tưởng và tổ chức cho sự ra đời của Đảng.","Đường Kách mệnh|chính trị, tư tưởng và tổ chức",33)
concept("youth1925",2,"Hội Thanh niên — 1925","Nguyễn Ái Quốc thành lập Hội Việt Nam Cách mạng Thanh niên vào tháng 6/1925, một bước chuẩn bị tổ chức cho sự ra đời của Đảng.","Hội Việt Nam Cách mạng Thanh niên|6/1925",32)
concept("ban-an",2,"Bản án chế độ thực dân Pháp","Bản án chế độ thực dân Pháp phân tích, tố cáo bản chất và thủ đoạn của chủ nghĩa thực dân Pháp.","Bản án chế độ thực dân Pháp|bản chất|thủ đoạn",32)
concept("vietminh",5,"Việt Minh — 1941","Mặt trận Việt Minh được thành lập ngày 19/5/1941. Không nhầm với Hội Thanh niên năm 1925 hoặc Mặt trận Tổ quốc Việt Nam năm 1955.","Việt Minh|19/5/1941",35)
concept("army1944",2,"Đội tuyên truyền — 1944","Ngày 22/12/1944 thành lập Đội Việt Nam Tuyên truyền Giải phóng quân, tiền thân của Quân đội nhân dân Việt Nam.","22/12/1944|Đội Việt Nam Tuyên truyền Giải phóng quân",35)
concept("independence1966",3,"Độc lập, tự do — 1966","Hồ Chí Minh nêu lời khẳng định Không có gì quý hơn độc lập, tự do ngày 17/7/1966.","17/7/1966|Không có gì quý hơn độc lập, tự do",42)
concept("value",2,"Giá trị tư tưởng","Tư tưởng Hồ Chí Minh đưa cách mạng giải phóng dân tộc đến thắng lợi, là nền tảng và kim chỉ nam; góp phần mở con đường giải phóng thuộc địa, đấu tranh vì độc lập, hòa bình và tiến bộ.","giải phóng dân tộc|nền tảng|tiến bộ xã hội",38)
concept("chinh-cuong",2,"Chánh cương vắn tắt","Chánh cương vắn tắt nêu chủ trương làm tư sản dân quyền cách mạng và thổ địa cách mạng để đi tới xã hội cộng sản.","Chánh cương vắn tắt|tư sản dân quyền|thổ địa cách mạng",33)
concept("declaration",3,"Tuyên ngôn Độc lập","Tuyên ngôn Độc lập khẳng định quyền bình đẳng, sống, sung sướng, tự do của các dân tộc và quyết tâm đem tinh thần, lực lượng, tính mạng, của cải giữ vững độc lập.","Tuyên ngôn Độc lập|các dân tộc|giữ vững độc lập",42)
concept("tax1908",2,"Chống thuế — 1908","Nguyễn Tất Thành tham gia phong trào chống thuế ở Thừa Thiên, Trung Kỳ năm 1908; đề mẫu hỏi cụ thể tháng 5/1908.","chống thuế|1908|Thừa Thiên",29)
concept("invasion",2,"Pháp xâm lược — 1858","Thực dân Pháp nổ súng xâm lược Việt Nam ngày 1/9/1858.","1/9/1858|Pháp xâm lược",18)
concept("patenotre",2,"Hiệp ước Pa-tơ-nốt","Hiệp ước Pa-tơ-nốt năm 1884 đánh dấu triều Nguyễn thừa nhận sự thống trị của thực dân Pháp trên toàn Việt Nam.","Pa-tơ-nốt|1884",18)
concept("dong-du",2,"Đông Du và Cần Vương","Đông Du do Phan Bội Châu khởi xướng, đưa thanh niên sang Nhật Bản. Cần Vương thuộc khuynh hướng phong kiến, thường do các sĩ phu, văn thân lãnh đạo.","Đông Du|Phan Bội Châu|Nhật Bản",19)
concept("nghia-thuc",2,"Đông Kinh Nghĩa Thục","Đông Kinh Nghĩa Thục gắn với Lương Văn Can và Nguyễn Quyền, khác phong trào Đông Du của Phan Bội Châu.","Đông Kinh Nghĩa Thục|Lương Văn Can|Nguyễn Quyền",6,source="summary")
concept("colonial",2,"Chính sách thuộc địa","Thực dân Pháp thực hiện chia để trị về chính trị, duy trì các tệ nạn như rượu và thuốc phiện để đầu độc nhân dân.","chia để trị|chính trị|rượu và thuốc phiện",18)
concept("classes",2,"Giai cấp và mâu thuẫn","Xã hội thuộc địa có năm giai cấp: địa chủ, nông dân, công nhân, tư sản, tiểu tư sản. Có hai mâu thuẫn cơ bản: dân tộc với thực dân Pháp và nông dân với địa chủ phong kiến.","5 giai cấp|2 mâu thuẫn|công nhân, tư sản, tiểu tư sản",19)
concept("world-contradictions",2,"Mâu thuẫn thời đế quốc","Những mâu thuẫn cơ bản gồm tư sản–vô sản, đế quốc–các dân tộc thuộc địa và giữa các nước đế quốc. Mâu thuẫn giữa các dân tộc thuộc địa với nhau không nằm trong nhóm này.","tư sản–vô sản|đế quốc–thuộc địa|giữa các nước đế quốc",21)
concept("comintern",2,"Quốc tế Cộng sản — 1919","Quốc tế Cộng sản (Quốc tế III) ra đời tháng 3/1919, khác mốc Cách mạng Tháng Mười Nga năm 1917.","Quốc tế Cộng sản|3/1919",21)
concept("october",2,"Cách mạng Tháng Mười — 1917","Cách mạng Tháng Mười Nga thành công năm 1917, mở ra thời đại mới và có ảnh hưởng đến con đường cách mạng Hồ Chí Minh lựa chọn.","Tháng Mười Nga|1917",21)
concept("lao-tu",2,"Lão Tử và Đạo giáo","Đạo giáo (Lão giáo) gắn với Lão Tử; không nhầm với Khổng Tử của Nho giáo.","Đạo giáo|Lão Tử",24)
concept("lenin-core",2,"Chủ nghĩa Lênin làm cốt","Trong Đường Kách mệnh, Hồ Chí Minh khẳng định chủ nghĩa chân chính nhất, chắc chắn nhất, cách mệnh nhất là chủ nghĩa Lênin.","chân chính nhất|chắc chắn nhất|chủ nghĩa Lênin",83)
concept("departure",2,"Ra đi — 5/6/1911","Ngày 5/6/1911, Nguyễn Tất Thành ra đi tìm đường cứu nước từ bến Nhà Rồng; đây là mốc mở đầu hành trình tìm con đường mới.","5/6/1911|Nhà Rồng",29)
concept("le-paria",2,"Le Paria — 1922","Nguyễn Ái Quốc tham gia sáng lập báo Le Paria (Người cùng khổ) năm 1922.","Le Paria|1922",32)
concept("socialist-party",2,"Đảng Xã hội Pháp — 1919","Nguyễn Ái Quốc gia nhập Đảng Xã hội Pháp năm 1919; tháng 12/1920 tham gia sáng lập Đảng Cộng sản Pháp.","Đảng Xã hội Pháp|1919|Đảng Cộng sản Pháp",30)
concept("tours",2,"Bước ngoặt tại Đại hội Tua","Tháng 12/1920, Nguyễn Ái Quốc bỏ phiếu tán thành Quốc tế Cộng sản, tham gia sáng lập Đảng Cộng sản Pháp, trở thành người cộng sản Việt Nam đầu tiên.","12/1920|Đại hội Tua|người cộng sản",31)
concept("letter1938",2,"Thư Quốc tế Cộng sản — 1938","Năm 1938, Hồ Chí Minh gửi thư cho Quốc tế Cộng sản, bày tỏ mong muốn thoát khỏi tình trạng không hoạt động, ở bên ngoài Đảng.","1938|thư Quốc tế Cộng sản",34)
concept("return1941",2,"Trở về nước — 1941","Hồ Chí Minh trở về nước trực tiếp lãnh đạo cách mạng cuối tháng 1/1941; tháng 5/1941 chủ trì Hội nghị Trung ương VIII.","1/1941|trở về nước",35)
concept("death-sentence",2,"Tòa án Vinh — 1929","Nguyễn Ái Quốc bị tòa án Vinh xử vắng mặt và kết án tử hình tháng 10/1929; đề mẫu chỉ hỏi năm 1929.","tòa án Vinh|1929",6,source="bonus")
concept("lenin-colonies",2,"Lênin và cách mạng thuộc địa","Hồ Chí Minh đánh giá V.I. Lênin là người đầu tiên đặt cơ sở cho một thời đại mới, thật sự cách mạng trong các nước thuộc địa.","Lênin|thời đại mới|các nước thuộc địa",21)
concept("pac-bo",2,"Tài liệu huấn luyện ở Pác Bó","Ở Pác Bó, Hồ Chí Minh dịch Lịch sử Đảng Cộng sản Nga làm tài liệu huấn luyện cán bộ.","Pác Bó|Lịch sử Đảng Cộng sản Nga",8,source="bonus")
concept("truong-son",2,"Quyết tâm độc lập — 7/1945","Câu Dù phải đốt cháy dãy Trường Sơn cũng phải giành cho được độc lập gắn với tháng 7/1945.","Trường Sơn|7/1945",10,source="bonus",confusion="Không nhầm với Lời kêu gọi toàn quốc kháng chiến năm 1946.")

concept("independence",3,"Bốn nội dung độc lập dân tộc","Độc lập là quyền thiêng liêng; phải gắn với tự do, hạnh phúc nhân dân; phải thật sự, hoàn toàn, triệt để; gắn với thống nhất và toàn vẹn lãnh thổ.","quyền thiêng liêng|tự do, hạnh phúc|toàn vẹn lãnh thổ",42,core=True)
concept("liberation",3,"Năm luận điểm giải phóng dân tộc","Giải phóng dân tộc đi theo con đường vô sản, do Đảng lãnh đạo, dựa vào đại đoàn kết lấy công–nông làm nền tảng; chủ động sáng tạo và có thể thắng trước chính quốc; dùng bạo lực cách mạng.","5 luận điểm|chủ động sáng tạo|bạo lực cách mạng",46,core=True)
concept("socialism",3,"Bốn đặc trưng CNXH","Bốn đặc trưng được trình bày theo chính trị; kinh tế; văn hóa, đạo đức và các quan hệ xã hội; chủ thể xây dựng CNXH. Nhân dân là chủ thể dưới sự lãnh đạo của Đảng.","4 đặc trưng|chính trị|chủ thể xây dựng",57,core=True)
concept("economy",3,"Kinh tế xã hội chủ nghĩa","Kinh tế phát triển cao dựa trên lực lượng sản xuất hiện đại và chế độ công hữu về tư liệu sản xuất chủ yếu.","lực lượng sản xuất hiện đại|công hữu|tư liệu sản xuất chủ yếu",58)
concept("transition",3,"Tính chất và đặc điểm quá độ","Quá độ là quá trình cải biến sâu sắc, phức tạp, lâu dài, khó khăn. Đặc điểm lớn nhất ở Việt Nam là từ nước nông nghiệp lạc hậu tiến lên CNXH, không trải qua giai đoạn phát triển tư bản chủ nghĩa.","nông nghiệp lạc hậu|không trải qua|phức tạp, lâu dài",64,core=True)
concept("transition-tasks",3,"Nhiệm vụ và nguyên tắc quá độ","Nhiệm vụ cải tạo, xây dựng trên các lĩnh vực chính trị, kinh tế, văn hóa và quan hệ xã hội. Nguyên tắc gồm nền tảng Mác–Lênin, giữ độc lập dân tộc, học tập kinh nghiệm và xây đi đôi với chống.","chính trị, kinh tế, văn hóa|giữ độc lập dân tộc|xây đi đôi với chống",66,core=True)
concept("human-motivation",3,"Động lực quyết định — con người","Con người là động lực quyết định nhất của CNXH; xây dựng phải phát huy sức dân và các nguồn lực sẵn có trong nhân dân.","con người|động lực quyết định|sức dân",61,core=True)
concept("violence",3,"Hai hình thức bạo lực cách mạng","Bạo lực cách mạng gồm đấu tranh chính trị và đấu tranh vũ trang, kết hợp phù hợp hoàn cảnh; dùng bạo lực cách mạng chống bạo lực phản cách mạng.","đấu tranh chính trị|đấu tranh vũ trang|phản cách mạng",53,confusion="Bạo lực cách mạng không đồng nghĩa chỉ dùng bạo động hoặc chỉ đấu tranh quân sự.")
concept("marx-violence",3,"Mác — bạo lực là bà đỡ","C. Mác nêu luận điểm bạo lực là bà đỡ của một xã hội cũ đang thai nghén một xã hội mới; Hồ Chí Minh vận dụng quan điểm bạo lực cách mạng vào thực tiễn.","C. Mác|bạo lực|bà đỡ",52)
concept("france1946",3,"Hiệp định Sơ bộ — quốc gia tự do","Trong Hiệp định Sơ bộ ngày 6/3/1946, Chính phủ Pháp công nhận Việt Nam Dân chủ Cộng hòa là một quốc gia tự do có chính phủ, nghị viện, quân đội và tài chính riêng.","quốc gia tự do|Pháp|6/3/1946",45,confusion="Đây là cách hỏi về quốc gia tự do trong Hiệp định Sơ bộ, không đồng nhất với công nhận ngoại giao sau này.")
concept("industrialization",3,"Công nghiệp hóa từ điều kiện thực tế","Công nghiệp hóa cần dựa trên xây dựng, phát triển nền nông nghiệp toàn diện, đồng thời phát triển công nghiệp nhẹ, tiểu thủ công nghiệp; không máy móc bắt đầu bằng công nghiệp nặng.","nông nghiệp toàn diện|công nghiệp nhẹ|không máy móc",67)
concept("van-phuc",3,"Lời kêu gọi — Vạn Phúc","Hồ Chí Minh viết Lời kêu gọi toàn quốc kháng chiến tại làng Vạn Phúc, Hà Đông, tháng 12/1946.","Lời kêu gọi toàn quốc kháng chiến|Vạn Phúc|1946",14,source="bonus")
concept("national-first",3,"Giải phóng dân tộc lên hàng đầu","Đặt quyền lợi dân tộc giải phóng lên trên hết đòi hỏi đoàn kết đánh đổ đế quốc và Việt gian bán nước, cứu giống nòi ra khỏi nước sôi lửa bỏng.","quyền lợi dân tộc giải phóng|đế quốc và Việt gian|đoàn kết",35)

concept("party-role",4,"Vai trò lãnh đạo của Đảng","Đảng giác ngộ, tổ chức, tập hợp dân chúng và liên lạc với các dân tộc bị áp bức, vô sản thế giới; Đảng có vững thì cách mạng mới thành công.","Đảng có vững|giác ngộ|tổ chức dân chúng",76,core=True)
concept("party-birth",4,"Ba yếu tố ra đời Đảng","Đảng Cộng sản Việt Nam ra đời từ sự kết hợp chủ nghĩa Mác–Lênin với phong trào công nhân và phong trào yêu nước.","Mác–Lênin|phong trào công nhân|phong trào yêu nước",78,core=True)
concept("party-founder",2,"Nguyễn Ái Quốc sáng lập Đảng","Người sáng lập Đảng Cộng sản Việt Nam là Hồ Chí Minh; ở thời điểm thành lập Đảng năm 1930, Người hoạt động với tên Nguyễn Ái Quốc, phù hợp nhất với cách hỏi trong ngân hàng.","Nguyễn Ái Quốc|sáng lập Đảng|1930",33,confusion="Các tên khác cũng chỉ cùng một người; câu hỏi đúng nhất gắn với tên được sử dụng trong sự kiện thành lập Đảng.")
concept("party-principles",4,"Nguyên tắc xây dựng Đảng","Các nguyên tắc nhấn mạnh nền tảng Mác–Lênin, tập trung dân chủ, tự phê bình và phê bình, kỷ luật nghiêm minh tự giác, đoàn kết thống nhất và gắn bó với nhân dân.","tập trung dân chủ|tự phê bình|kỷ luật nghiêm minh",83,core=True)
concept("party-foundation",4,"Đảng phải có chủ nghĩa làm cốt","Hình ảnh tàu không có bàn chỉ nam nói về Đảng thiếu nền tảng tư tưởng. Đảng phải lấy chủ nghĩa Mác–Lênin làm cốt và kim chỉ nam.","chủ nghĩa làm cốt|bàn chỉ nam|nền tảng tư tưởng",83)
concept("party-renewal",4,"Chỉnh đốn, đổi mới Đảng","Đảng phải thường xuyên tự chỉnh đốn, đổi mới cả về tư tưởng, chính trị và tổ chức, gắn với nâng cao năng lực lãnh đạo và đạo đức.","tư tưởng|chính trị|tổ chức",86)
concept("party-civilized",4,"Đảng là đạo đức, là văn minh","Quan điểm Đảng ta là đạo đức, là văn minh được nêu trong bài nói kỷ niệm 30 năm thành lập Đảng, năm 1960.","đạo đức, văn minh|30 năm|1960",79)
concept("three-relations",4,"Ba quan hệ đạo đức","Đạo đức được xem xét trong ba quan hệ: đối với mình, đối với người và đối với việc.","đối với mình|đối với người|đối với việc",80)
concept("cadres",4,"Yêu cầu cán bộ, đảng viên","Cán bộ, đảng viên phải trung thành với Đảng; rèn luyện đạo đức; có trách nhiệm, năng động, sáng tạo và học tập nâng cao trình độ. Làm giàu không phải yêu cầu được liệt kê ở đây.","trung thành|rèn luyện đạo đức|trách nhiệm",88)
concept("democracy",4,"Nhà nước của dân, do dân, vì dân","Của dân nói về quyền lực thuộc nhân dân; do dân nói về nhân dân tạo lập, tham gia quản lý và đóng góp; vì dân nói về phục vụ lợi ích, nguyện vọng nhân dân, không đặc quyền đặc lợi.","của dân|do dân|vì dân",93,core=True,confusion="Quyền lực → của dân; tạo lập, quản lý → do dân; phục vụ lợi ích → vì dân.")
concept("state-class",4,"Bản chất giai cấp công nhân","Bản chất giai cấp công nhân thể hiện ở sự lãnh đạo của Đảng, định hướng xã hội chủ nghĩa và nguyên tắc tập trung dân chủ; không chọn tam quyền phân lập trong câu hỏi này.","Đảng lãnh đạo|định hướng XHCN|tập trung dân chủ",91)
concept("law",4,"Pháp quyền nhân nghĩa","Nhà nước pháp quyền nhân nghĩa thượng tôn pháp luật, đồng thời tôn trọng và bảo vệ quyền con người; pháp luật mang tính nhân văn, khuyến thiện.","pháp quyền nhân nghĩa|con người|thượng tôn pháp luật",96,core=True)
concept("constitutional",4,"Hợp hiến, hợp pháp","Nhà nước hợp hiến, hợp pháp được xây dựng từ tổng tuyển cử, dân bầu và hiến pháp dân chủ theo ý nguyện nhân dân.","tổng tuyển cử|hiến pháp dân chủ|hợp hiến, hợp pháp",96)
concept("clean-state",4,"Nhà nước trong sạch, vững mạnh","Xây dựng Nhà nước trong sạch, vững mạnh gắn với phòng chống tiêu cực: đặc quyền, đặc lợi; tham ô, lãng phí, quan liêu; tư túng, chia rẽ, kiêu ngạo.","phòng chống tiêu cực|tham ô, lãng phí, quan liêu|đặc quyền, đặc lợi",99,core=True)
concept("internal-enemy",4,"Giặc nội xâm","Tham ô, lãng phí, quan liêu là giặc nội xâm, gây hại từ bên trong và cần chống kiên quyết.","giặc nội xâm|tham ô, lãng phí, quan liêu",100)
concept("centralism",4,"Tập trung dân chủ xuyên suốt","Tập trung dân chủ là nguyên tắc cơ bản, xuyên suốt, bao trùm quá trình tồn tại và phát triển của Đảng; tập trung trên nền dân chủ, dân chủ dưới sự chỉ đạo tập trung.","tập trung dân chủ|cơ bản, xuyên suốt",84)
concept("four-liberations",4,"Mục tiêu giải phóng","Mục đích hoạt động của Đảng gồm giải phóng dân tộc, giải phóng xã hội, giải phóng giai cấp và giải phóng con người.","dân tộc|giai cấp|con người",79)

concept("unity-role",5,"Đại đoàn kết có ý nghĩa chiến lược","Đại đoàn kết toàn dân tộc là vấn đề có ý nghĩa chiến lược, quyết định thành công của cách mạng, không phải thủ đoạn nhất thời.","ý nghĩa chiến lược|quyết định thành công",108,core=True)
concept("unity-conditions",5,"Ba điều kiện đoàn kết","Ba điều kiện được trình bày là kế thừa truyền thống yêu nước, nhân nghĩa, đoàn kết; có lòng khoan dung, độ lượng; có niềm tin vào nhân dân.","truyền thống|khoan dung, độ lượng|niềm tin vào nhân dân",114,core=True)
concept("front",5,"Mặt trận dân tộc thống nhất","Mặt trận dân tộc thống nhất quy tụ các tổ chức và cá nhân yêu nước trong và ngoài nước, là hình thức tổ chức khối đại đoàn kết; Đảng vừa là thành viên vừa lãnh đạo Mặt trận.","Mặt trận dân tộc thống nhất|quy tụ|vừa thành viên vừa lãnh đạo",116,core=True)
concept("unity-methods",5,"Phương thức xây dựng đoàn kết","Cần làm tốt dân vận; tổ chức đoàn thể phù hợp từng đối tượng; tập hợp, đoàn kết các đoàn thể trong Mặt trận dân tộc thống nhất.","dân vận|đoàn thể|Mặt trận",120,core=True)
concept("international-role",5,"Dân tộc kết hợp thời đại","Đoàn kết quốc tế nhằm kết hợp sức mạnh dân tộc với sức mạnh thời đại, tạo sức mạnh tổng hợp cho cách mạng.","sức mạnh dân tộc|sức mạnh thời đại|sức mạnh tổng hợp",122,core=True)
concept("international-forces",5,"Ba lực lượng đoàn kết quốc tế","Lực lượng gồm phong trào cộng sản và công nhân quốc tế; phong trào giải phóng dân tộc; các lực lượng tiến bộ, yêu chuộng hòa bình, dân chủ, tự do và công lý.","cộng sản và công nhân|giải phóng dân tộc|lực lượng tiến bộ",126)
concept("international-principles",5,"Hai nguyên tắc đoàn kết quốc tế","Đoàn kết trên cơ sở thống nhất mục tiêu, lợi ích, có lý có tình; đồng thời giữ độc lập, tự chủ.","thống nhất mục tiêu|có lý, có tình|độc lập, tự chủ",130,core=True)
concept("front1955",5,"Mặt trận Tổ quốc — 1955","Mặt trận Tổ quốc Việt Nam thành lập năm 1955; Mặt trận Việt Minh là năm 1941.","Mặt trận Tổ quốc|1955",117)
concept("lenin-slogan",5,"Lênin và đoàn kết dân tộc bị áp bức","V.I. Lênin phát triển khẩu hiệu đoàn kết giai cấp vô sản bằng việc bổ sung các dân tộc bị áp bức.","Lênin|các dân tộc bị áp bức|đoàn kết",123)

concept("culture1943",6,"Quan niệm văn hóa — 1943","Năm 1943, trong Nhật ký trong tù, Hồ Chí Minh nêu quan niệm văn hóa từ nhu cầu sinh tồn và mục đích cuộc sống.","1943|Nhật ký trong tù|văn hóa",139)
concept("culture-politics",6,"Văn hóa ở trong chính trị","Văn hóa không đứng ngoài mà ở trong chính trị, phục vụ nhiệm vụ chính trị và tham gia đời sống cách mạng.","văn hóa ở trong chính trị",140,core=True)
concept("culture-economy",6,"Văn hóa và kinh tế","Kinh tế là nền tảng, tạo điều kiện xây dựng văn hóa; văn hóa có tác động tích cực trở lại kinh tế, không hoàn toàn phụ thuộc hay tách rời.","tác động tích cực trở lại|kinh tế",141,core=True)
concept("culture-society",6,"Xã hội thế nào, văn hóa thế ấy","Giữa văn hóa và xã hội có quan hệ gắn bó: xã hội thế nào thì văn hóa thế ấy, giải phóng xã hội mở đường cho phát triển văn hóa.","xã hội thế nào|văn hóa thế ấy",141)
concept("identity",6,"Nội dung và hình thức bản sắc","Nội dung bản sắc gồm lòng yêu nước, tinh thần độc lập, tự cường, tự tôn dân tộc. Hình thức biểu hiện qua ngôn ngữ, phong tục, tập quán và lễ hội truyền thống.","nội dung|hình thức|ngôn ngữ, phong tục",142)
concept("culture-role",6,"Ba vai trò văn hóa","Văn hóa là mục tiêu, động lực của cách mạng; là một mặt trận; phục vụ quần chúng nhân dân.","mục tiêu, động lực|một mặt trận|phục vụ quần chúng",144,core=True)
concept("ethics-standards",6,"Bốn chuẩn mực đạo đức","Chuẩn mực gồm trung với nước, hiếu với dân; cần, kiệm, liêm, chính, chí công vô tư; thương yêu con người, sống có tình nghĩa; tinh thần quốc tế trong sáng.","trung với nước, hiếu với dân|cần, kiệm, liêm, chính|tinh thần quốc tế",151,core=True,confusion="Chuẩn mực là phẩm chất cần có; nguyên tắc là cách xây dựng và rèn luyện đạo đức.")
concept("ethics-principles",6,"Ba nguyên tắc xây dựng đạo đức","Ba nguyên tắc là nói đi đôi với làm, nêu gương đạo đức; xây đi đôi với chống; tu dưỡng đạo đức suốt đời.","nói đi đôi với làm|xây đi đôi với chống|tu dưỡng suốt đời",155,core=True)
concept("lifelong",6,"Tu dưỡng đạo đức suốt đời","Hình ảnh ngọc càng mài càng sáng, vàng càng luyện càng trong nhấn mạnh đạo đức được rèn luyện bền bỉ hàng ngày và tu dưỡng suốt đời.","ngọc càng mài|vàng càng luyện|suốt đời",157)
concept("human-role",6,"Con người vừa mục tiêu vừa động lực","Con người vừa là mục tiêu vừa là động lực của cách mạng; khi ngân hàng chỉ đưa một vế đúng thì chọn vế đó, khi hỏi đầy đủ phải nhớ cả hai.","con người|mục tiêu|động lực",159,core=True)
concept("education",6,"Vai trò giáo dục con người","Câu Hiền, dữ đâu phải là tính sẵn; phần nhiều do giáo dục mà nên nhấn mạnh vai trò của giáo dục trong xây dựng con người.","giáo dục|xây dựng con người",163)
concept("early-ethics",6,"Đạo đức trong Đường Kách mệnh","Đường Kách mệnh năm 1927 đặt vấn đề tư cách người cách mệnh, là tác phẩm sớm nêu nội dung đạo đức cách mạng.","Đường Kách mệnh|1927|tư cách người cách mệnh",147)
concept("young-generation",6,"Thế hệ vừa hồng vừa chuyên","Di chúc yêu cầu chăm lo giáo dục đạo đức cách mạng cho đoàn viên, thanh niên, đào tạo người thừa kế xây dựng CNXH vừa hồng vừa chuyên.","đoàn viên, thanh niên|vừa hồng vừa chuyên",149)

# Exact PDF pages, checked against extracted sections rather than the printed TOC.
page_corrections={
    "method":12,"phase4":34,"leech":51,"lenin-theses":31,"duong-kach-menh":32,
    "independence1966":43,"departure":30,"economy":57,"transition":65,
    "party-role":77,"party-principles":84,"party-civilized":80,"three-relations":148,
    "law":99,"clean-state":101,"internal-enemy":101,"unity-conditions":113,
    "international-role":123,"culture1943":141,"culture-politics":142,"culture-society":142,
}
for key,page in page_corrections.items():concepts[key]["references"][0]["pdfPage"]=page
for key,page in {"phases":30,"phase1":30,"phase2":30,"phase3":31,"phase4":33,"versailles":31,"army1944":35,"return1941":34,"letter1938":34}.items():
    concepts[key]["references"][0].update(sourceId="textbook",pdfPage=page)
concepts["nghia-thuc"]["references"][0].update(sourceId="quiz",pdfPage=2)
concepts["industrialization"]["references"][0].update(sourceId="bonus",pdfPage=26)
for key,page in {"party-principles":85,"three-relations":147,"classes":20,"transition-tasks":69,"early-ethics":148}.items():
    concepts[key]["references"].append({"sourceId":"ptit","pdfPage":page,"section":concepts[key]["title"],"evidence":concepts[key]["summary"]})

def review(source, group, number, key, answer="a", tags="", explanation="", *, note="", prompt=None, options=None, fixed=False, pending="", disputed=False):
    ident = f"{source}-g{group}-{number:02d}"
    assert ident in BY_ID, ident
    reviews[ident] = {"concept": key, "answer": answer, "tags": tags.split() if tags else [],
                      "explanation": explanation, "note": note, "prompt": prompt, "options": options,
                      "fixed": fixed, "pending": pending, "disputed": disputed}

# Every LMS item receives an explicit editorial decision.
for n,key in enumerate(["congress2","eulogy","congress4","congress5","congress6","definition","meaning","definition","meaning","method"],1):
    review("lms",1,n,key,tags="congress" if n in [1,3,4,5] else "date" if n==2 else "")
keys=["practical","theoretical","eastern","confucius","jesus","buddhism","marx-method","marx-method","tam-dan","subjective","phase2","phase3","phase4","leech","versailles","lenin-theses","phase4","phase2","vo-san","duong-kach-menh","youth1925","ban-an","vietminh","army1944","independence1966","value","value","chinh-cuong","declaration","tax1908"]
for n,key in enumerate(keys,1):
    review("lms",2,n,key,tags="date" if n in [11,12,13,15,17,18,21,23,24,25,30] else "")
review("lms",2,14,"leech",prompt="Hồ Chí Minh đã dùng hình tượng nào dưới đây để chỉ chủ nghĩa tư bản?",note="Bổ sung từ 'chỉ' bị thiếu trong đề gốc; không thay đổi kiến thức hỏi.")
review("lms",2,27,"value",explanation="Câu hỏi yêu cầu chọn nội dung không thuộc nhóm giá trị được trình bày. Phương án trực tiếp chỉ đạo cách mạng XHCN giành nhiều thành tựu không phải cách diễn đạt của nhóm giá trị này.")
review("lms",2,28,"chinh-cuong",note="Giữ tên Chính cương vắn tắt theo ngân hàng; tài liệu lý luận cũng dùng cách viết Chánh cương vắn tắt.")
keys=["independence","socialism","vo-san","declaration","violence","socialism","economy","socialism","transition","transition","transition-tasks","transition-tasks","transition-tasks","transition-tasks","human-motivation"]
for n,key in enumerate(keys,1):review("lms",3,n,key,tags="count" if n==2 else "")
review("lms",3,1,"independence",explanation="Mở rộng quan hệ đối ngoại không phải một trong bốn nội dung về độc lập dân tộc đang hỏi. Nhớ bốn ý: quyền thiêng liêng; tự do, hạnh phúc; độc lập thật sự; thống nhất và toàn vẹn lãnh thổ.")
review("lms",3,5,"violence",explanation="Điểm sai là chỉ nói bạo động cách mạng. Bạo lực cách mạng rộng hơn, kết hợp đấu tranh chính trị với đấu tranh vũ trang.")
keys=["party-role","party-principles","front","party-principles","party-foundation","party-renewal","party-principles","party-civilized","three-relations","cadres","democracy","state-class","democracy","democracy","law","clean-state","constitutional","clean-state","clean-state","internal-enemy"]
for n,key in enumerate(keys,1):review("lms",4,n,key)
review("lms",4,8,"party-civilized",tags="count")
review("lms",4,7,"party-principles",explanation="Số lượng đảng viên đông không phải nguyên tắc xây dựng Đảng. Nguyên tắc nhấn mạnh chất lượng tổ chức như tập trung dân chủ, kỷ luật và tự phê bình.")
review("lms",4,10,"cadres",explanation="Phải biết cách làm giàu không thuộc nhóm yêu cầu cán bộ, đảng viên được hỏi. Các yêu cầu chính là trung thành, đạo đức, trách nhiệm và năng lực.")
review("lms",4,11,"democracy",explanation="Bảo vệ lợi ích giai cấp tư sản không thuộc quan điểm về nhà nước dân chủ ở đây. Nhà nước phải của dân, do dân và vì dân.")
review("lms",4,12,"state-class",explanation="Tam quyền phân lập không thuộc ba biểu hiện bản chất giai cấp công nhân của Nhà nước được trình bày. Nguyên tắc tổ chức và hoạt động là tập trung dân chủ.")
keys=["unity-role","unity-conditions","unity-conditions","front","front","vietminh","unity-methods","international-role","international-forces","international-principles"]
for n,key in enumerate(keys,1):review("lms",5,n,key,tags="date" if n==6 else "")
review("lms",5,2,"unity-conditions",explanation="Đại đoàn kết không đòi mọi người cùng trình độ, nhận thức. Điều kiện cần nhớ là truyền thống yêu nước, lòng khoan dung và niềm tin vào nhân dân.")
review("lms",5,7,"unity-methods",explanation="Thường xuyên tổ chức các hoạt động không phải tên một trong ba phương thức được liệt kê. Nhớ dân vận, xây đoàn thể và tập hợp trong Mặt trận.")
review("lms",5,9,"international-forces",explanation="Phong trào không liên kết không thuộc ba nhóm lực lượng được liệt kê trong nội dung này: cộng sản–công nhân, giải phóng dân tộc, lực lượng tiến bộ yêu hòa bình.")
keys=["culture1943","culture-politics","culture-economy","culture-society","identity","identity","culture-role","ethics-standards","ethics-principles","human-role"]
for n,key in enumerate(keys,1):review("lms",6,n,key,tags="date" if n==1 else "")
review("lms",6,7,"culture-role",pending="Đánh dấu A trong nguồn mâu thuẫn với giáo trình trang in 115 (PDF 117) và slide chương 6 trang 12: văn hóa là mục tiêu, động lực là một vai trò. Chưa dùng câu này để chấm.",disputed=True)
review("lms",6,8,"ethics-standards",explanation="Sống hài hòa, đảm bảo lợi ích của nhân dân không phải tên một trong bốn chuẩn mực đạo đức được liệt kê. Đừng nhầm chuẩn mực với một diễn đạt tốt nhưng không thuộc danh mục đang hỏi.")

# Quiz decisions: answer letters refer to the source PDF, never UI position.
for n,key,ans,tags in [(7,"theoretical","d",""),(8,"congress5","c","congress"),(9,"definition","d",""),(10,"meaning","b",""),(11,"congress11","b","congress")]:review("quiz",1,n,key,ans,tags)
review("quiz",1,6,"value-definition",prompt="Điền từ còn thiếu: Tư tưởng Hồ Chí Minh là tài sản ... vô cùng to lớn và quý giá của Đảng và dân tộc ta.",options=["Tinh thần","Vật chất","Kinh tế","Quân sự"])
for n,key,ans,tags in [(1,"invasion","d","date"),(2,"patenotre","b",""),(4,"nghia-thuc","c",""),(6,"colonial","a",""),(7,"colonial","c",""),(8,"classes","a","count"),(9,"classes","a","count")]:review("quiz",2,n,key,ans,tags)
review("quiz",2,3,"dong-du",prompt="Phong trào Đông Du do ai lãnh đạo?",options=["Phan Bội Châu","Phan Châu Trinh","Lương Văn Can","Hoàng Hoa Thám"])
review("quiz",2,5,"dong-du",prompt="Phong trào Đông Du đưa thanh niên Việt Nam sang nước nào du học?",options=["Nhật Bản","Pháp","Trung Quốc","Ấn Độ"])
review("quiz",2,10,"dong-du",prompt="Phong trào Cần Vương là phong trào yêu nước theo khuynh hướng nào?",options=["Phong kiến","Dân chủ tư sản","Vô sản","Xã hội chủ nghĩa"])
for n,key,ans,tags in [(1,"invasion","a","date"),(3,"classes","d",""),(5,"dong-du","c",""),(6,"dong-du","a",""),(8,"world-contradictions","b",""),(9,"comintern","c","date"),(10,"october","c","date"),(12,"theoretical","b",""),(13,"buddhism","d",""),(14,"confucius","b",""),(15,"jesus","d",""),(16,"lao-tu","d","")]:review("quiz",3,n,key,ans,tags)
review("quiz",3,2,"invasion",pending="Câu dùng 'nguyên nhân' nhưng cần phân biệt với cái cớ cấm đạo; chưa có đáp án nguồn đủ rõ để chấm.")
review("quiz",3,4,"classes",pending="Hai phương án A và C có cùng nội dung dân tộc Việt Nam với thực dân Pháp; chưa có đáp án duy nhất.")
review("quiz",3,7,"practical",pending="Cần làm rõ phân biệt nguyên nhân sâu xa giữa giai cấp tư sản non yếu và thiếu đường lối đúng; nguồn không đánh dấu đáp án.")
review("quiz",3,11,"theoretical",pending="Cả bốn lựa chọn đều nêu nguồn thuộc cơ sở lý luận hoặc lặp ý; câu phủ định không có đáp án loại trừ rõ.")
review("quiz",3,17,"buddhism",prompt="Một ảnh hưởng của Phật giáo đến tư tưởng Hồ Chí Minh là đề cao quyền ... của con người và chân lý.",options=["Bình đẳng","Tư hữu","Đặc quyền","Thống trị"])
review("quiz",3,18,"lenin-core",prompt="Điền từ còn thiếu: Bây giờ học thuyết nhiều, chủ nghĩa nhiều, nhưng chủ nghĩa chân chính nhất, cách mạng nhất là...",options=["Chủ nghĩa Lênin","Chủ nghĩa Tam dân","Nho giáo","Lão giáo"])
review("quiz",3,19,"subjective",pending="Các lựa chọn đều có thể mô tả phẩm chất Hồ Chí Minh; chưa xác lập được một phương án sai rõ ràng theo câu nguồn.")
review("quiz",3,20,"subjective",pending="Bài giảng dùng 'khoảng 30 nước', trong khi phương án phân biệt gần/hơn 30; cần xác minh trước khi chấm.")
for n,key,ans,tags in [(1,"phases","b","count"),(2,"phase1","c","date"),(3,"departure","c","date"),(4,"phase2","b","date"),(5,"phase3","b","date"),(6,"vo-san","a",""),(7,"duong-kach-menh","b",""),(8,"youth1925","b","date"),(9,"vo-san","d",""),(10,"party-birth","b",""),(11,"le-paria","c","date"),(12,"socialist-party","b","date"),(13,"versailles","c","date"),(14,"lenin-theses","b","date"),(15,"tours","d",""),(16,"letter1938","c",""),(17,"return1941","b","date"),(18,"vietminh","a","date"),(19,"declaration","d",""),(20,"independence1966","d","date")]:review("quiz",4,n,key,ans,tags)
review("quiz",4,10,"party-founder",answer="b")
review("quiz",4,16,"letter1938",answer="c",tags="date")
for n,key,ans,tags in [(1,"independence","c","count"),(2,"independence","a",""),(4,"versailles","a","date"),(5,"return1941","b","date"),(6,"france1946","b",""),(7,"tam-dan","a",""),(8,"lenin-theses","a","date"),(11,"liberation","c","count"),(12,"marx-violence","a",""),(14,"violence","b","count")]:review("quiz",5,n,key,ans,tags)
review("quiz",5,3,"independence",prompt="Theo Hồ Chí Minh, độc lập dân tộc phải gắn liền tự do, cơm no, áo ấm và hạnh phúc của...",options=["Nhân dân","Riêng cán bộ","Riêng công nhân","Riêng nông dân"])
review("quiz",5,9,"vo-san",prompt="Điền cụm từ: Muốn cứu nước và giải phóng dân tộc không có con đường nào khác là con đường...",options=["Cách mạng vô sản","Cách mạng tư sản","Cần Vương","Đông Du"])
review("quiz",5,10,"violence",prompt="Điền từ: Trong cuộc đấu tranh gian khổ chống kẻ thù giai cấp và kẻ thù dân tộc, cần dùng bạo lực cách mạng chống lại bạo lực ..., giành lấy chính quyền và bảo vệ chính quyền.",options=["Phản cách mạng","Chính trị","Quần chúng","Vũ trang"])
review("quiz",5,13,"violence",prompt="Điền từ: Chế độ thực dân, tự bản thân nó đã là một hành vi ... của kẻ mạnh đối với kẻ yếu rồi.",options=["Bạo lực","Nhân nghĩa","Khoan dung","Bình đẳng"])
for n,key,ans in [(1,"party-role","d"),(2,"party-birth","b"),(3,"party-role","c"),(4,"party-role","a"),(5,"party-principles","a"),(6,"party-foundation","b"),(8,"three-relations","b"),(9,"centralism","c"),(10,"four-liberations","a"),(11,"party-principles","c"),(12,"party-role","a"),(13,"party-principles","c"),(15,"democracy","d"),(16,"democracy","c"),(17,"law","b"),(18,"constitutional","d"),(19,"law","c"),(20,"law","a"),(21,"clean-state","d")]:review("quiz",6,n,key,ans)
review("quiz",6,7,"party-civilized",pending="Phương án A đúng và D ('A đúng, B sai') cũng đúng về cùng sự kiện; giữ lại để biên tập lựa chọn.")
review("quiz",6,14,"cadres",pending="Cả bốn phương án đều thuộc yêu cầu cán bộ, đảng viên; câu hỏi phủ định chưa có đáp án hợp lệ.")
review("quiz",6,5,"party-principles",explanation="Lãnh đạo chính phủ và nhân dân là vai trò, không phải tên một nguyên tắc xây dựng Đảng. Phân biệt vai trò với nguyên tắc tổ chức, sinh hoạt.")
review("quiz",6,8,"three-relations",answer="b",explanation="Ba quan hệ được liệt kê là đối với mình, người và việc; 'đối với tổ chức' không nằm trong danh mục ba quan hệ của câu hỏi.")
review("quiz",6,12,"party-role",explanation="Chống lại giai cấp tư sản không thuộc ba vai trò đang được hỏi: giác ngộ, tổ chức dân chúng và đoàn kết với vô sản, dân tộc bị áp bức.")
review("quiz",6,13,"party-principles",answer="c",explanation="Nêu gương, đi trước không phải tên nguyên tắc xây dựng Đảng trong danh mục đang hỏi. Các lựa chọn còn lại là đoàn kết, kỷ luật và tự phê bình.")
review("quiz",6,15,"democracy",answer="d",explanation="Nhà nước của mọi người dân nói về 'của dân'. 'Do dân' nhấn mạnh nhân dân tạo lập, đóng góp và tham gia quản lý Nhà nước.")
for n,key,ans,tags in [(1,"unity-conditions","a",""),(2,"front","d",""),(3,"vietminh","c","date"),(4,"front1955","d","date"),(5,"international-role","c",""),(6,"international-forces","c",""),(7,"international-principles","d",""),(9,"unity-conditions","c","count"),(10,"international-principles","a","count"),(11,"international-principles","b","")]:review("quiz",7,n,key,ans,tags)
review("quiz",7,6,"international-forces",answer="c",explanation="Phong trào chống lại chủ nghĩa tư bản không phải tên một trong ba nhóm lực lượng được liệt kê. Nhớ cộng sản–công nhân, giải phóng dân tộc và lực lượng tiến bộ yêu hòa bình.")
review("quiz",7,8,"unity-conditions",prompt="Điền từ: Một điều kiện xây dựng đại đoàn kết toàn dân tộc là kế thừa truyền thống yêu nước, nhân nghĩa, đoàn kết của...",options=["Dân tộc","Riêng công nhân","Riêng nông dân","Riêng trí thức"])
for n,key,ans,tags in [(1,"culture1943","d","date"),(2,"culture-society","c",""),(3,"ethics-standards","b",""),(4,"human-role","c",""),(6,"education","b",""),(7,"ethics-standards","d",""),(8,"culture-economy","a",""),(9,"culture-politics","a",""),(11,"ethics-principles","d",""),(12,"lifelong","d",""),(13,"culture-role","b",""),(14,"culture-role","d",""),(15,"human-role","c",""),(16,"culture-society","a","")]:review("quiz",8,n,key,ans,tags)
review("quiz",8,5,"early-ethics",pending="Câu trích 'sông có nguồn, cây có gốc' thuộc Sửa đổi lối làm việc, nhưng tác phẩm này không có trong lựa chọn nguồn; không ép chọn một đáp án sai.")
review("quiz",8,10,"culture-role",pending="Cùng cấu trúc với câu LMS đang có đáp án mâu thuẫn; cần làm rõ lựa chọn 'sự nghiệp của quần chúng' trước khi đưa vào chấm.",disputed=True)
review("quiz",8,3,"ethics-standards",answer="b",explanation="Sống hài hòa, đảm bảo lợi ích của nhân dân không phải tên một trong bốn chuẩn mực đang học. Nhớ trung–hiếu; cần–kiệm–liêm–chính; yêu thương con người; quốc tế trong sáng.")
review("quiz",8,11,"ethics-principles",answer="d",explanation="Ý thức lập thân, lập nghiệp không thuộc ba nguyên tắc xây dựng đạo đức. Ba nguyên tắc là nói–làm/nêu gương, xây–chống và tu dưỡng suốt đời.")
review("quiz",8,14,"culture-role",answer="d",explanation="Văn hóa là tiền đề của cách mạng không phải một trong ba vai trò được trình bày. Ba vai trò là mục tiêu–động lực, mặt trận và phục vụ quần chúng.")

sample=[(3,"congress7","d","congress"),(4,"tax1908","c","date"),(5,"versailles","c","date"),(6,"youth1925","c","date"),(7,"death-sentence","c","date"),(8,"lenin-colonies","c",""),(9,"pac-bo","b",""),(10,"foundation","c",""),(11,"jesus","c",""),(12,"marx-method","d",""),(13,"industrialization","b",""),(14,"human-motivation","b",""),(15,"lenin-slogan","c",""),(16,"front","c",""),(17,"lenin-core","b",""),(18,"early-ethics","b",""),(19,"van-phuc","c",""),(20,"young-generation","c",""),(21,"national-first","c",""),(22,"truong-son","b","date")]
for n,key,ans,tags in sample:review("sample",1,n,key,ans,tags)
review("sample",1,13,"industrialization",answer="b",explanation="Không đúng là máy móc bắt đầu bằng phát triển công nghiệp nặng. Cần xuất phát từ nền nông nghiệp toàn diện và điều kiện thực tế.")

missing=set(BY_ID)-set(reviews)
assert not missing, f"Missing editorial decisions: {missing}"

def normalized(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.replace("đ","d").lower()).encode("ascii","ignore").decode())

published=[]
audit=[]
fingerprints={}
sample_ids=[]
for raw in RAW:
    r=reviews[raw["id"]]
    audit_item={"id":raw["id"],"sourceId":raw["sourceId"],"number":raw["originalNumber"],"chapter":raw["chapter"],"pdfPage":raw["pdfPage"]}
    if r["pending"]:
        audit.append({**audit_item,"status":"disputed" if r["disputed"] else "pending","reason":r["pending"]})
        continue
    c=concepts[r["concept"]]
    options=copy.deepcopy(raw["options"])
    notes=[r["note"]] if r["note"] else []
    if r["options"]:
        options=[{"id":chr(97+i),"text":value} for i,value in enumerate(r["options"])]
        notes.append("Chuyển từ câu trả lời ngắn; bổ sung lựa chọn nhiễu trong phạm vi môn học.")
    # Safe all-of-the-other-three phrasing preserves meaning after shuffling.
    for o in options:
        if re.fullmatch(r"(?:Cả|Tất cả) (?:3|ba|các) (?:đáp án|ý)(?: trên)?(?: đều đúng)?",o["text"],re.I):
            o["text"]="Cả ba phương án còn lại"
            notes.append("Chuẩn hóa phương án tổng hợp để việc đảo vị trí không đổi nghĩa.")
    fixed=r["fixed"] or any(re.search(r"\b[ABCD]\s*(?:đúng|sai)|đáp án trên|ý trên",o["text"],re.I) for o in options)
    source={"sourceId":raw["sourceId"],"pdfPage":raw["pdfPage"],"originalNumber":raw["originalNumber"],"group":f"Nhóm {raw['group']}, chương {raw['chapter']}"}
    q={"id":raw["id"],"revision":1,"chapter":raw["chapter"],"topic":c["title"],"conceptId":c["id"],"tags":r["tags"],
       "prompt":r["prompt"] or raw["prompt"],"options":options,"correctOptionId":r["answer"],"shufflePolicy":"fixed" if fixed else "safe",
       "originType":"converted" if r["options"] else "original","explanation":r["explanation"] or c["summary"],"keywords":c["keywords"],
       "confusionNote":c["confusionNote"],"sources":[source],"theoryReferences":c["references"],"editorialNote":" ".join(dict.fromkeys(notes)),"reviewStatus":"verified"}
    if raw["id"] in ["sample-g1-13","sample-g1-14","sample-g1-15"]:
        number={"sample-g1-13":363,"sample-g1-14":364,"sample-g1-15":366}[raw["id"]]
        q["theoryReferences"]=[*q["theoryReferences"],{"sourceId":"bonus","pdfPage":26,"section":f"Đối chiếu câu {number}","evidence":next(o["text"] for o in options if o["id"]==q["correctOptionId"])}]
    if raw["id"]=="sample-g1-14":q["explanation"]="Biện pháp quan trọng nhất trong câu hỏi này là huy động các nguồn lực sẵn có trong dân, phát huy sức mạnh của nhân dân để xây dựng CNXH."
    assert q["correctOptionId"] in [o["id"] for o in options], raw["id"]
    assert 2<=len(options)<=4, raw["id"]
    fingerprint=normalized(q["prompt"])+"|"+"|".join(sorted(normalized(o["text"]) for o in options))
    # Preserve the full sample, even when it shares a concept with the chapter pool.
    if fingerprint in fingerprints:
        existing=fingerprints[fingerprint]
        correct_text=next(o["text"] for o in options if o["id"]==q["correctOptionId"])
        existing_answer=next(o["text"] for o in existing["options"] if o["id"]==existing["correctOptionId"])
        assert normalized(correct_text)==normalized(existing_answer), (raw["id"],existing["id"])
        existing["sources"].append(source)
        audit.append({**audit_item,"status":"merged","questionId":existing["id"],"reason":"Trùng đề và nội dung lựa chọn sau chuẩn hóa dấu câu; giữ tất cả nguồn."})
        final_id=existing["id"]
    else:
        fingerprints[fingerprint]=q
        published.append(q)
        audit.append({**audit_item,"status":"published","questionId":q["id"],"reason":"Đã gắn đáp án, keyword, lời giải và căn cứ đối chiếu."})
        final_id=q["id"]
    if raw["sourceId"]=="sample":sample_ids.append(final_id)

chapters=[
 {"number":1,"title":"Khái niệm và phương pháp nghiên cứu","shortTitle":"Nhập môn","description":"Hiểu khái niệm, đối tượng và cách tiếp cận môn học.","icon":"book"},
 {"number":2,"title":"Cơ sở hình thành và phát triển","shortTitle":"Cơ sở hình thành","description":"Nguồn gốc tư tưởng và hành trình tìm đường cứu nước.","icon":"leaf"},
 {"number":3,"title":"Độc lập dân tộc và chủ nghĩa xã hội","shortTitle":"Độc lập & CNXH","description":"Nắm con đường cách mạng và mối quan hệ độc lập với CNXH.","icon":"flag"},
 {"number":4,"title":"Đảng và Nhà nước","shortTitle":"Đảng & Nhà nước","description":"Xây dựng Đảng, nhà nước của dân, do dân và vì dân.","icon":"building"},
 {"number":5,"title":"Đại đoàn kết dân tộc và quốc tế","shortTitle":"Đại đoàn kết","description":"Kết hợp sức mạnh dân tộc với sức mạnh thời đại.","icon":"people"},
 {"number":6,"title":"Văn hóa, đạo đức và con người","shortTitle":"Văn hóa & con người","description":"Phân biệt chuẩn mực, nguyên tắc và các vai trò cốt lõi.","icon":"heart"},
]
sources=[
 {"id":"lms","title":"TTHCM LMS.pdf","shortTitle":"Ngân hàng LMS","kind":"bank","pages":20},
 {"id":"quiz","title":"Quiz cô Khánh.pdf","shortTitle":"Quiz cô Khánh","kind":"bank","pages":16},
 {"id":"sample","title":"Đề mẫu 20 câu Thầy Cường.docx.pdf","shortTitle":"Đề mẫu thầy Cường","kind":"bank","pages":5},
 {"id":"textbook","title":"Giáo trình Tư tưởng Hồ Chí Minh - 2019.pdf","shortTitle":"Giáo trình 2019","kind":"theory","pages":144},
 {"id":"ptit","title":"Bài giảng TTHCM PTIT.pdf","shortTitle":"Bài giảng PTIT","kind":"theory","pages":175},
 {"id":"slides","title":"Slide cô Khánh — 6 chương","shortTitle":"Slide cô Khánh","kind":"theory","pages":249},
 {"id":"summary","title":"Tóm tắt TTHCM.docx.pdf","shortTitle":"Tóm tắt TTHCM","kind":"supplement","pages":58},
 {"id":"combined","title":"Tổng hợp TTHCM.pdf","shortTitle":"Tổng hợp TTHCM","kind":"supplement","pages":94},
 {"id":"bonus","title":"Trắc nghiệm mốc TG + Bonus .docx.pdf","shortTitle":"Mốc thời gian + Bonus","kind":"supplement","pages":34},
 {"id":"timeline","title":"Mốc Thời gian + Đại hội.pdf","shortTitle":"Mốc thời gian + Đại hội","kind":"supplement","pages":2},
]
bank={"subjectId":"tthcm","version":"2026.11.13.1","updatedAt":"2026-11-13","chapters":chapters,"concepts":list(concepts.values()),"questions":published,"sources":sources,"sampleQuestionIds":sample_ids,"audit":audit,
      "supplements":[{"sourceId":"combined","status":"Đã khảo sát; chưa nhập toàn bộ vì cần đối chiếu phiên bản kiến thức và bảng đáp án."},{"sourceId":"bonus","status":"Dùng chọn lọc để đối chiếu câu trong đề mẫu; chưa nhập toàn bộ các câu tiểu sử và phần bổ sung."},{"sourceId":"timeline","status":"Đã khảo sát, dùng hỗ trợ rà mốc; chưa chuyển thành bộ câu hỏi mới."}]}
out=ROOT/"src/subjects/tthcm";out.mkdir(parents=True,exist_ok=True)
(out/"bank.json").write_text(json.dumps(bank,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT/"content/tthcm/editorial-decisions.json").write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["# Báo cáo nội dung","","Ngân hàng chính gồm 233 mục nguồn; số câu xuất bản chỉ tính các câu chuẩn duy nhất.","","| Nguồn | Tổng mục | Xuất bản | Gộp | Chờ kiểm tra / mâu thuẫn |","| --- | ---: | ---: | ---: | ---: |"]
for source in ["lms","quiz","sample"]:
    entries=[a for a in audit if a["sourceId"]==source]
    lines.append(f"| {source} | {len(entries)} | {sum(a['status']=='published' for a in entries)} | {sum(a['status']=='merged' for a in entries)} | {sum(a['status'] in ['pending','disputed'] for a in entries)} |")
lines += ["",f"**{len(published)} câu chuẩn**, {sum(bool(q['tags']) for q in published)} câu số liệu; đề mẫu {len(sample_ids)} câu.","","## Những mục chưa dùng để chấm",""]
for a in audit:
    if a["status"] in ["pending","disputed"]:lines.append(f"- **{a['id']}**, trang PDF {a['pdfPage']}: {a['reason']}")
lines += ["","## Phạm vi nguồn bổ sung",""]+[f"- {s['sourceId']}: {s['status']}" for s in bank["supplements"]]
lines += ["","## Quy tắc biên tập","","Giữ nguyên đề và phương án, trừ ghi chú biên tập. Phương án tổng hợp được làm độc lập vị trí; câu tham chiếu A/B giữ thứ tự. Căn cứ đối chiếu ghi trong mỗi câu là diễn giải ngắn, không phải trích dẫn nguyên văn. Dữ liệu OCR chỉ hỗ trợ tìm kiếm, không tự dùng làm lời giải.",""]
(ROOT/"content/tthcm/BAO_CAO_NOI_DUNG.md").write_text("\n".join(lines),encoding="utf-8")
print(f"Published {len(published)} unique questions, {len(sample_ids)} sample questions, {len(audit)} source dispositions.")
print("Pending:",len([a for a in audit if a['status'] in ['pending','disputed']]))
