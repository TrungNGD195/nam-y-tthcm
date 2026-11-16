"""Build the static self-study collection from source snapshots and authored solutions."""
from pathlib import Path
from copy import deepcopy
import json, re, unicodedata, hashlib
from theory import BANK_MAP, UYEN_THEORY_MAP, CHAPTER_MAP
from theory_answers import resolve_answer, THEORY_KEY_PAGES, CORRECTIONS
from exercises import SOLUTIONS

ROOT=Path(__file__).resolve().parents[3]
raw=json.loads((ROOT/'content/xu-ly-anh/source-prompts.json').read_text(encoding='utf-8'))
sources=raw['sources']
def source_with(prefix):return next(s['id'] for s in sources if s['title'].startswith(prefix))
SLIDES={2:source_with('2_XLA2_'),3:source_with('3_XLA3_'),4:source_with('4_XLA4_'),5:source_with('5_XLA5_'),6:source_with('6_XLA6_'),7:source_with('7_XLA7_'),8:source_with('8_XLA8_')}
CHAPTERS={2:'Cơ bản và biểu diễn ảnh',3:'Nâng cao chất lượng ảnh',4:'Các hệ màu và kỹ thuật in ảnh',5:'Phát hiện biên và phân vùng ảnh',6:'Nén ảnh',7:'Xử lý ảnh hình thái',8:'Nhận dạng ảnh'}
REFS={
 'color':(22,'Màu sắc và mô hình màu'),'cmy':(23,'Hệ màu CMY'),'hsv':(24,'HSV trang 24–25; HSL trang 26–28'),
 'raster':(13,'Mô hình Raster và Vector'),'halftone':(19,'Kỹ thuật in ảnh'),'print-gray':(20,'Khuếch tán lỗi'),
 'diffusion':(20,'Khuếch tán lỗi'),'brightness':(30,'Tăng giảm độ sáng'),'equalize':(31,'Cân bằng tần suất'),
 'window':(33,'Cửa sổ di chuyển'),'noise':(40,'Nhiễu và mô hình nhiễu'),'edge':(44,'Biên và Gradient'),
 'indirect':(44,'Phân loại kỹ thuật dò biên'),'edge-noise':(44,'Biên và biến thiên mức xám'),
 'why-compress':(96,'Giới thiệu nén ảnh'),'mix':(23,'Biểu diễn màu'),'rgb-cmy':(23,'Hệ màu CMY'),
 'filters':(36,'Lọc trung vị; xem thêm trang 38–39: trung bình và k gần nhất'),
 'derivative':(44,'Gradient'),'kernels':(46,'Các mặt nạ gradient'),'canny':(48,'Kỹ thuật Canny (tiếp trang 49)'),
 'background':(70,'Thuật toán đối xứng nền'),'triangle':(71,'Thuật toán tam giác'),'split':(73,'Tách cây tứ phân; hợp/tách–hợp trang 76–77'),
 'kmeans':(87,'Thuật toán nhận dạng trong tự học'),'knn':(85,'Phân lớp theo khoảng cách; bổ sung slide nhận dạng'),
 'hopfield':(91,'Mạng Hopfield'),'kohonen':(93,'Mạng Kohonen'),'rlc':(97,'Mã hóa loạt dài'),
 'jpeg-dct':(105,'DCT và JPEG'),'laplace':(48,'Biên Laplace'),'smooth':(68,'Lược đồ xám và làm trơn'),
 'otsu':(32,'Tìm ngưỡng tự động; đẳng liệu trang 69'),'thresholds':(69,'Các thuật toán tìm ngưỡng, trang 69–71'),
 'restoration':(40,'Khôi phục ảnh'),'cmyk':(23,'CMY; bổ sung slide hệ màu'),
 'color-tf':(19,'In ảnh; màu sắc trang 22–28'),'lzw':(99,'Mã hóa LZW'),'redundancy':(96,'Nén ảnh'),
 'huffman':(97,'Huffman'),'compression':(96,'Nén không tổn thất/có tổn thất; tỷ lệ tham khảo ở slide tiếng Anh trang 17'),
 'coder':(96,'Nén ảnh; xem slide mô hình mã hóa'),'jpeg':(105,'Nén ảnh JPEG'),'compression-tf':(105,'DCT và lượng tử hóa'),
 'morphology':(59,'Các phép toán hình thái'),'erode-dilate':(59,'Co và giãn'),
 'open-close':(60,'Tính chất hình thái; bổ sung slide chương 7'),'clean':(60,'Mở và đóng'),
 'boundary':(65,'Phát hiện biên hình thái'),'fill':(65,'Hình thái; thuật toán làm đầy ở slide chương 7'),
 'component':(65,'Hình thái; thành phần liên thông ở slide chương 7'),'morph-tf':(60,'Các tính chất hình thái')
}
KEY_PAGES={**dict(zip([f'1.{i}' for i in range(1,12)],[2,2,3,3,4,4,5,5,6,6,7])),
           **dict(zip([f'2.{i}' for i in range(1,17)],[9,9,10,11,12,13,14,15,15,16,16,17,18,19,20,20])),
           **dict(zip([f'3.{i}' for i in range(1,12)],[21,22,23,26,27,28,30,30,32,33,34])),
           **dict(zip([f'4.{i}' for i in range(1,10)],[35,37,39,42,45,46,47,48,49]))}
