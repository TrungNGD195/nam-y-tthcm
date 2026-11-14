import assert from 'node:assert/strict';
import katex from 'katex';

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
    if(item.area==='bank')assert([1,2,3,4].includes(item.points));
    for(const step of item.steps) {
      assert(step.lead&&step.lead.length>8);
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
}
