import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

const bank = JSON.parse(readFileSync(new URL('../../../src/subjects/tthcm/bank.json', import.meta.url), 'utf8'));
const raw = JSON.parse(readFileSync(new URL('../../../content/tthcm/raw-questions.json', import.meta.url), 'utf8'));
const questions = new Map(bank.questions.map(q => [q.id, q]));
const concepts = new Map(bank.concepts.map(c => [c.id, c]));
const sources = new Map(bank.sources.map(s => [s.id, s]));
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
    assert(!q.options.some(o => /\b[ABCD]\s*(đúng|sai)|đáp án trên|ý trên/i.test(o.text)), label + 'unsafe position dependency');
  }
  assert(q.tags.every(t => ['date','congress','count'].includes(t)), label + 'unknown tag');
}
assert.equal(bank.sampleQuestionIds.length, 20, 'Sample requires 20 questions');
assert.equal(new Set(bank.sampleQuestionIds).size, 20, 'Sample must be unique');
assert(bank.sampleQuestionIds.every(id => questions.has(id)), 'Missing sample questions');
assert.equal(bank.audit.length, raw.length, 'Every raw item needs an editorial decision');
assert.equal(new Set(bank.audit.map(a => a.id)).size, raw.length, 'Duplicate editorial decisions');
for (const source of ['lms','quiz','sample']) {
  assert.equal(bank.audit.filter(a => a.sourceId === source).length, {lms:95,quiz:118,sample:20}[source]);
}
for (const a of bank.audit) {
  assert(raw.some(r => r.id === a.id), 'Unknown source item');
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
console.log(`Content OK: ${bank.questions.length} canonical questions; ${bank.audit.length} source items accounted for; 20-question sample; ${bank.audit.filter(a => ['pending','disputed'].includes(a.status)).length} held for review.`);
