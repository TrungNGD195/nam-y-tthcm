"""All 67 numerical source problems, with worked formulas and computed results."""
from calculations import *

def M(s):return [[int(x) for x in row.split()] for row in s.split('/')]
SOLUTIONS={}
def put(id,title,ch,keys,steps,note=''):
    SOLUTIONS[id]=solution(title,ch,keys,steps,note)

I=M('1 2 1 3 2 1/4 4 3 2 4 0/6 9 2 3 2 1/6 2 0 5 3 0/3 4 0 5 1 5/5 6 8 9 3 6')
H=hist(I,10)
put('bank-3-1','Histogram và |g−4|',3,'histogram|gộp mức xám',[histstep(H),transformed(H,lambda g:abs(g-4),r'|g-4|')])
put('bank-3-2','Histogram và |2g−9|',3,'histogram|gộp mức xám',[histstep(H),transformed(H,lambda g:abs(2*g-9),r'|2g-9|')])
put('bank-3-3','Làm trơn histogram W=3, W=5',3,'histogram|trung bình trượt',[histstep(H),smoothstep(H,3),smoothstep(H,5)],'Bản đáp án chi tiết thay nhầm pixel hàng 5 cột 5 từ 1 thành 0 và bỏ mức 7. Lời giải này giữ đúng ma trận của ngân hàng câu hỏi; không chép bảng đếm sai đó.')
for id,s in [('3-4','3 1 4 4 2 3/3 2 2 0 5 1/1 2 3 1 0 1/4 1 0 2 4 4/3 1 0 1 0 1/2 1 3 2 1 3'),('3-5','3 4 1 1 4 3/3 4 4 5 0 4/4 4 3 4 5 4/1 4 5 4 0 2/3 4 5 4 5 4/2 4 3 4 2 3')]:
    put('bank-'+id,'Cân bằng ảnh 6 mức xám',3,'tích lũy|TB|cân bằng lý tưởng',[equalstep(M(s),6)])
for id,s in [('3-6','1 23 156 22 45/133 13 12 12 212/12 232 127 32 21'),('3-7','11 23 156 2 45/12 133 32 12 112/12 232 127 32 128')]:
    put('bank-'+id,'Khuếch tán lỗi một chiều',4,'sai số lượng tử|đầu dòng',[diffusionstep(M(s))])

HB1=M('1 1 1 0 1 1 1 1 1 1 1 0 1 1 1 1 1 0 0 1/1 1 0 1 1 1 1 1 1 0 1 0 1 1 1 0 1 0 0 1/1 0 1 0 1 1 1 1 1 0 0 1 1 1 0 0 0 0 0 0/0 1 0 1 1 0 0 0 1 0 0 1 1 0 1 1 1 1 0 0/1 1 1 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1/0 0 0 1 1 1 1 0 1 1 0 1 1 1 0 0 0 0 1 1')
HB2=M('1 1 1 0 1 1 1 1 1 1 1 0 1 1 1 1 1 0 0 1/1 1 0 1 1 1 1 1 0 0 1 0 1 1 1 0 1 0 0 1/1 0 1 0 1 1 1 1 1 0 0 1 1 1 0 0 1 1 0 0/0 1 0 1 1 0 0 0 1 0 0 1 1 0 1 1 1 1 0 0/1 1 1 1 1 1 1 1 1 1 1 0 0 0 1 0 0 0 1 1/0 0 1 1 1 1 1 0 1 1 0 1 1 1 0 1 0 0 1 1')
for id,a in [('bank-3-8',HB1),('bank-3-9',HB2)]:put(id,'Huffman theo khối 2×2',6,'hai tần suất nhỏ nhất|tiền tố',huffmansteps(a))
XB=M('0 1 1 0 0 1 0 0/1 1 0 0 0 1 1 0/0 1 1 0 1 1 1 1/1 1 0 1 1 1 1 1/1 0 1 1 1 1 0 0/1 0 0 1 0 1 1 1/1 0 1 1 1 0 1 0/1 0 0 0 1 1 1 1')
put('bank-3-10','Co, giãn với SE chữ thập',7,'fit|hit',[morphstep(XB,CROSS)])
put('bank-3-11','Co, giãn với SE bất đối xứng',7,'fit|hit|phản xạ SE',[morphstep(XB,M('1 0 0/0 1 1/1 0 0'),True)],'Dùng quy ước fit/hit của slide cho kết quả chính; bổ sung riêng kết quả giãn tập hợp chuẩn vì SE không đối xứng, không tráo hai kết quả.')
IB=M('2 2 2 2 2 2 2/2 2 2 2 2 2 2/2 2 15 15 15 2 2/2 2 13 12 16 2 2/2 2 15 15 15 2 2/2 2 2 2 2 2 2/2 2 2 2 2 2 2')
for id,hx,hz in [('4-1',PREWITT,LAP8),('4-2',SOBEL,LAP4)]:
    put('bank-'+id,'Nhân chập và đáp ứng biên',5,'đặt tâm|gradient|Laplace',edge_steps(IB,hx,transpose(hx),hz,True),'Đề yêu cầu cộng hai đáp ứng: giữ phép cộng có dấu ở phần a. Để có độ lớn gradient cần |Gx|+|Gy|. Đề chỉ ghi tâm giữa, chưa nói biên: lời giải công bố đệm 0; phần trong không phụ thuộc cách đệm.')
for id,s1,s2,hx in [('4-3','5 5 5 5 5 5 5/4 5 5 5 5 5 5/3 4 5 5 5 5 5/3 3 4 5 5 5 5/3 3 3 4 4 4 4/3 3 3 3 3 3 3/3 3 3 3 3 3 3','5 5 5 5 5 5 5/14 5 5 5 5 5 5/3 14 5 5 5 5 5/3 3 14 5 5 5 5/3 3 3 14 14 14 14/3 3 3 3 3 3 3/3 3 3 3 3 3 3',PREWITT),('4-4','5 5 5 5 5 5 5/5 5 5 5 5 5 5/5 5 5 5 5 5 5/5 5 5 5 5 5 5/5 5 5 4 4 4 4/5 4 4 3 3 3 3/4 3 3 3 3 3 3','5 5 5 5 5 5 5/5 5 5 5 5 5 5/5 5 5 5 5 5 5/5 5 5 5 5 5 5/5 5 5 14 14 14 14/5 14 14 3 3 3 3/14 3 3 3 3 3 3',SOBEL)]:
    steps=edge_steps(M(s1),hx,transpose(hx),signed=True,name='I₁')+edge_steps(M(s2),hx,transpose(hx),signed=True,name='I₂')
    steps.append(step('So sánh đáp ứng của hai ảnh.',text='Ảnh thứ hai thay dải chuyển tiếp bằng mức 14 nên tạo biến thiên lớn hơn và thêm đáp ứng quanh dải đó; không chỉ khuếch đại đều toàn ảnh. Phép đạo hàm nhạy với nhiễu/đỉnh sáng; cần làm trơn trước khi tìm biên. Phép cộng có dấu có thể che khuất một số đáp ứng do triệt tiêu.'))
    put('bank-'+id,'So sánh biên ảnh có dải sáng',5,'đạo hàm|nhiễu|triệt tiêu',steps)
for id,s in [('4-5','1 4 1 1 2 3 2 3/3 2 3 2 5 2 6 2/2 3 8 2 3 2 5 6/4 5 2 4 2 9 1 4/2 4 3 2 0 1 2 1/3 5 7 1 2 4 5 6'),('4-6','1 4 1 1 2 3 2 3/3 2 3 2 5 2 6 2/2 1 8 2 3 2 5 6/2 5 2 4 2 9 1 4/2 2 3 2 0 1 2 1/1 5 7 1 2 4 5 6')]:
    a=M(s);put('bank-'+id,'Tìm ngưỡng tự động',3,'phương sai giữa lớp|cực đại',[histstep(hist(a,10)),otsustep(hist(a,10),a)])