records=[]
for original in raw['records']:
    r=deepcopy(original);code=r['code'];concept=None
    if r['kind']=='exercise':
        authored=deepcopy(SOLUTIONS[r['id']]);chapter=authored['chapter']
    else:
        if r['area']=='bank':concept=BANK_MAP[code]
        elif r['sourceId']=='uyen-theory':concept=UYEN_THEORY_MAP[code]
        else:concept=CHAPTER_MAP[r['chapter']][int(code.split('L')[-1])-1]
        authored=resolve_answer(r['id'],concept);chapter=r['chapter'] or authored['chapter']
    r.update(authored);r['chapter']=chapter;r['revision']=1
    if not r['prompt']:
        r['prompt']=f"Bài {code.replace('-bs',' (bổ sung không đánh số)')}: {r['title']}. Đọc đầy đủ dữ kiện và các ý hỏi trong đề gốc bên dưới."
    r['note']=r.get('note','')
    if r['id'] in CORRECTIONS:r['note']=CORRECTIONS[r['id']]
    if r['id']=='bank-3-10':
        r['note']='Bảng co trong đáp án tham khảo có điểm 1 tại vị trí vốn là 0, ví dụ (4,3), trái với điều kiện fit khi tâm SE là 1. Lời giải tính lại từ đúng ma trận X và kiểm tra ảnh co phải là tập con của X.'
    if r['id']=='uyen-5-T6':
        for s in r['steps']:
            for b in s.get('blocks',[]):
                if b['type']=='table' and 'h_s' in b['headers'][-1]:
                    b['rows']=[[row[0],round(row[1],2)] for row in b['rows']]
    if r['kind']=='theory':
        r['prompt']=re.split(r'●|PHẦN B\.|A\.2\.|2\. Bài tập tính toán',r['prompt'])[0].strip()
    for s in r['steps']:
        if s.get('formula'):
            s['formula']=''.join(c for c in unicodedata.normalize('NFD',s['formula'].replace('đ','d').replace('Đ','D')) if not unicodedata.combining(c))
    r['references']=[dict(sourceId=r['sourceId'],pdfPage=p,section=f"Câu/bài {code}") for p in r['sourcePages']]
    if r['area']=='bank':
        pages=THEORY_KEY_PAGES.get(code,[]) if r['kind']=='theory' else [KEY_PAGES[code]] if code in KEY_PAGES else []
        for page in pages:
            section='Đáp án tham khảo; đối chiếu theo nội dung câu hỏi và kiểm tra với lý thuyết' if r['kind']=='theory' else 'Đáp án tham khảo; đối chiếu và tính lại, không mặc định mọi dòng đều đúng'
            r['references'].append(dict(sourceId='key',pdfPage=page,section=section))
    if concept:
        page,section=REFS[concept]
    else:
        page,section={2:(13,'Biểu diễn ảnh'),3:(31,'Nâng cao chất lượng ảnh; công thức ngưỡng trang 32, lọc trang 33–39, ngưỡng theo histogram trang 68–71'),4:(20,'Khuếch tán lỗi; màu sắc trang 22–28'),5:(44,'Biên; Laplace/Canny trang 48–49, phân vùng trang 68–71'),6:(97,'Nén ảnh; Huffman trang 97, LZW trang 99, JPEG trang 105–109'),7:(59,'Hình thái; tham khảo thêm slide chương 7'),8:(85,'Nhận dạng ảnh')}[chapter]
    r['references'].append(dict(sourceId='textbook',pdfPage=page,section=section))
    if r['kind']=='theory':
        r['answerStyle']='complete'
        r['answerBasis']='checked-key' if r['area']=='bank' and code in THEORY_KEY_PAGES else 'course-theory'
        extra_pages={
            'noise':[40], 'filters':[37,38,39], 'canny':[49,50],
            'kernels':[45,46,47], 'hopfield':[91,92], 'kohonen':[93,94],
            'boundary':[65], 'background':[70], 'triangle':[71],
            'equalize':[31], 'compression':[96],
        }.get(concept,[])
        if r['id']=='bank-1-11':extra_pages+=[44]
        if r['id']=='uyen-5-L1':extra_pages+=[46]
        if r['id']=='uyen-5-L8':extra_pages+=[71]
        if concept=='restoration':
            for p in [70,71,72,75,78]:r['references'].append(dict(sourceId=SLIDES[3],pdfPage=p,section='Các bộ lọc không gian loại nhiễu'))
            for p in [68,69,70,71,73,77]:r['references'].append(dict(sourceId=source_with('3_DIP3_'),pdfPage=p,section='Restoration in the presence of noise; spatial filters'))
        for p in extra_pages:
            if not any(ref['sourceId']=='textbook' and ref['pdfPage']==p for ref in r['references']):
                r['references'].append(dict(sourceId='textbook',pdfPage=p,section=authored['title']+' — đối chiếu các vế câu hỏi'))
    # Page 1 identifies the supplied chapter slide deck; detailed reference is the section/topic.
    r['references'].append(dict(sourceId=SLIDES[chapter],pdfPage=1,section='Bộ slide chương '+str(chapter)+' — '+CHAPTERS[chapter]))
    if chapter==7:
        slide_page=43 if concept=='fill' or code in ['7.T9','7.T10'] else 40 if concept=='boundary' or code in ['7.T7','7.T8'] else 27 if concept in ['open-close','clean'] or code in ['7.T4','7.T5','7.T6'] else 6
        r['references'][-1].update(pdfPage=slide_page,section='Hình thái: fit/hit, mở/đóng, tách biên hoặc làm đầy theo nội dung bài')
    if chapter==6:
        english_slide=source_with('6_DIP6_')
        slide_page=33 if concept=='lzw' or code in ['4.9','6.T4','6.T5','6.T6'] else 49 if concept in ['jpeg','jpeg-dct','compression-tf'] or code in ['6.T8','6.T9','6.T10','6.T11'] else 15 if concept=='coder' else 24 if concept=='huffman' or code in ['3.8','3.9','6.T1','6.T2','6.T3'] else 20
        r['references'].append(dict(sourceId=english_slide,pdfPage=slide_page,section='Chi tiết nguyên lý và công thức nén ảnh trong bộ slide tiếng Anh'))
    if r['id']=='uyen-6-T12' or concept=='compression':
        r['references'].append(dict(sourceId=SLIDES[6],pdfPage=39,section='RMS và SNRms, tử số là năng lượng ảnh khôi phục'))
    if concept=='compression':
        r['references'].append(dict(sourceId=source_with('6_DIP6_'),pdfPage=17,section='Nén không tổn thất: thông thường 2–10'))
    records.append(r)

