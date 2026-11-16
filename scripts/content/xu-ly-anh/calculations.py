"""Deterministic calculations; conventions are explicit rather than hidden in UI code."""
import math, heapq
from collections import Counter

def rnd(x):
    return math.floor(x+0.5) if x >= 0 else math.ceil(x-0.5)

def fmt(x):
    if isinstance(x, float):
        return round(x, 5) if abs(x-round(x)) > 1e-9 else round(x)
    return x

def matrix(a, caption):
    return dict(type='matrix', rows=[[fmt(x) for x in row] for row in a], caption=caption)

def table(headers, rows, caption=''):
    return dict(type='table', headers=headers, rows=[[fmt(x) for x in row] for row in rows], caption=caption)

def step(lead, formula=None, substitution=None, result=None, text=None, blocks=None):
    return {k:v for k,v in locals().items() if v is not None}

def solution(title, chapter, keywords, steps, note=''):
    return dict(title=title, chapter=chapter, keywords=keywords.split('|'), steps=steps, note=note)

def hist(a, levels=None):
    c=Counter(x for row in a for x in row)
    return [c[i] for i in range(levels or max(c)+1)]

def histstep(h):
    return step('Đếm số pixel tại từng mức xám.', r'h(g)=\#\{(r,c):I(r,c)=g\},\quad N=\sum_g h(g)',
                f'N = '+ ' + '.join(map(str,h))+f' = {sum(h)}.', blocks=[table(['g','h(g)'],list(enumerate(h)))])

def transformed(h, func, tex):
    c=Counter()
    for g,n in enumerate(h): c[func(g)] += n
    sample=func(0)
    origins=[g for g in range(len(h)) if func(g)==sample]
    substitution=f"h′({sample}) = "+' + '.join(f'h({g})' for g in origins)+' = '+' + '.join(str(h[g]) for g in origins)+f' = {c[sample]}.'
    return step('Gộp các mức xám có cùng giá trị sau biến đổi.',r"h'(s)=\sum_{g:f(g)=s}h(g),\quad f(g)="+tex,
                substitution,
                f'Tổng h′ = {sum(c.values())} = N; không mất pixel.',blocks=[table(['s','h′(s)'],sorted(c.items()))])

