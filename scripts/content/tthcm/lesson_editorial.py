"""Chapter lessons reviewed against all 506 canonical questions and local theory.

Concept IDs are explicit editorial groupings, not similarity-generated assignments.
Question chapters, options, revisions and comprehensive-paper membership stay intact.
"""

CHAPTERS = []


def chapter(number, sections):
    CHAPTERS.append(dict(chapter=number, sections=sections))


def section(ident, title, summary, ids, page, *, milestones=False):
    return dict(id=ident, title=title, summary=summary, conceptIds=ids.split(),
                kind='milestones' if milestones else 'knowledge',
                references=[dict(sourceId='ptit', pdfPage=page, section=title, evidence=summary)])


chapter(1, [
    section('c1-khai-niem', 'Khái niệm: hiểu đủ các thành phần',
        'Nhớ cả bản chất, nguồn gốc và giá trị của tư tưởng Hồ Chí Minh. Khái niệm bàn những vấn đề cơ bản của cách mạng Việt Nam, bao gồm cách mạng dân tộc dân chủ nhân dân và cách mạng xã hội chủ nghĩa.',
        'definition-full definition purpose', 9),
    section('c1-gia-tri', 'Vị trí, giá trị và nền tảng tư tưởng',
        'Tư tưởng Hồ Chí Minh là tài sản tinh thần của Đảng và dân tộc, soi đường cho cách mạng; cùng chủ nghĩa Mác–Lênin tạo thành nền tảng tư tưởng, kim chỉ nam cho hành động của Đảng.',
        'value-definition soi-duong foundation', 9),
    section('c1-nghien-cuu', 'Đối tượng, phương pháp và ý nghĩa học tập',
        'Đối tượng nghiên cứu gồm hệ thống quan điểm của Hồ Chí Minh và quá trình hiện thực hóa những quan điểm ấy trong cách mạng Việt Nam. Phương pháp trả lời cách nghiên cứu; ý nghĩa học tập trả lời việc học giúp rèn luyện điều gì.',
        'method meaning theoretical', 11),
    section('c1-dai-hoi', 'Nhận diện Đại hội qua cụm từ đặc trưng',
        'Ghép đúng số Đại hội, năm và nội dung khẳng định. Phân biệt lần khẳng định nền tảng tư tưởng ở Đại hội VII với cách trình bày khái niệm đầy đủ ở Đại hội XI.',
        'congress2 congress4 congress5 congress6 congress7 congress11', 6, milestones=True),
    section('c1-ghi-nhan', 'Điếu văn và ghi nhận của UNESCO',
        'Phân biệt văn kiện trong nước với nghị quyết UNESCO; phân biệt năm thông qua nghị quyết với năm kỷ niệm 100 năm ngày sinh.',
        'eulogy unesco', 7, milestones=True),
])

chapter(2, [
    section('c2-thuc-tien', 'Bối cảnh Việt Nam và thế giới',
        'Cơ sở thực tiễn là hoàn cảnh xã hội và yêu cầu giải phóng dân tộc. Cần phân biệt bối cảnh này với các nguồn tư tưởng–lý luận và phẩm chất chủ quan của Hồ Chí Minh.',
        'origins-all practical invasion patenotre colonial classes dong-du nghia-thuc predecessors world-contradictions october comintern', 18),
    section('c2-truyen-thong', 'Truyền thống dân tộc và tinh hoa phương Đông',
        'Chủ nghĩa yêu nước là dòng chảy chính của truyền thống dân tộc. Các học thuyết được tiếp thu có chọn lọc: không đồng nhất toàn bộ Nho giáo, Phật giáo, Lão giáo hay Tam dân với tư tưởng Hồ Chí Minh.',
        'patriotism eastern confucius buddhism lao-tu tam-dan tam-dan-fit', 22),
    section('c2-mac-lenin', 'Phương Tây và vai trò quyết định của Mác–Lênin',
        'Phân biệt các giá trị nhân văn phương Tây với chủ nghĩa Mác–Lênin: nguồn sau cung cấp thế giới quan, phương pháp luận và có vai trò quyết định trong bước chuyển sang lập trường cộng sản.',
        'west jesus theoretical marx-method lenin-core lenin-colonies lenin-path marx-humanity oriental-marx', 25),
    section('c2-chu-quan', 'Nhân tố chủ quan của Hồ Chí Minh',
        'Các điều kiện khách quan không tự chuyển thành tư tưởng: phẩm chất, tư duy độc lập và hoạt động thực tiễn của Hồ Chí Minh quyết định cách tiếp thu, vận dụng sáng tạo.',
        'subjective', 27),
    section('c2-giai-doan', 'Năm giai đoạn: nhớ mốc kèm nội dung',
        'Học theo khung giai đoạn của giáo trình đang dùng. Nhớ đặc điểm tư tưởng của từng giai đoạn, không chỉ thuộc năm; đặc biệt phân biệt tìm đường với hình thành nội dung cơ bản và vượt thử thách.',
        'phases phase1 phase2 phase3 phase4', 28, milestones=True),
    section('c2-1911-1920', 'Trước 1920: từ chí hướng cứu nước đến con đường vô sản',
        'Các dấu mốc cần nối thành quá trình: trải nghiệm trước khi ra đi, khảo sát các nước, hoạt động ở Pháp, gửi Yêu sách, đọc Luận cương và lựa chọn con đường cách mạng vô sản.',
        'tax1908 duc-thanh-years departure usa-years uk-years jobs versailles demands1919 socialist-party lenin-theses tours vo-san', 30, milestones=True),
    section('c2-1920-1930', '1920–1930: chuẩn bị tư tưởng, chính trị và tổ chức',
        'Gắn tác phẩm, tổ chức và hoạt động với quá trình chuẩn bị thành lập Đảng. Với câu hỏi tác phẩm, cần nhớ cả nội dung đặc trưng và năm xuất bản.',
        'le-paria youth1925 ban-an book1925 leech duong-kach-menh book1927 letter1928 return1928 death-sentence party-founder chinh-cuong', 31, milestones=True),
    section('c2-1930-1969', 'Vượt thử thách, trở về lãnh đạo và tiếp tục phát triển',
        'Từ giai đoạn vượt thử thách đến lãnh đạo cách mạng trong nước, tư tưởng tiếp tục được bổ sung và phát triển. Các câu liên hệ Tuyên ngôn và độc lập năm 1966 vẫn giữ ở chương này theo ngân hàng.',
        'loseby letter1938 return1941 pac-bo vietminh history-poem army1944 truong-son declaration independence1966', 33, milestones=True),
    section('c2-gia-tri', 'Giá trị đối với Việt Nam và thế giới',
        'Giá trị tư tưởng không kết thúc ở một thời kỳ lịch sử: vừa soi đường cho cách mạng Việt Nam, vừa đóng góp vào tư tưởng và phong trào giải phóng các dân tộc trên thế giới.',
        'value', 38),
])

