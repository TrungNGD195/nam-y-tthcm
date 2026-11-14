import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import katex from 'katex';

export function validateBank(bank, subject, assetExists = () => true) {
  assert.equal(bank.subjectId,subject.id,'Bank belongs to another subject');
  assert(bank.chapters.length>0 && bank.questions.length>0,'Ready subject needs real content');
  const chapters=new Set(bank.chapters.map(c=>c.number));
  assert.equal(chapters.size,bank.chapters.length,'Duplicate chapters');
  assert([...chapters].every(n=>Number.isSafeInteger(n)&&n>0));
  const questions=new Map(bank.questions.map(q=>[q.id,q]));
  const concepts=new Map(bank.concepts.map(c=>[c.id,c]));
  const sources=new Map(bank.sources.map(s=>[s.id,s]));
  assert.equal(questions.size,bank.questions.length);assert.equal(concepts.size,bank.concepts.length);
  for(const c of bank.concepts)assert(chapters.has(c.chapter));
  function blocks(items=[]) {
    assert(Array.isArray(items));
    for(const block of items){
      if(block.type==='image'){
        assert(typeof block.alt==='string'&&block.alt.trim(),'Image needs alt text');
        assert(typeof block.src==='string'&&block.src.startsWith(`subjects/${subject.id}/`)&&!block.src.split('/').includes('..')&&/^subjects\/[a-z0-9-]+\/[a-zA-Z0-9_./-]+$/.test(block.src),'Image must belong to current subject');
        assert(assetExists(block.src),'Image file missing');
      }else if(block.type==='formula'){
        assert(typeof block.tex==='string'&&block.tex.length<20000);
        katex.renderToString(block.tex,{throwOnError:true,trust:false});
      }else if(block.type==='code')assert(typeof block.code==='string');
      else if(block.type==='table'||block.type==='matrix'){
        assert(Array.isArray(block.rows)&&block.rows.length>0);
        const width=block.type==='table'?block.headers?.length:block.rows[0]?.length;
        assert(width>0&&block.rows.every(row=>Array.isArray(row)&&row.length===width&&row.every(cell=>['string','number'].includes(typeof cell))),'Nonrectangular matrix/table');
        if(block.type==='table')assert(block.headers.every(h=>typeof h==='string'));
      }else assert.fail('Unknown content block');
    }
  }
  for(const q of bank.questions){
    assert.equal(q.reviewStatus,'verified');assert(chapters.has(q.chapter)&&concepts.has(q.conceptId));
    assert(Number.isSafeInteger(q.revision)&&q.revision>0);assert(typeof q.prompt==='string'&&q.prompt.length>10);
    assert(q.options.length>=2&&q.options.length<=4);assert.equal(new Set(q.options.map(o=>o.id)).size,q.options.length);
    assert(q.options.every(o=>typeof o.text==='string'&&o.text.trim()));assert(q.options.some(o=>o.id===q.correctOptionId));
    assert(q.explanation.length>20&&q.keywords.length>0&&q.keywords.length<=3);assert(q.sources.length>0&&q.theoryReferences.length>0);
    assert(q.tags.every(tag=>typeof tag==='string'&&/^[a-z0-9-]+$/.test(tag)));
    if(q.shufflePolicy==='safe')assert(!q.options.some(o=>/\b[ABCD]\s*(đúng|sai)|đáp án trên|ý trên/i.test(o.text)));
    for(const ref of [...q.sources,...q.theoryReferences])assert(sources.has(ref.sourceId)&&Number.isInteger(ref.pdfPage)&&ref.pdfPage>0&&ref.pdfPage<=sources.get(ref.sourceId).pages);
    blocks(q.blocks);blocks(q.explanationBlocks);for(const o of q.options)blocks(o.blocks);
  }
  assert.equal(new Set(bank.sampleQuestionIds).size,bank.sampleQuestionIds.length);assert(bank.sampleQuestionIds.every(id=>questions.has(id)));
  assert.equal(subject.questionCount,bank.questions.length);assert.equal(subject.chapterCount,bank.chapters.length);
  for(const a of bank.audit){if(['published','merged'].includes(a.status))assert(questions.has(a.questionId));else assert(!questions.has(a.id));}
}

if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const root=new URL('../../',import.meta.url);
  const subjects=JSON.parse(readFileSync(new URL('src/subjects/catalog.json',root),'utf8'));
  assert.equal(new Set(subjects.map(s=>s.id)).size,subjects.length);
  for(const subject of subjects){
    assert(/^[a-z0-9-]+$/.test(subject.id)&&subject.name&&/^#[0-9a-f]{6}$/i.test(subject.accent));
    const file=new URL(`src/subjects/${subject.id}/bank.json`,root);
    if(subject.status==='ready'){
      assert(existsSync(file));const bank=JSON.parse(readFileSync(file,'utf8'));
      validateBank(bank,subject,asset=>existsSync(new URL('public/'+asset,root)));
      console.log(`${subject.name}: ${bank.questions.length} questions, ${bank.chapters.length} chapters.`);
    }else{
      assert.equal(subject.status,'awaiting-materials');assert(!existsSync(file));assert(!subject.questionCount&&!subject.chapterCount);
      console.log(`${subject.name}: awaiting materials; no invented questions.`);
    }
  }
  await import('./tthcm/validate.mjs');
}