def smooth(h,w):
    return [sum(h[max(0,g-w//2):min(len(h),g+w//2+1)])/w for g in range(len(h))]

def smoothstep(h,w):
    return step(f'Làm trơn bằng cửa sổ W = {w}; ngoài miền mức xám coi h = 0.',
                r'h_s(g)=\frac1W\sum_{j=-(W-1)/2}^{(W-1)/2}h(g-j)',
                f'h_s(0) = ({" + ".join(map(str,[0]*(w//2)+h[:w//2+1]))})/{w} = {fmt(smooth(h,w)[0])}.',
                blocks=[table(['g',f'h_s, W={w}'],list(enumerate(smooth(h,w))))])

def equalstep(a, l, classic=False):
    h=hist(a,l); n=sum(h); cumul=[];t=0
    for x in h:t+=x;cumul.append(t)
    f=[rnd((l-1)*t/n) if classic else max(0,rnd(t/(n/l))-1) for t in cumul]
    out=[[f[x] for x in row] for row in a]
    formula=r's(g)=\operatorname{round}((L-1)t(g)/N)' if classic else r'TB=N/L,\quad f(g)=\max\{0,\operatorname{round}(t(g)/TB)-1\}'
    return step('Cân bằng theo '+('công thức slide.' if classic else 'công thức giáo trình/đề bài.'),
                r't(g)=\sum_{i=0}^g h(i),\quad '+formula,
                f'N = {n}, L = {l}, TB = {fmt(n/l)}; tại g=0: t(0)={h[0]}, mức mới={f[0]}.',
                f'Histogram mới = {hist(out,l)}; '+('cân bằng lý tưởng.' if len(set(hist(out,l)))==1 else 'chưa cân bằng lý tưởng vì các cột không bằng nhau.'),
                blocks=[table(['g','h(g)','t(g)','mức mới'],[[g,h[g],cumul[g],f[g]] for g in range(l)]),matrix(out,'Ảnh sau cân bằng')])

def diffuse(a,theta=127):
    out=[]; trace=[]
    for r,row in enumerate(a):
        e=0; result=[]
        for c,x in enumerate(row):
            u=x-e;b=0 if u<theta else 255;new_e=b-u
            trace.append([r+1,c+1,x,e,u,b,new_e]);e=new_e;result.append(b)
        out.append(result)
    return out,trace

def diffusionstep(a,theta=127):
    out,trace=diffuse(a,theta); original=sum(map(sum,a))/(len(a)*len(a[0])); threshold=[[0 if x<theta else 255 for x in row] for row in a]
    return step('Duyệt trái sang phải, đặt sai số bằng 0 ở đầu mỗi dòng.',
                r'\begin{gathered}u=I-e_{prev},\quad b=\begin{cases}0&u<\theta\\255&u\ge\theta\end{cases},\quad e=b-u\\ \bar I=\frac1N\sum_{r,c}I(r,c)\end{gathered}',
                f'Điểm (1,1): u = {a[0][0]} − 0 = {a[0][0]}; b = {out[0][0]}; e = {trace[0][-1]}. θ = {theta}. Sáng trung bình gốc: {sum(map(sum,a))}/{len(a)*len(a[0])} = {fmt(original)}.',
                f'Số pixel trắng: khuếch tán = {sum(x==255 for row in out for x in row)}, tách ngưỡng = {sum(x==255 for row in threshold for x in row)}. Trung bình sáng: gốc {fmt(original)}, khuếch tán {fmt(sum(map(sum,out))/(len(a)*len(a[0])))}, tách ngưỡng {fmt(sum(map(sum,threshold))/(len(a)*len(a[0])))}. Khuếch tán phân bố sai số để mô phỏng xám, không bảo toàn chính xác từng pixel.',
                blocks=[matrix(out,'Ảnh khuếch tán lỗi'),matrix(threshold,'Ảnh tách ngưỡng để so sánh'),table(['hàng','cột','I','e trước','u','b','e mới'],trace,'Bảng truyền sai số từng điểm')])

def correlate(a,h,valid=False):
    m,n=len(a),len(a[0]);hr,hc=len(h)//2,len(h[0])//2
    return [[sum(h[i][j]*(a[r+i-hr][c+j-hc] if 0<=r+i-hr<m and 0<=c+j-hc<n else 0)
                 for i in range(len(h)) for j in range(len(h[0])))
             for c in range(hc if valid else 0,n-hc if valid else n)]
            for r in range(hr if valid else 0,m-hr if valid else m)]

PREWITT=[[-1,0,1],[-1,0,1],[-1,0,1]]
SOBEL=[[1,0,-1],[2,0,-2],[1,0,-1]]
def transpose(a):return list(map(list,zip(*a)))
LAP8=[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]
LAP4=[[0,-1,0],[-1,4,-1],[0,-1,0]]
def edge_steps(a,hx,hy,hz=None,signed=False,name='I'):
    gx=correlate(a,hx);gy=correlate(a,hy)
    combined=[[x+y if signed else abs(x)+abs(y) for x,y in zip(rx,ry)] for rx,ry in zip(gx,gy)]
    rows=[matrix(gx,f'{name} ⊗ Hx'),matrix(gy,f'{name} ⊗ Hy'),matrix(combined, f'{name}₁ = '+('Gx + Gy (cộng có dấu theo đề)' if signed else '|Gx| + |Gy|'))]
    r,c=2,2; terms=[f'({a[r+i-1][c+j-1]}·{hx[i][j]})' for i in range(3) for j in range(3)]
    steps=[step('Đặt tâm mặt nạ, nhân các phần tử tương ứng rồi cộng; đệm ngoài ảnh bằng 0.',
                r'G_x(r,c)=\sum_{i=-1}^{1}\sum_{j=-1}^{1}I(r+i,c+j)H_x(i+1,j+1),\quad G_y=I\otimes H_y',
                f'Tại (hàng 3,cột 3): Gx = '+ ' + '.join(terms)+f' = {gx[r][c]}.',
                'Dùng quy ước thực hành của môn: không lật mặt nạ. Chưa cắt đáp ứng âm về 0.',blocks=rows)]
    steps[0]['ySubstitution']='Tại (hàng 3, cột 3): Gy = '+' + '.join(f'({a[r+i-1][c+j-1]}·{hy[i][j]})' for i in range(3) for j in range(3))+f' = {gy[r][c]}.'
    if hz:
        lap=correlate(a,hz)
        steps.append(step('Tính đáp ứng Laplace với cùng cách đặt tâm.',r'I_2(r,c)=\sum_i\sum_j I(r+i,c+j)H_z(i+1,j+1)',
                          'Tại (3,3): I₂ = '+' + '.join(f'({a[r+i-1][c+j-1]}·{hz[i][j]})' for i in range(3) for j in range(3))+f' = {lap[2][2]}.',blocks=[matrix(lap,'Ảnh I₂')]))
    steps.append(step('Chuyển đáp ứng thành biên cần thêm bước chọn biên.',text='Các ma trận trên là đáp ứng lọc. Với gradient, tính |Gx|+|Gy| (không cộng có dấu vì có thể triệt tiêu), rồi làm mảnh/đặt ngưỡng và liên kết biên. Laplace thường xét đổi dấu kết hợp ngưỡng sau làm trơn. Ví dụ minh họa gradient: chọn τ=10 thì pixel có |Gx|+|Gy|≥10 là ứng viên biên; đây là ngưỡng minh họa, không phải đáp án duy nhất của đề. Đệm 0 có thể tạo đáp ứng giả ở rìa ảnh.'))
    return steps

def otsu(h):
    n=sum(h); mu=sum(g*v for g,v in enumerate(h))/n; out=[]
    for k in range(len(h)-1):
        t=sum(h[:k+1]); moment=sum(g*h[g] for g in range(k+1)); m=moment/t if t else 0
        f=t/(n-t)*(m-mu)**2 if 0<t<n else 0
        out.append([k,h[k],t,m,f])
    best=max(x[-1] for x in out); opts=[x[0] for x in out if abs(x[-1]-best)<1e-10]
    return out,opts

def otsustep(h,a=None):
    rows,opts=otsu(h);theta=sum(opts)/len(opts);n=sum(h);mu=sum(i*v for i,v in enumerate(h))/n
    blocks=[table(['g','h(g)','t(g)','m(g)','f(g)'],rows+[[len(h)-1,h[-1],n,mu,'Không xét: lớp >g rỗng']],'m(g) là trung bình lớp ≤g; f(g) tương đương phương sai giữa hai lớp')]
    if a:blocks.append(matrix([[0 if x<=theta else 1 for x in row] for row in a],'Ảnh nhị phân (≤ θ là 0)'))
    return step('Lập histogram và tìm cực đại tiêu chuẩn tách hai lớp.',
                r't(g)=\sum_{i=0}^{g}h(i),\quad m(g)=\frac{\sum_{i=0}^{g}ih(i)}{t(g)},\quad f(g)=\frac{t(g)}{N-t(g)}[m(g)-\mu]^2',
                f'N = {n}; μ = {fmt(mu)}; tại g={opts[0]}: f = {fmt(rows[opts[0]][-1])}.',
                f'Các ngưỡng cực đại: {opts}; lấy trung bình khi có nhiều nghiệm ⇒ θ = {fmt(theta)}. Chỉ xét ngưỡng có hai lớp không rỗng. Có thể có nhiều cực đại bằng nhau; không chọn ngẫu nhiên mà nêu quy ước.',blocks=blocks)

def isodata(h,t,round_each=True):
    rows=[];seen=set()
    for _ in range(30):
        k=math.floor(t);n1=sum(h[:k+1]);n2=sum(h[k+1:])
        if not n1 or not n2: raise ValueError('Empty ISODATA class')
        mu1=sum(i*h[i] for i in range(k+1))/n1;mu2=sum(i*h[i] for i in range(k+1,len(h)))/n2
        nxt=rnd((mu1+mu2)/2) if round_each else (mu1+mu2)/2
        rows.append([t,mu1,mu2,nxt])
        if abs(nxt-t)<1e-10:break
        if nxt in seen:raise ValueError('ISODATA cycle')
        seen.add(t);t=nxt
    return rows

def isostep(h,t=5,round_each=True):
    rows=isodata(h,t,round_each)
    return step('Lặp ngưỡng đẳng liệu/đẳng điệu theo trung bình hai lớp.',
                r'\mu_1(t)=\frac{\sum_{g\le t}gh(g)}{\sum_{g\le t}h(g)},\quad \mu_2(t)=\frac{\sum_{g>t}gh(g)}{\sum_{g>t}h(g)},\quad t_{n+1}=\frac{\mu_1+\mu_2}{2}',
                f't₀ = {t}; t₁ trước làm tròn = ({fmt(rows[0][1])} + {fmt(rows[0][2])})/2 = {fmt((rows[0][1]+rows[0][2])/2)}.',
                f'Ngưỡng cuối = {fmt(rows[-1][-1])}; phân nhóm g ≤ t và g > t. '+('Làm tròn nửa lên ở mỗi vòng theo bộ cô Uyên.' if round_each else 'Giữ số thực trong khi lặp theo giáo trình; ngưỡng thực xác định cùng phân hoạch như phần nguyên của nó, không làm tròn mỗi vòng.'),
                blocks=[table(['t hiện tại','μ₁','μ₂','t kế tiếp'],rows)])

def backgroundstep(h,p,upper=True):
    n=sum(h);target=n*p/100;mode=max(range(len(h)),key=lambda i:h[i]);cum=[];v=0
    for x in h:v+=x;cum.append(v)
    a=next(i for i,x in enumerate(cum) if x>=target) if upper else max(i for i,x in enumerate(cum) if x<=target)
    theta=2*mode-a
    return step('Tìm đỉnh nền, mức phân vị rồi lấy đối xứng.',r'T=2\mathrm{maxp}-a,\quad P(a)=\frac{\sum_{g=0}^a h(g)}{N}',
                f'N={n}; {p}%N={fmt(target)}; maxp={mode}; a={a}; T=2·{mode}−{a}={theta}.',
                ('Lấy a nhỏ nhất có tích lũy ≥ p%N.' if upper else 'Theo quy ước riêng của đề này, lấy a lớn nhất có tích lũy ≤ p%N.')+' '+('Đỉnh nền rõ, chọn cách này hợp lý hơn khi nền trội gần đối xứng.' if mode>=len(h)*.55 else 'Histogram này không có nền sáng trội rõ; kết quả chỉ là áp dụng cơ học, cần xem lại giả thiết.'),
                blocks=[table(['g','h(g)','tích lũy'],[[i,h[i],cum[i]] for i in range(len(h))])])

def trianglestep(h,peak=None,end=None):
    peak=peak if peak is not None else max(range(len(h)),key=lambda i:h[i]); end=end if end is not None else (len(h)-1 if len(h)-1-peak>=peak else 0)
    x1,y1=peak,h[peak];x2,y2=end,h[end];aa=y1-y2;bb=x2-x1;cc=x1*y2-x2*y1;den=math.hypot(aa,bb)
    rows=[[i,h[i],abs(aa*i+bb*h[i]+cc)/den] for i in range(min(peak,end),max(peak,end)+1)]
    winner=max(rows,key=lambda row:row[-1])[0]
    return step('Nối đỉnh với điểm cuối đuôi dài, tìm khoảng cách lớn nhất.',r'd(g)=\frac{|Ax_g+By_g+C|}{\sqrt{A^2+B^2}}',
                f'Đỉnh ({x1},{y1}), cuối ({x2},{y2}); đường Δ: {aa}g + {bb}h + ({cc}) = 0.',
                f'Khoảng cách lớn nhất tại g={winner} ⇒ T={winner}. Không dùng tốt khi histogram nhiều đỉnh mạnh hoặc không có đuôi rõ.',blocks=[table(['g','h(g)','d(g)'],rows)])

def offsets(b):return [(i-len(b)//2,j-len(b[0])//2) for i,row in enumerate(b) for j,x in enumerate(row) if x]
CROSS=[[0,1,0],[1,1,1],[0,1,0]]
SQUARE=[[1,1,1],[1,1,1],[1,1,1]]
def morph(a,b,op='erode',standard=False):
    m,n=len(a),len(a[0]);o=offsets(b)
    if standard and op=='dilate':o=[(-i,-j) for i,j in o]
    return [[int((all if op=='erode' else any)(0<=r+i<m and 0<=c+j<n and a[r+i][c+j] for i,j in o)) for c in range(n)] for r in range(m)]
def count(a):return sum(map(sum,a))
def binary(a,b,fn):return [[int(fn(x,y)) for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def complement(a):return [[1-x for x in row] for row in a]
def morphstep(a,b,standard_extra=False):
    e=morph(a,b);d=morph(a,b,'dilate');blocks=[matrix(e,'X₁ — phép co'),matrix(d,'X₂ — giãn theo hit B của slide')]
    text=f'Số điểm 1: X={count(a)}, co={count(e)}, giãn={count(d)}. Co giữ vị trí fit; giãn giữ vị trí hit; gốc SE ở giữa, ngoài ảnh là 0.'
    if standard_extra:
        ds=morph(a,b,'dilate',True);br=[row[::-1] for row in b[::-1]]
        changes=[f'({i+1},{j+1})' for i in range(len(a)) for j in range(len(a[0])) if d[i][j]!=ds[i][j]]
        blocks += [matrix(br,'B̂ — phản xạ SE qua gốc'),matrix(ds,'Giãn chuẩn theo B̂ khi dò hit')]
        text+=' B không đối xứng; giãn chuẩn khác hit B tại '+', '.join(changes)+'. Phép co vẫn dùng fit B, không đổi.'
    return step('Đặt gốc SE lên từng điểm, kiểm tra các vị trí SE bằng 1.',
                r'E(p)=\bigwedge_{b\in B}X(p+b),\quad D_{hit}(p)=\bigvee_{b\in B}X(p+b)'+(r',\quad D_{std}(p)=\bigvee_{b\in B}X(p-b)' if standard_extra else ''),
                f'Ví dụ tại (1,1): co={e[0][0]}, giãn hit={d[0][0]}; xét đủ {len(offsets(b))} vị trí hoạt động, ngoài ảnh bằng 0.',text,blocks=blocks)

def grow(a,seeds,b,fill=False):
    allowed=complement(a) if fill else a; x=[[0]*len(a[0]) for _ in a]
    for r,c in seeds:
        assert allowed[r-1][c-1];x[r-1][c-1]=1
    trace=[]
    for k in range(1,len(a)*len(a[0])+2):
        y=binary(morph(x,b,'dilate'),allowed,lambda u,v:u and v)
        added=[f'({r+1},{c+1})' for r in range(len(a)) for c in range(len(a[0])) if y[r][c] and not x[r][c]]
        trace.append([k,', '.join(added) or 'Không có điểm mới — dừng',count(y)])
        if y==x:return y,trace
        x=y
    raise AssertionError('Growth did not converge')

def growstep(a,seeds,b,fill=False,caption=''):
    x,trace=grow(a,seeds,b,fill);blocks=[]
    if fill:blocks.append(matrix(complement(a),'Aᶜ'))
    blocks += [table(['k','Điểm mới (hàng,cột) từ 1','Tổng pixel trong Xk'],trace),matrix(x,'Xk khi dừng')]
    if fill:blocks.append(matrix(binary(a,x,lambda u,v:u or v),'A′ = A ∪ Xk'))
    return step(caption or ('Lan hạt giống trong phần không phải biên.' if fill else 'Lan hạt giống trong đối tượng.'),
                r'X_k=(X_{k-1}\oplus B)\cap '+('A^c' if fill else 'A'),
                'X₀ = '+', '.join(map(str,seeds))+f'; sau lần giãn đầu có {trace[0][2]} điểm.',
                f'Dừng ở k={trace[-1][0]} vì Xk=Xk−1. SE '+('chữ thập (4 hướng).' if b==CROSS else 'vuông (8 hướng).'),blocks=blocks)

def huffman(a):
    symbols=[''.join(str(a[r+i][c+j]) for i in range(2) for j in range(2)) for r in range(0,len(a),2) for c in range(0,len(a[0]),2)]
    freq=Counter(symbols);queue=[];serial=0;merges=[]
    for symbol,n in sorted(freq.items()):heapq.heappush(queue,(n,serial,symbol));serial+=1
    while len(queue)>1:
        n1,_,t1=heapq.heappop(queue);n2,_,t2=heapq.heappop(queue)
        merges.append([str(t1),n1,str(t2),n2,n1+n2])
        heapq.heappush(queue,(n1+n2,serial,(t1,t2)));serial+=1
    codes={}
    def walk(t,p=''):
        if isinstance(t,str):codes[t]=p or '0'
        else:walk(t[0],p+'0');walk(t[1],p+'1')
    walk(queue[0][2]);bits=''.join(codes[s] for s in symbols)
    return symbols,freq,codes,bits,merges

def huffmansteps(a):
    syms,freq,codes,bits,merges=huffman(a);n1=len(a)*len(a[0]);n2=len(bits);n=len(syms)
    entropy=-sum((c/n)*math.log2(c/n) for c in freq.values());avg=n2/n
    coded=[codes[s] for s in syms];w=len(a[0])//2
    return [step('Chia ảnh thành khối 2×2 không chồng lấn; quét theo hàng khối.',
                 r'p_i=n_i/N_b,\quad H=-\sum_i p_i\log_2p_i',
                 f'N_b={n1}/4={n}; khối đầu {syms[0][:2]}/{syms[0][2:]} có tần suất {freq[syms[0]]}.',
                 'Ký hiệu viết theo thứ tự trái→phải, trên→dưới trong mỗi khối.',
                 blocks=[table(['khối (2 hàng viết liền)','số lần','xác suất','mã'],[[s,freq[s],freq[s]/n,codes[s]] for s in sorted(freq)])]),
            step('Ghép hai trọng số nhỏ nhất liên tiếp để tạo cây Huffman.',
                 r'w_{\mathrm{cha}}=w_{\mathrm{trái}}+w_{\mathrm{phải}}',
                 f'Lần ghép đầu: {merges[0][1]} + {merges[0][3]} = {merges[0][4]}.',
                 'Bảng ghép mô tả cây: nhánh trái 0, phải 1; hòa tần suất dùng thứ tự khối nhị phân tăng dần rồi thứ tự tạo nút. Đổi các nhánh/hòa tần suất có thể đổi chuỗi mã nhưng không đổi độ dài tối ưu.',
                 blocks=[table(['cây con trái','n trái','cây con phải','n phải','n cha'],merges),matrix([coded[i:i+w] for i in range(0,n,w)],'Ma trận mã theo hàng khối')]),
            step('Tính độ dài mã, tỷ lệ nén và hiệu suất.',
                 r'n_2=\sum_i n_i\ell_i,\quad L=n_2/N_b,\quad C_R=n_1/n_2,\quad R_D=1-n_2/n_1,\quad\eta=H/L',
                 f'n₁={n1} bit; n₂='+ '+'.join(f'{freq[s]}·{len(codes[s])}' for s in sorted(freq))+f'={n2} bit.',
                 f'CR={fmt(n1/n2)}; RD={fmt(1-n2/n1)}; H={fmt(entropy)} bit/khối; L={fmt(avg)}; η={fmt(entropy/avg)}. Chưa tính header/bảng mã. Mã cố định cho {len(freq)} khối khác nhau cần ceil(log₂{len(freq)})={math.ceil(math.log2(len(freq)))} bit/khối, tổng {n*math.ceil(math.log2(len(freq)))} bit. Một ảnh nhỏ có thể nở nếu cộng chi phí bảng mã.')]

def lzw_encode(seq,initial):
    dictionary={(x,):x for x in range(initial)};nextcode=initial;w=(seq[0],);out=[];trace=[]
    for x in seq[1:]:
        new=w+(x,)
        if new in dictionary:trace.append([str(w),x,'—','—']);w=new
        else:
            out.append(dictionary[w]);dictionary[new]=nextcode
            trace.append([str(w),x,dictionary[w],f'{nextcode}: {new}']);nextcode+=1;w=(x,)
    out.append(dictionary[w]);trace.append([str(w),'Kết thúc',dictionary[w],'—'])
    return out,trace

def lzw_decode(codes,initial):
    d={x:(x,) for x in range(initial)};nextcode=initial;w=d[codes[0]];out=list(w);trace=[[codes[0],str(w),'—']]
    for code in codes[1:]:
        special=code==nextcode
        if code not in d and not special:raise AssertionError('Invalid LZW code')
        entry=d[code] if code in d else w+(w[0],)
        out.extend(entry);new=w+(entry[0],);d[nextcode]=new
        trace.append([code,str(entry),f'{nextcode}: {new}'+(' (mã chưa có: w + ký hiệu đầu của w)' if special else '')])
        nextcode+=1;w=entry
    return out,trace

def lzwsteps(a,unit=2,bits=None,gray=False):
    seq=[x for row in a for x in row] if gray else [int(''.join(map(str,row[c:c+unit])),2) for row in a for c in range(0,len(row),unit)]
    initial=256 if gray else 2**unit;codes,trace=lzw_encode(seq,initial);decoded,dt=lzw_decode(codes,initial)
    assert decoded==seq
    steps=[step('Đổi khối ảnh thành ký hiệu rồi xây từ điển thích nghi.',
                r'\text{Nếu }wc\notin D:\ \text{xuất }D[w],\ D[wc]=\text{mã mới},\ w=c',
                f'Từ điển ban đầu: 0…{initial-1}; mã mới bắt đầu {initial}. Chuỗi ký hiệu: '+', '.join(map(str,seq))+'.',
                'Dãy mã xuất: '+', '.join(map(str,codes))+'.',blocks=[table(['w đang xét','ký hiệu c đọc','mã xuất','mục mới'],trace)]),
           step('Giải mã và tái tạo cùng từ điển ở phía nhận.',
                r'D[\mathrm{next}]=w+\operatorname{first}(\mathrm{entry})',
                f'Mã đầu {codes[0]} giải thành {decoded[0]}; mỗi mã sau bổ sung chuỗi trước + ký hiệu đầu chuỗi hiện tại.',
                'Chuỗi sau giải mã trùng chuỗi ký hiệu ban đầu, ghép lại thu được đúng ảnh đề bài. Trường hợp mã bằng vị trí từ điển kế tiếp chưa có: entry = w + first(w).',blocks=[table(['mã đọc','chuỗi giải','mục mới'],dt),matrix(a,'Ảnh khôi phục')])]
    if bits:
        n1=len(a)*len(a[0])*(8 if gray else 1);n2=len(codes)*bits
        assert max(codes)<2**bits
        steps.append(step('Tính số bit theo độ dài từ mã mà đề cho.',r'n_1=MN\,b_{pixel},\quad n_2=N_{mã}\,b_{mã},\quad C_R=n_1/n_2',
                          f'n₁={n1}; n₂={len(codes)}·{bits}={n2}.',f'CR={fmt(n1/n2)}. '+('Dữ liệu nhỏ này nở sau mã hóa; ' if n2>n1 else '')+'LZW có lợi khi chuỗi đủ dài và nhiều lặp; từ điển đầy cần ngừng thêm hoặc reset đồng bộ.'))
    return steps

def zigzag(a):
    result=[];n=len(a)
    for s in range(2*n-1):
        cells=[(i,s-i) for i in range(n) if 0<=s-i<n]
        if s%2==0:cells.reverse()
        result.extend(a[i][j] for i,j in cells)
    return result

def acpairs(seq):
    pairs=[];zeros=0
    for x in seq:
        if x==0:zeros+=1
        else:
            while zeros>=16:pairs.append((15,0));zeros-=16
            pairs.append((zeros,x));zeros=0
    if zeros:pairs.append((0,0))
    return pairs

def dct(a):
    n=len(a)
    return [[(math.sqrt(1/n) if u==0 else math.sqrt(2/n))*(math.sqrt(1/n) if v==0 else math.sqrt(2/n))*
             sum(a[x][y]*math.cos((2*x+1)*u*math.pi/(2*n))*math.cos((2*y+1)*v*math.pi/(2*n)) for x in range(n) for y in range(n))
             for v in range(n)] for u in range(n)]

DC_CODES=['00','010','011','100','101','110','1110','11110','111110']
def category(x):return 0 if x==0 else math.floor(math.log2(abs(x)))+1
def amplitude(x):
    cat=category(x)
    return '' if not cat else format(x if x>0 else (2**cat-1)+x,f'0{cat}b')
