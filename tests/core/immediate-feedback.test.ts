import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {checkCurrent,createSession,enableImmediateExamFeedback,finishSession} from '../../src/core/engine.ts';
import {emptyProgress,parseProgress} from '../../src/core/storage.ts';
import type {Bank,Deck} from '../../src/core/types.ts';
const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8')) as Bank;
const qs=bank.questions.slice(0,3),qmap=new Map(bank.questions.map(q=>[q.id,q]));
const deck:Deck={kind:'mixed',title:'Đề ôn',count:3};

test('immediate exam grades by option ID, survives reload, and never counts again on submit',()=>{
  let p=emptyProgress(bank.version);p.activeSession=createSession(qs,deck,'exam',15,1000);
  p=enableImmediateExamFeedback(p,qmap,1000);
  p.activeSession!.items[0].selectedOptionId=qs[0].options.find(o=>o.id!==qs[0].correctOptionId)!.id;
  p=checkCurrent(p,qmap,false,2000);
  assert.equal(p.records[qs[0].id].lastOutcome,'incorrect');assert.equal(p.records[qs[0].id].seen,1);
  p=parseProgress(JSON.parse(JSON.stringify(p)),qmap,bank.version);
  assert.equal(p.activeSession!.examFeedback,'immediate');assert(p.activeSession!.items[0].checked);
  assert.equal(p.activeSession!.deadline,901000);
  p=checkCurrent(p,qmap,false,3000);assert.equal(p.records[qs[0].id].seen,1);
  p.activeSession!.cursor=1;p.activeSession!.items[1].selectedOptionId=qs[1].correctOptionId;
  p=checkCurrent(p,qmap,false,4000);assert.equal(p.records[qs[1].id].lastOutcome,'correct');
  p=finishSession(p,qmap,5000);
  assert.equal(p.records[qs[0].id].seen,1);assert.equal(p.records[qs[1].id].seen,1);
  assert.equal(p.records[qs[2].id].lastOutcome,'skipped');assert.equal(p.history[0].correct,1);
  assert.equal(parseProgress(p,qmap,bank.version).lastResult!.examFeedback,'immediate');
});

test('legacy exam keeps its choices, position, paper and original deadline when feedback is enabled',()=>{
  let p=emptyProgress(bank.version);p.activeSession=createSession(qs,deck,'exam',20,1000);
  p.activeSession.cursor=2;p.activeSession.items[0].selectedOptionId=qs[0].correctOptionId;
  const before=structuredClone(p.activeSession);
  p=enableImmediateExamFeedback(p,qmap,2000);
  assert.equal(p.activeSession!.cursor,before.cursor);assert.equal(p.activeSession!.id,before.id);
  assert.deepEqual(p.activeSession!.deck,before.deck);assert.equal(p.activeSession!.deadline,before.deadline);
  assert.deepEqual(p.activeSession!.items.map(i=>i.optionOrder),before.items.map(i=>i.optionOrder));
  assert(p.activeSession!.items[0].checked);assert(!p.activeSession!.items[1].checked);
  p=enableImmediateExamFeedback(p,qmap,3000);assert.equal(p.records[qs[0].id].seen,1);
});

test('exams without the immediate policy still hide answers and reject premature grading',()=>{
  const p=emptyProgress(bank.version);p.activeSession=createSession(qs,deck,'exam');
  p.activeSession.items[0].selectedOptionId=qs[0].correctOptionId;
  assert.deepEqual(checkCurrent(p,qmap).records,{});
  const bad=structuredClone(p);bad.activeSession!.items[0].checked=true;bad.activeSession!.items[0].recorded=true;
  assert.equal(parseProgress(bad,qmap,bank.version).activeSession,null);
  const invalid=structuredClone(p) as any;invalid.activeSession.examFeedback='anything';
  assert.equal(parseProgress(invalid,qmap,bank.version).activeSession,null);
});