chapter(3, [
    section('c3-doc-lap', 'Độc lập dân tộc: quyền, nội dung và mục tiêu',
        'Độc lập phải thực chất, gắn với quyền sống tự do, hạnh phúc của nhân dân và toàn vẹn lãnh thổ. Trong hoàn cảnh thuộc địa, giải phóng dân tộc là nhiệm vụ trước hết, tạo tiền đề giải phóng giai cấp.',
        'national-liberation independence declaration national-before-class national-first nationalism class-liberation tam-dan', 42),
    section('c3-giai-phong', 'Con đường, lãnh đạo và lực lượng giải phóng dân tộc',
        'Nắm trọn năm luận điểm giải phóng dân tộc. Phân biệt con đường vô sản, vai trò lãnh đạo của Đảng, lực lượng toàn dân và tính chủ động của cách mạng thuộc địa.',
        'liberation vo-san forces-all forces-combined active-colonies bird-wings revolution-not-through', 48),
    section('c3-bao-luc', 'Phương pháp cách mạng và tinh thần hòa bình',
        'Bạo lực cách mạng kết hợp đấu tranh chính trị và đấu tranh vũ trang, gắn với nhân đạo, hòa bình. Đường lối kháng chiến dựa vào toàn dân và sức mình là chính.',
        'violence peace-violence marx-violence resistance-line chess-strategy', 52),
    section('c3-cnxh', 'CNXH: cách tiếp cận, mục tiêu và đặc trưng',
        'Đích đến là nâng cao đời sống nhân dân. Bốn đặc trưng cần hiểu theo chính trị, kinh tế, văn hóa–xã hội và chủ thể xây dựng; không chỉ nhớ con số bốn.',
        'socialism-approach socialism-goal socialism political-owner economy distribution happiness-science', 54),
    section('c3-dong-luc', 'Động lực, lợi ích và trở lực',
        'Con người là động lực quyết định. Phát huy lợi ích vật chất đi đôi với động lực tinh thần, đồng thời chống chủ nghĩa cá nhân và các biểu hiện làm suy yếu công cuộc xây dựng CNXH.',
        'human-motivation khoan obstacles', 62),
    section('c3-qua-do', 'Thời kỳ quá độ: đặc điểm, nhiệm vụ và bước đi',
        'Việt Nam quá độ gián tiếp từ nền nông nghiệp lạc hậu, không trải qua giai đoạn phát triển tư bản chủ nghĩa. Vì vậy phải cải tạo và xây dựng lâu dài, có bước đi phù hợp thực tế.',
        'transition progress-need transition-tasks transition-steps industrialization agriculture state-economy foreign-capital', 64),
    section('c3-quan-he', 'Độc lập dân tộc gắn liền với CNXH',
        'Độc lập dân tộc là cơ sở, tiền đề đi lên CNXH; CNXH bảo đảm độc lập dân tộc vững chắc. Kiên trì con đường đã lựa chọn phải giữ cả hai mục tiêu trong mối quan hệ gắn bó.',
        'national-socialism', 70),
    section('c3-su-kien', 'Sự kiện, văn bản và câu nói cần nhận diện',
        'Các mốc trong ngân hàng chương này nối tư tưởng độc lập với hoạt động thực tiễn. Ghép đúng sự kiện, thời điểm và văn bản; đọc chính xác từ ngữ của câu trích.',
        'versailles lenin-theses return1941 france1946 van-phuc august-call independence1966', 43, milestones=True),
])

chapter(4, [
    section('c4-dang-ra-doi', 'Sự ra đời, bản chất và vai trò của Đảng',
        'Phân biệt ba câu hỏi: Đảng ra đời từ yếu tố nào, mang bản chất gì và có vai trò gì. Cùng nói về Đảng nhưng các cụm từ nguồn gốc, bản chất và nhân tố quyết định không thay thế nhau.',
        'party-birth party-class party-role party-purpose', 76),
    section('c4-nguyen-tac', 'Nền tảng và nguyên tắc xây dựng Đảng',
        'Đảng phải có chủ nghĩa làm cốt; tổ chức, sinh hoạt theo nguyên tắc, coi trọng chất lượng. Tập trung dân chủ và tự phê bình phải hiểu đúng nội dung, tránh học tên mà đảo ngược cách thực hiện.',
        'party-foundation party-principles centralism criticism party-leads-state front', 84),
    section('c4-dao-duc', 'Đảng là đạo đức, là văn minh; tự đổi mới, chỉnh đốn',
        'Đảng lãnh đạo để phụng sự Tổ quốc, phục vụ nhân dân, phải thường xuyên tự chỉnh đốn. Rèn đạo đức của tổ chức gắn với cán bộ và từng quan hệ cụ thể.',
        'party-civilized four-liberations party-renewal party-dichuc three-relations lenin-party', 79),
    section('c4-can-bo', 'Vai trò và yêu cầu đối với cán bộ',
        'Cán bộ là gốc của công việc; phải có đạo đức, năng lực và trách nhiệm. Yêu cầu đối với cán bộ phục vụ cách mạng không đồng nhất với việc làm giàu cá nhân.',
        'cadre-role cadres', 88),
    section('c4-dan-chu', 'Nhà nước của dân, do dân, vì dân và bản chất giai cấp',
        'Của dân nói về chủ thể quyền lực; do dân nói về sự tạo lập, tham gia và kiểm soát; vì dân nói về mục đích phục vụ. Bản chất giai cấp công nhân thống nhất với tính nhân dân và tính dân tộc.',
        'democracy state-class', 91),
    section('c4-phap-quyen', 'Nhà nước hợp hiến, hợp pháp và pháp quyền nhân nghĩa',
        'Phân biệt nền tảng pháp lý của nhà nước với cách quản lý bằng hiến pháp, pháp luật. Pháp quyền phải nghiêm minh và bảo vệ con người, gắn pháp luật với đạo đức.',
        'constitutional law', 96),
    section('c4-trong-sach', 'Nhà nước trong sạch, vững mạnh',
        'Kiểm soát quyền lực, xây dựng đội ngũ cán bộ và phòng chống tiêu cực là yêu cầu thiết thực. Nhớ đúng ba biểu hiện được gọi là giặc nội xâm.',
        'clean-state internal-enemy', 100),
    section('c4-van-kien', 'Tên Đảng, sự kiện và văn bản liên quan',
        'Gắn tên gọi với đúng thời điểm; phân biệt lễ ra mắt Đảng Lao động với lễ kỷ niệm 30 năm thành lập Đảng và các lời căn dặn trong Di chúc.',
        'party-names party-launch1951 letter-committees', 78, milestones=True),
])

