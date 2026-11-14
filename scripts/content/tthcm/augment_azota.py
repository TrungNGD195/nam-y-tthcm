"""Publish reviewed snapshots; preserve original extraction and source-to-question audit."""
from pathlib import Path
from collections import Counter
import copy
import hashlib
import json
import re
import unicodedata
from azota_editorial import DECISIONS, EXTRA_CONCEPTS, REPAIRS, HOLDS, BASE_REPAIRS, EXPLANATIONS, SNAPSHOT_HASHES

CODES = {'e9lwce':71,'rnaeqk':148,'ela4jq':88,'ijqzcg':44,'3eggrt':76,'n6fnzo':95}


def norm(text):
    return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',text.lower().replace('đ','d')).encode('ascii','ignore').decode())


def all_independent(text):
    """Only rewrite aggregate options, never a quote or a two-option combination."""
    simple = norm(text)
    letters=re.fullmatch(r'(?:ca|tatca)?([abcd])([abcd])(?:va)?([abcd])(?:deu)?(dung|sai)?',simple)
    if letters and len(set(letters.group(1,2,3)))==3:
        return 'Cả ba phương án còn lại'+(' đều sai' if letters.group(4)=='sai' else '')
    if re.fullmatch(r'(?:ca|tatca)(?:3|ba|abc|cac)(?:dap(?:an)?|phuongan|y)?(?:tren|conlai)?(?:deu)?(?:dung|sai)?',simple):
        return 'Cả ba phương án còn lại' + (' đều sai' if simple.endswith('sai') else '')
    return text


def fingerprint(q):
    return norm(q['prompt'])+'|'+'|'.join(sorted(norm(all_independent(o['text'])) for o in q['options']))


def apply_edit(q, edit):
    if edit.get('prompt'):q['prompt']=edit['prompt']
    if edit.get('fullest'):q['prompt']='Chọn phát biểu đầy đủ nhất. '+q['prompt']
    for option in q['options']:
        if option['id'] in (edit.get('options') or {}):option['text']=edit['options'][option['id']]
    for key in ['explanation','keywords']:
        if edit.get(key):q[key]=edit[key]
    q['editorialNote']=' '.join(filter(None,[q.get('editorialNote',''),edit['note']]))


def has_letter_ref(text):
    return bool(re.search(r'(?<!\w)[ABCD](?!\w)\s*(?:đúng|sai|[,;]|và)|đáp án trên|ý trên',text,re.I))


def number_tags(q):
    prompt=q['prompt'].lower()
    if re.search(r'(?:đại hội|hội nghị).*(?:nào|mấy|thứ|lần|năm|\d{4})',prompt):return ['congress']
    if re.search(r'bao nhiêu|mấy (?:đặc trưng|nội dung|hình thức|giai đoạn|điểm|tuổi|nguyên tắc|điều kiện)',prompt):return ['count']
    if re.search(r'\b(?:18|19|20)\d{2}\b|năm nào|thời gian nào|giai đoạn|được tính từ|khoảng thời gian|thời kỳ nào',prompt):return ['date']
    answer=next(o['text'] for o in q['options'] if o['id']==q['correctOptionId'])
    if re.search(r'\b(?:18|19|20)\d{2}\b',answer) or 'khi nào' in prompt:return ['date']
    return []


