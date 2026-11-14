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

test('ten full papers and a six-question tail cover every published question exactly once',()=>{
  assert.equal(papers.length,11);assert.equal(new Set(papers.flatMap(p=>p.questionIds)).size,506);
  assert.equal(papers.flatMap(p=>p.questionIds).length,506);
  assert.deepEqual(papers.map(p=>p.questionIds.length),[50,50,50,50,50,50,50,50,50,50,6]);
  assert.deepEqual(new Set(papers.flatMap(p=>p.questionIds)),new Set(bank.questions.map(q=>q.id)));
  for(const paper of papers){
    assert.equal(new Set(paper.questionIds).size,paper.questionIds.length);
    assert.equal(paper.chapterCounts.length,6);
    for(const c of paper.chapterCounts){
      assert.equal(paper.questionIds.filter(id=>map.get(id)!.chapter===c.chapter).length,c.count);
    }
  }
  assert(bank.questions.some(q=>q.tags.includes('date')));
  assert.equal(new Set(papers.flatMap(p=>p.questionIds)).size,bank.questions.length);
  assert(papers.at(-1)!.chapterCounts.every(c=>c.count===1));
});

test('paper membership and order are reproducible, independent of input array order and progress',()=>{
  const original=bank.questions.map(q=>q.id);
  assert.deepEqual(buildComprehensivePapers([...bank.questions].reverse(),50,`tthcm:${bank.version}`),papers);
  assert.deepEqual(bank.questions.map(q=>q.id),original);
  for(const paper of papers){
    const deck:Deck={kind:'comprehensive',count:paper.questionIds.length,title:paper.title,questionIds:paper.questionIds,paperKey:paper.key};
    assert.deepEqual(selectQuestions(bank.questions,deck,{}).map(q=>q.id),paper.questionIds);
    assert.deepEqual(selectQuestions(bank.questions,deck,{},[],()=>0).map(q=>q.id),paper.questionIds);
  }
  assert.notDeepEqual(buildComprehensivePapers(bank.questions,50,'different edition')[0].questionIds,papers[0].questionIds);
});

test('each chapter is spread evenly over full papers without any reuse',()=>{
  const frequency=new Map<string,number>();
  papers.forEach(p=>p.questionIds.forEach(id=>frequency.set(id,(frequency.get(id)??0)+1)));
  for(const chapter of bank.chapters){
    const counts=bank.questions.filter(q=>q.chapter===chapter.number).map(q=>frequency.get(q.id)??0);
    assert(counts.every(n=>n===1));
    const quotas=papers.filter(p=>p.questionIds.length===50).map(p=>p.chapterCounts.find(c=>c.chapter===chapter.number)!.count);
    assert(Math.max(...quotas)-Math.min(...quotas)<=1);
  }
});

test('noncontiguous chapters, exact multiples and tiny banks retain every question without padding',()=>{
  const qs=[2,7,12].flatMap((chapter,i)=>Array.from({length:[9,9,30][i]},(_,j)=>({...bank.questions[0],id:`${chapter}-${j}`,chapter})));
  const sets=buildComprehensivePapers(qs,8,'fixture');
  assert.equal(new Set(sets.flatMap(s=>s.questionIds)).size,qs.length);
  assert.equal(sets.flatMap(s=>s.questionIds).length,qs.length);
  for(const set of sets)assert.equal(new Set(set.questionIds).size,8);
  assert.deepEqual(buildComprehensivePapers(qs.slice(0,2),50,'tiny').map(p=>p.questionIds.length),[2]);
  assert.throws(()=>buildComprehensivePapers(qs,0,'fixture'));
});

test('fifty-question session round-trips with saved choices and rejects a corrupted paper definition',()=>{
  const paper=papers[0];const deck:Deck={kind:'comprehensive',count:50,title:paper.title,questionIds:paper.questionIds,paperKey:paper.key};
  const progress=emptyProgress(bank.version);progress.activeSession=createSession(selectQuestions(bank.questions,deck,{}),deck,'exam',60);
  const item=progress.activeSession.items[0];item.selectedOptionId=map.get(item.questionId)!.correctOptionId;
  const restored=parseProgress(JSON.parse(JSON.stringify(progress)),map,bank.version);
  assert.deepEqual(restored.activeSession,{...progress.activeSession,deck:{...deck,includeNumbers:false,order:'unseen'}});
  const corrupted=structuredClone(progress);corrupted.activeSession!.deck.questionIds![0]='missing-question';
  assert.equal(parseProgress(corrupted,map,bank.version).activeSession,null);
  const duplicate=structuredClone(progress);duplicate.activeSession!.deck.questionIds![0]=duplicate.activeSession!.deck.questionIds![1];
  assert.equal(parseProgress(duplicate,map,bank.version).activeSession,null);
});

test('reviewed duplicate merges keep sources, distinguish similar questions, and migrate progress once',()=>{
  const decisions=JSON.parse(readFileSync(new URL('../../content/tthcm/duplicate-decisions.json',import.meta.url),'utf8'));
  assert.equal(bank.questions.length,506);assert.equal(bank.questionAliases!.length,117);
  for(const group of decisions.groups){
    assert(map.has(group.keep));
    for(const id of group.remove){assert(!map.has(id));assert(bank.audit.some(a=>a.questionId===group.keep&&a.status==='merged'));}
  }
  for(const id of ['lms-g2-11','lms-g2-12','lms-g2-13','lms-g6-02','lms-g6-03','lms-g6-04'])assert(map.has(id));
  const alias=bank.questionAliases![0],canonical=map.get(alias.toId)!;
  const p=emptyProgress('old');
  p.records[alias.fromId]={revision:alias.revision,seen:2,correct:1,incorrect:1,lastOutcome:'incorrect',lastAt:10,bookmarked:true};
  p.records[alias.toId]={revision:canonical.revision,seen:3,correct:3,incorrect:0,lastOutcome:'correct',lastAt:20,bookmarked:false};
  const restored=parseProgress(p,map,bank.version,'tthcm',bank.questionAliases);
  assert.equal(Object.keys(restored.records).length,1);assert.equal(restored.records[alias.toId].seen,3);
  assert.equal(restored.records[alias.toId].lastOutcome,'correct');assert(restored.records[alias.toId].bookmarked);
  assert.deepEqual(parseProgress(restored,map,bank.version,'tthcm',bank.questionAliases).records,restored.records);
});