for id,ha,hb,p in [('4-7',[27,45,33,22,22,36,45,34,23,13],[2,3,4,5,7,8,12,47,10,2],88),('4-8',[13,45,33,22,22,36,47,43,32,13],[2,3,4,5,7,12,47,11,8,2],91),('4-8-bs',[20,40,30,50,70,60,120,250,100,20],[39,45,53,72,40,112,25,34,23,13],88)]:
    steps=[isostep(ha,5,False),backgroundstep(hb,p,False),step('Đánh giá giả thiết trước khi đổi phương pháp.',text='Đẳng liệu phù hợp khi hai lớp có trung bình khác nhau; đối xứng nền phù hợp nền trội gần đối xứng, không mặc nhiên đúng chỉ vì có một đỉnh lớn. Với mỗi biểu đồ cần nhìn hình dạng: nếu nền không trội hoặc nhiều đỉnh, ưu tiên thử Otsu/đẳng liệu và kiểm tra ảnh nhị phân; không thể chứng minh ngưỡng đúng về ngữ nghĩa chỉ từ histogram.')]
    put('bank-'+id,'Đẳng liệu và đối xứng nền',3,'trung bình hai lớp|đối xứng nền',steps,'Giữ đúng số liệu trong ngân hàng đề. Bản đáp án gọi một bài khác là 4.8 và còn thay 250 thành 120; không dùng bảng tính đó cho dữ kiện này. Ngân hàng không nêu quy ước phân vị rời rạc: dùng mức cuối không vượt p% như cách làm đáp án; xem thêm quy ước đạt p% ở bài cô Uyên chương 5.')
    if id=='4-8-bs':
        steps.extend([backgroundstep(ha,p,False),isostep(hb,5,False),step('Đề xuất đổi phương pháp cho bài bổ sung.',text='Ảnh A có đỉnh trội tại 7 với đuôi trái dài, có thể thử đối xứng nền; ảnh B có nhiều đỉnh, nền không trội rõ nên ưu tiên đẳng liệu/Otsu hơn đối xứng nền. Hai phép tính đổi chéo ở trên minh họa lựa chọn này; vẫn phải kiểm tra ảnh phân vùng vì histogram không cho biết hình học đối tượng.')])
    else:
        steps.append(step('Chốt cách chọn cho đúng cặp histogram này.',text='Giữ đẳng liệu cho ảnh A vì có hai cụm mức xám; giữ đối xứng nền cho ảnh B vì có đỉnh nền trội ở phía sáng. Không cần hoán đổi chỉ vì hai phương pháp cho ngưỡng khác nhau.'))
put('bank-4-9','Mã hóa và giải mã LZW',6,'từ điển|chuỗi lặp',lzwsteps(M('1 0 0 0 1 1 0 0/1 1 1 0 0 1 1 1/1 1 0 0 1 1 0 1/0 1 1 1 1 0 0 0')))

# Cô Uyên — chương 3
A=M('3 9 9 3 3 2/3 2 8 7 8 2/3 8 3 7 0 4/1 4 1 9 4 7/0 1 7 7 6 4/3 9 4 2 0 4')
put('uyen-3-T1','Histogram và hai phép biến đổi',3,'histogram|bảo toàn số pixel',[histstep(hist(A,10)),transformed(hist(A,10),lambda g:abs(g-5),r'|g-5|'),transformed(hist(A,10),lambda g:abs(2*g-7),r'|2g-7|')])
H=[3,7,2,9,12,6,4,0,5,8]
put('uyen-3-T2','Làm trơn biểu đồ tần suất',3,'cửa sổ|đệm 0',[smoothstep(H,3),smoothstep(H,5),step('So sánh tác dụng của W.',text='W=5 làm trơn mạnh hơn W=3 nhưng dễ làm mất đỉnh/thung lũng thật. Đệm 0 khiến tổng các cột trong miền giữ lại có thể giảm ở hai đầu; không tự chuẩn hóa lại.')])
A=M('2 5 1 5 2 2/4 2 2 0 3 2/2 3 2 2 1 2/1 2 3 2 2 5/5 3 2 2 1 5/2 1 3 3 3 4')
put('uyen-3-T3','So sánh hai công thức cân bằng',3,'tích lũy|làm tròn',[equalstep(A,6),equalstep(A,6,True),step('Giải thích sự khác nhau.',text='Hai công thức rời rạc hóa khác nhau nên có thể cho ánh xạ khác. Cả hai gộp nguyên nhóm pixel cùng mức xám, vì vậy không bảo đảm histogram lý tưởng.')])
H=[190,261,305,138,70,36,16,8];N=sum(H);cum=[sum(H[:i+1]) for i in range(8)];mapping=[rnd(7*x/N) for x in cum];out=Counter()
for i,n in enumerate(H):out[mapping[i]]+=n
put('uyen-3-T4','Cân bằng ảnh 32×32',3,'xác suất|tích lũy',[step('Chuẩn hóa histogram rồi dùng tổng tích lũy.',r'p(r_k)=n_k/1024,\quad s_k=\operatorname{round}(7\sum_{j=0}^k p(r_j))',f'p(0)=190/1024={fmt(190/1024)}; s₀=round(7·190/1024)={mapping[0]}.',f'Histogram mới: {[out[i] for i in range(8)]}; các mức 4,5,6,7 cùng gộp về mức 7, còn 0→1, 1→3, 2→5, 3→6.',blocks=[table(['r','n','p','CDF','s'],[[i,H[i],H[i]/N,cum[i]/N,mapping[i]] for i in range(8)])])])
A=M('20 45 90/130 180 230/10 100 250')
steps=[]
for label,formula,func in [('+60',r's=\min(255,\max(0,r+60))',lambda x:min(255,x+60)),('−60',r's=\min(255,\max(0,r-60))',lambda x:max(0,x-60)),('Âm bản',r's=255-r',lambda x:255-x),('Log',r's=\frac{255}{\ln256}\ln(1+r)',lambda x:rnd(255/math.log(256)*math.log(1+x))),('Gamma = 2',r's=255(r/255)^2',lambda x:rnd(255*(x/255)**2)),('Gamma = 0,5',r's=255(r/255)^{0.5}',lambda x:rnd(255*(x/255)**.5)),('Kéo giãn',r's=\begin{cases}0&r<50\\255(r-50)/150&50\le r\le200\\255&r>200\end{cases}',lambda x:rnd(min(255,max(0,255*(x-50)/150))))]:
    steps.append(step('Áp dụng toán tử điểm: '+label+'.',formula,f'Tại r=20 ⇒ s={func(20)}; làm tròn nửa lên khi cần.',blocks=[matrix([[func(x) for x in row] for row in A],label)]))
