"""Verify that every displayed screenshot belongs to its real, current PDF page."""
import hashlib
import json
from pathlib import Path
import pymupdf
from PIL import Image, ImageChops, ImageStat

ROOT=Path(__file__).resolve().parents[3]
manifest=json.loads((ROOT/'src/subjects/xu-ly-anh/documents.json').read_text(encoding='utf8'))
data=json.loads((ROOT/'src/subjects/xu-ly-anh/solutions.json').read_text(encoding='utf8'))
book_path=ROOT/'public'/manifest['book']['src']
assert hashlib.sha256(book_path.read_bytes()).hexdigest()==manifest['book']['sha256']
book=pymupdf.open(book_path)
assert len(book)==manifest['book']['pages']
assert len([x for x in book.get_toc() if x[0]>1])>=67
count=0
max_error=0
for item in data['items']:
    if item['kind']!='exercise':continue
    record=manifest['items'][item['id']]
    assert 'BÀI GIẢI' in book[record['answerStartPage']-1].get_text()
    for page in record['pages']:
        image_path=ROOT/'public'/page['src']
        assert hashlib.sha256(image_path.read_bytes()).hexdigest()==page['sha256']
        pdf_page=book[page['pdfPage']-1]
        pix=pdf_page.get_pixmap(matrix=pymupdf.Matrix(168/72,168/72),alpha=False)
        reference=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        screenshot=Image.open(image_path).convert('RGB')
        assert screenshot.size==(page['width'],page['height'])==reference.size
        error=sum(ImageStat.Stat(ImageChops.difference(reference,screenshot)).mean)/3
        assert error==0,f'{item["id"]}: lossless screenshot differs from PDF page {page["pdfPage"]}: {error}'
        max_error=max(error,max_error);count+=1
        assert '\ufffd' not in pdf_page.get_text()
print(json.dumps(dict(result='passed',exercises=len(manifest['items']),pdfPages=len(book),
    screenshotPages=count,maxMeanPixelError=round(max_error,5)),ensure_ascii=False))
