import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';

const bank = JSON.parse(readFileSync(new URL('../../../src/subjects/tthcm/bank.json', import.meta.url), 'utf8'));
const raw = JSON.parse(readFileSync(new URL('../../../content/tthcm/raw-questions.json', import.meta.url), 'utf8'));
const questions = new Map(bank.questions.map(q => [q.id, q]));
const concepts = new Map(bank.concepts.map(c => [c.id, c]));
const sources = new Map(bank.sources.map(s => [s.id, s]));
const codes={e9lwce:71,rnaeqk:148,ela4jq:88,ijqzcg:44,'3eggrt':76,n6fnzo:95};
const azota=Object.keys(codes).flatMap(code=>{
  const doc=JSON.parse(readFileSync(new URL(`../../../content/tthcm/azota/${code}.json`,import.meta.url),'utf8'));
  assert.equal(doc.questions.length,codes[code],`Incomplete Azota ${code}`);
  assert.deepEqual(doc.questions.map(q=>q.originalNumber),Array.from({length:codes[code]},(_,i)=>i+1));
  return doc.questions.map(q=>({...q,sourceId:'azota-'+code,pdfPage:q.originalNumber}));
});
const allRaw=[...raw,...azota];
assert.equal(questions.size, bank.questions.length, 'Duplicate question IDs');
assert.equal(concepts.size, bank.concepts.length, 'Duplicate concept IDs');
assert.deepEqual(bank.chapters.map(c => c.number), [1,2,3,4,5,6]);

for (const q of bank.questions) {
  const label = `${q.id}: `;
  assert.equal(q.reviewStatus, 'verified', label + 'unreviewed question');
  assert(Number.isInteger(q.revision) && q.revision > 0, label + 'revision');
  assert(q.chapter >= 1 && q.chapter <= 6 && concepts.has(q.conceptId), label + 'chapter/concept');
  assert(q.prompt.length > 10 && !q.prompt.includes('[!info:'), label + 'prompt');
  assert(q.options.length >= 2 && q.options.length <= 4, label + 'option count');
  assert.equal(new Set(q.options.map(o => o.id)).size, q.options.length, label + 'option IDs');
  assert(q.options.every(o => typeof o.text === 'string' && o.text.trim()), label + 'empty option');
  assert(q.options.some(o => o.id === q.correctOptionId), label + 'invalid answer ID');
  assert(q.explanation.length > 30 && q.keywords.length > 0 && q.keywords.length <= 3, label + 'learning content');
  assert(q.sources.length > 0 && q.theoryReferences.length > 0, label + 'missing provenance');
  for (const ref of [...q.sources, ...q.theoryReferences]) {
    const source = sources.get(ref.sourceId);
    assert(source && Number.isInteger(ref.pdfPage) && ref.pdfPage > 0 && ref.pdfPage <= source.pages, label + 'source page');
  }
  if (q.shufflePolicy === 'safe') {
    assert(!q.options.some(o => /(?<![\p{L}\p{N}_])[ABCD]\s*(đúng|sai)|đáp án trên|ý trên/iu.test(o.text)), label + 'unsafe position dependency');
  }
  assert(q.tags.every(t => ['date','congress','count'].includes(t)), label + 'unknown tag');
}
assert.equal(bank.sampleQuestionIds.length, 20, 'Sample requires 20 questions');
assert.equal(new Set(bank.sampleQuestionIds).size, 20, 'Sample must be unique');
assert(bank.sampleQuestionIds.every(id => questions.has(id)), 'Missing sample questions');
assert.equal(bank.audit.length, allRaw.length, 'Every raw item needs an editorial decision');
assert.equal(new Set(bank.audit.map(a => a.id)).size, allRaw.length, 'Duplicate editorial decisions');
for (const source of ['lms','quiz','sample']) {
  assert.equal(bank.audit.filter(a => a.sourceId === source).length, {lms:95,quiz:118,sample:20}[source]);
}
for (const a of bank.audit) {
  assert(allRaw.some(r => r.id === a.id), 'Unknown source item');
  if (a.status === 'published' || a.status === 'merged') {
    const q = questions.get(a.questionId);
    assert(q, 'Published item missing canonical question');
    assert(q.sources.some(s => s.sourceId === a.sourceId && s.originalNumber === a.number && s.pdfPage === a.pdfPage), 'Lost source citation');
  } else {
    assert(!questions.has(a.id), `Unresolved question leaked: ${a.id}`);
    assert(a.reason.length > 20, 'Quarantine reason missing');
  }
}
assert(!questions.has('lms-g6-07'), 'Known disputed culture answer must not be graded');
for (let chapter = 1; chapter <= 6; chapter++) {
  assert(bank.questions.some(q => q.chapter === chapter && !q.tags.length));
  assert(bank.concepts.filter(c => c.chapter === chapter && c.core).length >= 5);
}
const lessonReport=JSON.parse(readFileSync(new URL('../../../content/tthcm/lesson-coverage.json',import.meta.url),'utf8'));
const sortKeys=v=>Array.isArray(v)?v.map(sortKeys):v!==null&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,sortKeys(v[k])])):v;
const digest=v=>createHash('sha256').update(JSON.stringify(sortKeys(v))).digest('hex');
assert.equal(lessonReport.version,bank.lessons.version,'Stale lesson version');
assert.equal(lessonReport.questionBankVersion,bank.version,'Stale lesson bank version');
assert.equal(lessonReport.questionsHash,digest(bank.questions),'Questions changed: review and regenerate chapter lessons');
const lessonRows=new Map(lessonReport.questions.map(r=>[r.questionId,r]));
assert.equal(lessonRows.size,bank.questions.length,'Lesson audit must account for every question once');
assert.equal(lessonReport.questions.length,lessonRows.size,'Duplicate lesson audit rows');
for(const q of bank.questions){
  const row=lessonRows.get(q.id);
  assert(row&&row.chapter===q.chapter&&row.conceptId===q.conceptId&&row.questionHash===digest(q),`Stale lesson audit: ${q.id}`);
  const section=bank.lessons.chapters.find(c=>c.chapter===q.chapter)?.sections.find(s=>s.id===row.sectionId);
  assert(section?.conceptIds.includes(q.conceptId),`Wrong chapter lesson: ${q.id}`);
  assert.equal(row.answerText,q.options.find(o=>o.id===q.correctOptionId).text,'Lesson audit answer mismatch');
}
console.log(`Chapter lessons OK: ${bank.lessons.chapters.flatMap(c=>c.sections).length} sections; ${lessonRows.size}/${bank.questions.length} questions linked.`);
console.log(`Content OK: ${bank.questions.length} canonical questions; ${bank.audit.length} source items accounted for; 20-question sample; ${bank.audit.filter(a => ['pending','disputed'].includes(a.status)).length} held for review.`);
