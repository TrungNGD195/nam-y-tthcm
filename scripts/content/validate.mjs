import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
import katex from 'katex';
import { validateSolutions } from './xu-ly-anh/validate.mjs';

export function validateBank(bank, subject, assetExists = () => true) {
  assert.equal(bank.subjectId,subject.id,'Bank belongs to another subject');
  assert(bank.chapters.length>0 && bank.questions.length>0,'Ready subject needs real content');
  const chapters=new Set(bank.chapters.map(c=>c.number));
  assert.equal(chapters.size,bank.chapters.length,'Duplicate chapters');
  assert([...chapters].every(n=>Number.isSafeInteger(n)&&n>0));
  const questions=new Map(bank.questions.map(q=>[q.id,q]));
  const concepts=new Map(bank.concepts.map(c=>[c.id,c]));
  const sources=new Map(bank.sources.map(s=>[s.id,s]));
  assert.equal(sources.size,bank.sources.length,'Duplicate source IDs');
  for(const source of sources.values()){
    if(source.url)assert(/^https:\/\/[^\s"<>]+$/.test(source.url),'Unsafe source URL');
    if(source.locatorLabel)assert(['câu','mục'].includes(source.locatorLabel),'Unknown source locator');
  }
  assert.equal(questions.size,bank.questions.length);assert.equal(concepts.size,bank.concepts.length);
  const aliasIds=new Set();
  for(const alias of bank.questionAliases??[]){
    assert(!questions.has(alias.fromId)&&questions.has(alias.toId)&&!aliasIds.has(alias.fromId),'Invalid duplicate alias');
    assert(Number.isSafeInteger(alias.revision)&&alias.revision>0);aliasIds.add(alias.fromId);
  }
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
    if(q.shufflePolicy==='safe')assert(!q.options.some(o=>/(?<![\p{L}\p{N}_])[ABCD]\s*(đúng|sai)|đáp án trên|ý trên/iu.test(o.text)),`${q.id}: unsafe letter reference`);
    for(const ref of [...q.sources,...q.theoryReferences])assert(sources.has(ref.sourceId)&&Number.isInteger(ref.pdfPage)&&ref.pdfPage>0&&ref.pdfPage<=sources.get(ref.sourceId).pages);
    blocks(q.blocks);blocks(q.explanationBlocks);for(const o of q.options)blocks(o.blocks);
  }
  if(bank.lessons){
    assert(typeof bank.lessons.version==='string'&&bank.lessons.version);
    assert.equal(bank.lessons.chapters.length,chapters.size,'Lessons must cover all chapters');
    const lessonChapters=new Set(),sectionIds=new Set(),assignments=new Set();
    const refsValid=refs=>Array.isArray(refs)&&refs.length>0&&refs.every(r=>sources.has(r.sourceId)&&Number.isInteger(r.pdfPage)&&r.pdfPage>0&&r.pdfPage<=sources.get(r.sourceId).pages&&r.section&&r.evidence);
    for(const lesson of bank.lessons.chapters){
      assert(chapters.has(lesson.chapter)&&!lessonChapters.has(lesson.chapter),'Invalid lesson chapter');lessonChapters.add(lesson.chapter);
      assert(lesson.sections.length>0);
      for(const section of lesson.sections){
        assert(/^[a-z0-9-]+$/.test(section.id)&&!sectionIds.has(section.id),'Invalid lesson section ID');sectionIds.add(section.id);
        assert(section.title&&section.summary.length>30&&['knowledge','milestones'].includes(section.kind));
        assert(refsValid(section.references),'Lesson overview needs valid evidence');
        assert(section.conceptIds.length>0);
        for(const id of section.conceptIds){
          const c=concepts.get(id),assignment=`${lesson.chapter}:${id}`;
          assert(c&&!assignments.has(assignment),'Duplicate or unknown lesson concept');assignments.add(assignment);
          assert(bank.questions.some(q=>q.chapter===lesson.chapter&&q.conceptId===id),'Lesson concept must correspond to questions in this chapter');
          assert(c.summary.length>20&&c.keywords.length&&refsValid(c.references),'Lesson concept needs content and evidence');
          for(const p of c.learningPoints??[])assert(p.title&&p.text.length>15&&p.keywords.length&&p.keywords.every(k=>typeof k==='string'&&k),'Invalid learning point');
        }
      }
    }
    for(const q of bank.questions)assert(assignments.has(`${q.chapter}:${q.conceptId}`),`Question missing chapter lesson: ${q.id}`);
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
    if(subject.learningMode==='solutions'){
      assert.equal(subject.status,'ready');
      const data=JSON.parse(readFileSync(new URL(`src/subjects/${subject.id}/solutions.json`,root),'utf8'));
      if(subject.solutionPresentation==='documents')data.documents=JSON.parse(readFileSync(new URL(`src/subjects/${subject.id}/documents.json`,root),'utf8'));
      validateSolutions(data,subject,asset=>existsSync(new URL('public/'+asset,root)));
      console.log(`${subject.name}: ${data.items.length} solved items, ${data.chapters.length} chapter groups.`);
      continue;
    }
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
