import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { sourceName, sourceLocation, sourceDetails } from '../../src/shared/ui.ts';
import { emptyProgress, parseProgress } from '../../src/core/storage.ts';
import type { Bank, Source } from '../../src/core/types.ts';

const read=(path:string)=>JSON.parse(readFileSync(new URL('../../'+path,import.meta.url),'utf8'));
const bank=read('src/subjects/tthcm/bank.json') as Bank;
const report=read('content/tthcm/azota/reviewed.json');
const qmap=new Map(bank.questions.map(q=>[q.id,q]));
const norm=(s:string)=>s.toLowerCase().replaceAll('đ','d').normalize('NFD').replace(/[^a-z0-9]/g,'');
const sorted=(value:any):any=>Array.isArray(value)?value.map(sorted):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(k=>[k,sorted(value[k])])):value;

test('all 522 captured items have one auditable decision and correct content survives merges',()=>{
  const raw=Object.entries(report.sourceCounts).flatMap(([code,count])=>{
    const doc=read(`content/tthcm/azota/${code}.json`);assert.equal(doc.questions.length,count);
    assert.equal(createHash('sha256').update(JSON.stringify(sorted(doc.questions))).digest('hex'),report.sourceHashes[code]);
    return doc.questions;
  });
  assert.equal(raw.length,522);assert.equal(report.questions.length,522);
  assert.equal(bank.audit.length,755);assert.equal(new Set(bank.audit.map(a=>a.id)).size,755);
  for(const original of raw){
    const review=report.questions.find((r:any)=>r.id===original.id);assert(review);
    assert.equal(createHash('sha256').update(JSON.stringify(sorted(original))).digest('hex'),review.sourceHash,original.id);
    const audit=bank.audit.find(a=>a.id===original.id)!;assert.equal(audit.status,review.status);
    if(review.status==='pending'){
      assert(!qmap.has(original.id));assert(!review.answerText);assert(review.reason.length>30);continue;
    }
    const q=qmap.get(review.questionId)!;assert(q);
    assert.equal(norm(q.options.find(o=>o.id===q.correctOptionId)!.text),norm(review.answerText),original.id);
    assert(q.sources.some(s=>s.sourceId==='azota-'+original.code&&s.originalNumber===original.originalNumber));
    assert(review.theoryReferences.length>0);
  }
});

test('known source mistakes are corrected with original evidence retained',()=>{
  const review=(id:string)=>report.questions.find((r:any)=>r.id===id);
  assert.equal(review('azota-e9lwce-070').answerText,'Tháng 4/1908');
  const original=read('content/tthcm/azota/e9lwce.json').questions.find((q:any)=>q.id==='azota-e9lwce-070');
  assert.equal(original.options[0].text,'Tháng 5/1908');
  assert.match(review('azota-e9lwce-070').editorialNote,/5\/1908/);
  assert.match(review('azota-rnaeqk-069').answerText,/5\/1941/);
  assert.equal(review('azota-e9lwce-049').answerText,'1920 → 1930');
  assert.equal(review('azota-e9lwce-040').answerText,'Con đường dẫn tôi đến chủ nghĩa Lênin');
  assert.equal(review('azota-ela4jq-022').answerText,'Đa số phục tùng thiểu số');
  assert(bank.questions.every(q=>q.options.filter(o=>o.id===q.correctOptionId).length===1));
  // A, B và C was self-referential after Azota shuffled it into option B.
  assert.equal(review('azota-3eggrt-015').answerText,'Cả ba phương án còn lại');
  assert(!bank.questions.some(q=>q.options.some(o=>/^A, B và C$/.test(o.text))));
  for(const id of ['azota-e9lwce-003','azota-e9lwce-071'])assert(qmap.get(review(id).questionId)!.tags.includes('date'));
});

test('revised content drops obsolete mastery while keeping unchanged progress',()=>{
  assert.equal(report.baseReview.length,215);
  const corrected=qmap.get('sample-g1-04')!,unchanged=qmap.get('lms-g1-01')!;
  assert(corrected.revision>1);assert.equal(unchanged.revision,1);
  const progress=emptyProgress('old');
  for(const q of [corrected,unchanged])progress.records[q.id]={revision:1,seen:1,correct:1,incorrect:0,lastOutcome:'correct',lastAt:1,bookmarked:false};
  const loaded=parseProgress(progress,qmap,bank.version);
  assert(!loaded.records[corrected.id]);assert(loaded.records[unchanged.id]);
});

test('web references link to sources and never call online question numbers PDF pages',()=>{
  const source=bank.sources.find(s=>s.id==='azota-e9lwce')!;
  assert.equal(sourceLocation(source,70),'Câu 70');
  assert.equal(sourceLocation(bank.sources.find(s=>s.id==='official-bio'),1),'Nội dung trực tuyến');
  const q=qmap.get(report.questions.find((r:any)=>r.id==='azota-e9lwce-070').questionId)!;
  const html=sourceDetails(q,bank.sources);
  assert(html.includes('https://azota.vn/de-thi/e9lwce'));assert(html.includes('Câu 70'));
  assert(!html.includes('Trang PDF 70'));assert(html.includes('noopener noreferrer'));
  assert(!sourceName({...source,url:'javascript:alert(1)'} as Source).includes('href='));
});