chapter(5, [
    section('c5-vai-tro', 'Cơ sở, vai trò và mục tiêu đại đoàn kết',
        'Đại đoàn kết vừa là chiến lược quyết định thành công, vừa là mục tiêu, nhiệm vụ hàng đầu. Đây là chính sách lâu dài, xuất phát từ truyền thống và thực tiễn cách mạng.',
        'unity-origins unity-role unity-goal', 108),
    section('c5-luc-luong', 'Lực lượng, nền tảng và điều kiện đoàn kết',
        'Đoàn kết toàn dân rộng rãi trên nền tảng công nhân–nông dân–trí thức, lấy lợi ích chung làm điểm quy tụ. Không yêu cầu mọi người cùng trình độ hay xóa bỏ các khác biệt.',
        'unity-foundation unity-conditions', 111),
    section('c5-mat-tran', 'Tổ chức Mặt trận và phương thức xây dựng đoàn kết',
        'Mặt trận dân tộc thống nhất là hình thức tổ chức khối đại đoàn kết, đặt dưới sự lãnh đạo của Đảng trên nền tảng công–nông–trí thức. Hoạt động theo hiệp thương dân chủ, đoàn kết lâu dài, chân thành, cùng giúp nhau tiến bộ; kết hợp dân vận và xây dựng đoàn thể.',
        'front unity-methods three-fronts', 116),
    section('c5-suc-manh', 'Sức mạnh dân tộc kết hợp sức mạnh thời đại',
        'Hai nguồn sức mạnh cần kết hợp để tạo sức mạnh tổng hợp; nội lực là chính, ngoại lực quan trọng. Tranh thủ quốc tế luôn gắn với tự lực, tự chủ.',
        'international-role nation-strength international-strength self-reliance', 122),
    section('c5-quoc-te', 'Lực lượng và nguyên tắc đoàn kết quốc tế',
        'Nhớ ba nhóm lực lượng và hai nguyên tắc. Kiên định độc lập, tự chủ nhưng linh hoạt sách lược; đoàn kết trên mục tiêu, lợi ích chung và có lý, có tình.',
        'international-forces international-principles diplomacy democratic-friends four-seas', 126),
    section('c5-moc', 'Các mặt trận và sự kiện cần nhớ',
        'Tên mặt trận thay đổi theo nhiệm vụ cách mạng. Ghép từng tên gọi với đúng mốc, tránh nhầm Việt Minh với Mặt trận Tổ quốc.',
        'front1939 vietminh front1955 unity-success', 117, milestones=True),
    section('c5-khau-hieu', 'Phân biệt tác giả khẩu hiệu đoàn kết',
        'Cụm từ trong khẩu hiệu giúp nhận diện tác giả: có các dân tộc bị áp bức gắn với Lênin; khẩu hiệu lao động tất cả các nước trong ngân hàng gắn với Hồ Chí Minh.',
        'lenin-slogan ho-slogan', 123),
])

chapter(6, [
    section('c6-van-hoa', 'Văn hóa: khái niệm, vị trí và các mối quan hệ',
        'Phân biệt nghĩa rộng của văn hóa với vị trí văn hóa trong đời sống tinh thần. Quan hệ với chính trị, kinh tế và xã hội là ba cách hỏi khác nhau.',
        'culture-definition culture-position culture-politics culture-economy culture-society identity', 139),
    section('c6-vai-tro', 'Tính chất, chức năng và vai trò của văn hóa',
        'Tính chất trả lời nền văn hóa mới như thế nào; chức năng trả lời văn hóa bồi dưỡng điều gì; vai trò trả lời văn hóa đóng góp gì cho cách mạng. Văn nghệ là một mặt trận phục vụ nhân dân.',
        'culture-nature culture-functions culture-role artist new-life', 144),
    section('c6-dao-duc', 'Đạo đức là gốc và quan hệ đức–tài',
        'Đạo đức là nền tảng của người cách mạng và sức mạnh tinh thần của xã hội. Chống chủ nghĩa cá nhân nhưng tôn trọng lợi ích cá nhân chính đáng.',
        'ethics-root individual-interest human-love', 146),
    section('c6-chuan-muc', 'Bốn chuẩn mực đạo đức: hiểu từng phẩm chất',
        'Chuẩn mực là các phẩm chất cần có. Trung với nước, hiếu với dân giữ vị trí bao trùm; cần, kiệm, liêm, chính, chí công vô tư gắn chặt với hoạt động hằng ngày.',
        'ethics-standards highest-ethics ethics-life chinh-relations confucius-liem', 151),
    section('c6-nguyen-tac', 'Ba nguyên tắc xây dựng đạo đức',
        'Nguyên tắc là cách xây dựng, rèn luyện đạo đức: nói đi đôi với làm và nêu gương; xây đi đôi với chống; tu dưỡng suốt đời. Không lẫn chúng với tên chuẩn mực.',
        'ethics-principles lifelong', 155),
    section('c6-con-nguoi', 'Quan niệm, vai trò và giải phóng con người',
        'Xem con người cụ thể trong hoàn cảnh lịch sử, thống nhất mặt tự nhiên và xã hội. Con người vừa là mục tiêu, vừa là động lực; giải phóng con người hướng tới cá nhân và cả nhân loại.',
        'human-specific human-nature human-role human-liberation human-socialist final-wish', 156),
    section('c6-giao-duc', 'Giáo dục, xây dựng con người và bồi dưỡng thanh niên',
        'Giáo dục toàn diện, học gắn thực hành và học suốt đời nhằm đào tạo người tốt, có ích. Bồi dưỡng thế hệ sau phải kết hợp đạo đức và năng lực, vừa hồng vừa chuyên.',
        'education education-all education-lifelong illiteracy young-generation youth-spring youth-awaken', 163),
    section('c6-tac-pham', 'Tác phẩm, bút danh và mốc thời gian',
        'Ghép hình ảnh đặc trưng với đúng tác phẩm; phân biệt Sửa đổi lối làm việc, Đạo đức cách mạng và Nâng cao đạo đức cách mạng, quét sạch chủ nghĩa cá nhân.',
        'culture1943 early-ethics ethics1947 ethics1958 ethics1969 new-life1947 fairness1966', 148, milestones=True),
])

# Expand broad concepts into explanations that can be learned before doing questions.
# Existing reviewed references are retained; added references name the local theory page.
DETAILS = {}


def detail(ident, page, *points):
    DETAILS[ident] = dict(page=page, points=[dict(title=title, text=text, keywords=keywords.split('|'))
                                          for title, text, keywords in points])


detail('definition', 9,
    ('Bản chất và nội dung', 'Một hệ thống quan điểm toàn diện, sâu sắc về những vấn đề cơ bản của cách mạng Việt Nam; thể hiện bản chất khoa học và cách mạng.', 'hệ thống quan điểm|toàn diện|cách mạng Việt Nam'),
    ('Nguồn gốc', 'Vận dụng, phát triển sáng tạo chủ nghĩa Mác–Lênin vào Việt Nam; kế thừa truyền thống tốt đẹp dân tộc và tiếp thu tinh hoa văn hóa nhân loại.', 'vận dụng|phát triển sáng tạo|truyền thống'),
    ('Giá trị', 'Là tài sản tinh thần to lớn, quý giá của Đảng và dân tộc, soi đường cho sự nghiệp cách mạng. Quá trình hoặc thời gian hình thành được học riêng, không phải một nội hàm của định nghĩa.', 'tài sản tinh thần|soi đường'))