def augment(root, bank):
    folder=root/'content/tthcm/azota'
    docs=[json.loads((folder/f'{code}.json').read_text(encoding='utf8')) for code in CODES]
    raw=[q for doc in docs for q in doc['questions']]
    assert len(raw)==522 and set(DECISIONS)=={q['id'] for q in raw}
    assert all(len(doc['questions'])==CODES[doc['code']] for doc in docs)
    for doc in docs:
        digest=hashlib.sha256(json.dumps(doc['questions'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert digest==SNAPSHOT_HASHES[doc['code']],f"Source {doc['code']} changed: review again before using positional choices."
    assert len(bank['questions'])==215,'Run from the original curator, never append to an already augmented bank.'
    bank['sources']+=json.loads((folder/'official-sources.json').read_text(encoding='utf8'))
    bank['concepts']+=copy.deepcopy(EXTRA_CONCEPTS)
    concepts={c['id']:c for c in bank['concepts']}
    official_overrides={'death-sentence':'official-chronology1','truong-son':'official-truongson','marx-humanity':'official-lenin-party','front1939':'official-front1939','foreign-capital':'official-foreigncapital','agriculture':'official-agriculture'}
    for ident,source in official_overrides.items():
        c=concepts[ident]
        c['references']=[dict(sourceId=source,pdfPage=1,section=c['title'],evidence=c['summary'])]
    # Replace the unverified month embedded in the old teaching summary.
    tax=concepts['tax1908']
    tax.update(summary='Nguyễn Tất Thành tham gia biểu tình chống thuế Thừa Thiên tháng 4/1908 theo Tiểu sử Bảo tàng Hồ Chí Minh; một số đề ghi tháng 5, cần sửa.',keywords=['chống thuế Thừa Thiên','4/1908'])
    tax['references']=[dict(sourceId='official-bio',pdfPage=1,section='Thời niên thiếu — tháng 4/1908',evidence=tax['summary'])]
    concepts['industrialization']['references']=[dict(sourceId='ptit',pdfPage=66,section='Nhiệm vụ kinh tế trong quá độ',evidence=concepts['industrialization']['summary']),dict(sourceId='giao-trinh-2009',pdfPage=40,section='Bước đi công nghiệp hóa',evidence=concepts['industrialization']['summary'])]
    base_review=[]
    for q in bank['questions']:
        if q['conceptId'] in ['tax1908','industrialization',*official_overrides]:
            q['theoryReferences']=copy.deepcopy(concepts[q['conceptId']]['references'])
            if q['conceptId']=='tax1908':q['explanation']=tax['summary'];q['keywords']=tax['keywords'];q['revision']=2
        if q['id'] in BASE_REPAIRS:
            apply_edit(q,BASE_REPAIRS[q['id']]);q['revision']=2
        for o in q['options']:
            text=all_independent(o['text'])
            if text!=o['text']:
                o['text']=text;q['revision']=2
                q['editorialNote']=' '.join(filter(None,[q['editorialNote'],'Chuẩn hóa lựa chọn tổng hợp để không phụ thuộc vị trí chữ cái.']))
        # Retain fixed order for any remaining literal letter dependency.
        q['shufflePolicy']='fixed' if any(has_letter_ref(o['text']) for o in q['options']) else 'safe'
        base_review.append(dict(id=q['id'],correctOptionId=q['correctOptionId'],answer=next(o['text'] for o in q['options'] if o['id']==q['correctOptionId']),revision=q['revision'],theoryReferences=q['theoryReferences'],note=BASE_REPAIRS.get(q['id'],{}).get('note','Đọc lại đề, lựa chọn và đối chiếu luận điểm tương ứng; giữ đáp án.')))
    fingerprints={fingerprint(q):q for q in bank['questions']}
    manifest=[]
    for doc in docs:
        code=doc['code'];count=len(doc['questions'])
        source_id='azota-'+code
        bank['sources'].append(dict(id=source_id,title=doc['title'].removeprefix('Bắt đầu thi: '),shortTitle=f'Azota {code}',kind='bank',pages=count,locatorLabel='câu',url=doc['url']))
        for original in doc['questions']:
            ident=original['id'];d=DECISIONS[ident]
            source=dict(sourceId=source_id,pdfPage=original['originalNumber'],originalNumber=original['originalNumber'],group=original['sourceTitle'])
            audit=dict(id=ident,sourceId=source_id,number=original['originalNumber'],chapter=original['chapter'] or 1,pdfPage=original['originalNumber'])
            entry=dict(id=ident,sourceCode=code,originalNumber=original['originalNumber'],sourceChapter=original['chapter'],retrievedAt=doc['retrievedAt'],sourceHash=hashlib.sha256(json.dumps(original,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest())
            if ident in HOLDS:
                bank['audit'].append(dict(**audit,status='pending',reason=HOLDS[ident]))
                manifest.append(dict(**entry,status='pending',reason=HOLDS[ident]));continue
            c=concepts[d['concept']]
            q=dict(id=ident,revision=1,chapter=c['chapter'],topic=c['title'],conceptId=c['id'],tags=[],prompt=original['prompt'],options=copy.deepcopy(original['options']),correctOptionId=d['answer'],shufflePolicy='safe',originType='original',explanation=EXPLANATIONS.get(ident,c['summary']),keywords=copy.deepcopy(c['keywords']),confusionNote=c['confusionNote'],sources=[source],theoryReferences=copy.deepcopy(c['references']),editorialNote='',reviewStatus='verified')
            if ident in REPAIRS:
                apply_edit(q,REPAIRS[ident]);q['originType']='converted'
            for option in q['options']:
                text=all_independent(option['text'])
                if text!=option['text']:
                    option['text']=text
                    if 'Chuẩn hóa lựa chọn tổng hợp' not in q['editorialNote']:
                        q['editorialNote']=' '.join(filter(None,[q['editorialNote'],'Chuẩn hóa lựa chọn tổng hợp để không phụ thuộc vị trí chữ cái.']))
            q['shufflePolicy']='fixed' if any(has_letter_ref(o['text']) for o in q['options']) else 'safe'
            q['tags']=number_tags(q)
            audit['chapter']=q['chapter']
            answer=next(o['text'] for o in q['options'] if o['id']==q['correctOptionId'])
            fp=fingerprint(q)
            existing=fingerprints.get(fp)
            if existing:
                existing_answer=next(o['text'] for o in existing['options'] if o['id']==existing['correctOptionId'])
                assert norm(answer)==norm(existing_answer),f'Answer disagreement: {ident}, {existing["id"]}'
                existing['sources'].append(source)
                # Any newly corrected evidence stays visible in the merged question.
                for ref in q['theoryReferences']:
                    if ref not in existing['theoryReferences']:existing['theoryReferences'].append(ref)
                status='merged';final=existing['id']
            else:
                bank['questions'].append(q);fingerprints[fp]=q
                status='published';final=q['id']
            reason='Đối chiếu giáo trình và nguồn chính thống; '+('đã biên tập lỗi nguồn. ' if ident in REPAIRS else '')+('gộp câu trùng và giữ nguồn.' if existing else 'xuất bản câu có một đáp án.')
            bank['audit'].append(dict(**audit,status=status,questionId=final,reason=reason))
            manifest.append(dict(**entry,status=status,questionId=final,chapter=q['chapter'],answerOptionId=q['correctOptionId'],answerText=answer,explanation=q['explanation'],keywords=q['keywords'],theoryReferences=q['theoryReferences'],editorialNote=q['editorialNote'],studyPrompt=q['prompt'],studyOptions=q['options']))
    # Historical passages already cover their topical fact; references remain traceable.
    bank.update(version='2026.11.14.azota.1',updatedAt='2026-11-14')
    report=dict(version=bank['version'],reviewedAt='2026-11-14',policy='Giáo trình 2019 và bài giảng PTIT ưu tiên; số liệu thiếu/mâu thuẫn đối chiếu nguồn chính thống. Không dùng key Azota. Câu thiếu căn cứ không xuất bản.',sourceCounts=CODES,sourceHashes=SNAPSHOT_HASHES,baseReview=base_review,questions=manifest)
    (folder/'reviewed.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    (root/'src/subjects/tthcm/bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    catalog_path=root/'src/subjects/catalog.json'
    catalog=json.loads(catalog_path.read_text(encoding='utf8'))
    for subject in catalog:
        if subject['id']=='tthcm':subject['questionCount']=len(bank['questions']);subject['sourceDescription']='Theo giáo trình 2019, ngân hàng môn học và 6 đề Azota đã đối chiếu'
    catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    counts=Counter(e['status'] for e in manifest)
    lines=['# Báo cáo nội dung','',f"**{len(bank['questions'])} câu chuẩn** trên web; {sum(bool(q['tags']) for q in bank['questions'])} câu thuộc chuyên đề con số. Đề mẫu vẫn đủ 20 câu.",'','## Sáu đề Azota','', '| Đề | Mục gốc | Thêm câu | Gộp trùng | Chờ xác minh |','| --- | ---: | ---: | ---: | ---: |']
    for code in CODES:
        entries=[e for e in manifest if e['sourceCode']==code];c=Counter(e['status'] for e in entries)
        lines.append(f"| [{code}](https://azota.vn/de-thi/{code}) | {len(entries)} | {c['published']} | {c['merged']} | {c['pending']} |")
    lines+=['',f"Tổng cộng **522 mục gốc**: {counts['published']} câu thêm, {counts['merged']} lượt gộp, {counts['pending']} câu chờ. 233 mục nguồn ban đầu vẫn có đủ audit; 11 mục cũ còn giữ ngoài bài chấm.",'','## Quy tắc đáp án','', '- Ưu tiên giáo trình 2019 và bài giảng PTIT được cung cấp; không sao chép đáp án Azota.','- Giáo trình Bộ GDĐT bản cũ chỉ đối chiếu phần mở rộng, không thay khung giai đoạn hiện hành.','- Số liệu thiếu/mâu thuẫn đối chiếu Bảo tàng Hồ Chí Minh, tác phẩm gốc, Văn phòng Chủ tịch nước, Tư liệu Văn kiện Đảng và Báo Nhân Dân. Mỗi câu có vị trí/căn cứ đối chiếu.','- Bản chụp câu hỏi, thứ tự lựa chọn gốc tách khỏi bản biên tập. Chữ A–D chỉ đúng với đúng snapshot; không dùng chữ cái để suy đáp án giữa các lượt Azota.','- Sửa mốc chống thuế thành 4/1908; mốc Hội nghị TW8 thành 5/1941; giai đoạn hình thành nội dung cơ bản theo giáo trình là 1920–1930.','- Không coi lựa chọn “có vẻ đúng nhất” là đủ khi có hai phương án cùng đúng: sửa có ghi chú hoặc giữ ngoài bài chấm.','- Đã đọc lại 215 câu cũ; tăng revision cho câu thay ý nghĩa để kết quả cũ không tiếp tục chứng nhận một câu đã sửa.','','## Các câu chờ xác minh','']
    for entry in manifest:
        if entry['status']=='pending':lines.append(f"- **{entry['id']}**: {entry['reason']}")
    lines+=['','## Dữ liệu kiểm tra','', '- `azota/<code>.json`: bản gốc 522 câu và lựa chọn.','- `azota/reviewed.json`: quyết định từng mục, đáp án nội dung, keyword, bản biên tập, nguồn đối chiếu và băm snapshot.','- `azota/official-sources.json`: URL nguồn chính thống và tài liệu bổ sung.','- `scripts/content/tthcm/azota_editorial.py`: lựa chọn thủ công và lý do sửa.','','## Nguồn bổ sung cũ','']+[f"- {s['sourceId']}: {s['status']}" for s in bank['supplements']]
    (root/'content/tthcm/BAO_CAO_NOI_DUNG.md').write_text('\n'.join(lines)+'\n',encoding='utf8',newline='\n')
    print(f'Azota: 522 captured; {dict(counts)}. Website: {len(bank["questions"])} canonical questions.')
    return bank
