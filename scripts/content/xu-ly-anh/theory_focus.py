"""Curate repeated theory clauses only; numerical exercises are never shortened."""
from copy import deepcopy

REVIEW={}


def section(lead,text,formula=None):
    s=dict(lead=lead,text=text)
    if formula:s['formula']=formula
    return s


def apply(records):
    by_id={r['id']:r for r in records};original=deepcopy(by_id)
    def partial(ident,prompt,indices,prior,removed,retained,steps=None,title=None):
        r=by_id[ident];source=original[ident]
        r['theoryFocus']=dict(mode='new-parts',sourcePrompt=source['prompt'],
            previous=[dict(id=i,covered=c) for i,c in prior],removed=removed,retained=retained)
        r['prompt']=prompt;r['revision']=3
        r['steps']=deepcopy(steps if steps is not None else [source['steps'][i] for i in indices])
        if title:r['title']=title
        REVIEW[ident]=dict(mode='new-parts',previous=r['theoryFocus']['previous'],removed=removed,retained=retained)
    def reference(ident,prior,covered):
        r=by_id[ident];r['theoryFocus']=dict(mode='reference',sourcePrompt=original[ident]['prompt'],
            previous=[dict(id=i,covered=c) for i,c in prior],removed=covered,retained=[])
        r['prompt']='Các ý của câu này đã được hỏi ở những câu bên dưới. Mở câu tương ứng để ôn lại; đề gốc và câu trả lời đối chiếu vẫn được giữ.'
        r['revision']=3
        REVIEW[ident]=dict(mode='reference',previous=r['theoryFocus']['previous'],removed=covered,retained=[])

    partial('uyen-lt-1-6','Khuếch tán lỗi hỗ trợ kỹ thuật in nửa cường độ như thế nào? Khuếch tán lỗi hơn tách ngưỡng thông thường ở điểm nào?', [1,2],
      [('uyen-lt-1-5','Halftone và lý do dùng trong in ấn')],['Hỏi lại kỹ thuật in đa cấp xám chỉ bằng mực đen'],['Vai trò khuếch tán lỗi; so với tách ngưỡng'])
    partial('uyen-lt-1-7','Khuếch tán lỗi một chiều khác hai chiều như thế nào? Hai chiều khắc phục điểm yếu nào của một chiều?', [1,2],
      [('uyen-lt-1-6','Khái niệm, vai trò và khác biệt với tách ngưỡng')],['Định nghĩa lại khuếch tán lỗi'],['Một chiều/hai chiều; vệt giả theo hướng quét'])
    partial('uyen-lt-2-1','Trong những trường hợp nào dùng phối màu cộng, những trường hợp nào dùng phối màu trừ? Giải thích theo thiết bị phát sáng hoặc bề mặt phản xạ.', [],
      [('uyen-lt-1-2','Nguyên lý CMY và khác biệt với RGB')],['Định nghĩa lại hai nguyên lý phối màu'],['Trường hợp sử dụng'],steps=[
        section('Thiết bị phát sáng','Màn hình, tivi và máy chiếu dùng phối màu cộng RGB vì chúng tạo màu bằng cách cộng các nguồn ánh sáng đỏ, lục, lam.'),
        section('Bề mặt phản xạ','In ấn và hội họa dùng phối màu trừ vì mực hoặc chất màu hấp thụ một phần ánh sáng chiếu tới; mắt nhận phần ánh sáng phản xạ còn lại.')])
    partial('uyen-lt-2-2','Viết công thức chuyển từ RGB sang CMY cho dữ liệu chuẩn hóa trong [0,1] và cho ảnh RGB 8 bit.', [1,2],
      [('uyen-lt-1-2','CMY và khác biệt RGB'),('uyen-lt-2-1','Ứng dụng phối màu trừ')],['Định nghĩa CMY; hỏi lại lý do dùng trong in ấn'],['Phép chuyển RGB→CMY, hai miền giá trị'],title='Chuyển RGB sang CMY')
    partial('uyen-lt-2-3','Vector lưu điểm, đường và vùng như thế nào? Vì sao vector có ưu điểm khi thay đổi kích thước nhưng vẫn không thay thế hoàn toàn raster?', [0,2],
      [('uyen-lt-1-4','So sánh raster với vector')],['So sánh lại hai mô hình nói chung'],['Cách lưu hình học vector; lý do raster vẫn cần thiết'])
    partial('uyen-lt-2-6','Nêu ba loại mặt nạ Prewitt, Sobel, Frei–Chen để phát hiện biên bậc nhất. Với từng loại, viết mặt nạ và nêu các bước tiếp theo để thu được đường biên rõ.', [1,2,3,4],
      [('uyen-lt-2-5','Nguyên lý dùng đạo hàm')],['Nhắc lại nguyên lý phát hiện biên bằng đạo hàm'],['Ba cặp mặt nạ và hậu xử lý đáp ứng'])

    partial('uyen-3-L1','Kể tên ba biến đổi mức xám cơ bản: âm bản, logarithm và lũy thừa. Nêu công thức cùng tác dụng của từng biến đổi.', [2],
      [('uyen-lt-1-8','Tăng/giảm sáng bằng toán tử điểm')],['Cách tăng/giảm sáng; phân loại toán tử'],['Âm bản, log, gamma'])
    partial('uyen-3-L2','Thế nào là ảnh cân bằng lý tưởng? Vì sao ảnh số thường không đạt được histogram cân bằng lý tưởng?', [2],
      [('uyen-lt-1-9','Khái niệm và mục đích cân bằng histogram')],['Định nghĩa và lý do cân bằng'],['Cân bằng lý tưởng và giới hạn rời rạc'])
    partial('uyen-3-L3','Nêu các cách xử lý điểm ảnh ở biên khi dùng cửa sổ di chuyển và cho biết vì sao phải công bố quy ước biên.', [1],
      [('uyen-lt-1-10','Toán tử không gian và ý tưởng cửa sổ di chuyển')],['Định nghĩa, loại toán tử, ý tưởng cơ bản'],['Đệm 0, lặp rìa, phản xạ, bỏ biên'])
    partial('uyen-3-L4','Viết mô hình nhiễu liên tục, giải thích ký hiệu và kể tên các loại nhiễu thường gặp.', [1,3],
      [('uyen-lt-1-11','Khái niệm, mục đích và mô hình nhiễu rời rạc')],['Định nghĩa và mục đích mô hình; công thức rời rạc'],['Mô hình liên tục; các loại nhiễu'])
    reference('uyen-3-L5',[('uyen-lt-2-4','So sánh trung vị, trung bình, k gần nhất và trường hợp sử dụng')],['Toàn bộ yêu cầu so sánh ba bộ lọc'])
    bg=original['uyen-3-L6']['steps']
    partial('uyen-3-L6','Trình bày các bước tìm ngưỡng bằng đối xứng nền. Vì sao không nên chọn tỷ lệ tích lũy p% quá lớn?', [1],
      [('uyen-lt-2-8','Khái niệm và giả thiết nền phù hợp')],['Định nghĩa lại đối xứng nền và điều kiện nền'],['Các bước; ảnh hưởng của p%'],
      steps=[bg[1],section('Ảnh hưởng của tỷ lệ tích lũy','Chọn p quá lớn có thể kéo mức phân vị a sâu vào đuôi phân bố và làm ngưỡng T=2maxp−a bị lệch. Với histogram rời rạc phải dùng nhất quán quy tắc chọn mức đầu đạt p% hoặc mức cuối không vượt p% theo đề.')])
    reference('uyen-3-L7',[('uyen-lt-2-9','Ý tưởng tam giác và trường hợp không phù hợp')],['Toàn bộ yêu cầu về thuật toán tam giác'])
    partial('uyen-3-L8','So sánh Otsu và ISODATA về dạng histogram phù hợp, tham số phải cho trước, cách chọn ngưỡng và trường hợp có nhiều nghiệm.', [0,1],
      [('uyen-lt-2-8','Đối xứng nền'),('uyen-lt-2-9','Tam giác')],['Hỏi lại điều kiện và tham số của đối xứng nền/tam giác'],['Otsu và ISODATA: điều kiện, khởi tạo, lựa chọn và nhiều nghiệm'])
    r=original['uyen-3-L9']['steps']
    partial('uyen-3-L9','Phân biệt tăng cường với khôi phục ảnh, miền không gian với miền tần số. Trình bày các bộ lọc còn lại: trung bình hình học, điều hòa, phản điều hòa, min, max, điểm giữa và trung bình cắt tỉa; nêu loại nhiễu phù hợp.', [],
      [('uyen-lt-2-4','Trung bình số học, trung vị và k gần nhất')],['Trình bày lại trung bình số học và trung vị'],['Tăng cường/khôi phục; hai miền; các bộ lọc nhiễu còn lại'],steps=[r[0],r[1],
        section('Trung bình hình học','Trung bình hình học lấy căn bậc số phần tử của tích các mức xám trong cửa sổ. Nó có thể giảm nhiễu Gaussian và thường giữ chi tiết tốt hơn trung bình số học, nhưng kết quả còn phụ thuộc dữ liệu nhiễu.'),r[3],
        section('Bộ lọc min và max','Min lấy giá trị nhỏ nhất trong cửa sổ, giảm điểm sáng kiểu muối; max lấy giá trị lớn nhất, giảm điểm tối kiểu tiêu. Hai bộ lọc có thể làm thay đổi kích thước đối tượng.'),r[5]])

    partial('uyen-4-L1','Cho một ví dụ trộn hai màu gốc trong phối màu cộng và một ví dụ trong phối màu trừ.', [],
      [('uyen-lt-1-2','Phân biệt RGB và CMY'),('uyen-lt-2-1','Trường hợp sử dụng hai nguyên lý phối màu')],['Định nghĩa lại phối màu cộng/trừ; cơ chế màn hình RGB và máy in CMY'],['Ví dụ phối hai màu'],steps=[
        section('Hai ví dụ phối màu','Trong phối màu cộng RGB, ánh sáng đỏ cộng ánh sáng lục cho vàng. Trong phối màu trừ lý tưởng, cyan trộn yellow cho lục vì các mực hấp thụ bớt những thành phần ánh sáng khác nhau.')])
    partial('uyen-4-L2','Nêu ứng dụng điển hình của HSV/HSL trong việc chọn và hiệu chỉnh màu.', [],
      [('uyen-lt-1-1','Khái niệm và tên các mô hình màu'),('uyen-lt-1-3','Ý nghĩa các thành phần HSV/HSL'),('uyen-lt-2-1','Ứng dụng RGB và CMY')],['Định nghĩa và liệt kê lại mô hình; ứng dụng RGB/CMY'],['Ứng dụng HSV/HSL trong thao tác màu'],steps=[
        section('Ứng dụng chọn và hiệu chỉnh màu','HSV/HSL thuận tiện cho chọn và hiệu chỉnh màu vì tách tông màu, độ bão hòa và thành phần sáng. Người dùng có thể thay tông, tăng/giảm bão hòa hoặc điều chỉnh sáng theo các thuộc tính trực quan hơn việc thay riêng từng kênh RGB.')],title='Ứng dụng HSV/HSL trong chọn và chỉnh màu')
    partial('uyen-4-L3','Vì sao ba mực C, M, Y lý tưởng cho màu đen nhưng trong thực tế in ấn vẫn thêm mực đen K trong CMYK?', [1],
      [('uyen-lt-1-2','So sánh CMY với RGB')],['So sánh lại CMY và RGB'],['Lý do thực tế dùng thêm mực đen K'],title='Vì sao hệ CMYK cần mực đen K?')
    reference('uyen-4-L4',[('uyen-lt-1-3','Lý do phát triển HSV/HSL và ý nghĩa từng chữ cái')],['Toàn bộ yêu cầu HSV/HSL'])
    reference('uyen-4-L5',[('uyen-lt-1-4','Raster/vector và trường hợp sử dụng'),('uyen-lt-2-3','Vector và lý do vẫn dùng raster')],['Định nghĩa, so sánh và lựa chọn raster/vector'])
    reference('uyen-4-L6',[('uyen-lt-1-5','Mục đích và ý tưởng halftone')],['Toàn bộ yêu cầu halftone'])
    reference('uyen-4-L7',[('uyen-lt-1-6','Khuếch tán lỗi so với tách ngưỡng'),('uyen-lt-1-7','Một chiều, hai chiều và nhược điểm được khắc phục')],['Định nghĩa khuếch tán lỗi; so với ngưỡng; so sánh một/hai chiều'])
    partial('uyen-4-L8','Nhận định sau đúng hay sai? Giải thích: (d) Khuếch tán lỗi giữ nguyên số mức xám của ảnh gốc.', [3],
      [('uyen-lt-1-2','CMY là phối màu trừ'),('uyen-lt-1-4','Phóng to raster/vector'),('uyen-lt-1-5','Cảm nhận cường độ trung bình trong halftone')],['Các nhận định (a), (b), (c) đã hỏi'],['Nhận định (d): số mức xám sau lượng tử hóa'])

    reference('uyen-5-L1',[('uyen-lt-1-12','Biên và phát hiện trực tiếp'),('uyen-lt-2-6','Mặt nạ và cách tạo ảnh biên')],['Khái niệm biên, phát hiện trực tiếp, ví dụ mặt nạ và hậu xử lý'])
    partial('uyen-5-L2','Mặt nạ (−1,1)ᵀ khác về hướng so với (−1,1) như thế nào? Vì sao thường dùng |Gx|+|Gy| thay cho √(Gx²+Gy²)?', [1,2],
      [('uyen-lt-2-5','Nguyên lý đạo hàm và mặt nạ ngang')],['Hỏi lại nguyên lý phát hiện biên bằng đạo hàm'],['Mặt nạ chuyển vị theo hướng dọc; xấp xỉ độ lớn gradient'])
    partial('uyen-5-L3','Sobel khác Prewitt ở hệ số nào? Sự khác nhau đó có tác dụng gì khi phát hiện biên?', [],
      [('uyen-lt-2-6','Ba loại mặt nạ và các bước tạo biên')],['Nêu lại toàn bộ ba mặt nạ và hậu xử lý'],['So sánh trọng số và tác dụng của Sobel'],steps=[
        section('Khác biệt về trọng số','Prewitt dùng trọng số 1 ở hàng/cột giữa, còn Sobel dùng trọng số 2. Vì vậy Sobel nhấn mạnh các pixel gần tâm hơn trong hướng vuông góc với hướng lấy đạo hàm.'),
        section('Tác dụng','Trọng số 1–2–1 kết hợp lấy đạo hàm với làm trơn có trọng số theo hướng còn lại, giúp hạn chế ảnh hưởng của nhiễu hơn sai phân đơn giản. Điều này không bảo đảm Sobel luôn cho biên tốt hơn trên mọi ảnh.')],title='Sobel khác Prewitt ở đâu?')
    reference('uyen-5-L5',[('uyen-lt-2-7','Các bước Canny và vai trò các bước then chốt')],['Toàn bộ yêu cầu về Canny'])
    partial('uyen-5-L7','Trình bày các bước Otsu và công thức tiêu chuẩn chọn ngưỡng. Trình bày quá trình lặp ISODATA và điều kiện dừng.', [0,1,3],
      [('uyen-3-L8','So sánh tham số, điều kiện và trường hợp nhiều ngưỡng')],['Hỏi lại chung về nhiều ngưỡng và cách chọn nghiệm'],['Trình tự thực hiện và công thức Otsu; lặp ISODATA và dừng'])
    reference('uyen-5-L8',[('uyen-lt-2-8','Khái niệm và điều kiện đối xứng nền'),('uyen-3-L6','Các bước và tỷ lệ tích lũy'),('uyen-lt-2-9','Tam giác và trường hợp không phù hợp')],['Toàn bộ các ý đối xứng nền và tam giác'])
    reference('uyen-5-L9',[('uyen-lt-2-10','Ý tưởng và tiêu chuẩn của tách/hợp vùng')],['Toàn bộ yêu cầu tách cây tứ phân, hợp và tách–hợp'])

    partial('uyen-6-L1','Cho ví dụ bằng số minh họa một trường hợp RLC giảm kích thước và một trường hợp làm dữ liệu nở. Công bố rõ quy ước mã của ví dụ.', [1],
      [('uyen-lt-2-15','Khái niệm RLC và khi nào dữ liệu nở')],['Định nghĩa lại RLC và điều kiện chung'],['Ví dụ có số bit cụ thể'],title='Ví dụ bằng số về hiệu quả RLC')
    partial('uyen-6-L2','Ngoài lượng tử hóa, tính toán DCT/DCT ngược trong thực tế có thể phát sinh sai số như thế nào? Phân biệt sai số tính toán với tính khả nghịch của DCT về mặt lý thuyết.', [2],
      [('uyen-lt-2-16','Mục đích DCT và bước lượng tử gây tổn thất')],['Mục đích DCT; xác định lại bước lượng tử hóa'],['Sai số số học thực tế và tính khả nghịch lý thuyết'])
    by_id['uyen-6-L2']['steps'][0]['text']='Sai số hữu hạn của phép tính dấu chấm động, làm tròn hoặc cắt khi thực hiện DCT/DCT ngược có thể tạo sai lệch nhỏ trong thực tế. Về mặt toán học, DCT vẫn là phép biến đổi khả nghịch; sai số số học không làm thay đổi tính chất lý thuyết này.'
    h=original['uyen-6-L5']['steps']
    partial('uyen-6-L5','Trình bày nguyên lý và các bước Huffman. Vì sao giải mã là tức thời? Vì sao ảnh nhị phân cần chia khối trước khi mã hóa? Lỗi bit có thể ảnh hưởng thế nào tới đồng bộ giải mã?', [0,1,2],
      [('uyen-6-L3','Tần suất và việc gửi bảng mã trong Huffman tĩnh')],['Nhắc lại nhược điểm cần tần suất/bảng mã'],['Các bước; mã tiền tố; chia khối; mất đồng bộ vì lỗi bit'],steps=[*h[:3],section('Ảnh hưởng của lỗi bit','Từ mã Huffman có độ dài biến đổi. Một bit sai có thể đổi đường đi trên cây và ranh giới từ mã, làm một hoặc nhiều ký hiệu phía sau bị giải sai hoặc mất đồng bộ cho tới khi có điểm đồng bộ lại.')])
    partial('uyen-6-L7','Mô hình mã hóa ảnh gồm những khối nào? Nêu chức năng của mapper, quantizer và symbol encoder.', [0,1],
      [('uyen-lt-2-16','Lượng tử hóa không khôi phục chính xác'),('uyen-6-L2','Sai số và tổn thất trong JPEG')],['Hỏi lại riêng khối gây mất thông tin và lý do'],['Cấu trúc và chức năng các khối mã hóa'])
    tf=original['uyen-6-L9']['steps']
    partial('uyen-6-L9','Các nhận định sau đúng hay sai? Giải thích: (a) Mã Huffman luôn cho độ dài mã trung bình bằng đúng entropy của nguồn. (d) So với DFT, DCT ít gây méo ở mép khối hơn, nhưng JPEG vẫn có hiệu ứng khối khi nén mạnh. (e) Hệ số lượng tử Q(u,v) ở tần số cao thường lớn hơn ở tần số thấp.', [0,3,4],
      [('uyen-6-L3','LZW tự tái tạo từ điển'),('uyen-lt-2-16','DCT khả nghịch và lượng tử hóa gây mất mát')],['Nhận định (b) về gửi từ điển; (c) về DCT làm mất thông tin'],['(a) entropy/Huffman; (d) DCT/DFT và blocking; (e) bước lượng tử theo tần số'])

    partial('uyen-7-L8','Các nhận định sau đúng hay sai? Giải thích: (b) Nếu gốc SE là điểm 1 thì A⊖B⊆A⊆A⊕B. (c) Thực hiện phép mở hai lần với cùng SE cho kết quả khác một lần. (e) Với SE không đối xứng, dò hit trực tiếp B luôn trùng định nghĩa giãn chuẩn dùng B̂. (f) Phép co và giãn đối ngẫu: (A⊖B)ᶜ=Aᶜ⊕B̂.', [1,2,4,5],
      [('uyen-7-L3','Mở không luôn trả ảnh gốc; tác dụng nối khe của đóng'),('uyen-7-L6','Vì sao phải giao với Aᶜ khi làm đầy')],['Nhận định (a), (d), (g) đã hỏi'],['(b) điều kiện bao hàm co/giãn; (c) lũy đẳng; (e) SE bất đối xứng; (f) đối ngẫu'])

    # Keep the earlier response within its actual question, so new clauses really
    # belong to the later questions rather than appearing as unsolicited extras.
    by_id['uyen-lt-1-9']['steps']=deepcopy(original['uyen-lt-1-9']['steps'][:2])
    by_id['uyen-lt-1-10']['steps']=deepcopy(original['uyen-lt-1-10']['steps'][:1])
    by_id['uyen-lt-2-5']['steps']=[deepcopy(original['uyen-lt-2-5']['steps'][0]),
      section('Mặt nạ sai phân ngang','Đặt mặt nạ (−1,1) lên hai pixel kề ngang cho hiệu mức xám phía phải trừ phía trái. Đáp ứng lớn về độ lớn cho biết cường độ thay đổi mạnh theo hướng ngang.',r'G_x(r,c)=I(r,c+1)-I(r,c)')]
    by_id['uyen-7-L3']['steps']=deepcopy(original['uyen-7-L3']['steps'][:3])+[
      section('Quan hệ bao hàm','Theo định nghĩa hình thái chuẩn, mở là phép giảm còn đóng là phép tăng. Quan hệ dưới đây được hiểu trên miền nhất quán và đủ đệm trung gian, không cắt mất dữ liệu giữa hai phép.',r'A\circ B\subseteq A\subseteq A\bullet B')]
    for ident in ['uyen-lt-1-9','uyen-lt-1-10','uyen-lt-2-5','uyen-7-L3']:by_id[ident]['revision']=3
    assert len(REVIEW)==36
    assert all(by_id[i]['kind']=='theory' and by_id[i]['area']=='uyen' for i in REVIEW)
