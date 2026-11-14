"""Apply explicitly reviewed semantic merges; snapshots and original answers stay intact."""
import hashlib, json

def signature(q):
    payload={k:q[k] for k in ['id','revision','chapter','prompt','options','correctOptionId']}
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def deduplicate(root,bank,manifest):
    decisions=json.loads((root/'content/tthcm/duplicate-decisions.json').read_text(encoding='utf-8'))
    assert len(bank['questions'])==decisions['inputQuestionCount']
    byid={q['id']:q for q in bank['questions']};aliases=[];removed=set();mapping={}
    for group in decisions['groups']:
        keep=byid[group['keep']]
        for ident in [group['keep'],*group['remove']]:
            assert signature(byid[ident])==group['evidence'][ident]['hash'],f'Dedup decision needs new review: {ident}'
        for ident in group['remove']:
            assert ident not in removed and ident not in {g['keep'] for g in decisions['groups']}
            old=byid[ident];removed.add(ident);mapping[ident]=keep['id']
            aliases.append(dict(fromId=ident,toId=keep['id'],revision=old['revision']))
            for key in ['sources','theoryReferences']:
                for value in old[key]:
                    if value not in keep[key]:keep[key].append(value)
            keep['tags']=sorted(set(keep['tags'])|set(old['tags']))
        keep['editorialNote']=' '.join(filter(None,[keep['editorialNote'],'Gộp các bản hỏi trùng ý đã đối chiếu; giữ đầy đủ nguồn gốc.']))
    bank['questions']=[q for q in bank['questions'] if q['id'] not in removed]
    bank['questionAliases']=aliases
    assert not(set(bank['sampleQuestionIds'])&removed),'Keep original sample question IDs'
    for entry in bank['audit']:
        old=entry.get('questionId')
        if old in mapping:
            entry.update(status='merged',questionId=mapping[old],chapter=byid[mapping[old]]['chapter'],reason='Gộp trùng ý sau đối chiếu đề, đáp án và tài liệu; giữ nguồn trong câu chuẩn.')
    for entry in manifest:
        old=entry.get('questionId')
        if old in mapping:
            keep=byid[mapping[old]]
            entry.update(status='merged',questionId=keep['id'],chapter=keep['chapter'],
                         canonicalAnswerOptionId=keep['correctOptionId'],
                         canonicalAnswerText=next(o['text'] for o in keep['options'] if o['id']==keep['correctOptionId']),
                         mergeReason='Gộp trùng ý; answerText và studyOptions vẫn là bản đối chiếu riêng của mục nguồn.')
    return dict(before=decisions['inputQuestionCount'],groups=len(decisions['groups']),merged=len(removed),after=len(bank['questions']))
