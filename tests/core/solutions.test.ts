import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseMarks,filterItems,readingKey } from '../../src/features/solutions/model.ts';
import type { Solutions } from '../../src/features/solutions/types.ts';
import { validateSolutions } from '../../scripts/content/xu-ly-anh/validate.mjs';
import {exerciseHtml} from '../../scripts/content/xu-ly-anh/document-layout.mjs';

const data=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/solutions.json',import.meta.url),'utf8')) as Solutions;
data.documents=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/documents.json',import.meta.url),'utf8'));
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

test('document presentation refuses stale answers, missing pages and reused images',()=>{
  const subject=catalog.find((s:{id:string})=>s.id==='xu-ly-anh');
  const exercise=data.items.find(i=>i.kind==='exercise')!;
  const stale=structuredClone(data);stale.items.find(i=>i.id===exercise.id)!.steps[0].substitution+=' 123';
  assert.throws(()=>validateSolutions(stale,subject),/PDF solution is stale/);
  const missing=structuredClone(data);missing.documents!.items[exercise.id].pages.pop();
  assert.throws(()=>validateSolutions(missing,subject),/Missing screenshot page/);
  const absent=structuredClone(data);delete absent.documents!.items[exercise.id];
  assert.throws(()=>validateSolutions(absent,subject),/Every exercise/);
  const reused=structuredClone(data),other=data.items.filter(i=>i.kind==='exercise')[1];
  reused.documents!.items[other.id].pages[0].src=reused.documents!.items[exercise.id].pages[0].src;
  assert.throws(()=>validateSolutions(reused,subject),/Reused exercise screenshot/);
  const wrongPage=structuredClone(data);wrongPage.documents!.items[exercise.id].pages[0].pdfPage++;
  assert.throws(()=>validateSolutions(wrongPage,subject),/pages out of order/);
});

test('worked subparts match the source clauses and formulas explain symbols before substitution',()=>{
  const cases:{[id:string]:string[]}={
    'bank-4-1':['a','b','c'],'bank-3-6':['a','b'],'uyen-3-T3':['a','b','c'],
    'uyen-3-T5':['a','b','c','d','e','f'],'uyen-3-T7':['a','b','c'],
    'uyen-6-T1':['a','b','c','d','e'],'uyen-6-T9':['a','b','c','d','e'],
    'uyen-6-T11':['a','b','c','d','e','f','g'],'uyen-7-T7':['a','b','c'],
    'uyen-7-T11':['a','b','c','d'],
  };
  for(const [id,letters] of Object.entries(cases)){
    const item=data.items.find(i=>i.id===id)!;
    assert.deepEqual([...new Set(item.steps.map(s=>s.section!.match(/Câu \(([a-g])\)/)![1]))],letters,id);
    const html=exerciseHtml(item,data.sources,[]);
    assert.equal((html.match(/class="answer-part"/g)??[]).length,letters.length,id);
    for(const piece of html.split('class="answer-step"').slice(1)){
      assert.match(piece,/Bước \d+\./);
      if(piece.includes('class="equation"')){
        assert(piece.indexOf('class="equation"')<piece.indexOf('Ký hiệu:'));
        assert(piece.indexOf('Ký hiệu:')<piece.indexOf('Cách làm:'));
        if(piece.includes('Thay số / thực hiện:'))assert(piece.indexOf('Cách làm:')<piece.indexOf('Thay số / thực hiện:'));
      }
    }
  }
  for(const item of data.items.filter(i=>i.kind==='exercise'))for(const step of item.steps){
    assert(step.section&&step.method&&step.method.length>20);
    if(step.formula)assert(step.symbols&&step.symbols.length>25);
  }
});