detail('method', 12,
    ('Tính Đảng và tính khoa học', 'Giữ lập trường, mục tiêu cách mạng đồng thời phân tích khách quan, có căn cứ; không tách tính Đảng khỏi tính khoa học.', 'tính Đảng|tính khoa học|khách quan'),
    ('Lý luận và thực tiễn', 'Xuất phát từ thực tiễn, dùng lý luận soi sáng thực tiễn và kiểm nghiệm trong thực tiễn; chống học thuộc máy móc.', 'lý luận|thực tiễn'),
    ('Lịch sử cụ thể, toàn diện và phát triển', 'Đặt quan điểm vào đúng hoàn cảnh lịch sử; xem trong hệ thống và các mối liên hệ; kế thừa, phát triển sáng tạo. Kết hợp phương pháp lịch sử với phương pháp lôgíc.', 'lịch sử cụ thể|toàn diện|lôgíc'))
detail('practical', 18,
    ('Việt Nam', 'Pháp xâm lược làm xã hội chuyển thành thuộc địa nửa phong kiến. Các phong trào cứu nước theo khuynh hướng cũ thất bại, đặt ra yêu cầu tìm con đường mới.', 'thuộc địa nửa phong kiến|con đường mới'),
    ('Thế giới', 'Chủ nghĩa tư bản chuyển sang đế quốc chủ nghĩa; Cách mạng Tháng Mười Nga và Quốc tế Cộng sản mở ra điều kiện mới cho phong trào giải phóng dân tộc.', 'đế quốc chủ nghĩa|Tháng Mười|Quốc tế Cộng sản'))
detail('theoretical', 22,
    ('Ba nguồn', 'Giá trị truyền thống tốt đẹp dân tộc; tinh hoa văn hóa nhân loại, gồm phương Đông và phương Tây; chủ nghĩa Mác–Lênin.', 'truyền thống|tinh hoa văn hóa|Mác–Lênin'),
    ('Vai trò quyết định', 'Chủ nghĩa Mác–Lênin cung cấp thế giới quan và phương pháp luận khoa học, cách mạng; giúp chuyển từ người yêu nước thành người cộng sản. Không xếp bối cảnh xã hội vào nguồn lý luận.', 'quyết định|thế giới quan|phương pháp luận'))
detail('classes', 20,
    ('Năm giai cấp', 'Địa chủ, nông dân và ba giai cấp mới là công nhân, tư sản, tiểu tư sản.', '5|công nhân|tư sản|tiểu tư sản'),
    ('Hai mâu thuẫn', 'Mâu thuẫn toàn thể dân tộc Việt Nam với thực dân Pháp và tay sai là chủ yếu; mâu thuẫn nông dân với địa chủ phong kiến.', '2|dân tộc|chủ yếu'))
detail('west', 25,
    ('Nhận diện phương Tây', 'Tự do, bình đẳng, bác ái gắn với Cách mạng Pháp; tư tưởng Khai sáng Pháp, triết học Hy Lạp và lòng nhân ái Kitô giáo thuộc các nguồn văn hóa phương Tây được xét trong ngân hàng.', 'tự do, bình đẳng, bác ái|Pháp|phương Tây'),
    ('Tránh ghép sai', 'Không chuyển tư tưởng các nhà Khai sáng Pháp thành các nhà Khai sáng Anh; không xếp triết học Hy Lạp vào phương Đông. Với câu hỏi danh mục phương Đông, bám các học thuyết được giáo trình nêu.', 'Pháp|Anh|phương Đông'))
detail('subjective', 27,
    ('Phẩm chất và tư duy', 'Hoài bão cứu nước, thương dân; ý chí, nghị lực; tư duy độc lập, tự chủ, sáng tạo và khả năng tiếp thu có phê phán.', 'cứu nước|độc lập|sáng tạo'),
    ('Thực tiễn và tri thức', 'Vốn sống, hoạt động thực tiễn trong nước và quốc tế phong phú giúp tổng kết thực tiễn, tiếp thu và phát triển lý luận.', 'thực tiễn|tổng kết|phát triển'))
detail('phases', 30,
    ('Trước 1911', 'Hình thành tư tưởng yêu nước và chí hướng tìm đường cứu nước mới.', 'trước 1911|yêu nước'),
    ('1911–1920', 'Hình thành tư tưởng cứu nước, giải phóng dân tộc theo con đường cách mạng vô sản.', '1911–1920|con đường vô sản'),
    ('1920–1930', 'Hình thành những nội dung cơ bản của tư tưởng về cách mạng Việt Nam.', '1920–1930|nội dung cơ bản'),
    ('1930–1941', 'Vượt qua thử thách, giữ vững đường lối và phương pháp cách mạng đúng đắn, sáng tạo.', '1930–1941|vượt qua thử thách'),
    ('1941–1969', 'Tiếp tục phát triển, hoàn thiện tư tưởng, soi đường cho sự nghiệp cách mạng của Đảng và nhân dân.', '1941–1969|phát triển|hoàn thiện'))
detail('leech', 31,
    ('Tác phẩm và hình ảnh', 'Trong Bản án chế độ thực dân Pháp, hình ảnh con đỉa hai vòi chỉ chủ nghĩa tư bản bóc lột ở cả chính quốc và thuộc địa. Muốn đánh đổ phải chống sự bóc lột ở cả hai nơi.', 'Bản án chế độ thực dân Pháp|con đỉa hai vòi'),
    ('Phân biệt', 'Hai cánh của một con chim nói về quan hệ hai phong trào cách mạng; con đỉa hai vòi nói về chủ nghĩa tư bản.', 'hai cánh|chủ nghĩa tư bản'))
detail('value', 38,
    ('Đối với Việt Nam', 'Đưa sự nghiệp giải phóng dân tộc đến thắng lợi; là nền tảng tư tưởng, kim chỉ nam và tiếp tục soi đường cho công cuộc xây dựng đất nước.', 'giải phóng dân tộc|soi đường'),
    ('Đối với thế giới', 'Góp phần mở con đường giải phóng cho các dân tộc thuộc địa và đóng góp vào đấu tranh vì độc lập, dân chủ, hòa bình, tiến bộ xã hội.', 'thuộc địa|hòa bình|tiến bộ'))
detail('independence', 42,
    ('Quyền thiêng liêng', 'Độc lập, tự do là quyền thiêng liêng, bất khả xâm phạm của mọi dân tộc, không riêng Việt Nam.', 'thiêng liêng|bất khả xâm phạm'),
    ('Gắn hạnh phúc nhân dân', 'Độc lập phải đem lại tự do, cơm no, áo ấm và hạnh phúc cho nhân dân, không chỉ có tên gọi độc lập.', 'tự do|hạnh phúc|nhân dân'),
    ('Độc lập thực chất', 'Độc lập phải thật sự, hoàn toàn, triệt để trên các phương diện, không lệ thuộc về thực chất.', 'thật sự|hoàn toàn|triệt để'),
    ('Thống nhất lãnh thổ', 'Độc lập gắn liền thống nhất đất nước và toàn vẹn lãnh thổ.', 'thống nhất|toàn vẹn lãnh thổ'))