assert len(records)==168 and len(SOLUTIONS)==67
assert all(r['steps'] for r in records)
data=dict(subjectId='xu-ly-anh',version='2026.11.16.1',updatedAt='2026-11-16',
          chapters=[dict(number=n,title=t) for n,t in CHAPTERS.items()],sources=sources,items=records,
          coverage=dict(bank=51,uyen=117,theory=101,exercises=67,bankPoints={'1':14,'2':16,'3':11,'4':10},
                        englishTheory='28 câu trùng với Lý thuyết.pdf, gộp và giữ nguồn tiếng Anh trong danh mục'),
          exam=dict(ethics='Câu 1 — Đạo đức',theory='Câu 2 — Lý thuyết',exercises='Câu 3–4 — Bài tập chương 3–7',
                    note='Cấu trúc đề theo thông tin người học cung cấp. Chưa thấy bộ câu hỏi/đáp án đạo đức riêng trong tài liệu, nên chưa có lời giải phần này. Ngân hàng cũ chia mức điểm để tra bài, không dùng làm cấu trúc thi hiện tại.'))
target=ROOT/'src/subjects/xu-ly-anh/solutions.json';target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')).hexdigest()
theory_items=[r for r in records if r['kind']=='theory']
theory_audit=dict(version='2026.11.16.1',questionCount=len(theory_items),
    policy='Ngân hàng theo đáp án đã kiểm tra với giáo trình; cô Uyên theo giáo trình/slide và cùng lối trình bày câu trả lời hoàn chỉnh. Đối chiếu mục đáp án theo nội dung, không chỉ theo số câu.',
    keyBacked=sum(r['answerBasis']=='checked-key' for r in theory_items),
    questions=[dict(id=r['id'],chapter=r['chapter'],area=r['area'],basis=r['answerBasis'],
                    keyPages=[ref['pdfPage'] for ref in r['references'] if ref['sourceId']=='key'],
                    headings=[s['lead'] for s in r['steps']],promptHash=digest(r['prompt']),answerHash=digest(r['steps'])) for r in theory_items])
