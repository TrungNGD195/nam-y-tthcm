"""Human-reviewed answers for the six Azota snapshots, never Azota grading keys.

Letters refer ONLY to the immutable options in content/tthcm/azota/*.json.
The publisher stores the selected text as well, so reordered options cannot shift keys.
The 2019 textbook and PTIT lecture are the primary curriculum; changes are explicit.
"""

DECISIONS = {}
EXTRA_CONCEPTS = []
REPAIRS = {}
HOLDS = {}
# Bind positional review decisions to the exact captured text and option order.
SNAPSHOT_HASHES = {
    'e9lwce':'c59b80de0015962539d47b2e2246ff01f638882a2f6bb0ecdf4831d15686446e',
    'rnaeqk':'e00917ef8fd109e1fd3c9c87207e2fd3ca067081c53e0323b6f67472cee08404',
    'ela4jq':'407be192a160db8c1b0b8b3921f209f282b0e810fef6b168e4a732bac9ff378c',
    'ijqzcg':'103d69ddf6f515f94c31ddc5ddab98cbfa4a6a4bc28874e032d18473100d167d',
    '3eggrt':'b0da91eb27da8c3baa801d7d50b8c5ff36d9e91b163d5e44edbe236a63d9ccf3',
    'n6fnzo':'fdb5587c123c9f766c1ff34a7f6e7216ca2c6d7a6cd146fa604eca3e7ec6b6e2'
}
BASE_REPAIRS = {
    'lms-g1-09': {'prompt':'Ý nào không phải tên một trong ba ý nghĩa học tập môn Tư tưởng Hồ Chí Minh được liệt kê trong giáo trình?', 'note':'Hỏi đúng danh mục, không phủ nhận việc môn học hỗ trợ các môn khác.'},
    'quiz-g1-10': {'prompt':'Ý nào không phải tên một trong ba ý nghĩa học tập môn Tư tưởng Hồ Chí Minh được liệt kê trong giáo trình?', 'note':'Phân biệt danh mục ý nghĩa với các lợi ích học tập có thể có.'},
    'lms-g2-27': {'options':{'a':'Chỉ có giá trị trong một thời kỳ đã qua, không còn ý nghĩa hiện nay'},'explanation':'Sai ở chỗ giới hạn tư tưởng Hồ Chí Minh vào quá khứ. Giáo trình khẳng định giá trị nền tảng, định hướng đối với cách mạng Việt Nam và thế giới.','note':'Không đánh dấu một sự kiện lịch sử có thể đúng thành sai; thay bằng nhận định sai rõ ràng.'},
    'lms-g4-10': {'prompt':'Yêu cầu nào không thuộc danh mục yêu cầu cán bộ, đảng viên được liệt kê trong bài học?','note':'Giới hạn vào danh mục của bài học, không suy diễn thành cấm làm giàu chính đáng.'},
    'lms-g5-04': {'options':{'a':'Mặt trận là nơi quy tụ các tổ chức và cá nhân yêu nước trong và ngoài nước'},'note':'Bổ sung điều kiện yêu nước, không quy tụ vô điều kiện mọi cá nhân và tổ chức.'},
    'lms-g5-07': {'prompt':'Ý nào không phải tên một trong ba phương thức xây dựng đại đoàn kết được liệt kê trong giáo trình?','note':'Không phủ nhận giá trị thực tế của việc tổ chức hoạt động đoàn kết.'},
    'lms-g6-02': {'options':{'b':'Văn hóa tách rời mọi nhiệm vụ chính trị'},'note':'Hai ý ở trong chính trị và phục vụ chính trị cùng đúng; thay một nhiễu để có một đáp án.'},
    'quiz-g8-09': {'options':{'b':'Văn hóa tách rời mọi nhiệm vụ chính trị'},'note':'Thay lựa chọn chồng lấn với đáp án đúng.'},
    'quiz-g3-09': {'options':{'d':'1920'},'note':'Thay phương án nhiễu 1921 bị trùng; đáp án 1919 giữ nguyên.'},
    'quiz-g4-10': {'prompt':'Khi chủ trì Hội nghị thành lập Đảng đầu năm 1930, Hồ Chí Minh hoạt động với tên nào?','note':'Cả bốn tên đều cùng một người; hỏi rõ tên dùng tại thời điểm 1930 để chỉ có một đáp án.'},
    'quiz-g5-06': {'prompt':'Trong Hiệp định Sơ bộ ngày 6/3/1946, chính phủ nước nào công nhận Việt Nam Dân chủ Cộng hòa là một quốc gia tự do?','note':'Phân biệt quốc gia tự do trong Hiệp định Sơ bộ với công nhận ngoại giao năm 1950; bỏ khẳng định đầu tiên thiếu phạm vi.'},
    'quiz-g6-03': {'options':{'a':'Đoàn kết với giai cấp vô sản và các dân tộc bị áp bức trên thế giới'},'note':'Bổ sung chữ bị bị thiếu; không đoàn kết với dân tộc đi áp bức dân tộc khác.'},
    'quiz-g6-12': {'options':{'d':'Đoàn kết với giai cấp vô sản và các dân tộc bị áp bức trên thế giới'},'note':'Sửa lỗi thiếu chữ bị trong phương án nguồn.'},
    'quiz-g6-08': {'prompt':'Ý nào không thuộc danh mục ba quan hệ đối với mình, người và việc khi bàn về đạo đức?','note':'Hỏi danh mục, không khẳng định Hồ Chí Minh chưa từng bàn đạo đức trong tổ chức.'},
    'quiz-g6-13': {'prompt':'Ý nào không phải tên một nguyên tắc trong danh mục nguyên tắc xây dựng Đảng của phần bài học đang xét?','note':'Nêu gương cũng có vai trò trong xây dựng Đảng; giới hạn câu hỏi vào tên trong danh mục của bài học.'},
    'quiz-g7-01': {'prompt':'Điều kiện đại đoàn kết nào nhấn mạnh việc kế thừa các giá trị lịch sử, văn hóa của dân tộc?','note':'Khoan dung, rộng lượng cũng đúng; làm rõ ý hỏi thay vì chấm chúng thành sai.'},
    'quiz-g7-06': {'prompt':'Ý nào không phải tên một trong ba nhóm lực lượng đoàn kết quốc tế được liệt kê trong bài học?','note':'Phân biệt tên danh mục với tính chất có thể có của một phong trào.'},
    'sample-g1-04': {'options':{'a':'1905','b':'1906','c':'1908','d':'1911'},'note':'Câu hỏi chỉ hỏi năm; bỏ tháng 5 sai so với Tiểu sử Bảo tàng (tháng 4/1908).','explanation':'Nguyễn Tất Thành tham gia chống thuế ở Thừa Thiên năm 1908. Tiểu sử Bảo tàng Hồ Chí Minh xác định tháng 4/1908; không học mốc tháng 5 của lựa chọn nguồn.'},
    'sample-g1-10': {'prompt':'Chọn phát biểu đầy đủ nhất về hai nền tảng tư tưởng, kim chỉ nam cho hành động của Đảng.','note':'Làm rõ yêu cầu chọn đủ cả chủ nghĩa Mác–Lênin và tư tưởng Hồ Chí Minh.'}
}


def answers(code, rows):
    for row in rows.split():
        number, answer, concept = row.split(':')
        ident = f'azota-{code}-{int(number):03}'
        assert ident not in DECISIONS, ident
        DECISIONS[ident] = {'answer': answer, 'concept': concept}


def concept(ident, chapter, title, summary, keywords, page, source='ptit'):
    EXTRA_CONCEPTS.append(dict(id=ident, chapter=chapter, title=title, summary=summary,
        keywords=keywords.split('|'), confusionNote='', core=False,
        references=[dict(sourceId=source, pdfPage=page, section=title, evidence=summary)]))


def repair(code, number, note, *, prompt=None, options=None, explanation=None, keywords=None):
    REPAIRS[f'azota-{code}-{number:03}'] = dict(note=note, prompt=prompt, options=options,
        explanation=explanation, keywords=keywords)


def hold(code, number, reason):
    HOLDS[f'azota-{code}-{number:03}'] = reason


# Concept summaries paraphrase the curriculum, with exact PDF locations.
concept('definition-full',1,'Nội dung khái niệm',
    'Tư tưởng Hồ Chí Minh là hệ thống quan điểm toàn diện, sâu sắc về cách mạng Việt Nam; vận dụng và phát triển sáng tạo chủ nghĩa Mác–Lênin vào điều kiện cụ thể của nước ta.',
    'cách mạng Việt Nam|vận dụng và phát triển sáng tạo|điều kiện cụ thể',9)
concept('purpose',1,'Mục đích giải phóng',
    'Mục đích xuyên suốt là giải phóng dân tộc, giải phóng giai cấp và giải phóng con người; trong hoàn cảnh thuộc địa, giải phóng dân tộc được đặt trước hết.',
    'giải phóng dân tộc|giải phóng giai cấp|giải phóng con người',38)
concept('origins-all',2,'Các cơ sở hình thành',
    'Cơ sở hình thành gồm điều kiện thực tiễn Việt Nam và thế giới, các tiền đề tư tưởng–lý luận và nhân tố chủ quan Hồ Chí Minh.',
    'thực tiễn|tư tưởng–lý luận|nhân tố chủ quan',28)
concept('patriotism',2,'Chủ nghĩa yêu nước',
    'Chủ nghĩa yêu nước là giá trị cốt lõi, dòng chảy chính trong truyền thống dân tộc được Hồ Chí Minh kế thừa và phát triển.',
    'chủ nghĩa yêu nước|cốt lõi',22)
concept('west',2,'Văn hóa phương Tây',
    'Tự do, bình đẳng, bác ái gắn với Cách mạng Pháp; các nhà Khai sáng Pháp thuộc văn hóa phương Tây. Không xếp các giá trị này vào văn hóa phương Đông.',
    'tự do, bình đẳng, bác ái|Pháp|phương Tây',25)
concept('tam-dan-fit',2,'Tam dân và điều kiện Việt Nam',
    'Hồ Chí Minh nhận thấy chủ nghĩa Tam dân có những điểm thích hợp với điều kiện nước ta; tiếp thu có chọn lọc, không đồng nhất Tam dân với chủ nghĩa Mác–Lênin.',
    'Tam dân|thích hợp|điều kiện nước ta',5,'giao-trinh-2009')
concept('soi-duong',1,'Soi đường và tài sản tinh thần',
    'Khái niệm trong giáo trình nhấn mạnh tư tưởng Hồ Chí Minh là tài sản tinh thần vô cùng to lớn, quý giá, mãi mãi soi đường cho sự nghiệp cách mạng.',
    'soi đường|tài sản tinh thần',9)
concept('book1927',2,'Đường Kách mệnh — 1927',
    'Đường Kách mệnh được xuất bản năm 1927, tập hợp nội dung huấn luyện cán bộ cách mạng.',
    'Đường Kách mệnh|1927',32)
concept('book1925',2,'Bản án — 1925',
    'Bản án chế độ thực dân Pháp xuất bản năm 1925, tố cáo bản chất và thủ đoạn bóc lột của chủ nghĩa thực dân.',
    'Bản án chế độ thực dân Pháp|1925',32)