steps.append(step('Nhận xét theo dạng hàm.',text='Cộng/trừ làm sáng/tối và có thể bão hòa; âm bản đảo sáng–tối; log và gamma<1 nâng mức tối; gamma>1 hạ mức trung gian; kéo giãn tăng tương phản trong [50,200] nhưng cắt mất chi tiết ngoài đoạn.'))
put('uyen-3-T5','Các toán tử điểm',3,'cắt miền|log|gamma',steps)
A=M('10 12 11 13 12/11 40 42 41 12/10 43 60 45 11/12 44 46 47 13/11 10 12 11 12');mean=[[1/9]*3 for _ in range(3)];weighted=[[1/16,2/16,1/16],[2/16,4/16,2/16],[1/16,2/16,1/16]]
replicate_corner=(4*A[0][0]+2*A[0][1]+2*A[1][0]+A[1][1])/9
put('uyen-3-T6','Lọc trung bình và lọc trọng số',3,'cửa sổ 3×3|đệm 0|lặp rìa',[
    step('Tính tổng có trọng số trong cửa sổ.',r'g(r,c)=\sum_{i=-1}^{1}\sum_{j=-1}^{1}h(i,j)I(r+i,c+j)',f'Tâm (2,2), đếm từ 0: trung bình=(40+42+41+43+60+45+44+46+47)/9={fmt(sum(sum(row[1:4]) for row in A[1:4])/9)}; trọng số=(40+2·42+41+2·43+4·60+2·45+44+2·46+47)/16={fmt(correlate(A,weighted)[2][2])}.',blocks=[matrix(correlate(A,mean,True),'Trung bình — 9 điểm trong'),matrix(correlate(A,weighted,True),'Trọng số — 9 điểm trong')]),
    step('So sánh cách xử lý góc.',r'g_0(0,0)=\frac{I_{00}+I_{01}+I_{10}+I_{11}}9,\quad g_{lặp}(0,0)=\frac{4I_{00}+2I_{01}+2I_{10}+I_{11}}9',f'Đệm 0: (10+12+11+40)/9={fmt(73/9)}; lặp rìa: (4·10+2·12+2·11+40)/9={fmt(replicate_corner)}.','Đệm 0 làm tối rìa; lặp rìa giảm tác động đó.')])
A=M('50 50 52 51 50/50 51 255 52 51/52 0 53 53 52/51 52 53 255 53/50 51 52 53 53');med=[[sorted(A[r+i][c+j] for i in range(-1,2) for j in range(-1,2))[4] for c in range(1,4)] for r in range(1,4)];avg=correlate(A,mean,True);truth=M('51 52 52/52 53 53/52 53 54');mae=lambda a:sum(abs(a[r][c]-truth[r][c]) for r in range(3) for c in range(3))/9
put('uyen-3-T7','Lọc nhiễu muối tiêu',3,'trung vị|xung|giữ biên',[step('Lấy phần tử giữa hoặc trung bình trên cùng cửa sổ.',r'g_{med}=\operatorname{median}(W),\quad g_{avg}=\frac19\sum_{q\in W}I(q)',f'Tại điểm trong đầu: trung vị={med[0][0]}, trung bình={fmt(avg[0][0])}; trung bình=(50+50+52+50+51+255+52+0+53)/9.', 'Đối chiếu ma trận gốc dưới đây: trung vị gần các mức xám gốc hơn trung bình trong bài này. Xung 0/255 kéo lệch tổng trung bình mạnh; trung vị dựa thứ tự nên ít bị cực trị kéo lệch.',blocks=[matrix(truth,'9 điểm trong của ảnh gốc để đối chiếu'),matrix(med,'Trung vị'),matrix(avg,'Trung bình')])])
A=M('5 5 5 4 8/4 15 4 5 8/3 6 1 6 7/4 6 6 5 2/6 2 8 7 7');rows=[];result=[]
for r in range(1,4):
    line=[]
    for c in range(1,4):
        x=A[r][c];neighbors=sorted([A[r+i][c+j] for i in range(-1,2) for j in range(-1,2)],key=lambda v:(abs(v-x),v))[:3];av=sum(neighbors)/3;y=av if abs(x-av)>2 else x
        rows.append([f'({r+1},{c+1})',x,str(neighbors),av,abs(x-av),y]);line.append(y)
    result.append(line)
put('uyen-3-T8','Trung bình k=3 gần nhất, θ=2',3,'k gần nhất|giữ tâm|ngưỡng',[step('Chọn k giá trị gần tâm, rồi chỉ thay khi chênh lệch vượt θ.',r'AV_k=\frac1k\sum_{q\in K}I(q),\quad g(p)=\begin{cases}I(p)&|I(p)-AV_k|\le\theta\\AV_k&|I(p)-AV_k|>\theta\end{cases}',f'Tâm 15: chọn {rows[0][2]}, AV₃={fmt(rows[0][3])}; |15−AV₃|={fmt(rows[0][4])}>2 nên thay.', 'Kể cả tâm trong k giá trị; hòa khoảng cách chọn giá trị nhỏ trước. Các cửa sổ tính từ ảnh gốc, không cập nhật dây chuyền.',blocks=[table(['vị trí (từ 1)','tâm','3 giá trị','AV₃','độ lệch','kết quả'],rows),matrix(result,'9 điểm trong')])])
values=[24,26,25,200,27,26,25,3,24];ordered=sorted(values);results=[sum(values)/9,math.prod(values)**(1/9),ordered[4],max(values),min(values),(max(values)+min(values))/2,sum(ordered[1:-1])/7]
put('uyen-3-T9','So sánh bảy bộ lọc',3,'muối tiêu|trung vị|alpha-trimmed',[step('Tính mỗi bộ lọc trên đúng 9 mẫu.',r'\begin{gathered}\bar x=\frac{\sum x_i}9,\quad G=(\prod x_i)^{1/9},\quad M=\operatorname{median}(x_i)\\ A_{d=2}=\frac{\sum_{i=2}^{8}x_{(i)}}7,\quad P=\frac{\max(x_i)+\min(x_i)}2\end{gathered}',f'Dãy tăng: {ordered}; alpha-trimmed bỏ 3 và 200, lấy trung bình 7 số còn lại. Điểm giữa P=(200+3)/2=101,5.', 'Có xung sáng 200 và tối 3, dạng muối tiêu. Trung vị/alpha-trimmed loại ảnh hưởng cực trị tốt; trung bình số học/hình học còn chịu xung, max/min chỉ hợp một phía; điểm giữa chịu cả hai cực trị.',blocks=[table(['bộ lọc','kết quả'],list(zip(['số học','hình học','trung vị','max','min','điểm giữa','alpha-trimmed d=2'],results)))])])
A=M('6 4 0 3 1 7/4 1 2 0 6 2/1 2 1 6 0 1/1 1 2 6 1 7/3 4 2 7 7 5')
put('uyen-3-T10','Tìm ngưỡng tự động và tách ảnh',3,'trung bình lớp|cực đại',[otsustep(hist(A,8),A)],'Công thức f(g) trong PDF bị dàn trang dễ đọc nhầm. Dùng công thức giáo trình trang PDF 32: t/(N−t) nhân bình phương chênh trung bình, không chia cho bình phương đó.')
HA=[30,55,40,12,6,10,35,50,28,10];HB=[8,12,20,35,80,160,90,40,15,5]
put('uyen-3-T11','Đẳng điệu và đối xứng nền 92%',3,'trung bình hai lớp|phân vị',[isostep(HA,5),backgroundstep(HB,92,False),backgroundstep(HA,92,False),isostep(HB,5),step('So sánh việc chọn phương pháp.',text='A có hai cụm mức xám tách nhau, thích hợp đẳng điệu; B có nền trội gần đỉnh 5 nên có thể thử đối xứng nền. Khi hoán đổi, thuật toán vẫn ra số nhưng không bảo đảm ngưỡng phân vùng đúng: A thiếu nền trội, B không có hai lớp cân đối rõ.')],'Chương 3 quy định phân vị cuối không vượt p%; khác quy ước đầu tiên đạt p% của chương 5. Kết quả được tính theo từng đề, không trộn quy ước.')
put('uyen-3-T12','Tìm ngưỡng tam giác',3,'đỉnh|đuôi dài|khoảng cách',[trianglestep([3,4,6,18,70,160,120,60,34,20,11,6,3,2])])

# Cô Uyên — chương 4
rgb=[[200,100,50],[0,255,128],[255,255,0],[34,139,34]];rows=[]
for label,row in zip('abcd',rgb):
    cmy=[1-x/255 for x in row];maxi=max(cmy);inks='/'.join(k for k,v in zip(['C','M','Y'],cmy) if abs(v-maxi)<1e-8)
    rows.append([label,*cmy,inks])
