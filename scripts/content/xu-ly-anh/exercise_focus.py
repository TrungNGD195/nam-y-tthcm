"""Remove repeated requests, keeping every exercise and every distinct condition.

Inputs/intermediate results are taken from the already checked computations.
Original PDF images/transcripts remain separate and immutable.
"""
from copy import deepcopy
import ast
import math

REVIEW={}


def group(steps,letter):
    return [deepcopy(s) for s in steps if s['section'].startswith(f'Câu ({letter})')]


def blocks(steps):
    return [deepcopy(b) for s in steps for b in s.get('blocks',[])]


def question(label,text):return dict(label=label,text=text)
def supplied(title,steps=(),text='',data=()):
    if not text:
        text=' '.join(s.get('result') or s.get('text','') for s in steps if not s.get('blocks'))
    return dict(title=title,text=text,blocks=deepcopy(list(data))+blocks(steps))


def response(section,lead,text=None,**fields):
    s=dict(section=section,lead=lead,**fields)
    if text:s['text']=text
    s.setdefault('method',text or 'Đối chiếu dữ kiện đã cho và thực hiện đúng yêu cầu của câu này.')
    return s


def apply(solutions,inputs):
    def edit(ident,title,prior,removed,novel,parts,steps,givens=None,provided=(),intro=''):
        old=solutions[ident]
        assert steps and parts
        earlier=[dict(id=ref,covered=covered) for ref,covered in prior]
        old.update(title=title,steps=steps,editedQuestion=dict(
            intro=intro or 'Các kết quả trung gian được tính cho đúng dữ kiện của bài này và cho sẵn ở dưới. Chỉ làm các yêu cầu còn lại; phần phương pháp đã học có liên kết để xem lại.',
            givens=deepcopy(inputs.get(ident,[]) if givens is None else givens),
            supplied=deepcopy(list(provided)),parts=parts,previous=earlier))
        REVIEW[ident]=dict(previous=earlier,removedRequests=removed,preservedFocus=novel,
                           questionLabels=[p['label'] for p in parts])

    s=deepcopy(solutions['uyen-3-T4']['steps']);rows=s[0]['blocks'][0]['rows']
    mapping=[r[-1] for r in rows]
    prob=deepcopy(s[0]);prob.update(section='Câu (a) — Xác suất và tích lũy',lead='Chuẩn hóa số pixel thành xác suất.',
      formula=r'p(r_k)=n_k/N,\quad F(k)=\sum_{j=0}^k p(r_j)',
      symbols='n_k là số pixel ở mức r_k; N=1024 là tổng pixel; p là xác suất; F(k) là xác suất tích lũy tới k.',
      method='Chia từng số đếm cho 1024, sau đó cộng dồn các xác suất từ mức 0 tới mức đang xét. Tổng xác suất cuối phải bằng 1.',
      substitution='p(0)=190/1024=0,185546875; F(1)=(190+261)/1024=0,4404296875.',result='F(7)=1.')
    prob['blocks']=[dict(type='table',headers=['r','n(r)','p(r)','F(r)'],rows=[r[:4] for r in rows])]
    out=[0]*8
    for r in rows:out[r[-1]]+=r[1]
    merged=response('Câu (b) — Những mức bị gộp','Đọc bảng ánh xạ đã cho và cộng số pixel.',
      'Các mức 4,5,6,7 cùng được ánh xạ tới 7. Các nhóm còn lại là 0→1, 1→3, 2→5, 3→6. Không cần tính lại hàm cân bằng.',
      formula=r'h_{out}(s)=\sum_{k:\,s_k=s}n_k',symbols='s_k là mức đầu ra đã cho của mức k; n_k là số pixel mức k; h_out(s) là số pixel sau gộp ở mức s.',
      substitution=f'h_out(7)=70+36+16+8={out[7]}.',result=f'Histogram đầu ra: {out}.')
    edit('uyen-3-T4','Xác suất và các mức xám bị gộp',[('uyen-3-T3','Công thức cân bằng theo slide')],
      ['Tính lại toàn bộ ánh xạ cân bằng theo cùng công thức'],['Chuẩn hóa xác suất, CDF trên ảnh 32×32; nhận diện nhóm mức bị gộp'],
      [question('a','Lập p(r_k) và tổng tích lũy F(k). Kiểm tra tổng xác suất.'),question('b','Dùng bảng ánh xạ cho sẵn để chỉ ra các mức bị gộp và lập histogram đầu ra.')],[prob,merged],
      provided=[supplied('Ánh xạ cân bằng đã tính',data=[dict(type='table',headers=['r_k','s_k'],rows=list(enumerate(mapping)))])],intro='Ảnh 32×32 có 8 mức xám. Số pixel từng mức và ánh xạ đã tính theo công thức slide được cho dưới đây.')

    s=deepcopy(solutions['uyen-3-T7']['steps'])
    edit('uyen-3-T7','Trung vị và ảnh hưởng của nhiễu xung',[('uyen-3-T6','Lọc trung bình trên chín điểm trong')],
      ['Tính lại ma trận lọc trung bình'],['Lọc trung vị; so sánh hai bộ lọc trên nhiễu muối tiêu'],
      [question('a','Lọc trung vị 3×3 tại chín điểm trong (hàng/cột 1–3, chỉ số từ 0).'),question('c','So với ảnh gốc và kết quả trung bình đã cho, bộ lọc nào phù hợp hơn với nhiễu muối tiêu? Giải thích.')],
      group(s,'a')+group(s,'c'),provided=[supplied('Kết quả lọc trung bình đã tính',data=blocks(group(s,'b')))])

    s=deepcopy(solutions['uyen-3-T9']['steps']);answer=group(s,'a')[0];table=answer['blocks'][0]
    given_rows=[r for r in table['rows'] if r[0] in ['số học','trung vị']]
    answer['blocks'][0]['rows']=[r for r in table['rows'] if r[0] not in ['số học','trung vị']]
    answer.update(section='Câu (a) — Năm bộ lọc còn lại',lead='Tính năm bộ lọc còn lại.',formula=r'G=(\prod_{i=1}^9x_i)^{1/9},\quad P=\frac{\max x_i+\min x_i}{2},\quad A_{d=2}=\frac17\sum_{i=2}^8x_{(i)}',
      symbols='x_i là chín mẫu; x_(i) là mẫu thứ i sau sắp tăng; G là trung bình hình học; P là điểm giữa; d=2 nghĩa là bỏ một mẫu nhỏ nhất và một mẫu lớn nhất.',
      method='Tính căn bậc chín của tích; đọc max và min; lấy trung bình hai cực trị cho điểm giữa. Với alpha-trimmed bỏ 3 và 200, lấy trung bình bảy mẫu còn lại.')
    edit('uyen-3-T9','Năm bộ lọc còn lại và hai cực trị',[('uyen-3-T6','Trung bình số học'),('uyen-3-T7','Trung vị')],
      ['Tính lại trung bình số học và trung vị'],['Trung bình hình học, max, min, điểm giữa và alpha-trimmed; tác động của hai cực trị'],
      [question('a','Tính đầu ra của trung bình hình học, max, min, điểm giữa và alpha-trimmed với d=2.'),question('b','Với hai giá trị đột biến 200 và 3, các bộ lọc trên chịu ảnh hưởng thế nào? So sánh với hai kết quả đã cho.')],
      [answer,*group(s,'b')],provided=[supplied('Hai kết quả đã tính',data=[dict(type='table',headers=table['headers'],rows=given_rows)])])

    s=deepcopy(solutions['uyen-4-T3']['steps']);a,b=s
    same=response('Câu (b) — Trường hợp hai ảnh kết quả trùng nhau','Đối chiếu từng pixel của hai kết quả đã cho.',
      'Trong đúng ma trận này, khuếch tán lỗi và tách ngưỡng cho cùng ảnh nhị phân: không có pixel khác nhau. Cả hai có 7 điểm trắng, độ sáng trung bình 7·255/18=99,16667. Đây là kết quả riêng của dữ kiện này; không suy ra hai phương pháp luôn tương đương.',
      method='So từng cặp pixel cùng hàng/cột, không chỉ so số điểm trắng. Kết quả ở bài 4.T2 cho ví dụ khác; sự trùng nhau tại một ảnh không chứng minh hai phép biến đổi giống nhau với mọi đầu vào.')
    edit('uyen-4-T3','Khi hai cách nhị phân hóa cho cùng kết quả',[('uyen-4-T2','Tính khuếch tán lỗi và giải thích mục đích chung')],
      ['Tính lại toàn bộ khuếch tán lỗi với cùng ngưỡng 127','Hỏi lại mục đích và lợi ích chung'],['So sánh cụ thể trường hợp hai ma trận đầu ra trùng nhau'],
      [question('b','Với θ=127 và hai kết quả đã tính dưới đây, có pixel đầu ra nào khác nhau không? So sánh số điểm trắng và độ sáng trung bình. Có thể suy ra hai phương pháp luôn tương đương không?')],
      [same],provided=[supplied('Hai ảnh nhị phân đã tính',data=[a['blocks'][0],b['blocks'][0]])])
    solutions['uyen-4-T3']['note']='Đề gốc nhắc nhầm dòng 2 toàn 90; ma trận thực tế của 4.T3 có dòng 2 là 143,27,5,251,33,76. Dòng toàn 90 thuộc 4.T4. Phần ôn tập dùng đúng dữ kiện và hai kết quả đã kiểm tra.'

    s=deepcopy(solutions['uyen-4-T4']['steps']);a,b=s
    row=[r for r in a['blocks'][1]['rows'] if r[0]==2]
    out=a['blocks'][0]['rows'];threshold=b['blocks'][0]['rows'];masked=deepcopy(a['blocks'][0]);masked['rows'][1]=['?']*5
    row_step=deepcopy(a);row_step.update(section='Câu (a) — Dòng 2 với ngưỡng 100',lead='Chỉ tính dòng 2 với ngưỡng 100.',
      formula=r'u=I-e_{prev},\quad b=\begin{cases}0&u<\theta\\255&u\ge\theta\end{cases},\quad e=b-u',
      symbols='I là mức tâm gốc bằng 90; e_prev là sai số pixel trước cùng dòng; u là mức sau bù; θ=100; b là đầu ra 0/255; e là sai số truyền tiếp.',
      substitution='Đầu dòng đặt e_prev=0. Pixel đầu: u=90−0=90<100 ⇒ b=0, e=−90. Pixel tiếp: u=90−(−90)=180≥100 ⇒ b=255, e=75.',
      blocks=[dict(type='table',headers=a['blocks'][1]['headers'],rows=row),dict(type='matrix',rows=[out[1]],caption='Dòng 2 sau khuếch tán lỗi')])
    compare=response('Câu (b) — Cùng độ sáng, khác phân bố pixel','So kết quả trên dòng 2 và trên cả ảnh.',
      'Dòng 2 khuếch tán lỗi là 0,255,0,255,0; tách ngưỡng trực tiếp cho toàn 0 vì 90<100. Trên cả ảnh, hai cách đều có 7 điểm trắng và độ sáng trung bình 119, nhưng các vị trí trắng khác nhau. Số điểm trắng/độ sáng trung bình không mô tả hết cấu trúc ảnh.',
      method='Dùng dòng 2 vừa tính để hoàn thiện ảnh đã cho, so từng pixel với ảnh tách ngưỡng. Sau đó đếm tổng điểm trắng của cả ảnh; không suy từ tổng bằng nhau rằng hai ma trận bằng nhau.')
    edit('uyen-4-T4','Dòng đồng mức 90 với ngưỡng 100',[('uyen-4-T2','Quy trình khuếch tán lỗi toàn ảnh; mục đích chung'),('uyen-4-T3','Đối chiếu hai ảnh đầu ra')],
      ['Tính lại các dòng không có ý mới','Hỏi lại định nghĩa/mục đích khuếch tán lỗi'],['Đổi ngưỡng sang 100; xử lý riêng dòng toàn 90; hai ảnh cùng độ sáng nhưng khác vị trí pixel'],
      [question('a','Tính riêng dòng 2 (năm pixel đều bằng 90) bằng khuếch tán lỗi với θ=100. Ghi sai số từng pixel, bắt đầu dòng với sai số 0.'),question('b','Hoàn thiện ảnh cho sẵn rồi so sánh dòng 2, số điểm trắng và độ sáng trung bình với tách ngưỡng. Tổng độ sáng bằng nhau có đồng nghĩa hai ảnh giống nhau không?')],
      [row_step,compare],provided=[supplied('Các phần đã tính: chỉ còn điền dòng 2',data=[masked,dict(type='matrix',rows=threshold,caption='Tách ngưỡng trực tiếp θ=100')])])

    s=deepcopy(solutions['uyen-5-T2']['steps'])
    edit('uyen-5-T2','Sobel và Laplace 4 láng giềng',[('uyen-5-T1','Nhận xét đáp ứng lọc và các bước tạo biên')],
      ['Hỏi lại I₁/I₂ đã là ảnh biên chưa và cần làm gì tiếp'],['Hai mặt nạ mới Sobel/Laplace 4; ghép bằng trị tuyệt đối thay cho cộng có dấu'],
      [question('a','Dùng Hx,Hy đã cho để tính Gx,Gy và I₁=|Gx|+|Gy|. Đặt tâm, không lật mặt nạ, đệm 0.'),question('b','Tính I₂ bằng mặt nạ Hz (Laplace 4 láng giềng), cùng quy ước đặt tâm và đệm biên.')],group(s,'a')+group(s,'b'))

    s=deepcopy(solutions['uyen-5-T3']['steps']);g1=group(s,'a')[-1]['blocks'][0];g2=group(s,'b')[-1]['blocks'][0]
    diffs=[[r+1,c+1,g1['rows'][r][c],g2['rows'][r][c],g2['rows'][r][c]-g1['rows'][r][c]] for r in range(len(g1['rows'])) for c in range(len(g1['rows'][0])) if g1['rows'][r][c]!=g2['rows'][r][c]]
    compare=response('Câu (c) — Nhiễu làm thay đổi đáp ứng ở đâu?','Lấy hiệu hai đáp ứng đã cho.',
      group(s,'c')[0].get('text',''),formula=r'\Delta G(r,c)=G_2(r,c)-G_1(r,c)',symbols='G₁,G₂ là độ lớn gradient của S₁,S₂ đã cho; (r,c) đếm từ 1; ΔG≠0 đánh dấu pixel đáp ứng bị thay đổi.',
      method='So từng ô cùng vị trí, tính G₂−G₁. Mỗi điểm nhiễu chỉ tác động các cửa sổ 3×3 chứa nó; hai ảnh đầu vào chỉ khác hai pixel nhưng nhiều pixel đáp ứng có thể đổi.',
      substitution=f'Tại ({diffs[0][0]},{diffs[0][1]}): ΔG={diffs[0][3]}−{diffs[0][2]}={diffs[0][4]}.',
      result=f'Có {len(diffs)} vị trí đáp ứng khác nhau.',blocks=[dict(type='table',headers=['hàng','cột','G₁','G₂','ΔG'],rows=diffs)])
    edit('uyen-5-T3','Phạm vi ảnh hưởng của hai điểm nhiễu',[('uyen-5-T1','Nhân mặt nạ Prewitt và tính đáp ứng'),('uyen-5-T2','Tính độ lớn gradient')],
      ['Nhân chập lại toàn bộ hai ảnh'],['Vị trí đáp ứng thay đổi, ảnh hưởng khuếch đại/triệt tiêu và cách giảm nhiễu'],
      [question('c','Dùng hai đáp ứng gradient đã tính để chỉ ra các vị trí thay đổi. Vì sao hai điểm nhiễu có thể làm đổi nhiều điểm đáp ứng? Nêu cách khắc phục.')],
      [compare],provided=[supplied('Hai đáp ứng gradient đã tính',data=[g1,g2])])

    s=deepcopy(solutions['uyen-5-T4']['steps']);tie=group(s,'b')[0];table=tie['blocks'][0]
    values={r[0]:r[-1] for r in table['rows'][:-1]}
    answer=response('Câu (b) — Hai cực đại rời nhau','Kiểm tra trực tiếp tiêu chuẩn tại từng ngưỡng.',
      'Hai ngưỡng tối ưu là 3 và 5. Trung bình của chúng bằng 4 nhưng f(4) nhỏ hơn cực đại, nên 4 không phải nghiệm tối ưu Otsu của histogram này. Có thể chọn 3 hoặc 5 và công bố quy tắc phá hòa; chỉ lấy trung bình khi mức trung bình vẫn đạt cực đại.',
      formula=r'\Theta^*=\{g:f(g)=\max_k f(k)\}',symbols='f(g) là tiêu chuẩn Otsu đã tính trong bảng; Θ* là tập các ngưỡng đạt cực đại. g,k chỉ chạy qua ngưỡng có hai lớp không rỗng.',
      method='Tìm tất cả hàng đạt giá trị f lớn nhất. Kiểm tra riêng hàng của ngưỡng trung bình trước khi chọn, không giả định các nghiệm cực đại luôn tạo một đoạn liên tục.',
      substitution=f'f(3)=f(5)={values[3]}; f(4)={values[4]} < {values[3]}.',result='Chọn θ=3 hoặc θ=5; không chọn θ=4 nếu yêu cầu cực đại hóa Otsu.')
    edit('uyen-5-T4','Hai ngưỡng Otsu tối ưu không liền nhau',[('uyen-3-T10','Lập bảng Otsu và câu hỏi chung về nhiều ngưỡng')],
      ['Tính lại Otsu toàn ảnh','Hỏi lại chung chung khi nào có nhiều ngưỡng'],['Áp dụng trên histogram có hai cực đại rời nhau; kiểm tra quy tắc lấy trung bình'],
      [question('b','Từ bảng Otsu của histogram dưới đây, tìm mọi ngưỡng tối ưu. Trung bình của các ngưỡng đó có còn tối ưu không? Hãy kiểm tra bằng f(g) và nêu cách chọn ngưỡng.')],
      [answer],givens=[deepcopy(table)])
    solutions['uyen-5-T4']['note']='Histogram này có cực đại tại 3 và 5 nhưng không tại 4. Lấy trung bình máy móc sẽ làm mất điều kiện tối ưu; lời giải kiểm tra lại bằng tiêu chuẩn Otsu.'

    s=deepcopy(solutions['uyen-5-T5']['steps']);c=group(s,'c')
    background_b=group(s,'b')
    background_b[0]['result']+=' Ở 3.T11, a là mức lớn nhất có tích lũy ≤p%N; ở đây a là mức nhỏ nhất có tích lũy ≥p%N, nên hai quy ước có thể cho ngưỡng khác nhau.'
    edit('uyen-5-T5','Phân vị đầu đạt p% và lựa chọn phương pháp',[('uyen-3-T11','Lặp đẳng điệu và đối xứng nền với phân vị cuối không vượt p%')],
      ['Lặp lại các bảng đẳng điệu đã học'],['Quy ước phân vị đầu đạt p%; độ chính xác 95%/90%; đánh giá hai histogram mới'],
      [question('b','Với ảnh B và p=95%, lấy a nhỏ nhất có tích lũy ≥p%N, rồi tính T=2maxp−a. Chỉ rõ sự khác nhau với quy ước cuối không vượt p% ở 3.T11.'),question('c','Dùng cùng quy ước đầu đạt p% để tính đối xứng nền cho A với p=90%. So với các kết quả đẳng điệu cho sẵn, chọn phương pháp phù hợp cho từng histogram và giải thích theo giả thiết nền.')],
      background_b+c[:1]+c[-1:],provided=[supplied('Kết quả đẳng điệu A (t₀=2)',group(s,'a')),supplied('Kết quả đẳng điệu B (t₀=6)',c[1:2])])

    s=deepcopy(solutions['uyen-5-T6']['steps']);provided_blocks=blocks(s[:3])
    for b in provided_blocks:
        if b['type']=='table' and len(b['headers'])==2 and b['headers'][0]=='g' and 'h_s' in b['headers'][1]:
            b['rows']=[[r[0],round(r[1],2)] for r in b['rows']]
    edit('uyen-5-T6','Đếm đỉnh trước và sau làm trơn',[('uyen-3-T1','Đếm histogram'),('uyen-3-T2','Làm trơn W=3, W=5')],
      ['Đếm lại histogram và tính lại hai cửa sổ làm trơn'],['Đếm cực đại cục bộ, xử lý plateau, ảnh hưởng của làm trơn đến tìm ngưỡng'],
      [question('c','Đếm cực đại cục bộ trong miền trong của ba histogram đã cho; một plateau cao hơn hai phía tính là một đỉnh. Nhận xét tác dụng của làm trơn đối với tìm ngưỡng.')],
      group(s,'c'),givens=provided_blocks,intro='Ba histogram cùng dữ kiện nguồn đã được tính sẵn: h(g), h_s với W=3 và W=5 (hiển thị hai chữ số thập phân).')

    s=deepcopy(solutions['uyen-5-T7']['steps']);rows=s[0]['blocks'][0]['rows'];masked=deepcopy(rows)
    for r in masked:
        if r[0] in [3,4]:r[-1]='?'
    check=deepcopy(s[0]);check.update(section='Câu (a) — Hai khoảng cách cần hoàn thiện',lead='Thay hai điểm g=3,4 vào đường thẳng đã cho.',
      substitution='d(3)=|51·3+7·24−466|/√(51²+7²)=145/√2650≈2,81673; d(4)=|51·4+7·9−466|/√2650=199/√2650≈3,86572.',
      result='So với các khoảng cách còn lại đã cho, d lớn nhất tại g=4 nên T=4.')
    edit('uyen-5-T7','Hoàn thiện kiểm tra ngưỡng tam giác',[('uyen-3-T12','Dựng đường tam giác và tính mọi khoảng cách')],
      ['Dựng lại đường thẳng và tính lại toàn bộ bảng khoảng cách'],['Kiểm tra hai mức quanh ngưỡng trên dữ kiện có đỉnh g=2 đã cố định'],
      [question('a','Đường nối đỉnh (2,52) với cuối đuôi (9,1) đã có phương trình 51g+7h−466=0. Hoàn thiện d(3), d(4) trong bảng rồi chọn ngưỡng theo khoảng cách lớn nhất.')],
      [check],givens=[dict(type='table',headers=['g','h(g)','d(g)'],rows=masked)])

    s=deepcopy(solutions['uyen-6-T2']['steps'])
    s_b=response('Câu (b) — Đổi nhánh và hòa tần suất','Phân biệt chuỗi mã với độ dài mã.',
      'Đảo nhánh 0/1 đổi các bit của từ mã nhưng giữ độ sâu lá, nên giữ độ dài từng mã và tổng số bit. Hoán đổi hai ký hiệu có cùng tần suất có thể đổi từ mã của chúng; tổng n₂ không đổi vì hai tần suất bằng nhau. Với dữ liệu cụ thể, chuỗi bit có thể đổi dù tổng độ dài không đổi.',
      method='Với đảo nhánh, theo dõi số cạnh từ gốc tới lá. Với đổi hai ký hiệu cùng tần suất n, so n·ℓ₁+n·ℓ₂ trước/sau hoán đổi; hai tổng bằng nhau.')
    freq=group(s,'a')[0]['blocks'][0];nb=sum(r[1] for r in freq['rows']);n2=sum(r[1]*len(r[3]) for r in freq['rows'])
    freq['headers']=[freq['headers'][i] for i in [0,1,3]];freq['rows']=[[r[i] for i in [0,1,3]] for r in freq['rows']]
    edit('uyen-6-T2','Hòa tần suất và so sánh mã cố định',[('uyen-6-T1','Mã hóa Huffman, số bit và tỷ lệ nén')],
      ['Lập lại toàn bộ mã Huffman và tỷ lệ nén'],['Đổi vai trò ký hiệu cùng tần suất/nhánh 0–1; mã có độ dài cố định'],
      [question('b','Với bảng mã cho sẵn, nếu đổi hai ký hiệu có cùng tần suất hoặc đảo nhánh 0/1, chuỗi mã và tổng số bit có thay đổi không? Giải thích.'),question('c','Dùng mã độ dài cố định thay Huffman: mỗi khối cần ít nhất bao nhiêu bit? Tính n₂, CR và so với Huffman đã cho.')],
      [s_b,*group(s,'c')],givens=[],provided=[supplied('Huffman đã tính cho đúng ảnh này',text=f'Ảnh nhị phân có {nb} khối 2×2, n₁={nb*4} bit, n₂={n2} bit, CR={nb*4/n2:.5f}. Không tính chi phí bảng mã.',data=[freq])])

    s=deepcopy(solutions['uyen-6-T6']['steps']);decoder=s[1];trace=decoder['blocks'][0]['rows']
    special=[]
    for n,r in enumerate(trace):
        if 'mã chưa có' in str(r[-1]):special.append([r[0],str(ast.literal_eval(trace[n-1][1])),r[1]])
    assert special,'The intended new LZW case must actually occur'
    problem_rows=[[r[0],r[0],r[1]] for r in special]
    answer=response('Câu (a) — Mã kế tiếp chưa có trong từ điển','Dùng chuỗi trước để dựng mục còn thiếu.',
      'Khi mã nhận đúng bằng chỉ số mục kế tiếp chưa có, entry=w+first(w). Chỉ trường hợp này mới hợp lệ; mã khác không có trong từ điển là dữ liệu lỗi.',
      formula=r'entry=w+first(w)',symbols='w là chuỗi đã giải ở lượt trước; entry là chuỗi phải xuất cho mã hiện tại; first(w) là ký hiệu đầu; + là nối chuỗi, không phải cộng số.',
      method='Với từng trạng thái đã cho, lấy ký hiệu đầu của w và nối vào cuối w. Dùng entry vừa dựng để tiếp tục đúng quy tắc cập nhật từ điển.',
      substitution='; '.join(f'Mã {r[0]}: w={r[1]} ⇒ entry={r[2]}' for r in special)+'.',
      blocks=[dict(type='table',headers=['mã chưa có','w trước đó','entry đúng'],rows=special)])
    edit('uyen-6-T6','Trường hợp LZW nhận mã chưa có',[('uyen-6-T4','Mã hóa/giải mã LZW và tính số bit'),('uyen-6-T5','Thay đổi từ điển gốc và độ dài mã')],
      ['Lập lại toàn bộ bảng mã hóa và giải mã thường','Tính lại CR theo cùng cách'],['Tình huống thực tế mã nhận bằng mục kế tiếp; từ điển gốc 0–7 cho khối 1×3'],
      [question('a','Mỗi dòng cho một trạng thái trong giải mã ảnh khối 1×3, từ điển gốc 0–7. Mã nhận chưa có nhưng bằng đúng mục next. Hãy xác định entry cần xuất và giải thích quy tắc xử lý.')],
      [answer],givens=[dict(type='table',headers=['mã nhận','next','w đã giải trước đó'],rows=problem_rows)],
      provided=[supplied('Dãy mã đã tính',text=s[0]['result'])])

    s=deepcopy(solutions['uyen-6-T10']['steps']);e=group(s,'e')[0]
    e.update(lead='Giải các cặp RLE thành vị trí AC.',substitution='Dãy cặp nhận: (0,5), (1,−3), (3,2), (0,−1), (0,0).',
      method='Bắt đầu vị trí AC đầu là chỉ số 1 trong vector 1×64. Với mỗi cặp, bỏ qua skip ô 0 rồi đặt value; cặp (0,0) điền 0 tới hết AC thứ 63. Chỉ số 0 dành cho DC.')
    edit('uyen-6-T10','DPCM DC và giải mã ngược RLE',[('uyen-6-T9','Quét AC và mã hóa RLE thành cặp')],
      ['Mã hóa lại vector AC thành các cặp'],['DPCM và Huffman DC; khôi phục DC; giải ngược cặp RLE và xác định chỉ số AC'],
      [question('a','Tính dãy DPCM của các DC đã cho, DC trước khối đầu bằng 0.'),question('b','Xác định CAT, mã Huffman, bit biên độ và tổng bit cho tám hiệu DC.'),question('c','Khôi phục DC từ dãy DPCM 40,−3,5,0,−12,6,−1,2, với DC trước khối đầu bằng 0.'),question('d','Vì sao mã hóa hiệu DC có thể giảm số bit so với DC tuyệt đối?'),question('e','Giải dãy cặp (0,5),(1,−3),(3,2),(0,−1),(0,0) thành 63 AC; chỉ ra chỉ số và giá trị các hệ số khác 0 trong vector 1×64 có DC ở chỉ số 0.')],
      [*group(s,'a'),*group(s,'b'),*group(s,'c'),*group(s,'d'),e],givens=[b for b in inputs['uyen-6-T10'] if b.get('caption')!='63 hệ số AC, đọc theo hàng'])

    s=deepcopy(solutions['uyen-6-T11']['steps'])
    edit('uyen-6-T11','JPEG 2×2: DCT, mã AC và giải nén',[('uyen-6-T9','Lượng tử hóa và quét zig-zag'),('uyen-6-T10','Mã hóa DC bằng DPCM/CAT/bit biên độ')],
      ['Tính lại lượng tử hóa và vector zig-zag','Mã hóa lại DC theo quy trình đã học'],['DCT ma trận 2 điểm; Huffman RUN/CAT của AC; ghép chuỗi toàn khối; DCT ngược 2×2 và RMS'],
      [question('a','Tính I_DCT=T·I·Tᵀ theo ma trận DCT 2 điểm đã cho; bỏ dịch mức.'),question('e','Từ vector lượng tử đã cho, mã hóa AC thành RUN/value, xác định CAT, tra Huffman và nối bit biên độ. Có cần EOB không?'),question('f','Nối mã DC cho sẵn với các mã AC vừa tìm để viết toàn bộ chuỗi bit và độ dài.'),question('g','Giải lượng tử, DCT ngược và tính RMS so với I gốc. Viết rõ từng bước và ký hiệu.')],
      [*group(s,'a'),*group(s,'e'),*group(s,'f'),*group(s,'g')],givens=[b for b in inputs['uyen-6-T11'] if b.get('headers')!=['CAT','mã Huffman DC']],
      provided=[supplied('Kết quả lượng tử hóa đã tính',group(s,'b')),supplied('Vector zig-zag đã tính',text=group(s,'c')[0]['text'].split('. ')[0]+'.'),supplied('Mã DC đã tính, DC trước bằng 13',text=group(s,'d')[0]['result'].split('. ')[0]+'.')])

    s=deepcopy(solutions['uyen-6-T12']['steps'])
    edit('uyen-6-T12','SNR và đánh giá chất lượng ảnh nén',[('uyen-6-T8','RMS khi khôi phục bằng DC'),('uyen-6-T9','RMS từ sai số lượng tử'),('uyen-6-T11','RMS sau DCT ngược')],
      ['Tính lại RMS từ hai ma trận'],['SNR theo năng lượng ảnh khôi phục; đổi dB; so sánh CR kết hợp chất lượng cảm nhận'],
      [question('b','Dùng SSE=91 đã tính để tìm SNR_ms với năng lượng ảnh khôi phục ở tử số, rồi đổi sang dB.'),question('c','Ảnh có CR=12 có luôn tốt hơn ảnh có CR=6 không? Vì sao cần kết hợp đánh giá chủ quan?')],
      group(s,'b')+group(s,'c'),provided=[supplied('Sai số đã tính',text=s[0]['substitution'])])

    s=deepcopy(solutions['uyen-7-T2']['steps'])
    edit('uyen-7-T2','SE bất đối xứng và giãn chuẩn',[('uyen-7-T1','Tính co và giãn theo fit/hit')],
      ['Tính lại co và giãn hit toàn ảnh'],['Phản xạ SE bất đối xứng; phân biệt hit trực tiếp và giãn chuẩn; co có đổi không'],
      [question('b','SE B có đối xứng qua gốc không? Viết B̂ và tính giãn chuẩn bằng dò hit với B̂. So với giãn hit B cho sẵn, những pixel nào khác? Phép co có đổi không?')],
      group(s,'b'),provided=[supplied('Co và giãn hit B đã tính',group(s,'a'))])

    s=deepcopy(solutions['uyen-7-T3']['steps'])
    edit('uyen-7-T3','So sánh hai SE và chứng minh bao hàm',[('uyen-7-T1','Co và giãn'),('uyen-7-T2','Ảnh hưởng của SE')],
      ['Tính lại ba ma trận co/giãn cơ bản'],['Số điều kiện fit tăng khi SE lớn hơn; chứng minh quan hệ bao hàm với cùng gốc'],
      [question('c','So số điểm 1 trong hai ảnh co đã cho. Chứng minh B₁⊆B₂, cùng gốc, thì X⊖B₂⊆X⊖B₁.')],
      group(s,'c'),provided=[supplied('Các phép co/giãn đã tính',group(s,'a')+group(s,'b'))])

    for ident,prior,verb in [('uyen-7-T4','uyen-7-T1','Co'),('uyen-7-T5','uyen-7-T1','Giãn')]:
        s=deepcopy(solutions[ident]['steps']);opening=ident.endswith('T4')
        edit(ident,'Mở ảnh và chi tiết bị loại' if opening else 'Đóng ảnh, lỗ và khe hẹp',[(prior,f'{verb} cơ bản')],
          [f'Tính lại ảnh {verb.lower()} trung gian'],['Phép mở và các chi tiết mất' if opening else 'Phép đóng và phụ thuộc hình dạng khe/SE'],
          [question('b','Dùng ảnh co cho sẵn để tính phép mở A∘B.' if opening else 'Dùng ảnh giãn cho sẵn để tính phép đóng A•B.'),question('c','Những thành phần nào bị loại? Giải thích bằng điều kiện fit của SE.' if opening else 'Lỗ trong khối trái và khe cột 6 thay đổi thế nào? Vì sao khe chỉ lấp ở một số hàng?')],
          group(s,'b')+group(s,'c'),provided=[supplied(f'Ảnh {verb.lower()} trung gian đã tính',group(s,'a'))])

    s=deepcopy(solutions['uyen-7-T6']['steps'])
    known=blocks(group(s,'a'))[1:]
    known[0]['caption']='O=A∘B đã tính';known[1]['caption']='C=A•B đã tính'
    edit('uyen-7-T6','Bao hàm, lũy đẳng và chi tiết bị xóa',[('uyen-7-T4','Phép mở'),('uyen-7-T5','Phép đóng')],
      ['Tính lại mở và đóng lần thứ nhất'],['Kiểm tra bao hàm từng pixel; lặp trên kết quả để chứng minh lũy đẳng; vai trò lỗ đối với vùng rộng đúng 3 pixel'],
      [question('b','Kiểm tra O⊆A⊆C trên từng pixel của các ma trận đã cho.'),question('c','Tính O∘B và C•B bằng cùng SE rồi so với O,C. Rút ra tính chất.'),question('d','Vì sao phần bên trái cột 2–4 bị xóa sau mở dù rộng đúng ba pixel?')],
      group(s,'b')+group(s,'c')+group(s,'d'),provided=[supplied('O=A∘B và C=A•B đã tính',data=known)])

    s=deepcopy(solutions['uyen-7-T7']['steps'])
    edit('uyen-7-T7','Phần bù và tách biên từ ảnh co',[('uyen-7-T1','Tính ảnh co')],
      ['Tính lại ảnh co E'],['Phần bù trong khung ảnh; AND với ảnh gốc để tách biên trong; đếm điểm biên'],
      [question('b','Lấy phần bù Eᶜ trong đúng khung 6×10.'),question('c','Tính β(A)=A∩Eᶜ và đếm số điểm biên.')],
      group(s,'b')+group(s,'c'),provided=[supplied('E=A⊖s đã tính',group(s,'a'))])

    s=deepcopy(solutions['uyen-7-T8']['steps'])
    edit('uyen-7-T8','Hai đường biên và liên thông 4/8',[('uyen-7-T7','Tính biên trong bằng ảnh co')],
      ['Tính lại hai ảnh biên trong'],['Đối chiếu vị trí biên theo hai SE; phân biệt liên thông 4 và 8'],
      [question('b','Hai ảnh biên đã cho khác nhau ở những pixel nào? Kiểm tra liên thông 4 và liên thông 8 của từng đường biên.')],
      group(s,'b'),provided=[supplied('Hai ảnh biên đã tính',group(s,'a'))])

    for ident in REVIEW:
        solutions[ident]['revision']=2
    assert len(solutions)==67 and all(s['steps'] for s in solutions.values())