detail('liberation', 48,
    ('Con đường', 'Muốn thắng lợi phải đi theo con đường cách mạng vô sản, hướng tới giải phóng dân tộc gắn với CNXH.', 'cách mạng vô sản'),
    ('Lãnh đạo', 'Trong thời đại mới phải do Đảng Cộng sản lãnh đạo.', 'Đảng Cộng sản'),
    ('Lực lượng', 'Là sự nghiệp đại đoàn kết toàn dân; công–nông là gốc, mở rộng tập hợp các lực lượng yêu nước.', 'toàn dân|công–nông'),
    ('Tính chủ động', 'Cách mạng thuộc địa phải chủ động, sáng tạo, có thể thắng trước cách mạng vô sản ở chính quốc.', 'chủ động|sáng tạo|thắng trước'),
    ('Phương pháp', 'Tiến hành bằng bạo lực cách mạng, kết hợp đấu tranh chính trị và đấu tranh vũ trang.', 'bạo lực cách mạng|chính trị|vũ trang'))
detail('socialism', 56,
    ('Chính trị', 'Chế độ dân chủ, do nhân dân làm chủ; quyền lực thuộc về nhân dân.', 'nhân dân làm chủ'),
    ('Kinh tế', 'Kinh tế phát triển cao dựa trên lực lượng sản xuất hiện đại và công hữu về tư liệu sản xuất chủ yếu.', 'hiện đại|công hữu'),
    ('Văn hóa, đạo đức và quan hệ xã hội', 'Trình độ văn hóa, đạo đức phát triển; xã hội công bằng, hợp lý, không còn áp bức bóc lột, con người có điều kiện phát triển.', 'công bằng|không còn áp bức bóc lột'),
    ('Chủ thể xây dựng', 'Là công trình tập thể của nhân dân dưới sự lãnh đạo của Đảng Cộng sản.', 'tập thể nhân dân|Đảng Cộng sản'))
detail('transition', 65,
    ('Tính chất', 'Cải biến sâu sắc nhưng phức tạp, lâu dài, khó khăn, gian khổ; không thể nóng vội.', 'sâu sắc|phức tạp|lâu dài'),
    ('Đặc điểm lớn nhất', 'Từ nước nông nghiệp lạc hậu tiến lên CNXH, không trải qua giai đoạn phát triển tư bản chủ nghĩa. Đây là quá độ gián tiếp.', 'nông nghiệp lạc hậu|quá độ gián tiếp'))
detail('transition-tasks', 66,
    ('Nhiệm vụ', 'Cải tạo tàn tích xã hội cũ và xây dựng xã hội mới trên chính trị, kinh tế, văn hóa, quan hệ xã hội; xây dựng cơ sở vật chất–kỹ thuật, trong đó xây dựng là trọng tâm lâu dài.', 'cải tạo|xây dựng|cơ sở vật chất–kỹ thuật'),
    ('Nguyên tắc', 'Lấy Mác–Lênin làm nền tảng; giữ độc lập dân tộc; đoàn kết, học kinh nghiệm các nước anh em; xây đi đôi với chống.', 'Mác–Lênin|độc lập dân tộc|xây đi đôi với chống'))
detail('human-motivation', 62,
    ('Động lực quyết định', 'Con người, bao gồm cá nhân và cộng đồng. Phát huy sức dân, quyền làm chủ, đoàn kết và các nguồn lực sẵn có trong nhân dân.', 'con người|sức dân'),
    ('Cách phát huy', 'Kết hợp lợi ích vật chất với động lực chính trị–tinh thần; khuyến khích đóng góp, không chỉ dùng một phía vật chất hoặc tinh thần.', 'lợi ích vật chất|chính trị–tinh thần'))
detail('obstacles', 63,
    ('Các trở lực', 'Chủ nghĩa cá nhân, tham ô, lãng phí, quan liêu, chia rẽ, bảo thủ và lười biếng làm suy yếu xây dựng CNXH. Chủ nghĩa cá nhân là nguồn gây nhiều căn bệnh khác.', 'chủ nghĩa cá nhân|tham ô|quan liêu'),
    ('Phân biệt đối tượng đấu tranh', 'Giải phóng phải chống áp bức, đế quốc, thực dân, tay sai và nghèo nàn, lạc hậu. Không hiểu giải phóng giai cấp là đánh đổ mọi cá nhân thuộc tầng lớp địa chủ, tư sản.', 'áp bức|nghèo nàn, lạc hậu|không'))
detail('national-socialism', 70,
    ('Độc lập là tiền đề', 'Giành độc lập để nhân dân làm chủ, có điều kiện xây dựng xã hội mới và đi lên CNXH.', 'độc lập|tiền đề'),
    ('CNXH bảo đảm độc lập', 'Xây dựng CNXH tạo cơ sở bảo vệ độc lập vững chắc, đồng thời giải phóng giai cấp và con người, đem lại đời sống tự do, hạnh phúc.', 'CNXH|vững chắc|hạnh phúc'),
    ('Giữ cả hai mục tiêu', 'Cách mạng giải phóng dân tộc tiến lên cách mạng xã hội chủ nghĩa; thống nhất lập trường giai cấp, độc lập dân tộc và đoàn kết quốc tế.', 'giải phóng dân tộc|xã hội chủ nghĩa|đoàn kết quốc tế'))
detail('party-role', 77,
    ('Nhân tố quyết định hàng đầu', 'Đảng xác định đường lối, giác ngộ, tập hợp và tổ chức quần chúng; liên hệ các lực lượng cách mạng quốc tế.', 'đường lối|tổ chức|quần chúng'),
    ('Hình ảnh nhận diện', 'Trong Đường Kách mệnh, Đảng được ví như người cầm lái; Đảng có vững thì cách mạng mới thành công.', 'Đường Kách mệnh|người cầm lái'))
detail('party-birth', 77,
    ('Ba yếu tố kết hợp', 'Chủ nghĩa Mác–Lênin, phong trào công nhân và phong trào yêu nước. Phong trào yêu nước là yếu tố Hồ Chí Minh nêu thêm khi giải thích quy luật ra đời của Đảng ở Việt Nam.', 'Mác–Lênin|công nhân|yêu nước'),
    ('Nhận diện văn bản', 'Luận điểm về ba yếu tố được nêu trong Ba mươi năm hoạt động của Đảng, gắn với tổng kết quá trình thành lập và phát triển của Đảng.', 'Ba mươi năm hoạt động của Đảng'))
detail('party-class', 78,
    ('Bản chất', 'Đảng của giai cấp công nhân, đồng thời của nhân dân lao động và dân tộc Việt Nam; lợi ích giai cấp công nhân thống nhất với lợi ích nhân dân, dân tộc.', 'giai cấp công nhân|nhân dân lao động|dân tộc'),
    ('Biểu hiện', 'Bản chất thể hiện ở nền tảng lý luận Mác–Lênin, mục tiêu, đường lối và nguyên tắc tổ chức; không căn cứ đơn thuần vào số lượng hay thành phần xuất thân.', 'nền tảng lý luận|đường lối|tổ chức'),
    ('Vai trò giai cấp công nhân', 'Xuất phát từ đặc tính, vị trí kinh tế–xã hội của giai cấp công nhân, không phải số lượng đông hoặc ý muốn chủ quan.', 'đặc tính|vị trí kinh tế–xã hội'))
