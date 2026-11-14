"""Produce the complete, annotated Word archive from immutable snapshots and review."""
from pathlib import Path
from collections import Counter
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json,re,sys
sys.stdout.reconfigure(encoding='utf8')
ROOT=Path(__file__).resolve().parents[3]
FOLDER=ROOT/'content/tthcm/azota'
report=json.loads((FOLDER/'reviewed.json').read_text(encoding='utf8'))
bank=json.loads((ROOT/'src/subjects/tthcm/bank.json').read_text(encoding='utf8'))
reviews={r['id']:r for r in report['questions']}
sources={s['id']:s for s in bank['sources']}
doc=Document()
section=doc.sections[0]
section.top_margin=section.bottom_margin=Inches(.7)
section.left_margin=section.right_margin=Inches(.8)
section.page_width=Inches(8.27);section.page_height=Inches(11.69)
for style in ['Normal','Body Text']:
 doc.styles[style].font.name='Arial';doc.styles[style].font.size=Pt(10.5)
 doc.styles[style].paragraph_format.space_after=Pt(5)
 doc.styles[style].paragraph_format.line_spacing=1.08
for style in ['Title','Heading 1','Heading 2','Heading 3']:
 doc.styles[style].font.name='Arial';doc.styles[style].font.color.rgb=RGBColor.from_string('743B41')
doc.styles['Heading 3'].font.size=Pt(11)
doc.core_properties.title='TTHCM — 522 câu hỏi Azota và đáp án đối chiếu'
doc.core_properties.subject='Ôn thi theo giáo trình 2019 và bài giảng PTIT'
doc.core_properties.author='Nắm ý'

def hyperlink(paragraph,label,url):
 link=OxmlElement('w:hyperlink')
 link.set(qn('r:id'),paragraph.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True))
 run=OxmlElement('w:r');props=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),'286A65');props.append(color);run.append(props)
 text=OxmlElement('w:t');text.text=label;run.append(text);link.append(run);paragraph._p.append(link)

def para(text='',bold=False,color=None,keep=False,size=None):
 p=doc.add_paragraph();p.paragraph_format.keep_with_next=keep
 r=p.add_run(text);r.bold=bold
 if color:r.font.color.rgb=RGBColor.from_string(color)
 if size:r.font.size=Pt(size)
 return p

doc.add_heading('TƯ TƯỞNG HỒ CHÍ MINH',0)
para('522 CÂU HỎI AZOTA VÀ ĐÁP ÁN ĐỐI CHIẾU',True,'743B41',size=16)
para('Bản lưu ngày 14/11/2026 · Dùng tên trung để xem đề · Không sử dụng đáp án chấm của Azota.')
para('Cách đọc tài liệu',True)
para('Mỗi mục giữ nguyên câu hỏi và thứ tự A–D của lượt trích xuất. Sau đó là đáp án do biên soạn đối chiếu, lời giải ngắn, keyword và căn cứ. Thứ tự câu và lựa chọn trên Azota có thể thay đổi giữa các lượt; luôn nhớ nội dung đáp án.')
para('Giáo trình 2019 và bài giảng PTIT trong workspace là căn cứ chính. Số liệu thiếu hoặc mâu thuẫn được kiểm tra qua nguồn chính thống. Giáo trình Bộ GDĐT bản cũ chỉ hỗ trợ phần mở rộng, không thay cách chia giai đoạn hiện hành.')
para('Nếu câu nguồn có lỗi hoặc nhiều lựa chọn cùng đúng, phần biên tập ghi rõ bản sửa trên web. Đáp án sau biên tập không phải lời xác nhận rằng lựa chọn sai trong bản gốc là đúng.',True)
pending=[r for r in reviews.values() if r['status']=='pending']
para(f'{len(pending)} câu chưa đủ căn cứ được giữ trong tài liệu để không thất lạc nguồn, nhưng chưa có đáp án chấm và chưa đưa vào bài luyện. Không học thuộc một đáp án đoán cho các câu này.',True,'A24A23')
table=doc.add_table(rows=1,cols=4);table.style='Light Shading Accent 1'
for cell,text in zip(table.rows[0].cells,['Đề','Số mục gốc','Đã xử lý','Chờ xác minh']):cell.text=text
for code,count in report['sourceCounts'].items():
 raw=json.loads((FOLDER/f'{code}.json').read_text(encoding='utf8'))
 held=sum(r['status']=='pending' for r in reviews.values() if r['sourceCode']==code)
 for cell,text in zip(table.add_row().cells,[raw['title'].removeprefix('Bắt đầu thi: '),str(count),str(count-held),str(held)]):cell.text=text