put('uyen-4-T1','Đổi RGB sang CMY',4,'chuẩn hóa|phần bù',[step('Chuẩn hóa RGB 8 bit rồi lấy phần bù.',r'R_n=R/255,\ G_n=G/255,\ B_n=B/255;\quad(C,M,Y)=(1-R_n,1-G_n,1-B_n)',f'Màu a: C=1−200/255={fmt(55/255)}, M=1−100/255={fmt(155/255)}, Y=1−50/255={fmt(205/255)}.',blocks=[table(['màu','C','M','Y','mực cần nhiều nhất'],rows)])])
for id,s,theta in [('T2','20 200 90 140 60/250 35 180 70 120/15 100 230 45 160',127),('T3','8 64 190 12 99 205/143 27 5 251 33 76/220 101 60 134 18 240',127),('T4','130 125 128 40 200/90 90 90 90 90/210 15 177 63 142',100)]:
    put('uyen-4-'+id,'Khuếch tán lỗi một chiều',4,'truyền sai số|hai mức',[diffusionstep(M(s),theta)],'Câu 4.T3 phần b nói dòng 2 toàn 90 nhưng ma trận cho dòng 2 là 143,27,5,251,33,76. Giữ đúng ma trận; dòng toàn 90 nằm ở 4.T4. Không thay dữ kiện để khớp câu nhận xét.' if id=='T3' else '')

# Cô Uyên — chương 5
A=M('4 4 4 4 4 4 4/4 4 4 4 4 4 4/4 4 18 18 18 4 4/4 4 17 14 19 4 4/4 4 18 18 18 4 4/4 4 4 4 4 4 4/4 4 4 4 4 4 4')
put('uyen-5-T1','Prewitt và Laplace 8 láng giềng',5,'đặt tâm|cộng có dấu|Laplace',edge_steps(A,PREWITT,transpose(PREWITT),LAP8,True))
A=M('3 3 3 3 3 3 3/3 3 3 12 13 12 3/3 3 3 13 11 12 3/3 3 3 12 12 13 3/3 3 3 3 3 3 3/3 3 3 3 3 3 3/3 3 3 3 3 3 3')
put('uyen-5-T2','Sobel và Laplace 4 láng giềng',5,'gradient|Laplace',edge_steps(A,SOBEL,transpose(SOBEL),LAP4))
A=M('40 60 60 60 60 60/20 40 60 60 60 60/20 20 40 60 60 60/20 20 20 40 60 60/20 20 20 20 40 60/20 20 20 20 20 40');B=[row[:] for row in A];B[2][3]=90;B[4][3]=5
put('uyen-5-T3','Ảnh hưởng nhiễu lên đạo hàm',5,'gradient|khuếch đại nhiễu',edge_steps(A,PREWITT,transpose(PREWITT),name='S₁')+edge_steps(B,PREWITT,transpose(PREWITT),name='S₂')+[step('Đối chiếu hai đáp ứng.',text='Nhiễu tại (3,4) và (5,4) làm thay đổi các cửa sổ 3×3 phủ chúng, sinh đáp ứng mạnh hoặc triệt tiêu đáp ứng biên thật. Lọc nhiễu/làm trơn trước rồi mới tính đạo hàm; ngưỡng đơn lẻ không khắc phục được mọi ảnh hưởng.')])
A=M('3 7 3 2 5 2 3 7/1 1 2 4 8 4 1 9/9 2 7 2 7 2 2 5/0 8 7 8 1 0 2 6/8 4 5 1 1 1 6 4/7 8 2 2 7 1 1 2')
put('uyen-5-T4','Otsu và trường hợp nhiều ngưỡng',5,'phương sai giữa lớp|tập nghiệm',[otsustep(hist(A,10),A),otsustep([7,2,2,1,11,11,1,2,2,7])])
HA=[6,15,19,9,4,3,8,21,12,3];HB=[4,9,5,3,2,4,48,17,6,2]
put('uyen-5-T5','Đổi chéo hai phương pháp tìm ngưỡng',5,'đẳng điệu|đối xứng nền',[isostep(HA,2),backgroundstep(HB,95),backgroundstep(HA,90),isostep(HB,6),step('Đối chiếu giả thiết với histogram.',text='A có hai cụm nên đẳng điệu hợp lý hơn; B có đỉnh nền lớn tại 6 nên đối xứng nền có cơ sở hơn. Khi đổi chéo vẫn tính ra ngưỡng nhưng với A, đỉnh cao phía phải không áp đảo rõ và phân vị có thể làm ngưỡng lệch; không lấy việc thuật toán hội tụ làm chứng minh phân vùng đúng.')])
A=M('3 4 1 8 3 3/8 6 1 8 1 2/4 8 3 1 8 5/3 9 6 8 2 6/2 0 3 1 0 7/3 9 1 8 8 9');H=hist(A,10)
def peaks(h):
    # Strict interior local maxima; plateaus counted once if higher on both sides.
    out=[];i=1
    while i<len(h)-1:
        j=i
        while j+1<len(h) and abs(h[j+1]-h[i])<1e-9:j+=1
        if j<len(h)-1 and h[i]>h[i-1] and h[j]>h[j+1]:out.append(f'{i}' if i==j else f'{i}–{j}')
        i=j+1
    return out
put('uyen-5-T6','Làm trơn và đếm cực đại',5,'trung bình trượt|đỉnh cục bộ',[histstep(H),smoothstep(H,3),smoothstep(H,5),step('Đếm đỉnh theo cùng một quy ước.',text=f'Chỉ đếm cực đại trong miền trong, plateau cao hơn cả hai phía tính một đỉnh. Trước: {peaks(H)} ({len(peaks(H))} đỉnh); W=3: {peaks(smooth(H,3))} ({len(peaks(smooth(H,3)))} đỉnh); W=5: {peaks(smooth(H,5))} ({len(peaks(smooth(H,5)))} đỉnh). So sánh trước khi làm tròn để tránh tạo plateau giả. Làm trơn giảm dao động nhưng không bảo đảm số đỉnh giảm đơn điệu với mọi W.')])
put('uyen-5-T7','Ngưỡng tam giác từ đỉnh g=2',5,'khoảng cách vuông góc|đuôi',[trianglestep([3,10,52,24,9,5,3,2,1,1],2,9)])

# Cô Uyên — chương 6
HU1=M('0 0 1 1 0 0 1 1 1 0 0 0 0 0 0 1 0 0 1 1/0 0 1 1 0 0 1 1 0 1 0 0 0 0 0 1 0 0 0 0/0 0 0 0 0 1 0 0 1 1 0 1 0 0 1 0 1 1 1 1/0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 1 1 1 1/0 1 1 0 0 1 1 1 0 0 0 1 1 1 0 0 1 1 1 1/0 1 0 1 0 1 1 1 1 1 0 1 1 1 0 0 1 1 1 1')
HU2=M('1 0 1 1 1 1 1 1 0 1 1 0 0 1 0 1/0 1 1 1 1 1 1 1 0 1 1 0 0 1 0 1/1 1 0 1 0 0 0 0 1 1 1 1 1 0 1 0/1 1 0 1 0 0 0 0 1 1 0 0 1 0 0 1/1 0 1 1 1 0 0 0 1 1 1 0 0 0 1 0/1 0 0 0 1 0 0 0 1 1 0 1 0 0 1 0')
put('uyen-6-T1','Huffman: mã, tỷ lệ nén và entropy',6,'tần suất khối|entropy|hiệu suất',huffmansteps(HU1))
put('uyen-6-T2','Huffman và mã cố định',6,'hòa tần suất|độ dài tối ưu',huffmansteps(HU2),'Đề nhắc ký hiệu C, D nhưng chưa gán chữ cho mẫu khối. Lời giải dùng chuỗi 4 bit nhận diện khối để tránh gán nhầm; hòa tần suất đổi mã nhưng không đổi tổng số bit tối ưu.')
DECODE_MAP={'0':'A','10':'B','110':'C','1110':'D','1111':'E'};BLOCKS={'A':M('1 1/1 1'),'B':M('0 0/0 0'),'C':M('1 0/1 0'),'D':M('0 1/1 0'),'E':M('1 1/0 0')}
def decode_prefix(bits):
    out=[];word=''
    for b in bits:
        word+=b
        if word in DECODE_MAP:out.append(DECODE_MAP[word]);word=''
    return out,word