concept('demands1919',2,'Yêu sách: quyền tự do, dân chủ',
    'Yêu sách năm 1919 đòi các quyền tự do, dân chủ và bình đẳng pháp lý; chưa đòi độc lập hay quyền tự trị.',
    '1919|tự do, dân chủ|chưa đòi độc lập',31)
concept('unesco',1,'UNESCO — 1987',
    'UNESCO thông qua nghị quyết năm 1987 về kỷ niệm 100 năm ngày sinh Hồ Chí Minh vào năm 1990, ghi nhận Anh hùng giải phóng dân tộc và nhà văn hóa kiệt xuất của Việt Nam.',
    '1987|1990|Việt Nam',6)
concept('self-reliance',5,'Tự lực trước khi tranh thủ giúp đỡ',
    'Phải tự giúp mình, dựa vào sức mình là chính; sự giúp đỡ quốc tế rất quan trọng nhưng không thay thế nội lực.',
    'tự giúp lấy mình|sức mình là chính|quốc tế',132)
concept('final-wish',6,'Mong muốn cuối cùng trong Di chúc',
    'Mong muốn cuối cùng là toàn Đảng, toàn dân đoàn kết xây dựng Việt Nam hòa bình, thống nhất, độc lập, dân chủ, giàu mạnh và đóng góp cho cách mạng thế giới.',
    'hòa bình, thống nhất|độc lập, dân chủ, giàu mạnh|Di chúc',1,'official-dichuc')
concept('national-socialism',3,'Độc lập gắn với CNXH',
    'Nội dung cốt lõi là độc lập dân tộc gắn liền với chủ nghĩa xã hội. Kiên trì con đường Hồ Chí Minh lựa chọn là kiên định cả hai mục tiêu.',
    'độc lập dân tộc|gắn liền|chủ nghĩa xã hội',70)
concept('active-colonies',3,'Thuộc địa chủ động, sáng tạo',
    'Cách mạng giải phóng dân tộc phải chủ động, sáng tạo và có khả năng thắng trước cách mạng vô sản ở chính quốc; không phụ thuộc thắng lợi ở chính quốc.',
    'chủ động, sáng tạo|thắng trước|không phụ thuộc',51)
concept('transition-steps',3,'Bước đi phù hợp thực tiễn',
    'Xác định bước đi từ điều kiện thực tế và khả năng của nhân dân, học tập kinh nghiệm nhưng không rập khuôn; đi từng bước phù hợp, vững chắc.',
    'điều kiện thực tế|không rập khuôn|từng bước',69)
concept('distribution',3,'Phân phối theo lao động',
    'Trong CNXH, nguyên tắc phân phối chủ yếu là theo lao động: làm nhiều hưởng nhiều, làm ít hưởng ít; có bảo đảm cho người chưa hoặc không còn khả năng lao động.',
    'theo lao động|làm nhiều hưởng nhiều',58)
concept('political-owner',3,'Nhân dân làm chủ',
    'Chế độ chính trị XHCN là chế độ do nhân dân làm chủ. Quyền lực thuộc nhân dân; Đảng lãnh đạo, Nhà nước phục vụ nhân dân.',
    'nhân dân|làm chủ',57)
concept('national-liberation',3,'Giải phóng dân tộc',
    'Giải phóng dân tộc là xóa ách áp bức thực dân, giành độc lập, lập nhà nước dân tộc độc lập và lựa chọn con đường phát triển phù hợp thời đại.',
    'xóa ách thực dân|độc lập|nhà nước dân tộc',46)
concept('national-before-class',3,'Dân tộc trước hết',
    'Ở Việt Nam thuộc địa, giải phóng dân tộc là nhiệm vụ trước hết và là tiền đề cho giải phóng giai cấp; không đảo ngược thứ tự này.',
    'giải phóng dân tộc|trước hết|tiền đề',47)
concept('forces-all',3,'Lực lượng toàn dân',
    'Cách mạng giải phóng dân tộc là sự nghiệp của toàn dân, lấy liên minh công–nông làm nền tảng; không thu hẹp lực lượng vào một giai cấp.',
    'toàn dân|công–nông|nền tảng',49)
concept('nationalism',3,'Chủ nghĩa dân tộc chân chính',
    'Chủ nghĩa dân tộc được đánh giá là động lực lớn là chủ nghĩa yêu nước, dân tộc chân chính của người dân mất nước, không phải dân tộc hẹp hòi hay sôvanh.',
    'động lực lớn|chân chính|yêu nước',17,'giao-trinh-2009')
concept('obstacles',3,'Những trở lực cần chống',
    'Phải chống chủ nghĩa cá nhân, tham ô, lãng phí, quan liêu và chia rẽ, mất đoàn kết; đây là những trở lực làm suy yếu công cuộc xây dựng CNXH.',
    'chủ nghĩa cá nhân|tham ô, lãng phí, quan liêu|mất đoàn kết',36,'giao-trinh-2009')
concept('individual-interest',6,'Lợi ích cá nhân chính đáng',
    'Chống chủ nghĩa cá nhân không phải xóa bỏ hay chà đạp lợi ích cá nhân chính đáng; phải hài hòa lợi ích cá nhân với tập thể, xã hội.',
    'chủ nghĩa cá nhân|lợi ích chính đáng|không chà đạp',153)
concept('happiness-science',3,'CNXH và khoa học',
    'Luận điểm về CNXH cộng với khoa học nhấn mạnh đích đến là hạnh phúc vô tận cho con người.',
    'CNXH|khoa học|hạnh phúc vô tận',39,'giao-trinh-2009')
concept('people-resources',3,'Của dân, tài dân, sức dân',
    'Biện pháp cơ bản, quyết định, lâu dài là huy động của dân, tài dân, sức dân để làm lợi cho dân, dưới sự lãnh đạo của Đảng.',
    'của dân, tài dân, sức dân|làm lợi cho dân',40,'giao-trinh-2009')
concept('khoan',3,'Làm khoán: ích chung, lợi riêng',
    'Làm khoán gắn kết lợi ích người lao động, tập thể và Nhà nước; khuyến khích tăng năng suất đồng thời bảo đảm chất lượng.',
    'làm khoán|ích chung|lợi riêng',1,'official-khoan')
concept('peace-violence',3,'Bạo lực gắn với hòa bình, nhân đạo',
    'Bạo lực cách mạng gắn hữu cơ với tư tưởng nhân đạo, hòa bình: tranh thủ giải pháp hòa bình, chỉ dùng chiến tranh khi buộc phải bảo vệ độc lập.',
    'bạo lực|nhân đạo|hòa bình',54)
concept('bird-wings',3,'Hai cánh của một con chim',
    'Cách mạng thuộc địa và cách mạng vô sản ở chính quốc có quan hệ mật thiết như hai cánh của một con chim. Con đỉa hai vòi là hình ảnh chỉ chủ nghĩa tư bản.',
    'hai cánh|thuộc địa và chính quốc|con chim',51)
concept('progress-need',3,'Mâu thuẫn trong quá độ',
    'Mâu thuẫn cơ bản của thời kỳ quá độ là nhu cầu phát triển cao của đất nước với thực trạng kinh tế, xã hội còn thấp kém.',
    'nhu cầu phát triển cao|thấp kém',37,'giao-trinh-2009')
concept('state-economy',3,'Kinh tế quốc doanh và hợp tác xã',
    'Trong thời kỳ quá độ, ưu tiên phát triển kinh tế quốc doanh; hợp tác xã phải tự nguyện, cùng có lợi, từ thấp đến cao, tránh gò ép.',
    'quốc doanh|tự nguyện|cùng có lợi',67)
concept('class-liberation',3,'Xóa chế độ áp bức giai cấp',
    'Giải phóng giai cấp là xóa bỏ áp bức, bóc lột và địa vị thống trị của giai cấp bóc lột; không phải tiêu diệt con người thuộc giai cấp đó.',
    'xóa áp bức, bóc lột|địa vị thống trị|không tiêu diệt con người',18,'giao-trinh-2009')
concept('human-liberation',6,'Giải phóng con người',
    'Giải phóng con người hướng tới từng cá nhân và cả nhân loại, trước hết là quần chúng lao động bị áp bức, để con người phát triển tự do, toàn diện.',
    'cá nhân|nhân loại|quần chúng lao động',160)
concept('party-purpose',4,'Phụng sự Tổ quốc, nhân dân',
    'Đảng hoạt động để phụng sự Tổ quốc, phục vụ nhân dân; không có lợi ích riêng ngoài lợi ích của giai cấp, nhân dân và dân tộc.',
    'phụng sự Tổ quốc|phục vụ nhân dân',79)
concept('party-class',4,'Bản chất và lợi ích của Đảng',
    'Đảng mang bản chất giai cấp công nhân, đồng thời là Đảng của nhân dân lao động và dân tộc; bản chất thể hiện ở nền tảng lý luận, mục tiêu, đường lối, tổ chức.',
    'giai cấp công nhân|nhân dân lao động|dân tộc',79)
concept('criticism',4,'Phê bình để tiến bộ',
    'Tự phê bình và phê bình nhằm giúp nhau sửa chữa, tiến bộ; phải thật thà, chỉ rõ ưu khuyết điểm, phê bình việc làm và tránh công kích, mỉa mai.',
    'giúp nhau sửa chữa|tiến bộ|không công kích',85)
concept('party-dichuc',4,'Lời căn dặn về Đảng trong Di chúc',
    'Di chúc yêu cầu giữ Đảng trong sạch, cán bộ thấm nhuần đạo đức cách mạng, giữ đoàn kết như con ngươi của mắt mình; Đảng vừa lãnh đạo vừa phục vụ nhân dân.',
    'Di chúc|trong sạch|con ngươi của mắt mình',1,'official-dichuc')
concept('cadre-role',4,'Cán bộ tốt hay kém',
    'Cán bộ là gốc của công việc; công việc thành công hoặc thất bại do cán bộ tốt hay kém. Phải chú trọng đạo đức, năng lực và trách nhiệm của cán bộ.',
    'cán bộ|gốc|tốt hay kém',88)
concept('party-leads-state',4,'Phương thức Đảng lãnh đạo Nhà nước',
    'Đảng lãnh đạo Nhà nước bằng đường lối, chủ trương; qua tổ chức đảng, đảng viên và công tác kiểm tra, không làm thay quản lý của Nhà nước.',
    'đường lối|tổ chức, đảng viên|kiểm tra',82,'giao-trinh-2009')
concept('party-names',4,'Tên Đảng qua các mốc',
    'Tháng 2/1930 thành lập Đảng Cộng sản Việt Nam; tháng 10/1930 đổi thành Đảng Cộng sản Đông Dương; năm 1951 lấy tên Đảng Lao động Việt Nam.',
    '2/1930|10/1930|1951',33)
concept('party-launch1951',4,'Ra mắt Đảng Lao động Việt Nam',
    'Tại lễ ra mắt Đảng Lao động Việt Nam ngày 3/3/1951, Hồ Chí Minh nêu tám chữ: Đoàn kết toàn dân, phụng sự Tổ quốc.',
    '3/3/1951|ra mắt|Đoàn kết toàn dân',63)