detail('party-purpose', 86,
    ('Mục tiêu và lợi ích', 'Phụng sự Tổ quốc, phục vụ nhân dân; không có lợi ích riêng ngoài lợi ích của giai cấp công nhân, nhân dân và dân tộc.', 'Tổ quốc|nhân dân'),
    ('Tư cách người lãnh đạo', 'Có đạo đức và năng lực để dân tin, dân mến, dân phục, dân theo; gắn bó với dân, lắng nghe, học hỏi và chịu sự kiểm soát của nhân dân.', 'đạo đức|năng lực|kiểm soát'))
detail('party-principles', 84,
    ('Nền tảng và tổ chức', 'Mác–Lênin làm nền tảng, kim chỉ nam; tập trung dân chủ; tập thể lãnh đạo, cá nhân phụ trách.', 'Mác–Lênin|tập trung dân chủ|cá nhân phụ trách'),
    ('Rèn luyện trong Đảng', 'Tự phê bình và phê bình; kỷ luật nghiêm minh, tự giác; thường xuyên tự chỉnh đốn; đoàn kết, thống nhất.', 'tự phê bình|kỷ luật|đoàn kết'),
    ('Quan hệ', 'Liên hệ mật thiết với nhân dân và đoàn kết quốc tế. Số lượng đảng viên đông hoặc lãnh đạo chính phủ không phải tên nguyên tắc trong danh mục này.', 'nhân dân|đoàn kết quốc tế'))
detail('centralism', 84,
    ('Hai mặt gắn bó', 'Tập trung trên nền tảng dân chủ; dân chủ dưới sự chỉ đạo tập trung. Cá nhân phục tùng tổ chức, thiểu số phục tùng đa số, cấp dưới phục tùng cấp trên.', 'thiểu số phục tùng đa số|tập trung|dân chủ'),
    ('Điểm dễ đảo', 'Đa số phục tùng thiểu số là phát biểu sai. Không biến tập trung thành độc đoán hoặc dân chủ thành vô tổ chức.', 'đa số phục tùng thiểu số|sai'))
detail('party-civilized', 80,
    ('Nội dung', 'Đảng đạo đức, văn minh ở mục tiêu giải phóng dân tộc, xã hội, giai cấp và con người; tổ chức trong sạch, đường lối đúng và cán bộ gương mẫu, phục vụ nhân dân.', 'giải phóng|trong sạch|phục vụ nhân dân'),
    ('Sự kiện', 'Câu Đảng ta là đạo đức, là văn minh được nêu tại lễ kỷ niệm 30 năm thành lập Đảng, năm 1960.', '30 năm|1960'))
detail('party-dichuc', 81,
    ('Đảng cầm quyền', 'Cán bộ, đảng viên phải thấm nhuần đạo đức cách mạng, cần kiệm liêm chính, chí công vô tư; Đảng vừa là người lãnh đạo vừa là người đầy tớ trung thành của nhân dân.', 'đạo đức cách mạng|lãnh đạo|đầy tớ'),
    ('Đoàn kết và chỉnh đốn', 'Giữ đoàn kết như con ngươi của mắt mình; sau thắng lợi phải tiếp tục chỉnh đốn Đảng, ngăn ngừa thoái hóa.', 'con ngươi|chỉnh đốn Đảng'))
detail('democracy', 92,
    ('Của dân — quyền lực thuộc ai?', 'Mọi quyền lực nhà nước và xã hội thuộc về nhân dân. Nhân dân có quyền kiểm soát, phê bình, bãi miễn người đại diện không còn xứng đáng.', 'của dân|quyền lực|kiểm soát'),
    ('Do dân — ai tạo lập, tham gia?', 'Nhân dân bầu ra, đóng góp, tham gia xây dựng và quản lý Nhà nước. Quyền làm chủ gắn với trách nhiệm, nghĩa vụ công dân.', 'do dân|bầu ra|tham gia quản lý'),
    ('Vì dân — phục vụ ai?', 'Mọi hoạt động phục vụ lợi ích chính đáng của nhân dân; cán bộ vừa lãnh đạo vừa là công bộc, tránh đặc quyền. Việc lợi cho dân hết sức làm, việc hại dân hết sức tránh.', 'vì dân|lợi ích|công bộc'))
detail('state-class', 95,
    ('Ba biểu hiện', 'Đảng Cộng sản lãnh đạo; định hướng phát triển lên CNXH; tổ chức và hoạt động theo tập trung dân chủ.', 'Đảng Cộng sản|CNXH|tập trung dân chủ'),
    ('Tính thống nhất', 'Bản chất giai cấp công nhân gắn với tính nhân dân, tính dân tộc; trong danh mục này không chọn chế độ tam quyền phân lập.', 'giai cấp công nhân|nhân dân|dân tộc'))
detail('law', 97,
    ('Hiệu lực pháp lý', 'Nhà nước hợp hiến; quản lý bằng hiến pháp, pháp luật và chú trọng thực thi nghiêm minh; có đội ngũ cán bộ, công chức đủ đức, đủ tài.', 'hợp hiến|pháp luật|đủ đức, đủ tài'),
    ('Pháp quyền nhân nghĩa', 'Pháp luật vì con người, bảo vệ quyền con người; khoan hồng người cải tà quy chính nhưng nghiêm trị hành vi hại dân, hại nước. Kết hợp pháp trị với đức trị.', 'con người|pháp trị|đức trị'))
detail('front', 116,
    ('Hình thức tổ chức', 'Quy tụ tổ chức và cá nhân yêu nước trong, ngoài nước; không đồng nhất Mặt trận với cơ quan quyền lực như tòa án.', 'tổ chức|cá nhân yêu nước|Mặt trận'),
    ('Nguyên tắc hoạt động', 'Nền tảng công–nông–trí thức, Đảng lãnh đạo; hiệp thương dân chủ; đoàn kết chân thành, lâu dài, giúp nhau tiến bộ, lấy lợi ích dân tộc và quyền lợi nhân dân làm cơ sở.', 'công–nông–trí thức|hiệp thương dân chủ|lâu dài'),
    ('Vai trò của Đảng', 'Đảng vừa là thành viên, vừa là lực lượng lãnh đạo; thuyết phục, bàn bạc và thống nhất hành động, tránh áp đặt.', 'thành viên|lãnh đạo|thuyết phục'))
detail('unity-foundation', 111,
    ('Lực lượng rộng rãi', 'Đoàn kết mọi người Việt Nam yêu nước, không phân biệt giai cấp, dân tộc, tôn giáo, quá khứ; ai có tài, có đức, có lòng phụng sự đều cần được tập hợp.', 'mọi người Việt Nam|yêu nước'),
    ('Nền tảng và điểm chung', 'Công nhân, nông dân, lao động trí óc là nền tảng. Lấy lợi ích tối cao dân tộc và quyền lợi chính đáng nhân dân làm điểm tương đồng.', 'công nhân|nông dân|trí óc'))
detail('international-principles', 130,
    ('Thống nhất và có lý, có tình', 'Đoàn kết trên mục tiêu, lợi ích chung; giữ nguyên tắc, tôn trọng nhau, giúp đỡ chân thành.', 'mục tiêu|lợi ích|có lý, có tình'),
    ('Độc lập, tự chủ', 'Tự lực, tự cường, dựa vào sức mình là chính; giúp đỡ quốc tế rất quan trọng nhưng không thay cho nội lực.', 'độc lập|tự chủ|sức mình'))
