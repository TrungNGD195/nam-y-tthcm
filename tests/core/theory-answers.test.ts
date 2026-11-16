import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {canonical} from '../../scripts/content/xu-ly-anh/document-layout.mjs';
import {validateSolutions} from '../../scripts/content/xu-ly-anh/validate.mjs';

const data=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/solutions.json',import.meta.url),'utf8'));
data.documents=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/documents.json',import.meta.url),'utf8'));
const audit=JSON.parse(readFileSync(new URL('../../content/xu-ly-anh/theory-answer-review.json',import.meta.url),'utf8'));
const subject=JSON.parse(readFileSync(new URL('../../src/subjects/catalog.json',import.meta.url),'utf8')).find((s:any)=>s.id==='xu-ly-anh');
const hash=(v:any)=>createHash('sha256').update(JSON.stringify(canonical(v))).digest('hex');
const theory=data.items.filter((i:any)=>i.kind==='theory');
const item=(id:string)=>theory.find((i:any)=>i.id===id);
const text=(id:string)=>item(id).steps.map((s:any)=>s.lead+' '+s.text+' '+(s.formula??'')).join(' ');

test('101 theory responses have actual answers and correctly matched source-key provenance',()=>{
  assert.equal(theory.length,101);assert.equal(audit.keyBacked,27);
  assert.equal(audit.questions.length,101);
  for(const q of theory){
    const row=audit.questions.find((r:any)=>r.id===q.id)!;
    assert(row);assert.equal(row.answerHash,hash(q.steps));assert.equal(row.promptHash,hash(q.prompt));
    assert.equal(q.answerStyle,'complete');assert(q.steps.every((s:any)=>s.text?.length>35));
    assert(!/ý chính cần trình bày|khi hỏi.*nhấn mạnh/iu.test(text(q.id)));
  }
  for(const id of ['bank-1-12','bank-1-13','bank-1-14']){
    assert.equal(item(id).answerBasis,'course-theory');assert(!item(id).references.some((r:any)=>r.sourceId==='key'));
  }
  assert.deepEqual(item('bank-1-11').references.filter((r:any)=>r.sourceId==='key').map((r:any)=>r.pdfPage),[7,8]);
  assert.match(text('bank-1-11'),/Mô hình nhiễu|Mô hình rời rạc/);assert.match(text('bank-1-11'),/Phát hiện trực tiếp/);
  assert(!/Phát hiện trực tiếp/.test(text('uyen-lt-1-11')));
});

test('responses answer the additional clauses, numerical examples and true/false reasons',()=>{
  assert.match(text('bank-2-2'),/C=255-R/);assert.match(item('bank-2-2').note,/225/);
  assert.match(text('bank-2-4'),/ngưỡng θ/);
  assert.match(text('bank-2-13'),/W không thay đổi/);
  assert.match(text('uyen-3-L1'),/Âm bản/);assert.match(text('uyen-3-L1'),/gamma/);
  assert.match(text('uyen-5-L1'),/H_x/);
  assert.match(text('uyen-5-L7'),/P_1/);assert.match(text('uyen-5-L7'),/t_{n\+1}/);
  assert.match(text('uyen-6-L1'),/5 bit.*9 bit/);
  assert.equal(item('uyen-4-L8').steps.length,4);assert.equal(item('uyen-6-L9').steps.length,5);assert.equal(item('uyen-7-L8').steps.length,7);
  assert.deepEqual(item('uyen-7-L8').steps.map((s:any)=>s.lead.match(/^\(([a-g])\)/)[1]),['a','b','c','d','e','f','g']);
  const code=item('uyen-7-L5').steps.flatMap((s:any)=>s.blocks??[]).find((b:any)=>b.type==='code').code;
  assert.match(code,/padarray/);assert.match(code,/beta = A & ~E/);
});

test('theory-only version updates retain valid exercise PDFs, while exercise edits remain rejected',()=>{
  validateSolutions({...data,version:'next-theory-only'},subject);
  const changed=structuredClone(data);changed.items.find((i:any)=>i.kind==='exercise').steps[0].lead+=' Changed.';
  assert.throws(()=>validateSolutions(changed,subject),/PDF solution is stale/);
});
