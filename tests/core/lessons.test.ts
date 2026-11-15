import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {validateBank} from '../../scripts/content/validate.mjs';
import type {Bank} from '../../src/core/types.ts';

const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8')) as Bank;
const report=JSON.parse(readFileSync(new URL('../../content/tthcm/lesson-coverage.json',import.meta.url),'utf8'));
const subject={id:'tthcm',questionCount:506,chapterCount:6};
const sorted=(v:any):any=>Array.isArray(v)?v.map(sorted):v!==null&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,sorted(v[k])])):v;
const digest=(v:unknown)=>createHash('sha256').update(JSON.stringify(sorted(v))).digest('hex');

test('all 506 questions have an auditable lesson in their original chapter, including cross-chapter references',()=>{
  assert.equal(report.questionCount,506);assert.equal(report.conceptCount,213);assert.equal(report.sectionCount,45);
  assert.equal(digest(bank.questions),report.questionsHash);
  assert.equal(report.version,bank.lessons!.version);
  const rows=new Map<string,any>(report.questions.map((r:any)=>[r.questionId,r]));
  assert.equal(rows.size,506);
  for(const q of bank.questions){
    const row=rows.get(q.id)!;
    assert.equal(row.chapter,q.chapter);assert.equal(row.conceptId,q.conceptId);assert.equal(row.questionHash,digest(q));
    assert.equal(row.answerText,q.options.find(o=>o.id===q.correctOptionId)!.text);
    const sections=bank.lessons!.chapters.find(c=>c.chapter===q.chapter)!.sections.filter(s=>s.conceptIds.includes(q.conceptId));
    assert.equal(sections.length,1);assert.equal(sections[0].id,row.sectionId);
  }
  for(const id of ['lms-g2-19','lms-g2-23','lms-g2-25','lms-g2-29','lms-g4-03','quiz-g1-07','quiz-g5-04','quiz-g5-05','quiz-g5-07','quiz-g5-08']){
    const q=bank.questions.find(q=>q.id===id)!;assert.equal(rows.get(id).chapter,q.chapter);
  }
});

test('content validation refuses missing knowledge, duplicate placement and unsupported lesson sources',()=>{
  validateBank(bank,subject);
  const missing=structuredClone(bank);
  missing.lessons!.chapters[0].sections[0].conceptIds.pop();
  assert.throws(()=>validateBank(missing,subject),/Question missing chapter lesson/);
  const duplicate=structuredClone(bank);
  duplicate.lessons!.chapters[0].sections[1].conceptIds.push(duplicate.lessons!.chapters[0].sections[0].conceptIds[0]);
  assert.throws(()=>validateBank(duplicate,subject),/Duplicate or unknown lesson concept/);
  const evidence=structuredClone(bank);
  evidence.lessons!.chapters[0].sections[0].references[0].pdfPage=99999;
  assert.throws(()=>validateBank(evidence,subject),/valid evidence/);
});

test('broad theory has explained subpoints and keeps distinct exam cues',()=>{
  const cmap=new Map(bank.concepts.map(c=>[c.id,c]));
  for(const id of ['definition','phases','independence','liberation','socialism','democracy','ethics-standards','ethics-principles']){
    const c=cmap.get(id)!;assert(c.learningPoints!.length>=3,id);
    assert(c.learningPoints!.every(p=>p.title&&p.text.length>20&&p.keywords.length));
    assert(c.references.some(r=>r.sourceId==='ptit'));
  }
  assert.match(cmap.get('national-socialism')!.learningPoints!.map(p=>p.text).join(' '),/tiền đề|vững chắc/);
  assert.match(cmap.get('centralism')!.learningPoints!.map(p=>p.text).join(' '),/thiểu số phục tùng đa số/);
  assert.match(cmap.get('ethics-standards')!.confusionNote,/Chuẩn mực.*nguyên tắc/);
});