assert len(theory_items)==101 and theory_audit['keyBacked']==27
(ROOT/'content/xu-ly-anh/theory-answer-review.json').write_text(json.dumps(theory_audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
catalog_file=ROOT/'src/subjects/catalog.json';catalog=json.loads(catalog_file.read_text(encoding='utf-8'))
for s in catalog:
    if s['id']=='xu-ly-anh':
        s.update(status='ready',learningMode='solutions',solutionPresentation='documents',questionCount=len(records),chapterCount=len(CHAPTERS),
                 description='Giải ngân hàng theo mức điểm và giải bài cô Uyên theo chương. Công thức rõ, keyword dễ nhớ.')
catalog_file.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report=['# Kiểm kê nội dung Xử lý ảnh','',f'- Tổng: {len(records)} câu/bài; 101 lý thuyết, 67 bài tính.',
        '- Giải ngân hàng: 1 điểm 14 câu, 2 điểm 16 câu, 3 điểm 11 bài, 4 điểm 10 bài (gồm 4.8 bổ sung không đánh số).',
        '- Giải bài cô Uyên: 117 mục. 28 câu Lý thuyết.pdf gộp với bản Anh; các bộ chương 3/4/5/6/7 lần lượt 21/12/16/21/19 mục.',
        '- Chương hiển thị theo slide/bộ cô Uyên; chương giáo trình không trùng số nên trích dẫn ghi trang PDF cụ thể.',
        '- Câu 1 đạo đức chưa có ngân hàng riêng; không tự tạo câu hoặc nhận là đã giải đủ phần đạo đức.',
        '- Mỗi bài tính giữ ảnh đề gốc và bản chép văn bản; công thức và quy ước đặt trước thay số.',
        '- Quy tắc kiểm tra: scripts/content/xu-ly-anh/verify.py; dữ kiện chuẩn tại source-prompts.json.',
        '', '## Những chỗ cần đọc đúng quy ước hoặc đề có lỗi','']
for r in records:
    if r['note']:report.append(f"- **{r['id']}**: {r['note']}")
report+=['','## Danh mục và vị trí nguồn','', '| ID | Câu/bài | Khu vực | Chương | Trang PDF đề |','|---|---|---|---|---|']
for r in records:report.append(f"| {r['id']} | {r['code']} | {r['area']} | {r['chapter']} | {r['sourceId']}: {','.join(map(str,r['sourcePages']))} |")
report+=['','## Câu trả lời lý thuyết hoàn chỉnh — 16/11/2026','',
    '- 101 câu lý thuyết được trả lời thành đoạn văn theo từng vế đề hỏi, không phải dàn ý hoặc lời nhắc viết bài.',
    '- 30 câu ngân hàng: 27 câu có mục đáp án phù hợp để đối chiếu; 1.12–1.14 không có mục tương ứng trong PDF đáp án nên dùng giáo trình. Mục 1.11 của ngân hàng bao gồm nội dung cả 1.11 và 1.12 trong đáp án; không ghép theo số câu một cách máy móc.',
    '- 71 câu cô Uyên: theo giáo trình/slide, trình bày cùng lối định nghĩa → giải thích/các bước → công thức, ví dụ, so sánh khi đề hỏi.',
    '- Ghi rõ lỗi 225 thay vì 255 ở đáp án đổi RGB 8 bit sang CMY; sửa phát biểu gamut CMY và nhầm trọng số Prewitt, không chép theo phần sai.',
    '- Canny: tài liệu mô tả vai trò quan trọng của bước 4 và 5, không đưa xếp hạng tuyệt đối một bước duy nhất. Câu trả lời giải thích trực tiếp vai trò làm mảnh và liên kết bằng hai ngưỡng.',
    '- `theory-answer-review.json` lưu đủ 101 ID, căn cứ, trang đáp án, các vế trả lời và hash để theo dõi nội dung.',
    '- 67 bài tính và PDF/ảnh đã xuất giữ nguyên; hash của từng bài tính kiểm tra tính tương thích, độc lập với phiên bản của câu trả lời lý thuyết.']
(ROOT/'content/xu-ly-anh/KIEM_KE_VA_QUY_UOC.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(f'Built {len(records)} solved items; {sum(r["kind"]=="exercise" for r in records)} calculations.')
