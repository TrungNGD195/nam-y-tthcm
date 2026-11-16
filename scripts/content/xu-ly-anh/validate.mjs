import assert from 'node:assert/strict';
import katex from 'katex';
import {createHash} from 'node:crypto';
import {canonical} from './document-layout.mjs';

export function validateSolutions(data, subject, assetExists=()=>true) {
  assert.equal(data.subjectId,subject.id);
  assert.equal(data.items.length,subject.questionCount);
  assert.equal(data.chapters.length,subject.chapterCount);
  const ids=new Set(), chapters=new Set(data.chapters.map(c=>c.number)), sources=new Map(data.sources.map(s=>[s.id,s]));
  assert.equal(sources.size,data.sources.length);
  const asset=src=>{assert(/^subjects\/[a-z0-9-]+\/[a-zA-Z0-9_./-]+$/.test(src)&&src.startsWith(`subjects/${subject.id}/`)&&!src.split('/').includes('..'));assert(assetExists(src),`Missing image ${src}`);};
  for(const item of data.items) {
    assert(!ids.has(item.id));ids.add(item.id);
    assert(item.revision>0&&Number.isInteger(item.revision));assert(chapters.has(item.chapter));
    assert(['bank','uyen'].includes(item.area)&&['theory','exercise'].includes(item.kind));
    assert(item.title.length>5&&item.prompt.length>15&&item.keywords.length>0&&item.steps.length>0);
    assert(item.sourcePages.length>0&&item.references.length>1);
    for(const page of item.sourcePages)assert(item.references.some(r=>r.sourceId===item.sourceId&&r.pdfPage===page));
    for(const ref of item.references)assert(sources.has(ref.sourceId)&&Number.isInteger(ref.pdfPage)&&ref.pdfPage>0&&ref.pdfPage<=sources.get(ref.sourceId).pages&&ref.section.length>5);
    item.images.forEach(asset);
    if(item.kind==='exercise')assert(item.images.length>0&&item.steps.some(s=>s.formula&&s.substitution),`${item.id}: calculation requires original prompt, formula and substitution`);
    if(item.kind==='theory'){
      assert.equal(item.answerStyle,'complete',`${item.id}: theory requires a complete answer`);
      assert(['checked-key','course-theory'].includes(item.answerBasis));
      if(item.answerBasis==='checked-key')assert(item.references.some(r=>r.sourceId==='key'));
    }
    if(item.area==='bank')assert([1,2,3,4].includes(item.points));
    for(const step of item.steps) {
      assert(step.lead&&step.lead.trim().length>=(item.kind==='theory'?3:9));
      if(item.kind==='theory'){
        assert(typeof step.text==='string'&&step.text.length>35,`${item.id}: theory section needs an actual response`);
        assert(!/ý chính cần trình bày|khi hỏi.*nhấn mạnh|nhắc ba dạng/iu.test(step.lead+' '+step.text),`${item.id}: outline instructions leaked into answer`);
      }
      if(item.kind==='exercise'){
        assert(typeof step.section==='string'&&step.section.length>5,`${item.id}: missing source subpart heading`);
        assert(typeof step.method==='string'&&step.method.length>20,`${item.id}: missing explanation of the procedure`);
        if(step.formula)assert(typeof step.symbols==='string'&&step.symbols.length>25,`${item.id}: formula needs local symbol definitions`);
      }
      if(step.formula)katex.renderToString(step.formula,{throwOnError:true,trust:false});
      for(const block of step.blocks??[]) {
        if(block.type==='image')asset(block.src);
        else if(block.type==='formula')katex.renderToString(block.tex,{throwOnError:true,trust:false});
        else if(block.type==='table'||block.type==='matrix') {
          assert(block.rows.length>0,`${item.id}: empty matrix`);
          const width=block.type==='table'?block.headers.length:block.rows[0].length;
          assert(width>0&&block.rows.every(r=>r.length===width&&r.every(x=>typeof x==='string'||(typeof x==='number'&&Number.isFinite(x)))),`${item.id}: invalid table`);
        }else assert(block.type==='code');
      }
    }
  }
  assert.equal(data.coverage.bank,data.items.filter(i=>i.area==='bank').length);
  assert.equal(data.coverage.uyen,data.items.filter(i=>i.area==='uyen').length);
  assert.equal(data.coverage.exercises,data.items.filter(i=>i.kind==='exercise').length);
  assert.equal(data.coverage.theory,data.items.filter(i=>i.kind==='theory').length);
  for(const p of [1,2,3,4])assert.equal(data.coverage.bankPoints[p],data.items.filter(i=>i.area==='bank'&&i.points===p).length);
  if(subject.solutionPresentation==='documents')validateDocuments(data,assetExists);
}

export function validateDocuments(data,assetExists=()=>true){
  const docs=data.documents;
  // The document's dataVersion records its provenance. Per-exercise contentHash
  // below detects stale PDFs, without invalidating them after theory-only edits.
  assert(docs&&docs.subjectId===data.subjectId,'Missing exercise documents');
  const asset=(src,extension)=>assert(typeof src==='string'&&new RegExp(`^subjects/${data.subjectId}/answer-pages/[a-zA-Z0-9.-]+\\.${extension}$`).test(src)&&assetExists(src),`Missing or unsafe document asset: ${src}`);
  asset(docs.book.src,'pdf');assert(Number.isInteger(docs.book.pages)&&docs.book.pages>0);
  assert(/^[a-f0-9]{64}$/.test(docs.book.sha256));
  const exercises=data.items.filter(i=>i.kind==='exercise');
  assert.deepEqual(Object.keys(docs.items).sort(),exercises.map(i=>i.id).sort(),'Every exercise needs a rendered PDF solution');
  const seenPages=new Set(),seenImages=new Set();
  for(const item of exercises){
    const doc=docs.items[item.id];
    assert.equal(doc.contentHash,createHash('sha256').update(JSON.stringify(canonical(item))).digest('hex'),`${item.id}: PDF solution is stale; rerender after changing content`);
    assert([doc.pdfStartPage,doc.pdfEndPage,doc.answerStartPage].every(n=>Number.isInteger(n)&&n>0&&n<=docs.book.pages));
    assert(doc.pdfStartPage<doc.answerStartPage&&doc.answerStartPage<=doc.pdfEndPage);
    assert.equal(doc.pages.length,doc.pdfEndPage-doc.answerStartPage+1,'Missing screenshot page');
    asset(doc.textSrc,'txt');
    assert.deepEqual(doc.parts?.map(p=>p.title),[...new Set(item.steps.map(s=>s.section))],`${item.id}: PDF subparts mismatch`);
    for(const part of doc.parts){
      assert(Number.isInteger(part.pdfPage)&&part.pdfPage>=doc.answerStartPage&&part.pdfPage<=doc.pdfEndPage,`${item.id}: subpart page outside answer`);
      assert(typeof part.top==='number'&&part.top>=0&&part.top<1,`${item.id}: invalid subpart location`);
    }
    for(const [index,page] of doc.pages.entries()){
      asset(page.src,'png');assert(!seenImages.has(page.src),'Reused exercise screenshot');seenImages.add(page.src);
      assert.equal(page.pdfPage,doc.answerStartPage+index,'PDF screenshot pages out of order');
      assert(!seenPages.has(page.pdfPage),'PDF screenshot belongs to two exercises');seenPages.add(page.pdfPage);
      assert(Number.isInteger(page.width)&&page.width>=1200&&Number.isInteger(page.height)&&page.height>page.width);
      assert(/^[a-f0-9]{64}$/.test(page.sha256));
    }
  }
}