bits='0100110001011111101001110';syms,rest=decode_prefix(bits);bad=bits[:4]+('1' if bits[4]=='0' else '0')+bits[5:];badsyms,badrest=decode_prefix(bad)
reconstructed=[]
if len(syms)==12:
    for r in range(2):
        for rr in range(2):reconstructed.append([v for s in syms[r*6:(r+1)*6] for v in BLOCKS[s][rr]])
put('uyen-6-T3','Giải mã Huffman và ảnh hưởng lỗi bit',6,'mã tiền tố|mất đồng bộ',[
    step('Đọc bit đến khi khớp trọn một từ mã.',r'\text{Từ mã hợp lệ}\Rightarrow\text{xuất ký hiệu và quay về gốc cây}',f'Chuỗi gốc: {bits}; các ký hiệu: '+', '.join(syms)+f'; phần bit dư: {rest or "không"}.',
         'Bảng mã là tiền tố vì mỗi từ kết thúc ở một lá riêng, không từ nào mở đầu từ khác.',blocks=[matrix(reconstructed,'Ảnh I khôi phục')]),
    step('Tính tỷ lệ nén từ kích thước ảnh đã giải.',r'n_1=4\cdot12,\quad n_2=\text{số bit nhận},\quad C_R=n_1/n_2',f'n₁=48, n₂={len(bits)}, CR=48/{len(bits)}={fmt(48/len(bits))}.','Không tính bảng mã.'),
    step('Đảo bit thứ 5 rồi giải lại theo cùng cây.',text=f'Chuỗi lỗi: {bad}; giải được: '+', '.join(badsyms)+f'. Phần dư: {badrest or "không"}. Số khối từ {len(syms)} thành {len(badsyms)}: một bit sai có thể đổi ranh giới nhiều từ mã và mất đồng bộ. Không tự thêm/bớt bit để ép đủ kích thước.')])
put('uyen-6-T4','LZW khối 1×2, từ mã 4 bit',6,'từ điển|tỷ lệ nén',lzwsteps(M('0 0 1 0 1 0 1 0/1 1 1 1 0 1 1 0/1 1 0 1 1 0 1 1/1 0 1 0 1 1 0 1'),2,4))
put('uyen-6-T5','LZW ảnh xám, từ mã 9 bit',6,'từ điển gốc 256|chuỗi lặp',lzwsteps(M('25 25 25 25/80 80 25 25/80 80 25 25/25 25 80 80'),bits=9,gray=True))
put('uyen-6-T6','LZW khối 1×3 và mã chưa có',6,'mã kế tiếp|w + first(w)',lzwsteps(M('0 0 1 0 0 1 0 0 1/1 0 1 1 0 1 1 0 1/0 1 0 0 0 0 0 1 1/1 0 1 1 0 1 0 1 0'),3,4))
binary_string='00000000010001100000000000001000001100100000000000';runs=[];zeros=0
for b in binary_string:
    if b=='0':zeros+=1
    else:runs.append(zeros);zeros=0
runs.append(zeros);assert max(runs)<16
rlcbits=' '.join(format(x,'04b') for x in runs)
received=['0110','0000','1100','0011','0001','1001'];decoded=''.join('0'*int(b,2)+('1' if i<len(received)-1 else '') for i,b in enumerate(received))
chars='KKKKKKKKKKKUEEEEEEEEEEEEEEEEEENNNNNNNDDDD'
from itertools import groupby
char_runs=[(x,len(list(group))) for x,group in groupby(chars)];encoded=''.join(f'{x}{n:02}' for x,n in char_runs)
short='1011001010110100';short_runs=[(x,len(list(g))) for x,g in groupby(short)];short_bits=' '.join(x+format(n,'03b') for x,n in short_runs)
put('uyen-6-T7','Ba quy ước RLC',6,'độ dài chạy|quy ước|nở dữ liệu',[
    step('Đếm các dãy 0 trước mỗi 1, và dãy 0 tận cùng.',r'n_2=4N_{run},\quad C_R=\frac{n_1}{n_2}',f'Dãy đếm: {runs}; mã: {rlcbits}.',f'n₁={len(binary_string)}, n₂={4*len(runs)}, CR={fmt(len(binary_string)/(4*len(runs)))}. Giải mã 0110 0000 1100 0011 0001 1001 ⇒ {decoded}. Nhóm cuối chỉ là số 0 đuôi, không thêm bit 1 cuối.'),
    step('Mã hóa ký tự và số lần lặp bằng hai chữ số.',r'C_R=\frac{\text{số ký tự gốc}}{\text{số ký tự sau mã}}',f'Các dãy: {char_runs}; chuỗi mã {encoded}.',f'CR={len(chars)}/{len(encoded)}={fmt(len(chars)/len(encoded))}; U01 làm 1 ký tự thành 3. ABABABAB → A01B01A01B01A01B01A01B01: 8 thành 24, CR=1/3.'),
    step('Mỗi cặp giá trị–độ dài chạy dùng 4 bit.',r'n_2=4N_{cặp},\quad C_R=16/n_2',f'Các cặp {short_runs}; mã {short_bits}.',f'n₂={4*len(short_runs)}; CR={fmt(16/(4*len(short_runs)))}<1 nên nở vì các dãy quá ngắn.')])
A=[([30]*4+[110]*4) for _ in range(8)];T=dct(A)
put('uyen-6-T8','DCT khối hai vùng sáng',6,'DC|tần số thấp|năng lượng',[
    step('Tính DCT trực giao 8×8; đề chưa dịch mức nên dùng trực tiếp P.',r'T(u,v)=\frac14C(u)C(v)\sum_{x=0}^7\sum_{y=0}^7P(x,y)\cos\frac{(2x+1)u\pi}{16}\cos\frac{(2y+1)v\pi}{16},\quad C(0)=1/\sqrt2,\ C(k>0)=1',
         f'T(0,0)=(1/8)·[32·30+32·110]={fmt(T[0][0])}. Với u=0: T(0,v)=√2·Σ_y P(0,y)cos((2y+1)vπ/16), v>0.',
         f'T(0,1)={fmt(T[0][1])}; T(0,2)={fmt(T[0][2])}; T(0,3)={fmt(T[0][3])}. Các hàng P giống nhau nên tổng cos theo x bằng 0 với u≥1. Với v chẵn≠0, hai nửa bù nhau làm tổng bằng 0.'),
    step('Chỉ giữ hệ số DC rồi biến đổi ngược.',r'\hat P(x,y)=T(0,0)/8,\quad e_{rms}=\sqrt{\frac1{64}\sum(P-\hat P)^2}',f'P̂=560/8=70; e_rms=√((32·(30−70)²+32·(110−70)²)/64)=40.', 'DC giữ độ sáng trung bình; bỏ AC làm mất ranh giới hai nửa. Nếu có bước dịch −128 thì DC là −464 và cộng lại 128 khi khôi phục, kết quả ảnh vẫn là 70.')])