concept('unity-foundation',5,'Nền tảng công–nông–trí thức',
    'Nền tảng khối đại đoàn kết là liên minh giai cấp công nhân, nông dân và đội ngũ trí thức; đoàn kết phải dựa trên lợi ích dân tộc và quyền lợi chính đáng của nhân dân.',
    'công nhân|nông dân|trí thức',112)
concept('unity-goal',5,'Đoàn kết là mục tiêu, nhiệm vụ',
    'Đại đoàn kết toàn dân tộc là mục tiêu, nhiệm vụ hàng đầu của Đảng và của dân tộc; đồng thời là chiến lược quyết định thành công cách mạng.',
    'đại đoàn kết|mục tiêu|nhiệm vụ hàng đầu',110)
concept('unity-origins',5,'Cơ sở tư tưởng đại đoàn kết',
    'Đại đoàn kết hình thành từ truyền thống yêu nước, nhân ái; tổng kết thực tiễn cách mạng; quan điểm Mác–Lênin về quần chúng và cách mạng giải phóng.',
    'truyền thống|thực tiễn|Mác–Lênin',46,'giao-trinh-2009')
concept('nation-strength',5,'Sức mạnh dân tộc',
    'Sức mạnh dân tộc gồm lòng yêu nước, truyền thống văn hóa, tinh thần đoàn kết và ý chí đấu tranh cho độc lập.',
    'yêu nước|văn hóa|đoàn kết',123)
concept('international-strength',5,'Sức mạnh thời đại',
    'Sức mạnh thời đại gồm phong trào cộng sản, giải phóng dân tộc, các lực lượng tiến bộ và những thành tựu khoa học–kỹ thuật; cần kết hợp với sức mạnh dân tộc.',
    'cách mạng thế giới|tiến bộ|khoa học–kỹ thuật',124)
concept('diplomacy',5,'Nguyên tắc và sách lược',
    'Đối ngoại phải kiên định mục tiêu, nguyên tắc độc lập dân tộc, đồng thời linh hoạt về sách lược: dĩ bất biến, ứng vạn biến.',
    'kiên định nguyên tắc|linh hoạt sách lược|dĩ bất biến',131)
concept('culture-definition',6,'Nội hàm văn hóa',
    'Theo nghĩa rộng, văn hóa gồm các giá trị vật chất và tinh thần do con người sáng tạo để đáp ứng nhu cầu sinh tồn và mục đích cuộc sống.',
    'vật chất và tinh thần|sinh tồn|mục đích cuộc sống',141)
concept('culture-nature',6,'Dân tộc, khoa học, đại chúng',
    'Nền văn hóa mới trong kháng chiến chống Pháp mang tính dân tộc, khoa học, đại chúng; đại chúng nghĩa là phục vụ nhân dân và do nhân dân xây dựng.',
    'dân tộc|khoa học|đại chúng',147)
concept('culture-functions',6,'Ba chức năng văn hóa',
    'Ba chức năng: bồi dưỡng tư tưởng, tình cảm; nâng cao dân trí; bồi dưỡng phẩm chất, phong cách, lối sống tốt đẹp.',
    'tư tưởng, tình cảm|dân trí|phẩm chất, lối sống',101,'giao-trinh-2009')
concept('ethics-root',6,'Đạo đức là gốc',
    'Đạo đức là gốc, nền tảng của người cách mạng; đức và tài phải gắn bó. Tài giỏi mà thiếu đạo đức thì không lãnh đạo được nhân dân.',
    'đạo đức|gốc|nền tảng',148)
concept('highest-ethics',6,'Trung với nước, hiếu với dân',
    'Trung với nước, hiếu với dân là phẩm chất bao trùm: trung thành với sự nghiệp dựng nước, giữ nước; tin dân, thương dân và hết lòng phục vụ nhân dân.',
    'trung với nước|hiếu với dân|bao trùm',149)
concept('new-life',6,'Đời sống mới',
    'Xây dựng đời sống mới được đặt ra sau Cách mạng Tháng Tám; ba nội dung là đạo đức mới, lối sống mới và nếp sống mới.',
    'đạo đức mới|lối sống mới|nếp sống mới',105,'giao-trinh-2009')
concept('human-specific',6,'Con người cụ thể, lịch sử',
    'Hồ Chí Minh xem xét con người cụ thể trong hoàn cảnh lịch sử, quan hệ xã hội cụ thể, không phải con người trừu tượng, phi lịch sử.',
    'con người cụ thể|lịch sử|quan hệ xã hội',158)
concept('human-nature',6,'Mặt tự nhiên và xã hội',
    'Con người thống nhất mặt sinh học và xã hội, trong đó quan hệ xã hội được nhấn mạnh. Trong mỗi người đều có mặt tốt–xấu, thiện–ác cần được giáo dục, rèn luyện.',
    'tự nhiên và xã hội|thiện–ác|giáo dục',158)
concept('chinh-relations',6,'Chính trong ba quan hệ',
    'Chính là thẳng thắn, đứng đắn; thể hiện đối với mình, đối với người và đối với việc, đặt việc công và lợi ích chung lên trước.',
    'chính|mình, người, việc|việc công',152)
concept('education-all',6,'Giáo dục toàn diện',
    'Giáo dục phải toàn diện về đức, trí, thể, mỹ, đào tạo người tốt và có ích; học gắn với hành, lý luận gắn với thực tiễn để đạt hiệu quả.',
    'đức, trí, thể, mỹ|có ích|học đi đôi với hành',103,'giao-trinh-2009')
concept('artist',6,'Văn nghệ là mặt trận',
    'Văn nghệ là mặt trận, nghệ sĩ là chiến sĩ; tác phẩm là vũ khí đấu tranh, phục vụ nhân dân và xây dựng con người mới.',
    'mặt trận|nghệ sĩ–chiến sĩ|tác phẩm–vũ khí',145)
concept('culture-position',6,'Văn hóa trong đời sống',
    'Văn hóa thuộc đời sống tinh thần, kiến trúc thượng tầng; phải gắn với kinh tế, chính trị và xã hội, phục vụ nhiệm vụ chính trị và thúc đẩy kinh tế.',
    'kiến trúc thượng tầng|kinh tế|chính trị',142)
concept('ethics-life',6,'Cần, kiệm, liêm, chính',
    'Cần, kiệm, liêm, chính là các đức tính gắn với công việc hằng ngày, nền tảng đời sống mới, làm dân tộc giàu về vật chất và mạnh về tinh thần.',
    'cần, kiệm, liêm, chính|đời sống mới|hằng ngày',152)

concept('letter1928',2,'Thư tháng 4/1928',
    'Bức thư nói về tình cảnh không được hoạt động, thiếu tiền được viết ngày 12/4/1928; khác bức thư Quốc tế Cộng sản năm 1938 trong giáo trình.',
    '12/4/1928|không được hoạt động',1,'official-chronology1')
concept('return1928',2,'Quyết định về Đông Dương — 1928',
    'Quốc tế Cộng sản đồng ý để Nguyễn Ái Quốc trở về hoạt động ở Đông Dương ngày 25/4/1928.',
    '25/4/1928|Đông Dương',1,'official-bio')
concept('duc-thanh-years',2,'Dạy học ở Dục Thanh',
    'Nguyễn Tất Thành dạy ở Trường Dục Thanh, Phan Thiết, từ nửa sau tháng 9/1910 đến trước tháng 2/1911, rồi vào Sài Gòn.',
    'Dục Thanh|9/1910|2/1911',1,'official-chronology1')
concept('usa-years',2,'Ở Mỹ — 1912–1913',
    'Biên niên tiểu sử ghi Nguyễn Tất Thành dừng chân ở Mỹ cuối năm 1912, rời Mỹ khoảng đầu năm 1913.',
    'Mỹ|1912–1913',1,'official-chronology1')
concept('uk-years',2,'Ở Anh — 1913–1917',
    'Nguyễn Tất Thành sang Anh năm 1913, lao động và học tập, rồi trở lại Pháp cuối năm 1917.',
    'Anh|1913–1917',1,'official-bio')
concept('predecessors',2,'Nhận xét các con đường cũ',
    'Phan Bội Châu dựa Nhật nên được ví là đuổi hổ, rước beo; Phan Châu Trinh dựa Pháp nên được ví là xin giặc rủ lòng thương.',
    'Phan Bội Châu–Nhật|Phan Châu Trinh–Pháp',29)
concept('jobs',2,'Lao động trong hành trình cứu nước',
    'Trong hành trình hoạt động, Người làm nhiều nghề để sống và học hỏi, gồm phụ bếp, đốt lò, cào tuyết, làm bánh, thợ ảnh và bán báo.',
    'nhiều nghề|lao động|học hỏi',1,'official-bio')
concept('lenin-path',2,'Con đường dẫn tôi đến chủ nghĩa Lênin',
    'Bài Con đường dẫn tôi đến chủ nghĩa Lênin (1960) kể việc đọc Luận cương; tình cảm ban đầu với Lênin gắn với việc giải phóng đồng bào Nga.',
    'Con đường dẫn tôi đến chủ nghĩa Lênin|1960|Luận cương',1,'official-lenin-path')
concept('marx-humanity',2,'Học lý luận để sống có nghĩa, có tình',
    'Học chủ nghĩa Mác–Lênin phải vận dụng vào cuộc sống và quan hệ với con người, sống có nghĩa, có tình; không chỉ học thuộc hay khoe trình độ.',
    'có nghĩa, có tình|vận dụng',1,'official-dichuc')
concept('human-love',6,'Yêu nước, thương dân, nhân loại',
    'Tình cảm lớn gồm yêu nước, thương dân và thương nhân loại bị đau khổ, áp bức; không thu hẹp vào một vế.',
    'yêu nước|thương dân|nhân loại',101,'giao-trinh-2009')
concept('history-poem',2,'Lịch sử nước ta',
    'Lịch sử nước ta mở đầu bằng lời nhắc biết sử dân tộc; viết khoảng nửa sau 1941, xuất bản đầu tiên tháng 2/1942.',
    'Lịch sử nước ta|biết sử|2/1942',1,'official-history-poem')
concept('oriental-marx',2,'Thực tiễn phương Đông',
    'Hồ Chí Minh yêu cầu bổ sung cơ sở lịch sử của chủ nghĩa Mác bằng dân tộc học phương Đông; nêu vai trò chủ nghĩa dân tộc và khả năng phát triển chủ nghĩa cộng sản ở châu Á.',
    'dân tộc học phương Đông|châu Á|chủ nghĩa dân tộc',1,'official-selected1')
concept('revolution-not-through',3,'Cách mạng tư sản chưa đến nơi',
    'Hồ Chí Minh đánh giá cách mạng tư sản Mỹ và Pháp là cách mạng không đến nơi vì người lao động chưa được giải phóng triệt để.',
    'Mỹ và Pháp|không đến nơi|chưa triệt để',47)
concept('chess-strategy',3,'Học đánh cờ và thời cơ',
    'Hình ảnh trong Học đánh cờ nhấn mạnh tính toán thế, thời và quyết tâm; khi vận dụng vào cách mạng, gắn với chiến lược, chiến thuật.',
    'thế và thời|chiến lược, chiến thuật',1,'official-selected1')