detail('culture-functions', 145,
    ('Tư tưởng và tình cảm', 'Bồi dưỡng tư tưởng đúng đắn và tình cảm cao đẹp, hướng con người tới chân, thiện, mỹ.', 'tư tưởng|tình cảm'),
    ('Dân trí', 'Mở rộng hiểu biết, nâng cao trình độ dân trí để nhân dân tham gia xây dựng đất nước.', 'nâng cao dân trí'),
    ('Phẩm chất và lối sống', 'Bồi dưỡng phẩm chất, phong cách và lối sống tốt đẹp, lành mạnh; hướng con người tới những giá trị tốt.', 'phẩm chất|phong cách|lối sống'))
detail('culture-role', 144,
    ('Mục tiêu và động lực', 'Văn hóa là thành quả cần xây dựng, đồng thời bồi dưỡng tinh thần, ý chí và sức sáng tạo thúc đẩy cách mạng.', 'mục tiêu|động lực'),
    ('Một mặt trận', 'Đấu tranh chống lạc hậu, phản động; xây dựng giá trị và con người mới. Văn nghệ sĩ là chiến sĩ trên mặt trận đó.', 'mặt trận|chiến sĩ'),
    ('Phục vụ quần chúng', 'Đời sống nhân dân là nguồn chất liệu; sáng tạo văn hóa phải đáp ứng nhu cầu và nâng cao đời sống tinh thần của nhân dân.', 'quần chúng|chất liệu'))
detail('ethics-root', 147,
    ('Gốc và sức mạnh tinh thần', 'Đạo đức giúp người cách mạng gánh việc nặng, đi đường dài, giữ vững phẩm chất trong khó khăn; góp phần tạo sức mạnh tinh thần xã hội.', 'đạo đức|gốc|sức mạnh tinh thần'),
    ('Đức và tài', 'Đức là gốc nhưng phải gắn với tài, năng lực làm việc. Có tài mà thiếu đạo đức không đủ để lãnh đạo nhân dân; có đức cần rèn tài để hoàn thành nhiệm vụ.', 'đức|tài|năng lực'),
    ('Đối với xã hội', 'Đạo đức là thước đo lòng cao thượng, vũ khí tinh thần trong đấu tranh cách mạng và nhân tố tạo sức hấp dẫn của CNXH.', 'thước đo|vũ khí|sức hấp dẫn'))
detail('ethics-standards', 151,
    ('Trung với nước, hiếu với dân', 'Trung thành với sự nghiệp dựng nước, giữ nước; thương dân, tin dân và hết lòng phục vụ dân. Đây là phẩm chất quan trọng, bao trùm.', 'trung với nước|hiếu với dân|bao trùm'),
    ('Cần, kiệm, liêm, chính, chí công vô tư', 'Lao động siêng năng; tiết kiệm; trong sạch; ngay thẳng; đặt lợi ích chung lên trước lợi ích riêng, công bằng, không tư lợi.', 'cần|kiệm|liêm|chính|chí công vô tư'),
    ('Thương yêu con người', 'Sống có tình nghĩa, nhất là với người lao động, người bị áp bức; nghiêm với mình, rộng lượng với người, giúp nhau tiến bộ.', 'thương yêu|tình nghĩa|tiến bộ'),
    ('Quốc tế trong sáng', 'Đoàn kết với nhân dân lao động, các dân tộc bị áp bức và lực lượng tiến bộ; chống phân biệt, hẹp hòi, hướng tới hòa bình, công lý.', 'quốc tế|đoàn kết|hòa bình'))
detail('ethics-life', 152,
    ('Cần và kiệm', 'Cần là siêng năng, có kế hoạch, sáng tạo, năng suất; kiệm là tiết kiệm thời gian, công sức, của cải, không xa xỉ, không hoang phí.', 'cần|siêng năng|kiệm|tiết kiệm'),
    ('Liêm và chính', 'Liêm là trong sạch, không tham địa vị, tiền tài; chính là thẳng thắn, đứng đắn trong quan hệ với mình, người và việc.', 'liêm|trong sạch|chính|thẳng thắn'),
    ('Chí công vô tư', 'Công bằng, đặt việc công và lợi ích chung lên trước, không vì tư lợi. Các phẩm chất gắn bó, không thể coi từng phẩm chất tách rời.', 'chí công vô tư|lợi ích chung'))
detail('ethics-principles', 155,
    ('Nói đi đôi với làm, nêu gương', 'Lời nói thống nhất hành động; người có trách nhiệm phải tự mình làm gương, tránh nói một đằng làm một nẻo.', 'nói đi đôi với làm|nêu gương'),
    ('Xây đi đôi với chống', 'Bồi dưỡng phẩm chất tốt đồng thời đấu tranh với thói xấu; kết hợp thành phong trào quần chúng rộng rãi.', 'xây|chống|phong trào quần chúng'),
    ('Tu dưỡng suốt đời', 'Rèn luyện bền bỉ hằng ngày trong hoạt động thực tiễn và các quan hệ xã hội; đạo đức không tự có sẵn hay rèn một lần là đủ.', 'suốt đời|thực tiễn|quan hệ xã hội'))
detail('human-role', 159,
    ('Mục tiêu', 'Cách mạng nhằm độc lập cho đất nước, tự do cho đồng bào, ai cũng có cơm ăn, áo mặc, được học hành; giải phóng và phát triển con người.', 'mục tiêu|cơm ăn|áo mặc|học hành'),
    ('Động lực', 'Nhân dân là chủ thể tạo nên thắng lợi; con người là vốn quý nhất, nhân tố quyết định, cần phát huy quyền làm chủ và sức sáng tạo.', 'động lực|vốn quý nhất|quyết định'),
    ('Di chúc', 'Đầu tiên là công việc đối với con người: chăm lo con người, bồi dưỡng thế hệ cách mạng kế tiếp và khắc phục hậu quả chiến tranh.', 'công việc đối với con người'))
detail('education-all', 163,
    ('Nội dung và mục tiêu', 'Giáo dục toàn diện đức, trí, thể, mỹ; đào tạo người tốt, có ích, kết hợp đạo đức với năng lực.', 'đức, trí, thể, mỹ|có ích'),
    ('Phương châm', 'Học đi đôi với hành, lý luận liên hệ thực tiễn, học tập gắn lao động; kết hợp gia đình, nhà trường, xã hội để nâng chất lượng, hiệu quả.', 'học đi đôi với hành|gia đình|nhà trường|xã hội'))

