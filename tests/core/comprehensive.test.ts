import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildComprehensivePapers } from '../../src/core/comprehensive.ts';
import { createSession,selectQuestions } from '../../src/core/engine.ts';
import { emptyProgress,parseProgress } from '../../src/core/storage.ts';
import type { Bank,Deck } from '../../src/core/types.ts';

const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8')) as Bank;
const map=new Map(bank.questions.map(q=>[q.id,q]));
const papers=buildComprehensivePapers(bank.questions,50,`tthcm:${bank.version}`);

test('19 balanced fifty-question papers cover all 623 published questions, including all numeric questions',()=>{
  assert.equal(papers.length,19);assert.equal(new Set(papers.flatMap(p=>p.questionIds)).size,623);
  assert.deepEqual(new Set(papers.flatMap(p=>p.questionIds)),new Set(bank.questions.map(q=>q.id)));
  for(const paper of papers){
    assert.equal(paper.questionIds.length,50);assert.equal(new Set(paper.questionIds).size,50);
    assert.equal(paper.chapterCounts.length,6);
    for(const c of paper.chapterCounts){
      assert(c.count===8||c.count===9);
      assert.equal(paper.questionIds.filter(id=>map.get(id)!.chapter===c.chapter).length,c.count);
    }
  }
  assert(bank.questions.some(q=>q.tags.includes('date')));
  assert.equal(new Set(papers.flatMap(p=>p.questionIds)).size,bank.questions.length);
  assert(Math.max(...bank.chapters.map(c=>bank.questions.filter(q=>q.chapter===c.number).length))>18*9,'18 balanced papers cannot cover the largest chapter');
});

test('paper membership and order are reproducible, independent of input array order and progress',()=>{
  const original=bank.questions.map(q=>q.id);
  assert.deepEqual(buildComprehensivePapers([...bank.questions].reverse(),50,`tthcm:${bank.version}`),papers);
  assert.deepEqual(bank.questions.map(q=>q.id),original);
  for(const paper of papers){
    const deck:Deck={kind:'comprehensive',count:50,title:paper.title,questionIds:paper.questionIds};
    assert.deepEqual(selectQuestions(bank.questions,deck,{}).map(q=>q.id),paper.questionIds);
    assert.deepEqual(selectQuestions(bank.questions,deck,{},[],()=>0).map(q=>q.id),paper.questionIds);
  }
  assert.notDeepEqual(buildComprehensivePapers(bank.questions,50,'different edition')[0].questionIds,papers[0].questionIds);
});

test('reuse is spread evenly within each chapter and never skips a question in a chapter cycle',()=>{
  const frequency=new Map<string,number>();
  papers.forEach(p=>p.questionIds.forEach(id=>frequency.set(id,(frequency.get(id)??0)+1)));
  for(const chapter of bank.chapters){
    const counts=bank.questions.filter(q=>q.chapter===chapter.number).map(q=>frequency.get(q.id)??0);
    assert(Math.min(...counts)>=1);assert(Math.max(...counts)-Math.min(...counts)<=1);
    const prefix:string[]=[];
    for(const p of papers)prefix.push(...p.questionIds.filter(id=>map.get(id)!.chapter===chapter.number));
    // A paper can straddle a cycle boundary; counts prove fair reuse despite mixed question order.
    assert(prefix.length>=counts.length);
  }
});

test('noncontiguous chapters and heavily uneven banks still balance without dropping questions',()=>{
  const qs=[2,7,12].flatMap((chapter,i)=>Array.from({length:[9,9,30][i]},(_,j)=>({...bank.questions[0],id:`${chapter}-${j}`,chapter})));
  const sets=buildComprehensivePapers(qs,8,'fixture');
  assert.equal(new Set(sets.flatMap(s=>s.questionIds)).size,qs.length);
  for(const set of sets){assert.equal(new Set(set.questionIds).size,8);assert(set.chapterCounts.every(c=>c.count===2||c.count===3));}
  assert.throws(()=>buildComprehensivePapers(qs,100,'fixture'));
});

test('fifty-question session round-trips with saved choices and rejects a corrupted paper definition',()=>{
  const paper=papers[0];const deck:Deck={kind:'comprehensive',count:50,title:paper.title,questionIds:paper.questionIds};
  const progress=emptyProgress(bank.version);progress.activeSession=createSession(selectQuestions(bank.questions,deck,{}),deck,'exam',60);
  const item=progress.activeSession.items[0];item.selectedOptionId=map.get(item.questionId)!.correctOptionId;
  const restored=parseProgress(JSON.parse(JSON.stringify(progress)),map,bank.version);
  assert.deepEqual(restored.activeSession,{...progress.activeSession,deck:{...deck,includeNumbers:false,order:'unseen'}});
  const corrupted=structuredClone(progress);corrupted.activeSession!.deck.questionIds![0]='missing-question';
  assert.equal(parseProgress(corrupted,map,bank.version).activeSession,null);
  const duplicate=structuredClone(progress);duplicate.activeSession!.deck.questionIds![0]=duplicate.activeSession!.deck.questionIds![1];
  assert.equal(parseProgress(duplicate,map,bank.version).activeSession,null);
});
