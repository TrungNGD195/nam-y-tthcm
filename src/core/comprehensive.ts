import { shuffle } from './engine.ts';
import type { Question } from './types.ts';

export type ComprehensivePaper = { id: string; key: string; title: string; questionIds: string[]; chapterCounts: {chapter: number; count: number}[] };

function seeded(seed: string): () => number {
  let state=2166136261;
  for(const ch of seed)state=Math.imul(state^ch.charCodeAt(0),16777619);
  return ()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};
}

/** Every question appears once; distribute each chapter evenly over full papers and keep the tail short. */
export function buildComprehensivePapers(questions: Question[], size: number, seed: string): ComprehensivePaper[] {
  if(!Number.isSafeInteger(size)||size<1||!questions.length||new Set(questions.map(q=>q.id)).size!==questions.length)throw new Error('Dữ liệu chia đề không hợp lệ.');
  const chapters=[...new Set(questions.map(q=>q.chapter))].sort((a,b)=>a-b);
  const buckets=chapters.map(ch=>shuffle(questions.filter(q=>q.chapter===ch).sort((a,b)=>a.id.localeCompare(b.id,'en')),seeded(`${seed}:chapter:${ch}`)));
  const fullCount=Math.floor(questions.length/size),tailSize=questions.length%size;
  const tail=chapters.map(()=>0);
  if(tailSize){
    if(tailSize>=chapters.length)tail.fill(1);
    for(let left=tailSize-tail.reduce((a,b)=>a+b,0);left>0;left--){
      const best=buckets.map((bucket,i)=>({i,deficit:bucket.length*tailSize/questions.length-tail[i]}))
        .filter(x=>tail[x.i]<buckets[x.i].length).sort((a,b)=>b.deficit-a.deficit||a.i-b.i)[0];
      tail[best.i]++;
    }
  }
  const base=buckets.map((bucket,i)=>fullCount?Math.floor((bucket.length-tail[i])/fullCount):0);
  const extras=buckets.map((bucket,i)=>fullCount?(bucket.length-tail[i])%fullCount:0);
  const extraPerPaper=fullCount?size-base.reduce((a,b)=>a+b,0):0;
  const cursors=chapters.map(()=>0),papers:ComprehensivePaper[]=[];
  function append(quotas:number[]):void {
    const ids:string[]=[],chapterCounts:ComprehensivePaper['chapterCounts']=[];
    for(let i=0;i<chapters.length;i++){
      chapterCounts.push({chapter:chapters[i],count:quotas[i]});
      for(let j=0;j<quotas[i];j++)ids.push(buckets[i][cursors[i]++].id);
    }
    const id=String(papers.length+1).padStart(2,'0');
    papers.push({id,key:`no-repeat:${seed}:${id}`,title:`Đề tổng hợp ${id} · ${ids.length} câu`,questionIds:shuffle(ids,seeded(`${seed}:paper:${id}`)),chapterCounts});
  }
  for(let index=0;index<fullCount;index++){
    const extraChapters=new Set(extras.map((n,i)=>({n,i})).sort((a,b)=>b.n-a.n||((a.i-index+chapters.length*fullCount)%chapters.length)-((b.i-index+chapters.length*fullCount)%chapters.length)).slice(0,extraPerPaper).map(x=>x.i));
    append(base.map((n,i)=>n+(extraChapters.has(i)?1:0)));
    for(const i of extraChapters)extras[i]--;
  }
  if(tailSize)append(tail);
  if(papers.flatMap(p=>p.questionIds).length!==questions.length||new Set(papers.flatMap(p=>p.questionIds)).size!==questions.length)throw new Error('Chia đề chưa bao phủ duy nhất mỗi câu.');
  return papers;
}
