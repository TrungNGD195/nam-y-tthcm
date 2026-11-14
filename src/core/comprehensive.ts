import { shuffle } from './engine.ts';
import type { Question } from './types.ts';

export type ComprehensivePaper = { id: string; title: string; questionIds: string[]; chapterCounts: {chapter: number; count: number}[] };

function seeded(seed: string): () => number {
  let state=2166136261;
  for(const ch of seed)state=Math.imul(state^ch.charCodeAt(0),16777619);
  return ()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};
}

/** Fixed, reproducible papers; cover every published question with balanced chapter quotas. */
export function buildComprehensivePapers(questions: Question[], size: number, seed: string): ComprehensivePaper[] {
  if(!Number.isSafeInteger(size)||size<1||questions.length<size)throw new Error('Không đủ câu để lập bộ đề.');
  const chapters=[...new Set(questions.map(q=>q.chapter))].sort((a,b)=>a-b);
  const base=Math.floor(size/chapters.length),remainder=size%chapters.length;
  if(!base||new Set(questions.map(q=>q.id)).size!==questions.length)throw new Error('Dữ liệu chia đề không hợp lệ.');
  const buckets=chapters.map(ch=>shuffle(questions.filter(q=>q.chapter===ch).sort((a,b)=>a.id.localeCompare(b.id,'en')),seeded(`${seed}:chapter:${ch}`)));
  if(buckets.some(b=>b.length<base+(remainder?1:0)))throw new Error('Một chương chưa đủ câu để chia đều mà không lặp trong đề.');
  let count=Math.ceil(questions.length/size);
  // A chapter can receive at most one extra slot per paper, beyond its base quota.
  while(buckets.some(b=>b.length>count*(base+(remainder?1:0)))||buckets.reduce((n,b)=>n+Math.max(0,b.length-count*base),0)>count*remainder)count++;
  const extras=buckets.map(b=>Math.max(0,b.length-count*base));
  for(let left=count*remainder-extras.reduce((a,b)=>a+b,0);left>0;left--){
    const least=extras.map((n,i)=>({n,i})).filter(x=>x.n<count).sort((a,b)=>a.n-b.n||a.i-b.i)[0];
    extras[least.i]++;
  }
  const cursors=chapters.map(()=>0),papers:ComprehensivePaper[]=[];
  for(let index=0;index<count;index++){
    const extraChapters=new Set(extras.map((n,i)=>({n,i})).sort((a,b)=>b.n-a.n||((a.i-index+chapters.length*count)%chapters.length)-((b.i-index+chapters.length*count)%chapters.length)).slice(0,remainder).map(x=>x.i));
    const ids:string[]=[],chapterCounts:ComprehensivePaper['chapterCounts']=[];
    for(let i=0;i<chapters.length;i++){
      const quota=base+(extraChapters.has(i)?1:0);
      if(extraChapters.has(i))extras[i]--;
      chapterCounts.push({chapter:chapters[i],count:quota});
      for(let j=0;j<quota;j++)ids.push(buckets[i][cursors[i]++%buckets[i].length].id);
    }
    const id=String(index+1).padStart(2,'0');
    papers.push({id,title:`Đề tổng hợp ${id} · ${size} câu`,questionIds:shuffle(ids,seeded(`${seed}:paper:${id}`)),chapterCounts});
  }
  if(extras.some(n=>n!==0)||new Set(papers.flatMap(p=>p.questionIds)).size!==questions.length)throw new Error('Chia đề chưa bao phủ đủ ngân hàng.');
  return papers;
}