para(f"Web sau cập nhật có {len(bank['questions'])} câu chuẩn, gộp câu trùng và giữ đủ dấu vết nguồn. Bộ gốc tại 6 link có 522 mục; hai số này tính hai phạm vi khác nhau.")
doc.add_heading('Những khác biệt cần nhớ',1)
for text in ['Chống thuế Thừa Thiên: nguồn Bảo tàng ghi tháng 4/1908; không học tháng 5/1908 trong một số đề.',
 'Hội nghị Trung ương 8: tháng 5/1941; không phải 11/1941.',
 'Theo giáo trình 2019: giai đoạn hình thành nội dung cơ bản là 1920–1930; tài liệu cũ có thể dùng 1921–1930.',
 'Con đường dẫn tôi đến chủ nghĩa Lênin là tên tác phẩm đúng, không thêm Mác vào tên.',
 'Lịch sử nước ta: viết khoảng nửa sau 1941, xuất bản lần đầu tháng 2/1942.',
 'Thiểu số phục tùng đa số là nội dung đúng của tập trung dân chủ; không chọn nó như một nguyên tắc sai.']:
 para('• '+text)

total=0
for code in report['sourceCounts']:
 raw=json.loads((FOLDER/f'{code}.json').read_text(encoding='utf8'))
 doc.add_page_break()
 doc.add_heading(raw['title'].removeprefix('Bắt đầu thi: '),1)
 p=doc.add_paragraph('Nguồn: ');hyperlink(p,raw['url'],raw['url'])
 para(f"{len(raw['questions'])} câu · Giữ thứ tự trong snapshot {code} · Không bỏ câu trùng.")
 for question in raw['questions']:
  total+=1;review=reviews[question['id']]
  doc.add_heading(f"Câu {question['originalNumber']} · {question['id']}",3)
  para('BẢN GỐC',True,'666666',keep=True,size=9)
  para(question['prompt'],keep=True)
  for i,option in enumerate(question['options']):para(f"{option['id'].upper()}. {option['text']}",keep=i<3)
  if review['status']=='pending':
   para('CHƯA CÓ ĐÁP ÁN CHẤM — KHÔNG ĐƯA LÊN BÀI LUYỆN',True,'A24A23',keep=True)
   para(review['reason']);continue
  original_answer=next(o['text'] for o in question['options'] if o['id']==review['answerOptionId'])
  changed=question['prompt']!=review['studyPrompt'] or question['options']!=review['studyOptions']
  answer_label=f"ĐÁP ÁN ĐỐI CHIẾU: {review['answerOptionId'].upper()}. {review['answerText']}" if original_answer==review['answerText'] else f"ĐÁP ÁN KIẾN THỨC (BẢN ĐÃ SỬA): {review['answerText']}"
  para(answer_label,True,'286A65',keep=True)
  para('Nhớ: '+' · '.join(review['keywords']),True,keep=True)
  para('Giải thích: '+review['explanation'])
  if changed:
   para('BẢN TRÊN WEB ĐÃ BIÊN TẬP',True,'743B41',keep=True,size=9)
   if question['prompt']!=review['studyPrompt']:para('Đề sửa: '+review['studyPrompt'],keep=True)
   for original,study in zip(question['options'],review['studyOptions']):
    if original['text']!=study['text']:para(f"Sửa {study['id'].upper()}: {study['text']}")
  if review['editorialNote']:para('Lưu ý biên tập: '+review['editorialNote'],color='743B41',size=9)
  for ref in review['theoryReferences']:
   source=sources[ref['sourceId']]
   p=doc.add_paragraph();p.paragraph_format.space_after=Pt(3)
   label=source['shortTitle']
   if source.get('url'):hyperlink(p,label,source['url'])
   else:p.add_run(label)
   p.add_run((' · '+ref['section']) if source.get('locatorLabel')=='mục' else f" · trang PDF {ref['pdfPage']} · {ref['section']}")
   for run in p.runs:run.font.size=Pt(8.5)
assert total==522
doc.add_page_break();doc.add_heading('Các câu chưa có đáp án chấm',1)
for r in pending:para(r['id']+' — '+r['reason'])
doc.add_heading('Nguồn đối chiếu trực tuyến',1)
for s in bank['sources']:
 if s.get('url') and s['kind']=='theory':
  para(s['title'],True,keep=True)
  p=doc.add_paragraph();hyperlink(p,s['url'],s['url'])
footer=section.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
footer.add_run('Nắm ý · TTHCM · Trang ')
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
target=ROOT/'TTHCM_AZOTA_522_CAU_HOI_VA_DAP_AN.docx'
doc.save(target)
# Reopen the actual artifact: counts, all original text and decisive corrections must survive.
saved=Document(target);text='\n'.join(p.text for p in saved.paragraphs)
assert sum(p.style.name=='Heading 3' for p in saved.paragraphs)==522
for code in report['sourceCounts']:
 for q in json.loads((FOLDER/f'{code}.json').read_text(encoding='utf8'))['questions']:
  assert q['prompt'] in text,q['id']
  assert all(f"{o['id'].upper()}. {o['text']}" in text for o in q['options']),q['id']
assert '4/1908' in text and '5/1941' in text and '1920–1930' in text
print(f'Word verified: {target.name}; 522 original prompts and 2088 choices; {len(pending)} explicit holds; {target.stat().st_size:,} bytes.')