# Small gaps revealed by reviewing the questions: these sentences are part of
# the lesson, not changes to a question or its marking key.
SUMMARY_UPDATES = {
    'departure': 'Ngày 5/6/1911, Nguyễn Tất Thành, 21 tuổi, rời bến Nhà Rồng trên tàu Amiral Latouche-Tréville để tìm đường cứu nước.',
    'chinh-cuong': 'Chánh cương vắn tắt năm 1930 nêu phương hướng làm tư sản dân quyền cách mạng và thổ địa cách mạng để đi tới xã hội cộng sản; đánh đổ đế quốc Pháp và phong kiến, làm Việt Nam hoàn toàn độc lập.',
    'nationalism': 'Chủ nghĩa dân tộc chân chính, tức chủ nghĩa yêu nước của dân tộc bị áp bức, là động lực lớn; luận điểm này gắn với Báo cáo về Bắc Kỳ, Trung Kỳ và Nam Kỳ. Phân biệt với dân tộc hẹp hòi, sôvanh.',
    'state-economy': 'Trong quá độ còn nhiều hình thức sở hữu, thành phần kinh tế; ưu tiên phát triển kinh tế quốc doanh. Cải tạo tư sản dân tộc thành người lao động mới; hợp tác xã tự nguyện, cùng có lợi, từ thấp đến cao, không gò ép.',
    'human-specific': 'Con người luôn cụ thể, gắn với hoàn cảnh lịch sử và quan hệ xã hội: hẹp là gia đình, anh em, họ hàng, bạn bè; rộng là đồng bào cả nước, rộng hơn là cả loài người.',
    'culture-position': 'Văn hóa thuộc đời sống tinh thần, kiến trúc thượng tầng, được đặt ngang hàng kinh tế, chính trị và xã hội; phải phục vụ nhiệm vụ chính trị, thúc đẩy kinh tế và cùng kinh tế được phát triển để tiến lên CNXH.',
    'illiteracy': 'Bài Chống nạn thất học nhấn mạnh việc cấp tốc nâng cao dân trí sau khi giành độc lập, đặc biệt khuyến khích phụ nữ học tập để tiến kịp nam giới.',
    'three-relations': 'Đạo đức được xem xét trên mọi lĩnh vực, phạm vi, đối tượng; tập trung trong ba quan hệ đối với mình, đối với người và đối với việc.',
    'ethics-standards': 'Bốn nhóm chuẩn mực đạo đức cách mạng gồm trung với nước, hiếu với dân; cần, kiệm, liêm, chính, chí công vô tư; thương yêu con người, sống có tình nghĩa; tinh thần quốc tế trong sáng. Xây dựng đạo đức cách mạng trên lập trường giai cấp công nhân.',
}

# Page spans were checked in the supplied PTIT text. A multi-part concept needs
# the continuation pages too, rather than attributing all subpoints to its first page.
DETAIL_PAGE_SPANS = {
    'method': [12, 13, 14, 15, 16], 'practical': [18, 19, 20, 21, 22],
    'theoretical': [22, 23, 24, 25, 26], 'subjective': [27, 28],
    'phases': [30, 31, 33, 34, 35], 'value': [38, 39, 40, 41],
    'independence': [42, 43, 44, 45, 46, 47], 'liberation': [48, 49, 50, 51, 52, 53],
    'socialism': [57, 58, 59], 'transition-tasks': [66, 67, 68, 69],
    'human-motivation': [62, 63, 64], 'national-socialism': [70, 71, 72],
    'party-principles': [83, 84, 85, 86, 87, 88], 'party-purpose': [86, 87],
    'party-civilized': [79, 80, 81], 'party-dichuc': [81, 86, 87],
    'democracy': [92, 93, 94], 'state-class': [94, 95, 96],
    'law': [96, 97, 98, 99, 100], 'front': [116, 117, 118, 119, 120],
    'unity-foundation': [111, 112, 113], 'international-principles': [130, 131, 132, 133],
    'culture-role': [144, 145, 146], 'ethics-root': [147, 148, 149],
    'ethics-standards': [150, 151, 152, 153, 154], 'ethics-life': [151, 152],
    'ethics-principles': [154, 155, 156, 157], 'human-role': [159, 160, 161],
    'education-all': [149, 164], 'culture-functions': [101, 102],
    'leech': [31, 51], 'party-birth': [78], 'party-class': [79],
}
DETAIL_SOURCES = {'culture-functions': 'giao-trinh-2009'}

CONFUSIONS = {
    'definition-full': 'Toàn diện, sâu sắc nói về hệ thống quan điểm; vận dụng, phát triển sáng tạo nói về cách tiếp thu Mác–Lênin. Không học thành sao chép nguyên xi.',
    'phases': '1911–1920 là tìm con đường vô sản; 1920–1930 mới là hình thành nội dung cơ bản. Không dùng khung 1921–1930 của tài liệu cũ thay khung đang học.',
    'versailles': '1919: Yêu sách và tên Nguyễn Ái Quốc; tháng 7/1920: đọc Luận cương; tháng 12/1920: Đại hội Tua.',
    'letter1928': 'Thư ngày 12/4/1928 nói thiếu tiền, không được hoạt động; thư 1938 xin thoát tình trạng đứng bên ngoài Đảng. Hai câu trích khác nhau.',
    'socialism': 'Bốn đặc trưng CNXH khác bốn nội dung độc lập dân tộc; phải nhớ tên các ý, không chỉ nhớ số 4.',
    'violence': 'Bạo lực cách mạng gồm cả chính trị và vũ trang. Bạo động chỉ nói một cách thức, không thay thế được toàn bộ quan điểm này.',
    'national-socialism': 'Độc lập là tiền đề; CNXH bảo đảm độc lập vững chắc. Không bỏ một trong hai mục tiêu.',
    'party-birth': 'Nguồn gốc ra đời có ba yếu tố; vai trò lãnh đạo là nhân tố quyết định; bản chất là giai cấp công nhân. Đây là ba nhóm câu khác nhau.',
    'party-principles': 'Nêu gương có vai trò trong xây dựng Đảng, nhưng câu hỏi phủ định về tên danh mục phải đọc đúng phạm vi bài học, không suy thành nêu gương là sai.',
    'democracy': 'Của → quyền lực; do → tạo lập và tham gia quản lý; vì → mục đích phục vụ. Từ nhân dân trong cả ba ý không làm chúng đồng nghĩa.',
    'constitutional': 'Tổng tuyển cử, hiến pháp dân chủ → hợp hiến, hợp pháp; quản lý nghiêm minh bằng pháp luật → thượng tôn pháp luật.',
    'unity-role': 'Chiến lược nói vai trò lâu dài, quyết định thành công; mục tiêu, nhiệm vụ hàng đầu nói yêu cầu hoạt động. Cả hai đều đúng khi hỏi đúng khía cạnh.',
    'international-forces': 'Câu hỏi tên ba nhóm lực lượng phải chọn đúng danh mục; không đồng nhất một tên gọi rộng như chống chủ nghĩa tư bản với tên nhóm trong giáo trình.',
    'culture-role': 'Vai trò khác chức năng. Với câu hỏi tên ba vai trò, sự nghiệp của quần chúng không thay tên phục vụ quần chúng; không suy ra quần chúng không sáng tạo văn hóa.',
    'ethics-standards': 'Chuẩn mực → phẩm chất cần có; nguyên tắc → cách xây dựng. Trung với nước, hiếu với dân là chuẩn mực, tu dưỡng suốt đời là nguyên tắc.',
    'ethics1958': 'Ngọc, vàng → Đạo đức cách mạng (1958); sông, cây → Sửa đổi lối làm việc (1947); T.L. và quét sạch chủ nghĩa cá nhân → bài năm 1969.',
}