concept('illiteracy',6,'Chống nạn thất học',
    'Chống nạn thất học yêu cầu nâng cao dân trí, đặc biệt khuyến khích phụ nữ học tập để tiến kịp nam giới.',
    'Chống nạn thất học|dân trí|phụ nữ',1,'official-selected2')
concept('foreign-capital',3,'Hợp tác kinh tế với nước ngoài',
    'Hồ Chí Minh hoan nghênh tư bản nước ngoài thật thà hợp tác để kiến thiết Việt Nam, điều hòa kinh tế và giữ gìn hòa bình.',
    'thật thà hợp tác|kiến thiết|hòa bình',1,'official-selected2')
concept('socialism-approach',3,'Các cách tiếp cận CNXH',
    'Hồ Chí Minh tiếp cận CNXH từ khát vọng giải phóng dân tộc, đạo đức và truyền thống văn hóa Việt Nam, trên nền tảng lý luận Mác–Lênin.',
    'giải phóng dân tộc|đạo đức|văn hóa Việt Nam',28,'giao-trinh-2009')
concept('socialism-goal',3,'Không ngừng nâng cao đời sống',
    'Mục tiêu của CNXH là không ngừng nâng cao đời sống vật chất và tinh thần của nhân dân, đem lại tự do và hạnh phúc thiết thực.',
    'nâng cao đời sống|vật chất và tinh thần|nhân dân',60)
concept('human-socialist',6,'Con người xã hội chủ nghĩa',
    'Muốn xây dựng CNXH, trước hết cần có những con người xã hội chủ nghĩa; phải coi trọng giáo dục, rèn luyện con người.',
    'trước hết|con người xã hội chủ nghĩa',162)
concept('agriculture',3,'Nông nghiệp và đời sống đất nước',
    'Hồ Chí Minh nhấn mạnh nông dân giàu thì nước giàu, nông nghiệp thịnh thì nước thịnh; từ cần điền là nông nghiệp.',
    'nông dân giàu|nông nghiệp thịnh',1,'official-selected2')
concept('august-call',3,'Thư kêu gọi Tổng khởi nghĩa',
    'Thư kêu gọi Tổng khởi nghĩa tháng 8/1945 nêu yêu cầu toàn quốc đồng bào đứng dậy, đem sức ta mà tự giải phóng cho ta.',
    '8/1945|Tổng khởi nghĩa|đem sức ta',1,'official-selected1')
concept('resistance-line',3,'Đường lối kháng chiến',
    'Kháng chiến toàn dân, toàn diện, lâu dài, dựa vào sức mình là chính; kháng chiến gắn với kiến quốc.',
    'toàn dân, toàn diện|lâu dài|tự lực',1,'official-bio')
concept('forces-combined',3,'Kết hợp các lực lượng cách mạng',
    'Sự nghiệp giải phóng dựa vào toàn dân và liên minh công–nông–trí thức, dưới sự lãnh đạo của Đảng, kết hợp với các lực lượng cách mạng thế giới.',
    'toàn dân|Đảng lãnh đạo|cách mạng thế giới',49)
concept('loseby',2,'Luật sư Lôdơbi',
    'Luật sư Ph. H. Lôdơbi (Frank Henry Loseby) đã giúp bảo vệ, giải thoát Nguyễn Ái Quốc khỏi nhà tù Anh ở Hồng Kông.',
    'Lôdơbi|Hồng Kông|luật sư',1,'official-bio')
concept('letter-committees',4,'Thư gửi các ủy ban nhân dân',
    'Thư gửi Ủy ban nhân dân các kỳ, tỉnh, huyện và làng ngày 17/10/1945 nhấn mạnh làm việc lợi cho dân, tránh việc hại cho dân.',
    '17/10/1945|Ủy ban nhân dân|lợi cho dân',1,'official-selected2')
concept('education-lifelong',6,'Học tập suốt đời',
    'Học không bao giờ cùng: còn sống còn phải học, học ở mọi lúc, mọi nơi, mọi người, coi trọng tự học và thực tiễn.',
    'suốt đời|tự học|mọi lúc, mọi nơi',1,'official-lifelong')
concept('democratic-friends',5,'Làm bạn với mọi nước dân chủ',
    'Tuyên bố ngoại giao của Hồ Chí Minh nêu Việt Nam muốn làm bạn với mọi nước dân chủ, không gây thù oán với một ai.',
    'mọi nước dân chủ|không gây thù oán',1,'official-selected2')
concept('ho-slogan',5,'Khẩu hiệu về người lao động',
    'Khẩu hiệu gắn với Hồ Chí Minh là Lao động tất cả các nước, đoàn kết lại; phân biệt với khẩu hiệu vô sản và các dân tộc bị áp bức của Lênin.',
    'Hồ Chí Minh|Lao động tất cả các nước',1,'official-ho-slogan')
concept('unity-success',5,'Đại hội Mặt trận lần II',
    'Hồ Chí Minh nhắc lại bài học đoàn kết, đại đoàn kết gắn với thành công, đại thành công tại Đại hội Mặt trận Tổ quốc Việt Nam lần II năm 1961.',
    'đại đoàn kết|đại thành công|Mặt trận lần II',1,'official-unity1961')
concept('three-fronts',5,'Ba tầng mặt trận đoàn kết',
    'Đoàn kết được tổ chức ở ba phạm vi: toàn dân tộc Việt Nam, nhân dân ba nước Đông Dương và nhân dân tiến bộ thế giới ủng hộ Việt Nam.',
    'dân tộc|Đông Dương|thế giới',129)
concept('front1939',5,'Mặt trận phản đế — 1939',
    'Hội nghị Trung ương tháng 11/1939 chủ trương lập Mặt trận thống nhất dân tộc phản đế Đông Dương.',
    '11/1939|Mặt trận phản đế|Đông Dương',116)
concept('four-seas',5,'Bốn biển một nhà',
    'Câu thơ về tình đoàn kết các dân tộc nhắc vàng, đen, trắng, đỏ đều là anh em, không phân biệt màu da.',
    'vàng đen trắng đỏ|anh em|đoàn kết',127)
concept('ethics1947',6,'Sửa đổi lối làm việc — 1947',
    'Hình ảnh sông phải có nguồn, cây phải có gốc nằm trong Sửa đổi lối làm việc; nhấn mạnh đạo đức là gốc người cách mạng.',
    'sông có nguồn, cây có gốc|Sửa đổi lối làm việc|1947',1,'official-selected2')
concept('ethics1958',6,'Đạo đức cách mạng — 1958',
    'Đạo đức cách mạng ký Trần Lực đăng Tạp chí Học tập tháng 12/1958, có hình ảnh ngọc càng mài càng sáng, vàng càng luyện càng trong.',
    'Đạo đức cách mạng|Tạp chí Học tập|12/1958',1,'official-ethics1958')
concept('ethics1969',6,'Bút danh T.L. — 1969',
    'Nâng cao đạo đức cách mạng, quét sạch chủ nghĩa cá nhân đăng Báo Nhân Dân ngày 3/2/1969, ký T.L., tức Trần Lực.',
    'T.L.|Trần Lực|3/2/1969',1,'official-ethics1969')
concept('fairness1966',6,'Công bằng trong phân phối — 1966',
    'Lời nhắc không sợ thiếu mà sợ không công bằng thuộc bài nói tại kỳ họp Hội đồng Chính phủ cuối năm 1966.',
    'công bằng|cuối năm 1966',1,'official-dichuc')
concept('confucius-liem',6,'Lời Khổng Tử được dẫn lại',
    'Trong bài Liêm, Hồ Chí Minh dẫn lời Khổng Tử để nhấn mạnh sự cần thiết của đức liêm; cần phân biệt tác giả lời được dẫn với người trích dẫn.',
    'Khổng Tử|Liêm|dẫn lại',1,'official-selected2')
concept('youth-spring',6,'Tuổi trẻ và mùa xuân',
    'Trong Thư gửi thanh niên và nhi đồng Tết 1946, Hồ Chí Minh ví tuổi trẻ là mùa xuân của xã hội.',
    'tuổi trẻ|mùa xuân|1946',1,'official-selected2')
concept('youth-awaken',6,'Thức tỉnh thanh niên',
    'Muốn thức tỉnh một dân tộc, trước hết phải thức tỉnh thanh niên; thanh niên là lực lượng quan trọng của sự nghiệp cách mạng.',
    'thức tỉnh|thanh niên',126,'giao-trinh-2009')
concept('lenin-party',4,'Trí tuệ, danh dự, lương tâm',
    'Lênin nêu Đảng là trí tuệ, danh dự và lương tâm của thời đại. Không gán câu này thành lời riêng của Hồ Chí Minh.',
    'Lênin|trí tuệ|danh dự, lương tâm',1,'official-lenin-party')
concept('new-life1947',6,'Đời sống mới — 3/1947',
    'Hồ Chí Minh hoàn thành Đời sống mới ngày 20/3/1947, ký bút danh Tân Sinh.',
    'Đời sống mới|3/1947|Tân Sinh',1,'official-newlife')

# Context-dependent rankings are not factual answer keys.
hold('rnaeqk',18,'Câu hỏi đánh giá “thành tựu nổi bật nhất” nhưng không nêu giai đoạn, văn kiện hay tiêu chí. Không áp một lựa chọn thành kết luận của giáo trình.')
hold('ela4jq',27,'“Nguy cơ lớn nhất” không có phạm vi, thời điểm và trích dẫn đủ rõ; các lựa chọn chồng lấn. Không ép chọn khi chưa xác định được luận điểm nguồn.')
hold('ela4jq',39,'Việc xếp luận điểm vào “vị thế/phương thức/năng lực cầm quyền” không có căn cứ phân loại đủ rõ trong giáo trình; chưa dùng để chấm.')
hold('ela4jq',85,'Câu hỏi về hệ tư tưởng và phương thức sản xuất của giai cấp nông dân thuộc nội dung lý luận rộng hơn; chưa có đoạn giáo trình môn này đối chiếu trực tiếp để chấm.')

# Locations refined after reading adjoining pages; do not cite a TOC or preceding page.
for item in EXTRA_CONCEPTS:
    if item['id'] in {'front1939':'117','human-socialist':'163','socialism-goal':'59','three-fronts':'130','democratic-friends':'132'}:
        page={'front1939':117,'human-socialist':163,'socialism-goal':59,'three-fronts':130,'democratic-friends':132}[item['id']]
        item['references'][0].update(sourceId='ptit',pdfPage=page)

# The snapshot remains verbatim. These edits affect only the unambiguous study version.
repair('e9lwce',5,'Đổi câu hỏi thành nhận diện cặp học thuyết; sửa phương án nhiễu trùng nhau, không phủ nhận Lão giáo trong giáo trình.',
    prompt='Cặp học thuyết nào dưới đây đều thuộc văn hóa phương Đông mà Hồ Chí Minh tiếp thu có chọn lọc?',
    options={'b':'Thiên Chúa giáo và Hồi giáo','c':'Thiên Chúa giáo và Do Thái giáo','d':'Triết học Hy Lạp và La Mã cổ đại'})
