import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {canonical} from '../../scripts/content/xu-ly-anh/document-layout.mjs';
const read=(path:string)=>JSON.parse(readFileSync(new URL('../../'+path,import.meta.url),'utf8'));
const data=read('src/subjects/xu-ly-anh/solutions.json');
const raw=read('content/xu-ly-anh/source-prompts.json');
const audit=read('content/xu-ly-anh/theory-focus-review.json');
const hash=(v:any)=>createHash('sha256').update(JSON.stringify(canonical(v))).digest('hex');

test('all numerical exercises retain original questions and every source image',()=>{
  const items=data.items.filter((i:any)=>i.kind==='exercise');assert.equal(items.length,67);
  assert.equal(items.filter((i:any)=>i.area==='uyen').length,46);
  for(const item of items){
    const source=raw.records.find((r:any)=>r.id===item.id);
    assert.equal(item.originalText,source.originalText,item.id);
    assert.deepEqual(item.images,source.images,item.id);
    if(source.prompt)assert.equal(item.prompt,source.prompt,item.id);
    assert(!item.editedQuestion&&!item.theoryFocus,item.id);
  }
});

test('theory-only curation preserves IDs, original wording, remaining clauses and audit hashes',()=>{
  const uyen=data.items.filter((i:any)=>i.area==='uyen'&&i.kind==='theory');
  assert.equal(uyen.length,71);
  assert.deepEqual(uyen.map((i:any)=>i.id).sort(),raw.records.filter((i:any)=>i.area==='uyen'&&i.kind==='theory').map((i:any)=>i.id).sort());
  const focused=uyen.filter((i:any)=>i.theoryFocus);assert.equal(focused.length,36);
  assert.equal(focused.filter((i:any)=>i.theoryFocus.mode==='reference').length,10);
  assert.equal(audit.items.length,36);
  for(const item of focused){
    const focus=item.theoryFocus,review=audit.items.find((r:any)=>r.id===item.id);
    assert.equal(review.promptHash,hash(item.prompt));assert.equal(review.answerHash,hash(item.steps));
    assert.equal(review.sourcePromptHash,hash(focus.sourcePrompt));
    assert(item.originalText.replace(/\s+/g,' ').trim().includes(focus.sourcePrompt.replace(/\s+/g,' ').trim()),item.id);
    assert.equal(item.revision,3);
    assert(focus.previous.every((p:any)=>uyen.some((i:any)=>i.id===p.id&&!i.theoryFocus?.previous.some((r:any)=>r.id===item.id))));
    assert.equal(focus.retained.length===0,focus.mode==='reference');
  }
  assert(data.items.filter((i:any)=>i.theoryFocus).every((i:any)=>i.area==='uyen'&&i.kind==='theory'));
  for(const [id,labels] of [['uyen-4-L8',['d']],['uyen-6-L9',['a','d','e']],['uyen-7-L8',['b','c','e','f']]] as const){
    const item=uyen.find((i:any)=>i.id===id);
    assert.deepEqual([...item.prompt.matchAll(/\(([a-g])\)/g)].map(m=>m[1]),labels);
    assert.deepEqual(item.steps.map((s:any)=>s.lead.match(/^\(([a-g])\)/)[1]),labels);
  }
});