JT=M('425 51 33 -42 -25 14 -17 -6/85 -58 37 11 12 14 14 -7/38 29 -12 11 -14 10 10 9/29 16 -25 -12 -18 -15 13 5/15 16 7 17 -16 -7 -12 -6/-16 -15 17 13 -11 -8 -12 9/-15 14 -10 7 9 -10 -10 9/7 15 -14 -8 -8 -11 -10 -9')
JQ=M('16 11 10 16 24 40 51 61/12 12 14 19 26 58 60 55/14 13 16 24 40 57 69 56/14 17 22 29 51 87 80 62/18 22 37 56 68 109 103 77/24 35 55 64 81 104 113 92/49 64 78 87 103 121 120 101/72 92 95 98 112 100 103 99')
JOUT=[[rnd(x/q) for x,q in zip(rt,rq)] for rt,rq in zip(JT,JQ)];ZZ=zigzag(JOUT);JERR=sum((JT[i][j]-JOUT[i][j]*JQ[i][j])**2 for i in range(8) for j in range(8))
put('uyen-6-T9','Lượng tử hóa, zig-zag và RLE JPEG',6,'lượng tử hóa|zig-zag|sai số',[
    step('Chia từng hệ số cho bước lượng tử và làm tròn gần nhất.',r'T^{\prime}(u,v)=\operatorname{round}(T(u,v)/Q(u,v))',f'T′(0,0)=round(425/16)={JOUT[0][0]}; T′(0,1)=round(51/11)={JOUT[0][1]}.',f'Có {sum(x!=0 for row in JOUT for x in row)} hệ số khác 0.',blocks=[matrix(JOUT,'Ma trận sau lượng tử hóa')]),
    step('Quét đường chéo zig-zag rồi đếm 0 trước mỗi AC khác 0.',r'\mathrm{RLE}_{AC}=(\mathrm{skip},\mathrm{value})',f'Vector zig-zag: {ZZ}.',f'Các cặp AC: {acpairs(ZZ[1:])}. (0,0) là EOB cho phần đuôi toàn 0; (15,0) nếu xuất hiện là ZRL cho 16 số 0.'),
    step('Giải lượng tử hóa và dùng bảo toàn năng lượng DCT để tính sai số.',r'T^{\prime\prime}=T^{\prime}\odot Q,\quad SSE=\sum(T-T^{\prime\prime})^2,\quad e_{rms}=\sqrt{SSE/64}',f'DC: {JOUT[0][0]}·16={JOUT[0][0]*16} so với 425; (0,1): {JOUT[0][1]}·11={JOUT[0][1]*11} so với 51. SSE={JERR}.',f'e_rms={fmt(math.sqrt(JERR/64))}, bỏ qua làm tròn pixel theo đề.')])
DC=[58,61,67,64,72,72,69,53];diff=[DC[0]]+[DC[i]-DC[i-1] for i in range(1,len(DC))];dcrows=[[x,category(x),DC_CODES[category(x)],amplitude(x),len(DC_CODES[category(x)])+category(x)] for x in diff];decdiff=[40,-3,5,0,-12,6,-1,2];decdc=[sum(decdiff[:i+1]) for i in range(len(decdiff))];AC=[0,0,-2,0,0,0,0,1,3,0,0,0,0,0,0,-1,0,2]+[0]*45
put('uyen-6-T10','DPCM hệ số DC và RLE hệ số AC',6,'hiệu DC|category|EOB',[
    step('Lấy hiệu DC với khối liền trước; khối đầu dùng DC trước bằng 0.',r'd_i=DC_i-DC_{i-1},\quad CAT=\lfloor\log_2|d_i|\rfloor+1\ (d_i\ne0)',f'Dãy DPCM: {diff}; d₁=58−0=58, CAT=6.',f'Tổng số bit DC={sum(row[-1] for row in dcrows)}.',blocks=[table(['DPCM','CAT','Huffman CAT','bit biên độ','tổng bit'],dcrows)]),
    step('Cộng dồn DPCM để khôi phục DC.',r'DC_i=DC_{i-1}+d_i',f'DC đầu=0+40=40; DC tiếp=40−3=37.',f'Dãy DC giải mã: {decdc}. DPCM hiệu quả vì DC các khối kề thường gần nhau nên hiệu cần CAT nhỏ hơn giá trị DC tuyệt đối.'),
    step('Đếm số 0 trước hệ số AC, EOB kết thúc đuôi 0.',r'\mathrm{pair}=(\mathrm{skip},\mathrm{value})',f'Vector đề cho ⇒ {acpairs(AC)}.', 'Giải dãy (0,5),(1,−3),(3,2),(0,−1),(0,0): AC khác 0 ở chỉ số vector 1×64 là 1:5, 3:−3, 7:2, 8:−1; tất cả vị trí AC còn lại bằng 0. Chỉ số 0 dành cho DC, không phải AC.')])
A=M('11 5/15 13');Q=M('2 10/3 2');D=dct(A);D=[[round(x,10) for x in row] for row in D];quant=[[rnd(D[i][j]/Q[i][j]) for j in range(2)] for i in range(2)];zz=zigzag(quant);delta=zz[0]-13;dcbit=DC_CODES[category(delta)]+amplitude(delta);pairs=acpairs(zz[1:]);AC_TABLE={(0,1):'00',(0,2):'01',(0,3):'100',(0,4):'1011',(0,5):'11010',(1,1):'1100',(1,2):'11011',(1,3):'1111001',(1,4):'111110110'};acbit='';acrows=[]
for run,value in pairs:
    word='1010' if (run,value)==(0,0) else AC_TABLE[(run,category(value))]+amplitude(value)
    acbit+=word;acrows.append([run,value,category(value),word])
dequant=[[quant[i][j]*Q[i][j] for j in range(2)] for i in range(2)]
restored=[[sum((1/math.sqrt(2) if u==0 else ((1 if x==0 else -1)/math.sqrt(2)))*(1/math.sqrt(2) if v==0 else ((1 if y==0 else -1)/math.sqrt(2)))*dequant[u][v] for u in range(2) for v in range(2)) for y in range(2)] for x in range(2)];rms=math.sqrt(sum((A[i][j]-restored[i][j])**2 for i in range(2) for j in range(2))/4)
put('uyen-6-T11','Một vòng JPEG 2×2',6,'DCT|lượng tử hóa|bit biên độ',[
    step('Biến đổi DCT theo ma trận đề cho, bỏ dịch mức.',r'I_{DCT}=TIT^T,\quad T=\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}', 'I_DCT(0,0)=(11+5+15+13)/2=22.',blocks=[matrix(D,'I_DCT')]),
    step('Lượng tử hóa từng hệ số rồi quét zig-zag.',r'I_Q=\operatorname{round}(I_{DCT}/Q)',f'I_Q(0,0)=round(22/2)=11; I_Q(0,1)=round(4/10)=0.',f'Zig-zag (00,01,10,11): {zz}. Làm tròn nửa ra xa 0.',blocks=[matrix(quant,'I_Q')]),
    step('Mã DC bằng hiệu, category và biên độ.',r'd=DC-DC_{trước},\quad\mathrm{bits}_{DC}=\mathrm{Huff}(CAT)+\mathrm{amplitude}(d)',f'd={zz[0]}−13={delta}; CAT={category(delta)}; Huff={DC_CODES[category(delta)]}; biên độ={amplitude(delta)}.',f'Bit DC: {dcbit}. Số âm dùng phần bù các bit của độ lớn trong CAT bit, không phải biểu diễn bù hai.'),
    step('Mã hóa AC theo RUN/CAT và ghép toàn bộ khối.',r'\mathrm{bits}_{AC}=\mathrm{Huff}(RUN/CAT)+\mathrm{amplitude}(value)',f'Các cặp: {pairs}; bit AC={acbit}.',f'Chuỗi toàn khối: {dcbit+acbit} ({len(dcbit+acbit)} bit). '+('Có EOB vì đuôi còn hệ số 0.' if pairs[-1]==(0,0) else 'Không gửi EOB vì hệ số AC cuối khác 0, đã đủ 3 AC.'),blocks=[table(['RUN','value','CAT','bit gửi'],acrows)]),
    step('Giải lượng tử, DCT ngược và đo sai số.',r'I^{\prime}=T^T(I_Q\odot Q)T,\quad e_{rms}=\sqrt{\frac14\sum(I-I^{\prime})^2}',f'I_Q⊙Q={dequant}; e_rms={fmt(rms)}.',blocks=[matrix(dequant,'DCT sau giải lượng tử'),matrix(restored,'Ảnh I′ sau giải nén'),matrix(A,'Ảnh gốc I để đối chiếu')])])
