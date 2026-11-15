import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {exerciseHtml,escapeHtml} from '../../scripts/content/xu-ly-anh/document-layout.mjs';

const data=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/solutions.json',import.meta.url),'utf8'));

test('every exercise retains its leads, formulas, substitutions and results in the printable document',()=>{
  for(const item of data.items.filter((i:any)=>i.kind==='exercise')){
    const html=exerciseHtml(item,data.sources,item.images);
    assert.equal((html.match(/data-step=/g)??[]).length,item.steps.length,item.id);
    for(const [n,step] of item.steps.entries()){
      const fragment=html.split(`data-step="${n}"`)[1].split('</section>')[0];
      const lead=fragment.indexOf(escapeHtml(step.lead));assert(lead>=0,item.id);
      if(step.formula){
        const formula=fragment.indexOf('data-tex=');assert(formula>lead,item.id);
        assert(formula<fragment.indexOf('class="substitution"')||!step.substitution,item.id);
        assert(fragment.includes(escapeHtml(step.formula)),item.id);
      }
      if(step.substitution)assert(fragment.includes('class="substitution"'),item.id);
      if(step.result)assert(fragment.includes('class="result"'),item.id);
      assert(!fragment.includes('katex-error'),item.id);
    }
    if(item.note)assert(html.includes(escapeHtml(item.note)),item.id);
  }
});

test('histogram is horizontal and Huffman nodes remain fully defined rather than nested tuple strings',()=>{
  const histogram=data.items.find((i:any)=>i.id==='bank-3-1');
  const h=exerciseHtml(histogram,data.sources,histogram.images);
  assert(h.includes('<th>g</th><td>0</td><td>1</td>'));
  assert(h.includes('h′(4) = h(0) + h(8) = 4 + 1 = 5.'));
  for(const id of ['bank-3-8','bank-3-9','uyen-6-T1','uyen-6-T2']){
    const item=data.items.find((i:any)=>i.id===id),html=exerciseHtml(item,data.sources,item.images);
    const merges=item.steps.flatMap((s:any)=>s.blocks??[]).find((b:any)=>b.headers?.[0]==='cây con trái');
    for(let n=1;n<=merges.rows.length;n++)assert(html.includes(`<td>N${n}</td>`),id);
    assert(!html.includes("(&#39;"),id);
  }
});
