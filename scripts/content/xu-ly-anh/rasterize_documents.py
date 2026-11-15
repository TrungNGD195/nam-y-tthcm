"""Merge the rendered PDFs and screenshot their actual solution pages for the site."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--sample', action='store_true')
args = parser.parse_args()
work = ROOT/'.analysis/solution-documents'
render = json.loads((work/('sample-manifest.json' if args.sample else 'render-manifest.json')).read_text(encoding='utf8'))
data = json.loads((ROOT/'src/subjects/xu-ly-anh/solutions.json').read_text(encoding='utf8'))
items = {i['id']: i for i in data['items'] if i['kind'] == 'exercise'}
if not args.sample:
    assert {r['id'] for r in render['items']} == set(items), 'Every exercise must have a PDF'
fingerprint = hashlib.sha256((json.dumps(render,sort_keys=True,ensure_ascii=False)+
    (ROOT/'scripts/content/xu-ly-anh/document-layout.mjs').read_text(encoding='utf8')).encode('utf8')).hexdigest()[:12]
relative = 'subjects/xu-ly-anh/answer-pages'
target = work/'sample-pages' if args.sample else ROOT/'public'/relative
target.mkdir(parents=True,exist_ok=True)
book_name = f'xu-ly-anh-67-bai-giai-{fingerprint}.pdf'
book = pymupdf.open()
cover = pymupdf.open(work/'cover.pdf')
book.insert_pdf(cover)
toc = []
manifest = dict(subjectId='xu-ly-anh',version=render['version'],dataVersion=data['version'],
                renderFingerprint=fingerprint,book={},items={})
previous_area, previous_chapter = None, None
audit = []
for record in render['items']:
    item = items[record['id']]
    doc = pymupdf.open(work/(item['id']+'.pdf'))
    answer_start = next((n for n,p in enumerate(doc) if 'BÀI GIẢI' in p.get_text()),None)
    assert answer_start is not None and answer_start > 0, f'{item["id"]}: missing separate answer section'
    offset = len(book)
    book.insert_pdf(doc)
    if item['area'] != previous_area:
        toc.append([1,'giải ngân hàng' if item['area']=='bank' else 'giải bài cô Uyên',offset+1])
        previous_area=item['area']
    if item['area']=='uyen' and previous_chapter!=item['chapter']:
        toc.append([2,f'Chương {item["chapter"]}',offset+1]);previous_chapter=item['chapter']
    toc.append([2 if item['area']=='bank' else 3,f'Bài {item["code"]}. {item["title"]}',offset+1])
    pages=[]
    for n in range(answer_start,len(doc)):
        page=doc[n]
        text=page.get_text()
        assert len(text.strip())>35 and '\ufffd' not in text, f'{item["id"]}: empty or invalid text on answer page {n+1}'
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    if not span['text'].strip(): continue
                    x0,y0,x1,y1=span['bbox']
                    assert x0>=15 and x1<=page.rect.width-15 and y0>=8 and y1<=page.rect.height-8, f'{item["id"]}: clipped text {span["text"]}'
        filename=f'{item["id"]}-{fingerprint}-p{len(pages)+1}.png'
        cached=None
        if (target/filename).exists():
            try:
                with Image.open(target/filename) as image:
                    cached=image.size;image.verify()
            except (OSError,ValueError):cached=None
        if not cached:
            pix=page.get_pixmap(matrix=pymupdf.Matrix(168/72,168/72),alpha=False)
            pix.save(target/filename)
            cached=(pix.width,pix.height)
        pages.append(dict(src=relative+'/'+filename,width=cached[0],height=cached[1],pdfPage=offset+n+1,
                          sha256=hashlib.sha256((target/filename).read_bytes()).hexdigest()))
    plain=[f'Bài {item["code"]}. {item["title"]}',item.get('note','')]
    for n,step in enumerate(item['steps'],1):
        plain.extend([f'{n}. {step["lead"]}',*(f'{k}: {step[k]}' for k in ['formula','substitution','text','result'] if k in step)])
        for block in step.get('blocks',[]):
            plain.append(block.get('caption',''))
            if 'headers' in block:plain.append('\t'.join(map(str,block['headers'])))
            plain.extend('\t'.join(map(str,row)) for row in block.get('rows',[]))
    text_name=f'{item["id"]}-{fingerprint}.txt'
    (target/text_name).write_text('\n'.join(plain)+'\n',encoding='utf8')
    manifest['items'][item['id']]=dict(contentHash=record['contentHash'],pdfStartPage=offset+1,
        pdfEndPage=offset+len(doc),answerStartPage=offset+answer_start+1,
        textSrc=relative+'/'+text_name,pages=pages)
    audit.append(dict(id=item['id'],pdfPages=len(doc),answerPages=len(pages),answerCharacters=sum(len(doc[n].get_text()) for n in range(answer_start,len(doc)))))
    if len(audit)%10==0:print(f'Rasterized {len(audit)}/{len(render["items"])} exercises',flush=True)
book.set_toc(toc)
book.set_metadata(dict(title='Xử lý ảnh — 67 bài tập và lời giải đối chiếu',author='Nắm ý',subject='Giải ngân hàng và giải bài cô Uyên'))
book.save(target/book_name,garbage=4,deflate=True)
manifest['book']=dict(src=relative+'/'+book_name,pages=len(book),
    sha256=hashlib.sha256((target/book_name).read_bytes()).hexdigest())
output=work/'sample-documents.json' if args.sample else ROOT/'src/subjects/xu-ly-anh/documents.json'
output.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(work/'render-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(exercises=len(audit),pdfPages=len(book),answerImages=sum(x['answerPages'] for x in audit),
                     pdfBytes=(target/book_name).stat().st_size,output=str(output)),ensure_ascii=False))