F=M('52 85 128 160/97 78 107 86/61 175 115 80/42 135 127 99');FH=M('54 82 128 161/96 82 105 86/64 175 111 82/42 134 128 94');err=sum((F[i][j]-FH[i][j])**2 for i in range(4) for j in range(4));energy=sum(x*x for row in FH for x in row)
put('uyen-6-T12','Đánh giá RMS và SNR sau nén',6,'sai số căn quân phương|SNR|cảm nhận',[
    step('Lấy bình phương sai số rồi trung bình trên 16 pixel.',r'e_{rms}=\sqrt{\frac{\sum(\hat f-f)^2}{16}}',f'SSE={err}; e_rms=√({err}/16)={fmt(math.sqrt(err/16))}.'),
    step('Tính SNR theo công thức slide: năng lượng ảnh khôi phục ở tử.',r'SNR_{ms}=\frac{\sum\hat f^2}{\sum(\hat f-f)^2},\quad SNR_{dB}=10\log_{10}(SNR_{ms})',f'Σf̂²={energy}; SNRms={energy}/{err}={fmt(energy/err)}.',f'SNR={fmt(10*math.log10(energy/err))} dB. Nếu dùng năng lượng ảnh gốc ở tử số sẽ ra {fmt(sum(x*x for row in F for x in row)/err)}; đó là quy ước khác, không trộn với slide.'),
    step('Đánh giá tỷ lệ nén đi cùng mục đích sử dụng.',text='CR=12 không luôn tốt hơn CR=6: cần so cả chất lượng, chi tiết quan trọng, sai dạng và yêu cầu lưu trữ/truyền. RMS/SNR không phản ánh hoàn toàn cảm nhận nên cần đánh giá chủ quan.')])

# Cô Uyên — chương 7
XA=M('1 1 0 0 0 0 1 1/1 1 1 0 0 1 1 1/0 1 1 1 0 1 1 0/0 0 1 1 1 1 0 0/0 0 1 1 1 1 1 0/1 0 0 1 1 1 1 0/1 1 0 0 0 1 1 1/1 1 1 0 0 0 1 1')
put('uyen-7-T1','Co và giãn với chữ thập',7,'fit|hit',[morphstep(XA,CROSS)])
XA=M('0 0 1 1 0 0 1 0/0 1 1 1 0 1 1 0/1 1 0 1 1 1 0 0/1 1 1 1 0 1 1 1/0 1 1 0 1 1 1 1/0 0 1 1 1 0 1 0/1 0 1 1 1 1 1 0/1 0 0 1 0 0 1 1')
put('uyen-7-T2','SE bất đối xứng: hit và giãn chuẩn',7,'phản xạ SE|gốc ở tâm',[morphstep(XA,M('0 0 1/1 1 0/0 0 1'),True)])
XA=M('0 0 0 0 0 0 0 0/0 1 1 1 1 0 0 0/0 1 1 1 1 1 0 0/0 1 1 1 1 1 1 0/0 0 1 1 1 1 1 0/0 0 0 1 1 1 1 0/0 1 0 0 1 1 0 0/0 0 0 0 0 0 0 0')
put('uyen-7-T3','So sánh SE chữ thập và vuông',7,'tập con|điều kiện fit',[morphstep(XA,CROSS),step('Co bằng SE vuông có nhiều điều kiện hơn.',r'B_1\subseteq B_2\Rightarrow A\ominus B_2\subseteq A\ominus B_1',f'Co chữ thập có {count(morph(XA,CROSS))} điểm 1, co vuông có {count(morph(XA,SQUARE))}.','Nếu toàn bộ B₂ fit thì tập con B₁ cũng fit; chiều ngược không bảo đảm.',blocks=[matrix(morph(XA,SQUARE),'X ⊖ B₂ (vuông)')])])
def openclose(a,b):
    e=morph(a,b);d=morph(a,b,'dilate');op=morph(e,b,'dilate');cl=morph(d,b)
    return e,d,op,cl
