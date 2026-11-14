"""Read supplied ZIPs; retain original prompts and crop exercise figures, never execute files."""
from pathlib import Path
import re, json, zipfile, hashlib
import pymupdf

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'content/xu-ly-anh'
ASSETS = ROOT / 'public/subjects/xu-ly-anh/prompts'
OUT.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def lines(page):
    result = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            text = ''.join(s['text'] for s in line['spans'])
            result.append((line['bbox'], text))
    return sorted(result, key=lambda x: (round(x[0][1], 1), x[0][0]))

sources, records = [], []
for archive in sorted((ROOT / 'materials/xu-ly-anh').glob('*.zip')):
    with zipfile.ZipFile(archive) as z:
        for member in z.namelist():
            if not member.endswith('.pdf'):
                continue
            payload = z.read(member)
            doc = pymupdf.open(stream=payload, filetype='pdf')
            name = member.split('/')[-1]
            bank = name == 'Ngân hàng câu hỏi.pdf'
            uyen = member.startswith('Ôn tập/') and name != 'Theory Questions.pdf'
            source_id = ('bank' if bank else 'key' if 'Đáp án' in name else
                         'textbook' if name == 'Giáo trình xử lý ảnh.pdf' else
                         'uyen-theory' if name == 'Lý thuyết.pdf' else
                         f'uyen-{re.search(r"[3-7]", name)[0]}' if uyen else
                         'english-theory' if name == 'Theory Questions.pdf' else
                         'slide-' + hashlib.sha256(member.encode()).hexdigest()[:8])
            sources.append(dict(id=source_id, title=name, path=member, pages=len(doc), sha256=hashlib.sha256(payload).hexdigest()))
            if not (bank or uyen):
                continue
            starts = []
            for pno, page in enumerate(doc):
                for bbox, text in lines(page):
                    match = re.match(r'^(?:Câu |Bài )?(\d\.(?:[LT])?\d+)\s*(?:\([A-D]\))?\s*[.:;(]', text.strip())
                    if match:
                        starts.append(dict(code=match[1], page=pno, y=bbox[1]-3))
                    # Bank includes an unnumbered additional problem after 4.8.
                    elif bank and pno == 9 and text.strip().startswith('a. Thực hiện tìm ngưỡng tự động'):
                        starts.append(dict(code='4.8-bs', page=pno, y=bbox[1]-3))
            for idx, start in enumerate(starts):
                end = starts[idx+1] if idx+1 < len(starts) else dict(page=len(doc)-1, y=doc[-1].rect.height-35)
                if bank and start['code'] == '4.9':
                    end = dict(page=10, y=doc[10].rect.height-53)
                texts, images, pages = [], [], []
                code = start['code']
                theory = (bank and int(code[0]) < 3) or ('L' in code) or source_id == 'uyen-theory'
                rid = ('bank-' if bank else 'uyen-lt-' if source_id == 'uyen-theory' else 'uyen-') + code.replace('.', '-')
                for pno in range(start['page'], end['page']+1):
                    page = doc[pno]
                    top = start['y'] if pno == start['page'] else (60 if bank else 33)
                    bottom = end['y'] if pno == end['page'] else page.rect.height-(55 if bank else 33)
                    if bottom-top < 8:
                        continue
                    clip = pymupdf.Rect(28 if bank else 30, top, page.rect.width-25, bottom)
                    text = page.get_text(clip=clip, sort=True)
                    text = re.sub(r'lOMoARcPSD\|\d+|messages\.\w+', '', text)
                    if not text.strip():
                        continue
                    texts.append(text.strip())
                    pages.append(pno+1)
                    if not theory:
                        path = ASSETS / f'{rid}-p{pno+1}.webp'
                        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.65, 1.65), clip=clip)
                        from PIL import Image
                        Image.frombytes('RGB', [pix.width, pix.height], pix.samples).save(path, 'WEBP', quality=88)
                        images.append('subjects/xu-ly-anh/prompts/'+path.name)
                records.append(dict(id=rid, code=code, area='bank' if bank else 'uyen', sourceId=source_id,
                                    sourcePages=pages, kind='theory' if theory else 'exercise',
                                    points=int(code[0]) if bank else None,
                                    chapter=None if bank or source_id=='uyen-theory' else int(code[0]),
                                    originalText='\n'.join(texts), prompt=clean(' '.join(texts)) if theory else '', images=images))

assert len({r['id'] for r in records}) == len(records), 'Duplicate question IDs'
(OUT/'source-prompts.json').write_text(json.dumps(dict(sources=sources, records=records), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
used_images={ROOT/'public'/image for r in records for image in r['images']}
for path in ASSETS.glob('*.webp'):
    if path not in used_images:
        assert path.resolve().is_relative_to(ASSETS.resolve())
        path.unlink()
from collections import Counter
print(json.dumps(dict(total=len(records), groups=dict(Counter(r['sourceId'] for r in records))), ensure_ascii=False))
