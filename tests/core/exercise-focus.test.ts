import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {canonical,exerciseHtml} from '../../scripts/content/xu-ly-anh/document-layout.mjs';
import {validateSolutions} from '../../scripts/content/xu-ly-anh/validate.mjs';
import {parseMarks} from '../../src/features/solutions/model.ts';
const read=(p:string)=>JSON.parse(readFileSync(new URL(p,import.meta.url),'utf8'));
const data=read('../../src/subjects/xu-ly-anh/solutions.json');
data.documents=read('../../src/subjects/xu-ly-anh/documents.json');
const raw=read('../../content/xu-ly-anh/source-prompts.json');
const audit=read('../../content/xu-ly-anh/exercise-focus-review.json');
const subject=read('../../src/subjects/catalog.json').find((s:any)=>s.id===data.subjectId);
const item=(id:string)=>data.items.find((i:any)=>i.id===id);
const hash=(v:any)=>createHash('sha256').update(JSON.stringify(canonical(v))).digest('hex');

test('all 46 Uyen exercises survive; revised requests preserve source evidence and explicit new focus',()=>{
  const exercises=data.items.filter((i:any)=>i.area==='uyen'&&i.kind==='exercise');
  assert.equal(exercises.length,46);assert.equal(data.items.length,168);
  assert.deepEqual(new Set(exercises.map((i:any)=>i.id)),new Set(raw.records.filter((i:any)=>i.area==='uyen'&&i.kind==='exercise').map((i:any)=>i.id)));
  assert.equal(audit.editedExercises,23);assert.equal(audit.items.length,23);
  for(const q of exercises){
    const original=raw.records.find((r:any)=>r.id===q.id);
    assert.equal(q.originalText,original.originalText);assert.deepEqual(q.images,original.images);
    if(!q.editedQuestion)continue;
    const row=audit.items.find((r:any)=>r.id===q.id);
    assert.equal(row.sourceHash,hash(q.originalText));assert.equal(row.questionHash,hash(q.editedQuestion));assert.equal(row.answerHash,hash(q.steps));
    assert(row.removedRequests.length>0&&row.preservedFocus.length>0);
    assert.deepEqual(q.editedQuestion.parts.map((p:any)=>p.label),[...new Set(q.steps.map((s:any)=>s.section.match(/^Câu \(([a-g])\)/)[1]))]);
    const html=exerciseHtml(q,data.sources,q.images);
    assert(html.includes('Đề ôn tập — tập trung ý mới'));
    assert(!html.includes('prompt-figure'),'Source images must not reintroduce the removed requests in the edited PDF');
  }
});

test('repeated calculations become supplied data while the distinct questions remain',()=>{
  assert.deepEqual(item('uyen-5-T6').editedQuestion.parts.map((p:any)=>p.label),['c']);
  assert.match(item('uyen-5-T6').prompt,/cực đại cục bộ/);
  assert(item('uyen-5-T6').editedQuestion.givens.length>=3);
  assert.deepEqual(item('uyen-6-T2').editedQuestion.parts.map((p:any)=>p.label),['b','c']);
  assert.match(item('uyen-6-T2').prompt,/độ dài cố định/);
  assert.deepEqual(item('uyen-6-T11').editedQuestion.parts.map((p:any)=>p.label),['a','e','f','g']);
  assert(item('uyen-6-T11').editedQuestion.supplied.some((s:any)=>s.title.includes('Mã DC')&&s.text.includes('Bit DC')));
  assert.match(item('uyen-6-T6').prompt,/chưa có/);
  assert.match(item('uyen-7-T6').prompt,/O∘B/);
  assert.deepEqual(item('uyen-7-T8').editedQuestion.parts.map((p:any)=>p.label),['b']);
  const bad=structuredClone(data);bad.items.find((q:any)=>q.id==='uyen-6-T11').editedQuestion.parts.pop();
  assert.throws(()=>validateSolutions(bad,subject),/focused question and answer disagree/);
});

test('Otsu disjoint maxima never turn the suboptimal middle into the answer, and diffusion uses the actual source row',()=>{
  const q=item('uyen-5-T4');const rows=q.editedQuestion.givens[0].rows;
  assert.equal(rows[3].at(-1),rows[5].at(-1));assert(rows[4].at(-1)<rows[3].at(-1));
  assert.match(q.steps[0].result,/θ=3.*θ=5/);assert.match(q.steps[0].text,/4 không phải nghiệm tối ưu/);
  const diffusion=item('uyen-4-T3').steps.map((s:any)=>s.text).join(' ');
  assert(!diffusion.includes('Dòng 2 của ảnh gốc đều bằng 90'));
  assert.match(item('uyen-4-T4').steps[0].substitution,/90−0=90/);
});

test('only revised items reject their old mastery mark',()=>{
  const changed=item('uyen-5-T6'),unchanged=item('uyen-3-T1');
  const marks=parseMarks(JSON.stringify({[changed.id]:{revision:1,state:'known'},[unchanged.id]:{revision:unchanged.revision,state:'known'}}),data.items);
  assert(!marks[changed.id]);assert.equal(marks[unchanged.id].state,'known');
});
