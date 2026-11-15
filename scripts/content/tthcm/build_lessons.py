"""Compile explicit chapter lessons and a question-to-lesson coverage audit."""
import copy
import hashlib
import json
from collections import Counter
from lesson_editorial import CHAPTERS, DETAILS, DETAIL_PAGE_SPANS, DETAIL_SOURCES, SUMMARY_UPDATES, CONFUSIONS


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode('utf8')).hexdigest()


def enrich_lessons(root, bank):
    before = digest(bank['questions'])
    bank['concepts'] = copy.deepcopy(bank['concepts'])
    concepts = {c['id']: c for c in bank['concepts']}
    chapters = copy.deepcopy(CHAPTERS)
    assigned = {}
    for chapter in chapters:
        seen = set()
        for section in chapter['sections']:
            for ident in section['conceptIds']:
                assert ident in concepts, f'Unknown lesson concept {ident}'
                assert ident not in seen, f'Duplicate chapter lesson concept {ident}'
                assert any(q['chapter'] == chapter['chapter'] and q['conceptId'] == ident
                           for q in bank['questions']), f'Lesson has no corresponding chapter question: {ident}'
                seen.add(ident)
                assigned[chapter['chapter'], ident] = section['id']
    for ident, summary in SUMMARY_UPDATES.items():
        concepts[ident]['summary'] = summary
    for ident, confusion in CONFUSIONS.items():
        concepts[ident]['confusionNote'] = confusion
    for ident, data in DETAILS.items():
        c = concepts[ident]
        c['learningPoints'] = copy.deepcopy(data['points'])
        for page in DETAIL_PAGE_SPANS.get(ident, [data['page']]):
            c['references'].append(dict(sourceId=DETAIL_SOURCES.get(ident,'ptit'), pdfPage=page,
                section=c['title'], evidence='Diễn giải phần '+c['title']+'; xem cùng các trang liên tiếp được dẫn cho mục này.'))
    # Keep the already reviewed evidence for specifics absent from the main book,
    # including official-source checks of dates, titles and original quotations.
    for ident in set(DETAILS) | set(SUMMARY_UPDATES):
        c = concepts[ident]
        refs = c['references'] + [r for q in bank['questions'] if q['conceptId'] == ident
                                  for r in q['theoryReferences']]
        unique = {}
        for r in refs:
            key = (r['sourceId'], r['pdfPage'], r['section'])
            unique.setdefault(key, r)
        c['references'] = list(unique.values())
    rows = []
    for q in bank['questions']:
        key = (q['chapter'], q['conceptId'])
        assert key in assigned, f'Question missing chapter lesson: {q["id"]} / {key}'
        rows.append(dict(questionId=q['id'], chapter=q['chapter'], conceptId=q['conceptId'],
                         sectionId=assigned[key], questionHash=digest(q),
                         answerText=next(o['text'] for o in q['options'] if o['id'] == q['correctOptionId'])))
    bank['lessons'] = dict(version='2026.11.15.1', chapters=chapters)
    assert before == digest(bank['questions']), 'Lessons must not edit questions or answers'
    report = dict(version=bank['lessons']['version'], questionBankVersion=bank['version'],
                  policy='Xét toàn bộ câu chuẩn; gom ý theo chương của ngân hàng, đối chiếu giáo trình và nguồn đã xác minh. Không đổi chương hoặc đáp án để khớp bài học.',
                  questionsHash=before, questionCount=len(rows),
                  conceptCount=len({r['conceptId'] for r in rows}),
                  sectionCount=sum(len(c['sections']) for c in chapters),
                  chapterCounts=dict(Counter(r['chapter'] for r in rows)), questions=rows)
    (root/'content/tthcm/lesson-coverage.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
    print(f'Chapter lessons: {report["sectionCount"]} sections, {report["conceptCount"]} concepts; '
          f'{len(rows)}/{len(bank["questions"])} questions linked without changing chapters or keys.')