XA=M('0 0 0 0 0 0 0 0 0 0 0/0 1 1 1 0 0 0 1 1 1 0/0 1 1 1 1 1 1 1 1 1 0/0 1 1 1 0 0 0 1 1 1 0/0 0 0 0 0 0 0 1 1 1 0/0 1 0 0 0 0 0 1 1 0 0/0 0 0 0 0 0 0 0 0 0 0');e,d,op,cl=openclose(XA,SQUARE)
put('uyen-7-T4','Mở ảnh: bỏ cầu hẹp và nhiễu',7,'co rồi giãn|cầu hẹp',[step('Co bằng SE vuông rồi giãn kết quả co.',r'A\circ B=(A\ominus B)\oplus B',f'Số điểm 1: A={count(XA)}, co={count(e)}, mở={count(op)}.','Điểm nhiễu đơn lẻ và dải nối một pixel bị loại vì không chứa được SE 3×3; một số mép nhô nhỏ cũng mất.',blocks=[matrix(e,'A ⊖ B'),matrix(op,'A ∘ B')])])
XA=M('0 0 0 0 0 0 0 0 0 0 0/0 1 1 1 1 0 1 1 1 0 0/0 1 0 1 1 0 1 1 1 0 0/0 1 1 1 1 0 1 1 1 1 0/0 1 1 1 1 0 1 1 1 1 0/0 0 0 0 0 0 0 0 0 0 0');e,d,op,cl=openclose(XA,CROSS)
put('uyen-7-T5','Đóng ảnh: lấp lỗ và khe',7,'giãn rồi co|hình SE',[step('Giãn trước, sau đó co bằng cùng SE chữ thập.',r'A\bullet B=(A\oplus B)\ominus B',f'Số điểm 1: A={count(XA)}, giãn={count(d)}, đóng={count(cl)}.',f'Lỗ (3,3) sau đóng={cl[2][2]}; cột 6 sau đóng={[row[5] for row in cl]}. Khe chỉ lấp tại vị trí có đủ láng giềng chữ thập sau giãn; không phải mọi khoảng trống 1 pixel đều tự được lấp.',blocks=[matrix(d,'A ⊕ B'),matrix(cl,'A • B')])])
XA=M('0 0 0 0 0 0 0 0/0 1 1 1 0 0 1 0/0 1 1 1 1 1 1 0/0 1 1 0 1 1 1 0/0 1 1 1 1 1 1 0/0 0 0 0 1 1 1 0/0 0 0 0 0 0 0 0');e,d,op,cl=openclose(XA,SQUARE);op2=openclose(op,SQUARE)[2];cl2=openclose(cl,SQUARE)[3]
assert op2==op and cl2==cl
put('uyen-7-T6','Mở/đóng, bao hàm và lũy đẳng',7,'bao hàm|lũy đẳng|fit',[step('Tính hai phép ghép và lặp lại trên kết quả.',r'O=(A\ominus B)\oplus B,\quad C=(A\oplus B)\ominus B',f'Số điểm 1: A={count(XA)}, O={count(op)}, C={count(cl)}; O lần 2={count(op2)}, C lần 2={count(cl2)}.', 'Kiểm tra từng pixel cho O⊆A⊆C; O∘B=O và C•B=C (lũy đẳng). Phần bên trái có bề rộng 3 nhưng lỗ ở (4,4) và chiều cao/biên làm không có cửa sổ vuông 3×3 fit đầy đủ, nên mở xóa phần đó.',blocks=[matrix(e,'Ảnh co trung gian'),matrix(op,'Mở (lần 1 = lần 2)'),matrix(cl,'Đóng (lần 1 = lần 2)')])])
XA=M('1 1 1 1 0 0 1 1 1 1/1 1 1 1 0 0 1 1 1 1/1 1 1 1 1 1 1 1 1 1/1 1 1 1 1 1 1 1 1 0/1 1 1 1 1 1 1 1 1 0/0 1 1 1 1 1 1 1 0 0');e=morph(XA,SQUARE);boundary=binary(XA,e,lambda x,y:x and not y)
put('uyen-7-T7','Tách biên bằng ảnh co và phần bù',7,'biên trong|phần bù',[step('Co ảnh rồi lấy phần đối tượng bị loại.',r'E=A\ominus s,\quad\beta(A)=A\cap E^c',f'A có {count(XA)} điểm, E có {count(e)} điểm ⇒ biên có {count(XA)}−{count(e)}={count(boundary)} điểm.', 'Eᶜ chỉ tính trong khung ảnh 6×10; ngoài ảnh đệm 0 khi co.',blocks=[matrix(e,'E'),matrix(complement(e),'Eᶜ'),matrix(boundary,'β(A)')])])
XA=M('0 0 0 0 0 0 0/0 1 1 1 1 0 0/0 1 1 1 1 1 0/0 1 1 1 1 1 0/0 0 1 1 1 1 0/0 0 0 0 0 0 0');b1=binary(XA,morph(XA,SQUARE),lambda x,y:x and not y);b2=binary(XA,morph(XA,CROSS),lambda x,y:x and not y);changes=[f'({r+1},{c+1})' for r in range(len(XA)) for c in range(len(XA[0])) if b1[r][c]!=b2[r][c]]
put('uyen-7-T8','Biên theo SE vuông và chữ thập',7,'biên trong|liên thông',[step('Tách biên lần lượt với từng SE.',r'\beta_i=A\setminus(A\ominus B_i)',f'Số điểm biên vuông={count(b1)}, chữ thập={count(b2)}.', 'Khác tại '+', '.join(changes)+'. Kiểm tra lân cận trên ma trận: biên vuông liên thông 4 (nên cũng liên thông 8); biên chữ thập chỉ liên thông 8, không liên thông 4. Không gọi hai khái niệm là loại trừ nhau.',blocks=[matrix(b1,'β₁ — SE vuông'),matrix(b2,'β₂ — SE chữ thập')])])
XA=M('0 0 0 0 0 0 0 0/0 0 1 1 1 0 0 0/0 1 0 0 0 1 1 0/0 1 0 0 0 0 1 0/0 1 0 1 0 0 1 0/0 0 1 1 1 1 0 0/0 0 0 0 0 0 0 0');x4,tr4=grow(XA,[(3,3)],CROSS,True);x8,tr8=grow(XA,[(3,3)],SQUARE,True)
put('uyen-7-T9','Làm đầy vùng và rò qua góc',7,'hạt giống|giao Aᶜ|4 hướng',[growstep(XA,[(3,3)],CROSS,True),growstep(XA,[(3,3)],SQUARE,True,'Thử thay bằng SE vuông để thấy rò qua góc.'),step('Xác định chỗ rò đầu tiên.',text='Ngay k=1 với SE vuông, từ (3,3) đi chéo được tới (2,2), vốn là nền ngoài nhưng không thuộc A; đó là chỗ rò đầu tiên. Sau đó lan ra nền ngoài qua (1,1),... Chữ thập không cho đi chéo vượt cặp pixel biên nên giữ được trong vùng.')])
XA=M('0 0 0 0 0 0 0 0 0 0 0/0 1 1 1 1 0 0 0 0 0 0/0 1 0 0 1 0 0 1 1 1 0/0 1 0 0 1 0 1 0 0 0 1/0 1 1 1 1 0 1 0 0 0 1/0 0 0 0 0 0 0 1 1 1 0/0 0 0 0 0 0 0 0 0 0 0');outside,trace=grow(XA,[(1,1)],CROSS,True);allfilled=complement(outside)
put('uyen-7-T10','Làm đầy đồng thời hai vùng',7,'mỗi vùng một hạt|nền ngoài',[growstep(XA,[(3,3),(4,9)],CROSS,True),growstep(XA,[(3,3)],CROSS,True,'Chỉ chọn hạt giống ở vùng trái.'),growstep(XA,[(1,1)],CROSS,True,'Chọn nhầm hạt giống ở nền ngoài.'),step('Tận dụng nền ngoài để tô tất cả vùng kín.',r'A_{đầy}=X_{ngoài}^{c}',f'Nền ngoài có {count(outside)} điểm; phần bù có {count(allfilled)} điểm.', 'Một hạt chỉ tô vùng liên thông chứa nó, nên muốn tô riêng cả hai cần hạt trong mỗi vùng. Cách tô toàn bộ: lan từ mọi pixel biên khung thuộc nền ngoài, rồi lấy phần bù; trong bài này (1,1) nối được toàn nền ngoài nên đủ.',blocks=[matrix(allfilled,'Cả hai vùng đã tô bằng phần bù nền ngoài')])])
XA=M('0 0 0 0 0 0 0 0 0/0 1 1 0 0 0 1 1 0/0 1 0 0 0 0 0 1 0/0 0 1 1 0 0 1 1 0/0 0 0 0 0 1 0 0 0/0 1 1 0 0 1 1 0 0/0 0 0 0 0 0 0 0 0')
def components(a,b):
    remaining={(r,c) for r,row in enumerate(a) for c,x in enumerate(row) if x};countc=0
    while remaining:
        r,c=min(remaining);x,_=grow(a,[(r+1,c+1)],b);remaining -= {(r,c) for r,row in enumerate(x) for c,v in enumerate(row) if v};countc+=1
    return countc
put('uyen-7-T11','Trích thành phần liên thông 4 và 8',7,'giao A|liên thông chéo',[growstep(XA,[(2,2)],SQUARE),growstep(XA,[(2,2)],CROSS),growstep(XA,[(2,7)],SQUARE),step('Đếm toàn bộ thành phần, không chỉ thành phần có hạt đã chọn.',text=f'Liên thông 8: {components(XA,SQUARE)} thành phần; liên thông 4: {components(XA,CROSS)} thành phần. Các tiếp xúc chéo nối được với SE vuông nhưng không nối với chữ thập.')])

from worked_parts import apply as apply_worked_parts
apply_worked_parts(SOLUTIONS)

# Full exercise requests restored after clarifying the scope.
for ident in ['uyen-5-T2', 'uyen-5-T3', 'uyen-5-T4', 'uyen-5-T5', 'uyen-5-T6', 'uyen-5-T7', 'uyen-3-T4', 'uyen-3-T7', 'uyen-3-T9', 'uyen-4-T3', 'uyen-4-T4', 'uyen-7-T2', 'uyen-7-T3', 'uyen-7-T4', 'uyen-7-T5', 'uyen-7-T6', 'uyen-7-T7', 'uyen-7-T8', 'uyen-6-T2', 'uyen-6-T6', 'uyen-6-T10', 'uyen-6-T11', 'uyen-6-T12']:
    SOLUTIONS[ident]['revision']=3
