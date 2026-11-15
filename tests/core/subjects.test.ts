import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createSession, selectQuestions } from '../../src/core/engine.ts';
import { emptyProgress, loadProgress, parseProgress, saveProgress, storageKey, LEGACY_STORAGE_KEY } from '../../src/core/storage.ts';
import { legacyRedirect, resolveRoute, subjectHref, scopeSubjectLinks } from '../../src/app/router.ts';
import { renderBlocks } from '../../src/shared/ui.ts';
import { validateBank } from '../../scripts/content/validate.mjs';
import type { Bank, Question } from '../../src/core/types.ts';

const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8')) as Bank;
const qmap=new Map(bank.questions.map(q=>[q.id,q]));
function storage(){const values=new Map<string,string>();Object.defineProperty(globalThis,'localStorage',{configurable:true,value:{getItem:(k:string)=>values.get(k)??null,setItem:(k:string,v:string)=>{values.set(k,v);}}});return values;}

test('legacy progress migrates once and keeps both the original and active session',()=>{
  const values=storage();const old=emptyProgress(bank.version);
  old.activeSession=createSession([bank.questions[0]],{kind:'chapter',chapter:1,count:1,title:'Chương 1'},'practice');
  const raw={...old,schemaVersion:1,subjectId:undefined};values.set(LEGACY_STORAGE_KEY,JSON.stringify(raw));
  const migrated=loadProgress(qmap,bank.version,'tthcm').progress;
  assert.equal(migrated.schemaVersion,2);assert.equal(migrated.subjectId,'tthcm');
  assert.deepEqual(migrated.activeSession?.items,old.activeSession.items);
  assert(values.has(storageKey('tthcm'))&&values.has(LEGACY_STORAGE_KEY));
  migrated.activeSession!.cursor=0;migrated.activeSession!.items[0].usedHint=true;saveProgress(migrated);
  assert(loadProgress(qmap,bank.version,'tthcm').progress.activeSession!.items[0].usedHint);
});

test('subjects store independently even with overlapping question IDs; wrong-subject imports reject',()=>{
  const values=storage();const a=emptyProgress('v1','tthcm'),b=emptyProgress('v1','xu-ly-anh');
  a.history=[{id:'a',title:'TTHCM',at:1,total:1,correct:1,assisted:0,mode:'practice'}];
  saveProgress(a);saveProgress(b);assert.equal(values.size,2);
  assert.equal(loadProgress(qmap,'v1','tthcm').progress.history.length,1);
  assert.equal(loadProgress(qmap,'v1','xu-ly-anh').progress.history.length,0);
  assert.throws(()=>parseProgress(a,qmap,'v1','xu-ly-anh'),/môn khác/);
  assert.throws(()=>parseProgress({...a,schemaVersion:1},qmap,'v1','xu-ly-anh'),/môn khác/);
});

test('engine and stored session accept chapter 7 and noncontiguous chapter numbers',()=>{
  const qs=[1,7,12].map(n=>({...bank.questions[0],id:'q'+n,chapter:n,conceptId:'c'+n,tags:[]} as Question));
  assert.equal(selectQuestions(qs,{kind:'mixed',count:3,title:'Thử'},{}).length,3);
  const p=emptyProgress('v1','fixture');p.activeSession=createSession([qs[1]],{kind:'chapter',chapter:7,count:1,title:'Chương 7'},'practice');
  assert(parseProgress(p,new Map(qs.map(q=>[q.id,q])),'v1','fixture').activeSession);
});

test('special collections are configured per subject and ordinary tags do not hide chapter questions',()=>{
  const q={...bank.questions[0],chapter:7,tags:['image']} as Question;
  assert.equal(selectQuestions([q],{kind:'chapter',chapter:7,count:10,title:'Ảnh',tags:['formula']},{}).length,1);
  assert.equal(selectQuestions([q],{kind:'collection',tags:['image'],count:10,title:'Ảnh'},{}).length,1);
  assert.equal(selectQuestions([q],{kind:'collection',tags:['date'],count:10,title:'Ngày'},{}).length,0);
});

test('routes keep old bookmarks and isolate links by subject',()=>{
  assert.equal(legacyRedirect('#/chuong/2'),'#/mon/tthcm/chuong/2');
  assert.deepEqual(resolveRoute('#/mon/xu-ly-anh/chuong/7'),{kind:'subject',subjectId:'xu-ly-anh',localHash:'#/chuong/7'});
  assert.equal(subjectHref('khoa-hoc-du-lieu'),'#/mon/khoa-hoc-du-lieu');
  assert.equal(scopeSubjectLinks('<a href="#/" data-global>Trang chủ</a><a href="#/keyword">Keyword</a>','tthcm'),'<a href="#/" data-global>Trang chủ</a><a href="#/mon/tthcm/keyword">Keyword</a>');
});

test('scientific blocks escape code, preserve matrices and reject foreign image paths',()=>{
  assert(renderBlocks([{type:'code',code:'<script>alert(1)</script>'}]).includes('&lt;script&gt;'));
  assert(!renderBlocks([{type:'code',code:'<script>alert(1)</script>'}]).includes('<script>'));
  assert(renderBlocks([{type:'matrix',rows:[[0,1],[2,3]],caption:'Ma trận'}]).includes('<td>3</td>'));
  assert.equal(renderBlocks([{type:'image',src:'https://example.com/a.png',alt:'Ảnh'}]),'');
  const q={...bank.questions[0],chapter:7,blocks:[{type:'image',src:'subjects/tthcm/a.png',alt:'Ảnh'}]};
  const fixture={...bank,subjectId:'fixture',chapters:[{...bank.chapters[0],number:7}],questions:[q],concepts:[{...bank.concepts.find(c=>c.id===q.conceptId)!,chapter:7}],sampleQuestionIds:[],audit:[],questionAliases:[]};
  assert.throws(()=>validateBank(fixture,{id:'fixture',questionCount:1,chapterCount:1}),/current subject/);
});