repair('e9lwce',17,'Hai phương án nguồn trùng nhau và diễn đạt gần nghĩa; sửa lựa chọn nhiễu để chỉ một phương án phù hợp khái niệm.',
    prompt='Theo khái niệm trong giáo trình, tư tưởng Hồ Chí Minh được hình thành bằng cách tiếp cận chủ nghĩa Mác–Lênin như thế nào?',
    options={'a':'Sao chép nguyên vẹn mô hình của các nước khác','b':'Tách rời điều kiện lịch sử cụ thể của Việt Nam','c':'Phủ nhận giá trị của chủ nghĩa Mác–Lênin'})
repair('e9lwce',23,'Thuật ngữ đã xuất hiện trước 1991; làm rõ câu hỏi về Đại hội chính thức xác lập nền tảng tư tưởng, tránh khẳng định sai rằng lần đầu dùng thuật ngữ.',
    prompt='Đảng chính thức khẳng định chủ nghĩa Mác–Lênin và tư tưởng Hồ Chí Minh là nền tảng tư tưởng, kim chỉ nam cho hành động tại Đại hội năm nào?')
repair('e9lwce',28,'Các lựa chọn quá rộng; làm rõ đang hỏi nguồn bắt nguồn từ lịch sử dân tộc Việt Nam.',
    prompt='Nguồn lý luận nào của tư tưởng Hồ Chí Minh bắt nguồn trực tiếp từ lịch sử và văn hóa dân tộc Việt Nam?')
repair('e9lwce',40,'Tên tác phẩm trong lựa chọn nguồn bị ghi sai. Đối chiếu bài gốc trên Báo Nhân Dân, sửa thành Con đường dẫn tôi đến chủ nghĩa Lênin.',
    options={'b':'Con đường dẫn tôi đến chủ nghĩa Lênin'})
repair('e9lwce',42,'Biên niên ghi từ nửa sau 9/1910 đến trước 2/1911; diễn đạt lựa chọn chính xác hơn.',
    options={'b':'Từ nửa sau tháng 9/1910 đến trước tháng 2/1911'})
repair('e9lwce',49,'Nguồn dùng 1921–1930; chuẩn hóa theo khung giáo trình 2019 là 1920–1930.',
    options={'c':'1920 → 1930'}, explanation='Giáo trình 2019 chia giai đoạn hình thành các nội dung cơ bản là 1920–1930. Một số tài liệu cũ dùng 1921–1930; bản ôn này theo giáo trình hiện tại.')
repair('e9lwce',57,'Câu nguồn gán tháng cho một lời kể nhưng không có căn cứ xác định ngày phát biểu; giữ ý hỏi, chuyển sang sự kiện ra đi có mốc xác thực.',
    prompt='Nguyễn Tất Thành ra đi tìm đường cứu nước từ bến Nhà Rồng vào tháng, năm nào?')
repair('e9lwce',65,'Hai lựa chọn cùng chỉ Luận cương lần thứ nhất về dân tộc và thuộc địa; thay lựa chọn trùng nghĩa để chỉ còn một đáp án.',
    options={'a':'Sơ thảo lần thứ nhất những luận cương về vấn đề dân tộc và vấn đề thuộc địa','b':'Sơ thảo lần thứ hai về vấn đề dân tộc và thuộc địa'})
repair('e9lwce',67,'Các lựa chọn nguồn chồng lấn; làm rõ cặp nền tảng tư tưởng đầy đủ, không coi hai thành tố riêng lẻ là các nền tảng tách biệt.',
    prompt='Cặp nền tảng tư tưởng và kim chỉ nam cho hành động của Đảng được khẳng định đầy đủ là gì?',
    options={'a':'Chỉ có chủ nghĩa Mác–Lênin','b':'Chỉ có tư tưởng Hồ Chí Minh','d':'Chỉ có chủ nghĩa yêu nước'})
repair('e9lwce',70,'Nguồn ghi 5/1908 nhưng Tiểu sử Bảo tàng Hồ Chí Minh ghi 4/1908. Sửa lựa chọn theo nguồn chính thống; giữ nguyên bản gốc trong Word.',
    options={'a':'Tháng 4/1908'}, explanation='Tiểu sử do Bảo tàng Hồ Chí Minh biên soạn ghi Nguyễn Tất Thành tham gia biểu tình chống thuế Thừa Thiên tháng 4/1908. Bản Azota ghi tháng 5/1908; không dùng mốc đó để chấm.',
    keywords=['chống thuế Thừa Thiên','4/1908'])

repair('rnaeqk',7,'Hai lựa chọn đồng nghĩa; thay phương án sở hữu chung để câu điền từ có một đáp án.',options={'d':'Của một nhóm có đặc quyền'})
repair('rnaeqk',13,'Làm rõ việc vận dụng hình ảnh thơ vào hoạt động cách mạng, thay phương án tổng hợp không phân biệt được ý hỏi.',
    prompt='Khi vận dụng hình ảnh thế, thời trong bài Học đánh cờ vào hoạt động cách mạng, nội dung nào được nhấn mạnh?',
    options={'a':'Chỉ nghiên cứu nguồn gốc tự nhiên của con người','c':'Chỉ học quy tắc chơi cờ để giải trí','d':'Chỉ học niên đại các triều vua'})
repair('rnaeqk',20,'Phân biệt lực lượng trong nước với đoàn kết quốc tế.',prompt='Theo Hồ Chí Minh, lực lượng trong nước của cách mạng giải phóng dân tộc bao gồm ai?')
repair('rnaeqk',23,'Thay phương án tổng hợp bằng phát biểu đầy đủ đặc điểm lớn nhất theo giáo trình.',
    prompt='Chọn phát biểu đầy đủ nhất về đặc điểm lớn nhất của thời kỳ quá độ lên CNXH ở Việt Nam.',
    options={'a':'Từ nước nông nghiệp lạc hậu tiến thẳng lên CNXH, không trải qua giai đoạn phát triển tư bản chủ nghĩa'})
repair('rnaeqk',25,'Thay tham chiếu A/B bằng nội dung độc lập vị trí.',
    options={'d':'Cả hai luận điểm: tự nỗ lực giải phóng và đem sức ta tự giải phóng cho ta'})
repair('rnaeqk',30,'Xác định chính xác văn kiện chứa câu trích, không gộp Chánh cương với Sách lược.',options={'b':'Chánh cương vắn tắt của Đảng'})
repair('rnaeqk',31,'Phương án người lao động chồng lấn với nhân dân; thay nhiễu để xác định chủ thể quyền lực duy nhất.',options={'a':'Chỉ người đứng đầu các nhà máy'})
repair('rnaeqk',40,'Câu nguồn bị thiếu chủ ngữ “của người khác”; làm rõ câu nào Hồ Chí Minh tiếp thu từ học thuyết khác.',
    prompt='Trong các câu sau, câu nào là nội dung chủ nghĩa Tam dân của Tôn Trung Sơn được Hồ Chí Minh tiếp thu?')
repair('rnaeqk',50,'Các lựa chọn nguồn chồng lấn; bỏ lựa chọn tổng hợp để chọn phát biểu đầy đủ nhất.',
    prompt='Chọn phát biểu đầy đủ nhất về thực chất giải phóng dân tộc theo tư tưởng Hồ Chí Minh.',
    options={'d':'Duy trì chế độ thuộc địa dưới một hình thức bảo hộ mới'})
repair('rnaeqk',69,'Nguồn ghi sai 11/1941; Hội nghị Trung ương 8 do Nguyễn Ái Quốc chủ trì là tháng 5/1941.',options={'a':'Hội nghị Trung ương 8 (5/1941)'})
for number, answer in [(89,'d'),(122,'b')]:
    repair('rnaeqk',number,'Nhân dân và nhân dân lao động đều có thể mô tả chế độ; thay lựa chọn chồng lấn để không chấm một ý đúng thành sai.',options={answer:'Do một nhóm có đặc quyền làm chủ'})
repair('rnaeqk',92,'Viết phương án kết hợp không phụ thuộc chữ A/B.',options={'d':'Kết hợp lợi ích vật chất với các động lực chính trị–tinh thần'})
repair('rnaeqk',97,'Nguồn chép sai câu nói; làm rõ thiếu mục tiêu đi tới xã hội cộng sản trong phương hướng Cương lĩnh 1930.',
    prompt='Phát hiện phương án viết thiếu mục tiêu cuối cùng trong phương hướng Cương lĩnh đầu tiên năm 1930: làm tư sản dân quyền cách mạng và thổ địa cách mạng để đi tới xã hội cộng sản.',
    options={'a':'Làm tư sản dân quyền cách mạng và thổ địa cách mạng để đi tới xã hội cộng sản','b':'Chỉ dừng ở tư sản dân quyền cách mạng và thổ địa cách mạng','c':'Đi tới xã hội cộng sản sau cách mạng dân quyền và ruộng đất','d':'Gắn cách mạng dân quyền và ruộng đất với mục tiêu xã hội cộng sản'},
    explanation='Phần bị thiếu là mục tiêu đi tới xã hội cộng sản. Không học câu chép sai trong bản gốc như một lời trích nguyên văn của Hồ Chí Minh.',keywords=['đi tới','xã hội cộng sản'])
repair('rnaeqk',101,'Viết đầy đủ nội dung lựa chọn kết hợp thay tham chiếu A/B.',options={'d':'Giải phóng dân tộc, giải phóng giai cấp và giải phóng con người'})
repair('rnaeqk',119,'Làm rõ mốc viết và mốc xuất bản, dựa theo biên niên Bảo tàng.',
    explanation='Đó là Lịch sử nước ta, viết khoảng nửa sau năm 1941, xuất bản lần đầu tháng 2/1942. Không nhầm năm viết với năm xuất bản.')
repair('rnaeqk',121,'Thay phương án sở hữu chung trùng nghĩa với của chung.',options={'a':'Tài sản riêng của cán bộ quản lý'})
repair('rnaeqk',126,'Sửa câu thơ từ thuộc sử ta thành biết sử ta; câu hỏi chỉ hỏi lời nhắc trực tiếp, không gộp các hàm ý tùy cách hiểu.',
    prompt='Lời nhắc trực tiếp trong câu “Dân ta phải biết sử ta; Cho tường gốc tích nước nhà Việt Nam” là gì?',
    options={'a':'Không cần tìm hiểu lịch sử dân tộc','b':'Chỉ học lịch sử các nước khác','c':'Chỉ ghi nhớ tên nhân vật mà không hiểu lịch sử'})
repair('rnaeqk',146,'Các lựa chọn gần nghĩa; dùng phát biểu tính chất đầy đủ theo giáo trình 2019.',
    prompt='Theo cách trình bày trong giáo trình 2019, tính chất của thời kỳ quá độ lên CNXH ở Việt Nam được mô tả đầy đủ nhất như thế nào?',
    options={'d':'Cải biến sâu sắc nhất nhưng phức tạp, lâu dài, khó khăn, gian khổ'})

