import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { checkCurrent, createSession, finishSession, needsReview, normalize, scoreSession, selectQuestions, toggleBookmark } from '../src/engine.ts';
import { emptyProgress, parseProgress } from '../src/storage.ts';
import type { Bank, Deck, Question } from '../src/types.ts';

const bank = JSON.parse(readFileSync(new URL('../src/data/bank.json', import.meta.url), 'utf8')) as Bank;
const qmap = new Map(bank.questions.map(q => [q.id, q]));
const deck: Deck = { kind:'chapter', chapter:2, count:10, title:'Chương 2', order:'unseen' };
const q = bank.questions.find(q => q.chapter === 2 && q.shufflePolicy === 'safe')!;

test('shuffled option positions grade by ID, once, including after reload', () => {
  let p = emptyProgress(bank.version);
  p.activeSession = createSession([q],deck,'practice',0,1000,()=>0);
  assert.notDeepEqual(p.activeSession.items[0].optionOrder,q.options.map(o=>o.id));
  p.activeSession.items[0].selectedOptionId=q.correctOptionId;
  p=checkCurrent(p,qmap,false,2000);
  assert.equal(p.records[q.id].correct,1);
  p=parseProgress(JSON.parse(JSON.stringify(p)),qmap,bank.version);
  p=checkCurrent(p,qmap,false,3000);
  p=finishSession(p,qmap,4000);
  p=finishSession(p,qmap,5000);
  assert.equal(p.records[q.id].seen,1);
  assert.equal(p.history.length,1);
  assert.equal(scoreSession(p.lastResult!,qmap).correct,1);
});

test('hinted correct answer needs review; later independent answer clears it', () => {
  let p=emptyProgress(bank.version);
  p.activeSession=createSession([q],deck,'practice');
  p.activeSession.items[0].usedHint=true;
  p.activeSession.items[0].selectedOptionId=q.correctOptionId;
  p=checkCurrent(p,qmap);
  assert.equal(p.records[q.id].correct,0);
  assert(needsReview(p.records[q.id]));
  p=finishSession(p,qmap);
  p.activeSession=createSession([q],deck,'practice');
  p.activeSession.items[0].selectedOptionId=q.correctOptionId;
  p=checkCurrent(p,qmap);
  assert(!needsReview(p.records[q.id]));
  p=toggleBookmark(p,q);
  assert(needsReview(p.records[q.id]));
});

test('skip is recorded once, including an unfinished session submission', () => {
  let p=emptyProgress(bank.version);
  p.activeSession=createSession([q],deck,'practice');
  p=checkCurrent(p,qmap,true);
  assert.equal(p.records[q.id].lastOutcome,'skipped');
  p=finishSession(p,qmap);
  assert.equal(p.records[q.id].seen,1);
  assert.equal(scoreSession(p.lastResult!,qmap).skipped,1);
});

test('practice cannot grade empty answers without explicit skip; exam cannot grade before submit', () => {
  let p=emptyProgress(bank.version);
  p.activeSession=createSession([q],deck,'practice');
  p=checkCurrent(p,qmap);
  assert.equal(Object.keys(p.records).length,0);
  p.activeSession=createSession([q],deck,'exam',15,1000);
  p.activeSession.items[0].selectedOptionId=q.correctOptionId;
  p=checkCurrent(p,qmap);
  assert.equal(Object.keys(p.records).length,0);
  assert.equal(p.activeSession!.deadline,901000);
  p=finishSession(p,qmap);
  assert.equal(p.records[q.id].correct,1);
});

test('mixed 20-question exam covers six chapters without duplicates', () => {
  const qs=selectQuestions(bank.questions,{kind:'mixed',count:20,title:'Đề trộn'},{});
  assert.equal(qs.length,20);
  assert.equal(new Set(qs.map(q=>q.id)).size,20);
  assert.equal(new Set(qs.map(q=>q.chapter)).size,6);
  assert(qs.some(q=>q.tags.length),'Mixed exam must contain number questions');
  const distribution=Array.from({length:6},(_,i)=>qs.filter(q=>q.chapter===i+1).length);
  assert(Math.max(...distribution)-Math.min(...distribution)<=1);
});

test('chapter defaults exclude number questions; number filters contain requested tags', () => {
  const qs=selectQuestions(bank.questions,{...deck,count:9999},{});
  assert(qs.every(q=>q.chapter===2&&!q.tags.length));
  const dates=selectQuestions(bank.questions,{kind:'numbers',tag:'date',count:9999,title:'Mốc'},{});
  assert(dates.length>0&&dates.every(q=>q.tags.includes('date')));
  const all=selectQuestions(bank.questions,{...deck,count:9999,includeNumbers:true},{});
  assert(all.length>qs.length);
});

test('source sample keeps its exact 20-item sequence and fixed questions keep option order', () => {
  const qs=selectQuestions(bank.questions,{kind:'sample',count:20,title:'Mẫu'}, {},bank.sampleQuestionIds);
  assert.deepEqual(qs.map(q=>q.id),bank.sampleQuestionIds);
  const fixed={...q,shufflePolicy:'fixed'} as Question;
  assert.deepEqual(createSession([fixed],deck,'practice').items[0].optionOrder,q.options.map(o=>o.id));
});

test('unseen-first selection avoids seen questions while sufficient unseen candidates remain', () => {
  const candidates=bank.questions.filter(q=>q.chapter===2&&!q.tags.length);
  const p=emptyProgress(bank.version);
  p.activeSession=createSession([candidates[0]],deck,'practice');
  const seen=checkCurrent(p,qmap,true);
  const selected=selectQuestions(bank.questions,{...deck,count:3},seen.records);
  assert(!selected.some(q=>q.id===candidates[0].id));
});

test('corrupt imports, duplicated option orders and stale revisions cannot resume', () => {
  assert.throws(()=>parseProgress({},qmap,bank.version));
  const p=emptyProgress(bank.version);
  p.activeSession=createSession([q],deck,'practice',0,1000);
  const corrupt=structuredClone(p);
  corrupt.activeSession!.items[0].optionOrder.fill(q.options[0].id);
  assert.equal(parseProgress(corrupt,qmap,bank.version).activeSession,null);
  p.activeSession.items[0].revision++;
  assert.equal(parseProgress(p,qmap,bank.version).activeSession,null);
});

test('Vietnamese search matches diacritics, đ and uppercase', () => {
  assert.equal(normalize('ĐẠI đoàn kết'),'dai doan ket');
});

test('retrying a result subset retains the exact original IDs even after later answers clear review state', () => {
  const ids=bank.questions.slice(0,3).map(q=>q.id);
  const selected=selectQuestions(bank.questions,{kind:'review',count:3,title:'Ôn lại',questionIds:ids},{});
  assert.deepEqual(selected.map(q=>q.id).sort(),ids.sort());
  const p=emptyProgress(bank.version);
  p.activeSession=createSession(selected,{kind:'review',count:3,title:'Ôn lại',questionIds:ids},'practice');
  assert.deepEqual(parseProgress(p,qmap,bank.version).activeSession?.deck.questionIds,ids);
});
