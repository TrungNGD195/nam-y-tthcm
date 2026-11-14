import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseMarks,filterItems,readingKey } from '../../src/features/solutions/model.ts';
import type { Solutions } from '../../src/features/solutions/types.ts';
import { validateSolutions } from '../../scripts/content/xu-ly-anh/validate.mjs';

const data=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/solutions.json',import.meta.url),'utf8')) as Solutions;
const catalog=JSON.parse(readFileSync(new URL('../../src/subjects/catalog.json',import.meta.url),'utf8'));
test('every source item has a solution; original bilingual theory is counted once',()=>{
  const raw=JSON.parse(readFileSync(new URL('../../content/xu-ly-anh/source-prompts.json',import.meta.url),'utf8'));
  assert.deepEqual(data.items.map(i=>i.id).sort(),raw.records.map((i:{id:string})=>i.id).sort());
  assert.equal(data.items.length,168);assert.equal(data.coverage.bank,51);assert.equal(data.coverage.uyen,117);
  assert.deepEqual(data.coverage.bankPoints,{'1':14,'2':16,'3':11,'4':10});
  validateSolutions(data,catalog.find((s:{id:string})=>s.id==='xu-ly-anh'));
});
test('solution marks tolerate corruption, reject stale revisions and never touch quiz storage',()=>{
  const item=data.items[0];
  assert.deepEqual(parseMarks('bad json',data.items),{});
  assert.deepEqual(parseMarks('[]',data.items),{});
  assert.deepEqual(parseMarks(JSON.stringify({[item.id]:{revision:item.revision+1,state:'known'}}),data.items),{});
  const marks=parseMarks(JSON.stringify({[item.id]:{revision:item.revision,state:'review'},foreign:{revision:1,state:'known'}}),data.items);
  assert.deepEqual(marks,{[item.id]:{revision:item.revision,state:'review'}});
  assert.notEqual(readingKey('tthcm'),readingKey('xu-ly-anh'));
  assert(!readingKey('xu-ly-anh').includes('progress:v2'));
});
test('search supports Vietnamese without accents and combines filters',()=>{
  const items=filterItems(data.items,'khuech tan','exercise','all',{});
  assert(items.length>=5&&items.every(i=>i.kind==='exercise'));
  const item=items[0],marks={[item.id]:{revision:item.revision,state:'review' as const}};
  assert.deepEqual(filterItems(items,'','all','review',marks),[item]);
  assert(!filterItems(items,'','all','new',marks).includes(item));
});
test('validation rejects missing formulas, foreign assets and nonexistent source pages',()=>{
  const subject=catalog.find((s:{id:string})=>s.id==='xu-ly-anh');
  const clone=()=>structuredClone(data);
  const bad=clone();bad.items.find(i=>i.kind==='exercise')!.steps=[];
  assert.throws(()=>validateSolutions(bad,subject));
  const badAsset=clone();badAsset.items.find(i=>i.images.length)!.images=['subjects/tthcm/foreign.webp'];
  assert.throws(()=>validateSolutions(badAsset,subject));
  const badRef=clone();badRef.items[0].references[0].pdfPage=9999;
  assert.throws(()=>validateSolutions(badRef,subject));
});