for number in [17,58]:
    repair('ela4jq',number,'Làm rõ đang hỏi nền tảng pháp lý của nhà nước, tránh lẫn với các đặc điểm dân chủ nói chung.',
        prompt='Yêu cầu đầu tiên về nền tảng pháp lý để xây dựng nhà nước có hiệu lực pháp lý mạnh mẽ là gì?')
for number in [22,59]:
    repair('ela4jq',number,'Thiểu số phục tùng đa số là nội dung đúng của tập trung dân chủ. Sửa nhiễu thành quy tắc đảo ngược, không dạy điều đúng thành sai.',
        options={'c':'Đa số phục tùng thiểu số'}, explanation='Quy tắc sai là đa số phục tùng thiểu số. Tập trung dân chủ yêu cầu thiểu số phục tùng đa số, cấp dưới phục tùng cấp trên.')
repair('ela4jq',23,'Không gọi một đặc điểm đúng của nhà nước dân chủ là sai; hỏi rõ đặc trưng của dân thay vì vì dân.',
    prompt='Trong các ý sau, ý nào trực tiếp nói về quyền làm chủ của dân, thay vì mô tả mục đích phục vụ của nhà nước vì dân?',
    explanation='Do nhân dân làm chủ trực tiếp nói tới chủ thể quyền lực. Vì dân nhấn mạnh mục đích phục vụ lợi ích và đời sống nhân dân. Đây là phân biệt khía cạnh, không phủ nhận quyền làm chủ.')
repair('ela4jq',24,'Cả bốn lựa chọn nguồn đều đúng; chuyển lựa chọn cuối thành phương án tổng hợp.',options={'d':'Cả ba phương án còn lại'})
repair('ela4jq',37,'Sửa đủ sức, đủ tài thành đủ đức, đủ tài, đúng yêu cầu cán bộ.',options={'c':'Nhà nước có đội ngũ cán bộ, công chức đủ đức, đủ tài'})
repair('ela4jq',40,'Tám chữ được nêu tại lễ ra mắt Đảng Lao động ngày 3/3/1951, không đồng nhất sự kiện này với Đại hội II.',options={'a':'Lễ ra mắt Đảng Lao động Việt Nam ngày 3/3/1951'})
repair('ela4jq',41,'Các phẩm chất nguồn có thể cùng đúng; thay nhiễu để chỉ còn một yêu cầu đúng.',
    options={'a':'Chỉ cần bằng cấp, không cần trách nhiệm','c':'Tự đặt mình đứng trên nhân dân','d':'Không cần tu dưỡng đạo đức'})
repair('ela4jq',43,'Nguồn thiếu số thập kỷ; bỏ phần lỗi, giữ nguyên câu hỏi về yếu tố phong trào yêu nước.',
    prompt='Điền cụm từ: Đảng Cộng sản Việt Nam ra đời từ sự kết hợp chủ nghĩa Mác–Lênin với phong trào công nhân và ...')
repair('ela4jq',44,'Hai phương án nguồn cùng mô tả do dân; làm rõ phát biểu đầy đủ và thay một nhiễu chồng lấn.',
    prompt='Chọn phát biểu đầy đủ nhất về nhà nước do dân.',options={'b':'Nhà nước do một nhóm ít người tự lập và tự quản lý'})
repair('ela4jq',60,'Phân biệt quyền lực thuộc dân với việc dân bầu đại biểu; thay phương án tổng hợp gây nhiều cách hiểu.',
    prompt='Điểm cốt lõi về chủ thể quyền lực của nhà nước của dân là gì?',options={'d':'Quyền lực chỉ thuộc về một nhóm cán bộ'})
repair('ela4jq',81,'Làm rõ câu hỏi về chủ nghĩa làm cốt trong tư tưởng xây dựng Đảng, không phủ nhận tư tưởng Hồ Chí Minh trong nền tảng hiện hành.',
    prompt='Học thuyết nào được Hồ Chí Minh nhấn mạnh làm nền tảng lý luận khi bàn về xây dựng Đảng cách mạng?',
    explanation='Học thuyết được hỏi là chủ nghĩa Mác–Lênin. Còn nền tảng tư tưởng được Đảng khẳng định từ Đại hội VII gồm cả chủ nghĩa Mác–Lênin và tư tưởng Hồ Chí Minh.')
repair('ela4jq',88,'Thay lựa chọn nhân dân lao động chồng lấn với nhân dân.',options={'d':'Do một nhóm có đặc quyền làm chủ'})

repair('ijqzcg',12,'Cả tòa án và Nhà nước đều không phải thành viên Mặt trận; thay phương án Nhà nước bằng một tổ chức thành viên để có một đáp án.',options={'d':'Đoàn Thanh niên Cộng sản Hồ Chí Minh'},
    explanation='Tòa án là cơ quan nhà nước, không phải tổ chức thành viên Mặt trận. Đảng và các tổ chức chính trị–xã hội tham gia Mặt trận.')
repair('ijqzcg',19,'Khôi phục đầy đủ khẩu hiệu bị chép thiếu; thêm thời điểm để xác định lần phát biểu đang hỏi.',
    prompt='Tại sự kiện nào năm 1961, Hồ Chí Minh nhắc lại bài học “Đoàn kết, đoàn kết, đại đoàn kết; Thành công, thành công, đại thành công”?')
repair('ijqzcg',24,'Giới hạn câu hỏi vào sức mạnh nội lực để tránh chồng lấn với phương án kết hợp quốc tế.',
    prompt='Theo tư tưởng Hồ Chí Minh, yếu tố nào trong nội lực dân tộc có ý nghĩa chiến lược, quyết định thành công cách mạng?')
repair('ijqzcg',26,'Dĩ bất biến, ứng vạn biến đồng nghĩa với lựa chọn kết hợp; thay nhiễu trùng nghĩa.',
    prompt='Chọn cách kết hợp đầy đủ nhất giữa nguyên tắc và sách lược ngoại giao theo tư tưởng Hồ Chí Minh.',options={'d':'Thay đổi cả mục tiêu độc lập dân tộc để nhận viện trợ'})
repair('ijqzcg',33,'Hai phương án nguồn đồng nghĩa; thay một nhiễu để có đáp án duy nhất.',
    prompt='Chọn cách kết hợp đầy đủ nhất giữa nguyên tắc và sách lược ngoại giao theo tư tưởng Hồ Chí Minh.',options={'a':'Thay đổi mục tiêu chiến lược để nhận viện trợ'})
repair('ijqzcg',38,'Hai lựa chọn diễn đạt tương đương; đổi các nhiễu thành phạm vi chỉ một nhóm để hỏi đầy đủ ba lực lượng.',
    prompt='Chọn phương án bao quát đầy đủ ba nhóm lực lượng cần đoàn kết quốc tế theo Hồ Chí Minh.',
    options={'a':'Chỉ phong trào cộng sản và công nhân thế giới','b':'Chỉ phong trào giải phóng dân tộc','d':'Chỉ các lực lượng tiến bộ yêu chuộng hòa bình'})
repair('ijqzcg',39,'Bỏ từ hiện nay không gắn văn kiện, thời điểm; hỏi đúng vai trò đại đoàn kết trong bài học.',
    prompt='Theo nội dung tư tưởng đại đoàn kết, sức mạnh nào được coi là động lực to lớn cho phát triển đất nước?')
repair('ijqzcg',42,'Phân biệt vai trò giúp đỡ quốc tế với nội lực theo đúng nguyên tắc tự lực, không xếp hạng thắng lợi khi thiếu bối cảnh.',
    prompt='Theo nguyên tắc dựa vào sức mình là chính, sự giúp đỡ quốc tế có vai trò như thế nào?',
    options={'a':'Thay thế hoàn toàn nội lực','b':'Quyết định duy nhất, nội lực không cần thiết','d':'Chỉ có ý nghĩa khi Việt Nam từ bỏ tự chủ'})
repair('ijqzcg',43,'Hai lựa chọn nguồn gần tương đương; thay nhiễu để giữ một phương án gồm đủ hai nguyên tắc.',options={'d':'Thống nhất mục tiêu, lợi ích nhưng phải phụ thuộc vào viện trợ nước ngoài'})

repair('3eggrt',17,'Đối chiếu bài gốc ký T.L.; ghi cả dạng chữ ký và tên bút danh trong đáp án.',options={'d':'T.L. (Trần Lực)'})
repair('3eggrt',21,'Ba tính chất gắn với giai đoạn văn hóa mới trong kháng chiến chống Pháp; không khẳng định mọi thời kỳ đều dùng cùng một cách gọi.',
    prompt='Trong kháng chiến chống Pháp, nền văn hóa mới được Hồ Chí Minh khẳng định có ba tính chất nào?')
repair('3eggrt',27,'Làm rõ đoạn trích về công việc đối với con người, tránh lẫn với lời căn dặn chỉnh đốn Đảng trước tiên.',
    prompt='Cụm “Đầu tiên là công việc đối với...” trong Di chúc nêu lĩnh vực công việc nào?',
    explanation='Trong đoạn bàn công việc sau chiến thắng, Hồ Chí Minh nhấn mạnh công việc đối với con người. Không nhầm với đoạn căn dặn việc cần làm trước tiên là chỉnh đốn lại Đảng.')
repair('3eggrt',32,'Diễn đạt lại ý hỏi thay vì coi câu chép không hoàn toàn nguyên văn là trích dẫn chuẩn.',prompt='Quan điểm “còn sống còn phải học”, học không bao giờ cùng gắn với ai?')
repair('3eggrt',42,'Câu nguồn pha thêm cả dân tộc vào lời Lênin. Chuẩn hóa câu, giữ đúng tác giả được nguồn chính thống dẫn.',
    prompt='Luận điểm Đảng là “trí tuệ, danh dự và lương tâm của thời đại” gắn với ai?')
repair('3eggrt',49,'Đức, tài là một cách nói đúng khác của giáo dục toàn diện; thay nhiễu chồng lấn để không chấm ý đúng thành sai.',
    options={'c':'Chỉ giáo dục tài năng, không cần đạo đức'})
repair('3eggrt',53,'Hồ Chí Minh có nhiều bài cùng tên Đạo đức cách mạng; thêm năm 1958 để xác định chính xác tác phẩm.',
    prompt='Tác phẩm Đạo đức cách mạng viết tháng 12/1958 được in lần đầu trên tạp chí nào?')
repair('3eggrt',58,'Các vai trò tác giả, phê bình có thể cùng đúng; xác định trực tiếp vai trò trên mặt trận và thay phương án tổng hợp.',
    prompt='Trong quan điểm văn nghệ là một mặt trận, vai trò cách mạng của người nghệ sĩ là gì?',
    options={'a':'Chỉ sáng tác cho bản thân, tách khỏi nhân dân','c':'Chỉ phê bình, không tham gia đời sống cách mạng','d':'Đứng ngoài cuộc đấu tranh của nhân dân'})
repair('3eggrt',63,'Lời giải đi thẳng vào hai công cụ quản lý, phân biệt pháp trị với đức trị.',
    explanation='Pháp trị là quản lý bằng pháp luật; đức trị là phát huy đạo đức và truyền thống tốt đẹp. Hồ Chí Minh kết hợp cả hai, không tách pháp luật khỏi giáo dục đạo đức.',keywords=['pháp trị','đức trị','kết hợp'])
repair('3eggrt',71,'Hai phương án nguồn chỉ đảo thứ tự từ mà cùng nghĩa; thay nhiễu để không dạy phát triển văn hóa cùng kinh tế là sai.',
    options={'a':'Chỉ phát triển văn hóa, bỏ qua kinh tế','b':'Không cần phát triển kinh tế và văn hóa'},
    explanation='Phải phát triển cả kinh tế và văn hóa. Kinh tế tạo điều kiện vật chất; văn hóa tác động trở lại. Không coi một cách đảo thứ tự hai từ là một quan điểm sai.')
repair('3eggrt',74,'Phân biệt lập trường giai cấp với ba nguyên tắc xây dựng đạo đức; chỉnh câu hỏi về lập trường.',
    prompt='Theo tư tưởng Hồ Chí Minh, xây dựng đạo đức cách mạng phải đứng trên lập trường giai cấp nào?')

repair('n6fnzo',3,'Bỏ đoạn phương án của câu khác bị dính vào đề.',prompt='Tài liệu nào chuẩn bị mọi mặt về chính trị, tư tưởng và tổ chức cho sự ra đời của Đảng Cộng sản Việt Nam?')
repair('n6fnzo',4,'Làm rõ căn cứ pháp lý; sự ủng hộ nói chung không tự nó xác định tính hợp hiến.',
    prompt='Nhà nước hợp hiến có nền tảng pháp lý trực tiếp nào?',options={'b':'Chỉ dựa vào quyết định tùy ý của người đứng đầu'})
repair('n6fnzo',12,'Hỏi danh mục trong giáo trình, không phủ nhận ích lợi của hoạt động đoàn kết thực tế.',
    prompt='Ý nào không phải tên một trong ba phương thức xây dựng đại đoàn kết được liệt kê trong giáo trình?')
repair('n6fnzo',14,'Bỏ mảnh văn bản bị dính từ một lựa chọn khác.',prompt='Đâu là các điều kiện xây dựng khối đại đoàn kết toàn dân tộc theo Hồ Chí Minh?')
repair('n6fnzo',33,'Không khẳng định Mặt trận quy tụ mọi cá nhân, tổ chức bất kể mục tiêu; bổ sung điều kiện yêu nước.',
    options={'c':'Nơi quy tụ các tổ chức và cá nhân yêu nước trong và ngoài nước'})
repair('n6fnzo',35,'Bổ sung từ chỉ bị thiếu trong câu nguồn.',prompt='Hồ Chí Minh dùng hình tượng nào để chỉ chủ nghĩa tư bản?')
repair('n6fnzo',46,'Diễn đạt trực tiếp chỉ đạo có thể là sự kiện đúng nhưng không phải tiêu chí phân biệt giá trị; thay nhiễu bằng nhận định sai rõ ràng.',
    options={'d':'Chỉ có giá trị trong một thời kỳ đã qua, không còn ý nghĩa hiện nay'},
    explanation='Sai ở chỗ giới hạn tư tưởng Hồ Chí Minh vào quá khứ. Giáo trình khẳng định giá trị nền tảng, định hướng của tư tưởng này đối với cách mạng Việt Nam và thế giới.')
repair('n6fnzo',59,'Làm rõ ba ý nghĩa được liệt kê, không khẳng định học môn này không hỗ trợ môn khác.',
    prompt='Ý nào không phải tên một trong ba ý nghĩa học tập môn Tư tưởng Hồ Chí Minh được liệt kê trong giáo trình?')
repair('n6fnzo',69,'Làm rõ danh mục yêu cầu cán bộ trong bài học, không suy diễn thành cấm phát triển kinh tế chính đáng.',
    prompt='Yêu cầu nào không thuộc danh mục yêu cầu cán bộ, đảng viên được liệt kê trong bài học?')
repair('n6fnzo',78,'Văn hóa ở trong chính trị và phục vụ chính trị đều đúng; thay lựa chọn chồng lấn để có một đáp án.',options={'b':'Văn hóa tách rời mọi nhiệm vụ chính trị'})
repair('n6fnzo',95,'Loại ghi chú tranh luận bị chèn trong phương án. Phân biệt tên ba vai trò với khẳng định về chủ thể xây dựng văn hóa; không dùng key LMS mâu thuẫn.',
    prompt='Ý nào không phải tên một trong ba vai trò của văn hóa được trình bày trong giáo trình 2019?',
    options={'b':'Văn hóa là mục tiêu, động lực của sự nghiệp cách mạng'},
    explanation='Ba vai trò được liệt kê là mục tiêu–động lực, một mặt trận và phục vụ quần chúng. Sự nghiệp của quần chúng nói về chủ thể xây dựng văn hóa, không phải tên một trong ba vai trò. Không hiểu ý này là phủ nhận vai trò của nhân dân.',keywords=['ba vai trò','mục tiêu–động lực','chủ thể'])

EXPLANATIONS = {
 'azota-e9lwce-015':'Phạm vi là toàn bộ cách mạng Việt Nam, gồm cả cách mạng dân tộc dân chủ nhân dân và cách mạng XHCN; không chỉ giới hạn ở một giai đoạn.',
 'azota-e9lwce-030':'Tiếp thu chủ nghĩa Mác–Lênin giúp Nguyễn Ái Quốc chuyển từ người yêu nước thành người cộng sản. Không nhầm với chủ nghĩa yêu nước vốn là điểm xuất phát.',
 'azota-e9lwce-066':'Người sinh ngày 19/5/1890 và ra đi ngày 5/6/1911, lúc đã tròn 21 tuổi.',
 'azota-rnaeqk-001':'Câu đúng là Không có gì quý hơn độc lập, tự do. Lựa chọn dùng chữ bằng đã làm sai câu nói đang được hỏi.',
 'azota-rnaeqk-024':'Mâu thuẫn chủ yếu ở xã hội thuộc địa là dân tộc bị áp bức với thực dân xâm lược. Mâu thuẫn nông dân–địa chủ cũng tồn tại nhưng không phải mâu thuẫn chủ yếu đang hỏi.',
 'azota-rnaeqk-062':'Sai ở chỗ coi tất cả địa chủ, tư sản đều là đối tượng phải đánh đổ. Cần phân hóa, tập hợp lực lượng; không đồng nhất xóa áp bức với tiêu diệt con người.',
 'azota-rnaeqk-067':'Cương lĩnh đầu tiên nêu đánh đổ đế quốc Pháp và phong kiến, làm cho nước Nam hoàn toàn độc lập; ba nội dung đều thuộc mục tiêu chính trị.',
 'azota-rnaeqk-080':'Lòng nhân ái, đức hy sinh được bài học gắn với Kitô giáo, không phải Hồi giáo. Ba nguồn phương Đông còn lại trong lựa chọn thuộc nội dung được trình bày.',
 'azota-rnaeqk-081':'Sai ở việc đặt giải phóng giai cấp lên trước hết trong hoàn cảnh Việt Nam thuộc địa. Nhiệm vụ trước hết là giải phóng dân tộc.',
 'azota-rnaeqk-083':'Thời kỳ quá độ có nhiều hình thức sở hữu: Nhà nước, hợp tác xã, người lao động riêng lẻ và một bộ phận tư liệu sản xuất tư nhân; không đồng nhất quá độ với công hữu hoàn toàn ngay lập tức.',
 'azota-rnaeqk-087':'Thực dân, đế quốc dùng bạo lực áp bức dân tộc; phải dùng bạo lực cách mạng chống bạo lực phản cách mạng. Điều này gắn với việc tranh thủ hòa bình, không cổ súy chiến tranh bằng mọi giá.',
 'azota-rnaeqk-092':'Phải kết hợp lợi ích, nhu cầu vật chất với động lực chính trị–tinh thần để phát huy con người. Không chỉ tác động vào một mặt.',
 'azota-rnaeqk-116':'Đối với tư sản dân tộc, chủ trương là hướng dẫn, giúp đỡ cải tạo theo CNXH, trở thành người lao động; không tiêu diệt con người hay tịch thu tùy tiện tài sản.',
 'azota-ela4jq-003':'Đảng phục vụ lợi ích giai cấp công nhân thống nhất với lợi ích nhân dân và toàn dân tộc, không hoạt động vì lợi ích riêng của tổ chức Đảng.',
 'azota-ela4jq-036':'Vai trò lãnh đạo xuất phát từ đặc tính, vị trí kinh tế–xã hội của giai cấp công nhân, không do số lượng đông hay ý muốn chủ quan.',
 'azota-ela4jq-077':'Đoạn căn dặn về sau thắng lợi nói việc cần làm trước tiên là chỉnh đốn lại Đảng. Không nhầm với đoạn riêng nhấn mạnh công việc đối với con người.',
 'azota-3eggrt-012':'Con người là vốn quý nhất và là nhân tố quyết định thành công cách mạng; đáp án đầy đủ phải có cả vị trí quý nhất và vai trò quyết định.',
 'azota-3eggrt-030':'Con người là vốn quý nhất, nhân tố quyết định thành công cách mạng. Phương án chỉ nói quan trọng hoặc vốn quý chưa diễn đạt đầy đủ.',
 'azota-3eggrt-045':'Con người là vốn quý nhất, nhân tố quyết định thành công cách mạng; không chỉ là một bộ phận tham gia.',
 'azota-3eggrt-057':'Chữ Người được xét từ phạm vi hẹp (gia đình, bầu bạn), rộng (đồng bào cả nước) đến rộng nữa (cả loài người); không giới hạn vào một cấp độ.',
}

# Remove remaining equivalent alternatives instead of marking a correct idea wrong.
repair('3eggrt',28,'Người lao động và nhân dân chồng lấn về chủ thể; thay nhiễu để có một đáp án.',options={'b':'Chỉ cán bộ cơ quan nhà nước'})
for code,number in [('rnaeqk',2),('rnaeqk',28),('rnaeqk',103),('rnaeqk',63),('3eggrt',12),('3eggrt',30)]:
    REPAIRS[f'azota-{code}-{number:03}']={'note':'Làm rõ yêu cầu chọn phát biểu đầy đủ nhất, phân biệt với các lựa chọn chỉ nêu một phần.','prompt':None,'options':None,'explanation':None,'keywords':None,'fullest':True}

# Each row was read with all four options; no positional key scraped from Azota.
answers('e9lwce', '''
1:d:lenin-theses 2:b:theoretical 3:a:letter1928 4:a:chinh-cuong 5:a:eastern
6:b:versailles 7:d:west 8:c:eulogy 9:c:jesus 10:a:usa-years
11:d:phase2 12:a:book1927 13:d:tam-dan-fit 14:d:origins-all 15:c:definition-full
16:b:definition-full 17:d:definition-full 18:b:confucius 19:c:marx-humanity 20:c:unesco
21:d:demands1919 22:c:confucius 23:d:congress7 24:b:soi-duong 25:c:vo-san
26:c:buddhism 27:d:unesco 28:a:patriotism 29:b:duong-kach-menh 30:a:theoretical
31:b:patriotism 32:a:phase1 33:d:theoretical 34:b:declaration 35:a:predecessors
36:a:foundation 37:d:congress7 38:d:uk-years 39:a:predecessors 40:b:lenin-path
41:b:book1925 42:b:duc-thanh-years 43:b:book1927 44:b:lenin-theses 45:c:west
46:d:jobs 47:a:self-reliance 48:d:soi-duong 49:c:phase3 50:d:unity-origins
51:d:marx-method 52:d:origins-all 53:d:buddhism 54:c:marx-method 55:d:return1928
56:c:duc-thanh-years 57:c:departure 58:d:human-love 59:a:history-poem 60:a:youth1925
61:b:versailles 62:a:purpose 63:d:departure 64:b:west 65:a:lenin-theses
66:a:departure 67:c:foundation 68:a:final-wish 69:b:versailles 70:a:tax1908 71:d:tours
''')

answers('rnaeqk', '''
1:a:independence1966 2:a:transition-steps 3:d:economy 4:d:active-colonies 5:d:transition
6:b:obstacles 7:a:economy 8:c:national-before-class 9:a:forces-all 10:d:national-socialism
11:b:national-socialism 12:d:distribution 13:b:chess-strategy 14:b:declaration 15:c:declaration
16:d:oriental-marx 17:d:obstacles 18:d:political-stability 19:a:class-liberation 20:a:forces-all
21:c:return1941 22:d:foreign-capital 23:a:transition 24:a:classes 25:d:self-reliance
26:d:people-resources 27:a:happiness-science 28:c:transition-steps 29:c:economy 30:b:chinh-cuong
31:b:political-owner 32:c:return1941 33:c:individual-interest 34:a:obstacles 35:a:lenin-colonies
36:d:resistance-line 37:c:human-motivation 38:b:self-reliance 39:d:violence 40:d:tam-dan
41:c:national-socialism 42:d:oriental-marx 43:d:revolution-not-through 44:b:illiteracy 45:d:active-colonies
46:c:khoan 47:d:people-resources 48:c:independence 49:d:oriental-marx 50:c:national-liberation
51:d:party-role 52:d:obstacles 53:d:socialism 54:d:independence 55:b:chinh-cuong
56:b:national-liberation 57:d:socialism-approach 58:a:political-owner 59:d:economy 60:b:vo-san
61:d:party-role 62:c:obstacles 63:d:transition 64:b:nationalism 65:d:forces-all
66:a:national-before-class 67:a:chinh-cuong 68:d:lenin-path 69:a:return1941 70:c:industrialization
71:a:state-economy 72:b:transition 73:c:progress-need 74:c:economy 75:c:vo-san
76:b:national-liberation 77:a:nationalism 78:d:bird-wings 79:a:party-role 80:d:west
81:c:national-before-class 82:b:forces-all 83:d:state-economy 84:b:independence 85:c:party-role
86:d:transition-steps 87:d:violence 88:a:national-before-class 89:c:political-owner 90:b:transition
91:d:transition 92:d:human-motivation 93:d:versailles 94:c:self-reliance 95:a:leech
96:a:socialism-goal 97:b:vo-san 98:d:khoan 99:a:peace-violence 100:a:forces-combined
101:d:purpose 102:a:violence 103:a:transition-steps 104:c:economy 105:a:national-before-class
106:c:transition-tasks 107:c:national-liberation 108:a:party-founder 109:c:national-socialism 110:d:transition-steps
111:d:party-role 112:b:independence 113:a:independence 114:d:human-socialist 115:d:human-role
116:a:state-economy 117:d:vo-san 118:d:human-socialist 119:d:history-poem 120:c:obstacles
121:d:economy 122:a:political-owner 123:c:oriental-marx 124:c:happiness-science 125:c:human-liberation
126:d:history-poem 127:b:oriental-marx 128:c:national-socialism 129:c:agriculture 130:b:van-phuc
131:c:return1941 132:c:final-wish 133:c:industrialization 134:a:party-role 135:d:independence
136:d:august-call 137:a:declaration 138:c:state-economy 139:d:national-liberation 140:d:economy
141:a:leech 142:b:national-liberation 143:b:human-liberation 144:a:loseby 145:c:active-colonies
146:d:transition 147:d:national-liberation 148:d:national-socialism
''')

answers('ela4jq', '''
1:c:party-purpose 2:b:party-civilized 3:c:party-purpose 4:b:democracy 5:a:party-foundation
6:c:party-class 7:b:democracy 8:b:party-role 9:a:criticism 10:c:obstacles
11:b:internal-enemy 12:a:democracy 13:a:foundation 14:c:party-renewal 15:c:party-purpose
16:d:democracy 17:c:constitutional 18:d:party-birth 19:b:party-role 20:d:state-class
21:a:party-class 22:c:centralism 23:c:democracy 24:d:democracy 25:d:party-leads-state
26:b:party-class 27:a:party-renewal 28:b:party-dichuc 29:a:party-birth 30:c:party-dichuc
31:b:party-founder 32:b:party-foundation 33:c:party-foundation 34:d:party-role 35:d:party-names
36:b:party-class 37:d:law 38:d:party-birth 39:b:party-leads-state 40:a:party-launch1951
41:b:cadres 42:d:party-birth 43:d:party-birth 44:d:democracy 45:b:party-dichuc
46:d:party-principles 47:d:education-lifelong 48:d:democracy 49:a:party-role 50:b:party-names
51:a:party-renewal 52:b:clean-state 53:d:party-role 54:a:patriotism 55:d:party-founder
56:d:party-birth 57:c:internal-enemy 58:c:constitutional 59:c:centralism 60:a:democracy
61:b:party-names 62:d:cadre-role 63:d:party-dichuc 64:d:state-class 65:c:party-class
66:a:party-role 67:b:centralism 68:d:democracy 69:c:democracy 70:b:democracy
71:c:party-class 72:c:party-birth 73:c:centralism 74:c:party-dichuc 75:c:letter-committees
76:a:party-class 77:c:party-dichuc 78:d:democracy 79:d:party-role 80:c:internal-enemy
81:a:party-foundation 82:d:party-purpose 83:b:law 84:c:final-wish 85:c:party-class
86:a:party-dichuc 87:b:party-role 88:b:political-owner
''')

answers('ijqzcg', '''
1:c:ho-slogan 2:b:unity-foundation 3:b:democratic-friends 4:a:self-reliance 5:d:nation-strength
6:c:nationalism 7:a:democratic-friends 8:d:unity-foundation 9:c:unity-foundation 10:b:unity-foundation
11:d:three-fronts 12:c:front 13:b:ho-slogan 14:a:unity-goal 15:c:unity-role
16:a:party-dichuc 17:b:self-reliance 18:b:ho-slogan 19:b:unity-success 20:c:international-strength
21:c:nation-strength 22:d:vietminh 23:c:self-reliance 24:d:unity-role 25:a:unity-role
26:a:diplomacy 27:a:unity-foundation 28:d:unity-goal 29:c:international-principles 30:a:unity-role
31:d:unity-origins 32:a:party-dichuc 33:d:diplomacy 34:b:unity-goal 35:b:unity-role
36:c:unity-goal 37:b:front1939 38:c:international-forces 39:b:unity-role 40:a:four-seas
41:d:unity-origins 42:c:self-reliance 43:c:international-principles 44:c:self-reliance
''')

answers('3eggrt', '''
1:a:education-all 2:b:human-specific 3:a:culture-nature 4:b:highest-ethics 5:b:ethics-principles
6:d:new-life 7:d:culture-functions 8:d:ethics1958 9:a:human-specific 10:c:internal-enemy
11:a:human-motivation 12:b:human-role 13:c:culture-position 14:d:ethics-standards 15:b:ethics-principles
16:a:individual-interest 17:d:ethics1969 18:a:artist 19:b:artist 20:c:lifelong
21:d:culture-nature 22:d:new-life 23:c:ethics-root 24:d:ethics-standards 25:d:new-life
26:a:human-nature 27:d:human-role 28:d:political-owner 29:b:criticism 30:a:human-role
31:c:culture-definition 32:a:education-lifelong 33:c:ethics-root 34:d:ethics-root 35:a:chinh-relations
36:d:early-ethics 37:a:fairness1966 38:d:ethics-principles 39:a:education-all 40:d:culture-functions
41:a:youth-spring 42:b:lenin-party 43:c:ethics-root 44:a:obstacles 45:c:human-role
46:d:party-dichuc 47:d:confucius-liem 48:c:culture-position 49:d:education-all 50:a:highest-ethics
51:b:highest-ethics 52:a:human-nature 53:a:ethics1958 54:d:ethics-standards 55:a:youth-awaken
56:c:ethics-principles 57:d:human-specific 58:b:artist 59:b:ethics-root 60:a:highest-ethics
61:d:lifelong 62:b:highest-ethics 63:c:law 64:d:ethics-life 65:a:lifelong
66:b:three-relations 67:a:ethics-root 68:c:culture-position 69:d:education-all 70:c:new-life1947
71:c:culture-position 72:c:ethics-root 73:d:artist 74:c:ethics-standards 75:c:ethics1947 76:c:ethics-principles
''')

answers('n6fnzo', '''
1:a:culture-economy 2:a:vo-san 3:a:duong-kach-menh 4:a:constitutional 5:d:definition
6:a:socialism 7:c:phase2 8:c:versailles 9:a:phase3 10:b:congress2
11:d:democracy 12:c:unity-methods 13:c:violence 14:d:unity-conditions 15:b:independence
16:d:phase2 17:a:socialism 18:d:human-role 19:d:ethics-standards 20:d:unity-role
21:c:front 22:b:front 23:c:lenin-theses 24:c:buddhism 25:a:clean-state
26:b:confucius 27:d:party-renewal 28:b:ethics-principles 29:b:army1944 30:d:definition
31:a:international-forces 32:d:transition-tasks 33:c:front 34:b:democracy 35:d:leech
36:d:vietminh 37:d:tax1908 38:b:state-class 39:d:chinh-cuong 40:a:independence1966
41:a:declaration 42:a:phase4 43:d:subjective 44:c:party-principles 45:d:transition-tasks
46:d:value 47:c:transition-tasks 48:a:party-role 49:d:congress6 50:d:three-relations
51:d:identity 52:a:internal-enemy 53:c:party-civilized 54:d:identity 55:c:value
56:c:democracy 57:d:ban-an 58:b:clean-state 59:b:meaning 60:c:party-principles
61:b:transition 62:c:marx-method 63:a:vietminh 64:c:unity-conditions 65:c:method
66:b:clean-state 67:c:socialism 68:b:economy 69:c:cadres 70:c:international-role
71:b:law 72:d:eulogy 73:b:congress4 74:b:tam-dan 75:a:eastern
76:b:marx-method 77:d:congress5 78:a:culture-politics 79:b:international-principles 80:a:party-foundation
81:c:declaration 82:a:transition-tasks 83:d:party-principles 84:a:youth1925 85:a:human-motivation
86:b:culture-society 87:a:lenin-theses 88:c:transition 89:a:jesus 90:b:culture1943
91:c:theoretical 92:c:practical 93:d:phase4 94:b:meaning 95:a:culture-role
''')
