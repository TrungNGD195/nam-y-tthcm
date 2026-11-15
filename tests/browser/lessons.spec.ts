import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8'));
const key='nam-y:progress:v2:tthcm';

test('chapter lessons contain exactly their bank questions and keep every chapter freely accessible',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  for(const chapter of bank.lessons.chapters){
    await page.goto(`/#/mon/tthcm/chuong/${chapter.chapter}`);
    await expect(page.locator('.lesson-guide')).toBeVisible();
    await expect(page.locator('[data-lesson-section]')).toHaveCount(chapter.sections.length);
    const ids=await page.locator('[data-lesson-question]').evaluateAll(els=>els.map(el=>(el as HTMLElement).dataset.lessonQuestion).sort());
    expect(ids).toEqual(bank.questions.filter((q:any)=>q.chapter===chapter.chapter).map((q:any)=>q.id).sort());
    expect(new Set(ids).size).toBe(ids.length);
    await expect(page.locator('[data-action=start]')).toBeEnabled();
  }
  expect(errors).toEqual([]);
});

test('read a section, retain its open state, practice only its questions and grade after reload',async({page})=>{
  await page.goto('/#/mon/tthcm/chuong/4');
  await page.locator('[data-action=collapse-lessons]').click();
  await expect(page.locator('[data-lesson-section][open]')).toHaveCount(0);
  const jump=page.locator('[data-action=lesson-jump][data-section=c4-dan-chu]');
  await jump.focus();await page.keyboard.press('Enter');
  const section=page.locator('#c4-dan-chu');
  await expect(section).toHaveAttribute('open','');
  await expect(section.locator('.learning-points')).toContainText(['Của dân','Ba biểu hiện']);
  await page.locator('[data-action=count][data-value="20"]').click();
  await expect(section).toHaveAttribute('open','');
  await section.locator('[data-action=practice-section]').click();
  await expect(page).toHaveURL(/lam-bai/);
  let p=await page.evaluate(key=>JSON.parse(localStorage.getItem(key)!),key);
  const ids=p.activeSession.items.map((i:any)=>i.questionId).sort();
  expect(ids).toEqual(bank.questions.filter((q:any)=>q.chapter===4&&['democracy','state-class'].includes(q.conceptId)).map((q:any)=>q.id).sort());
  const q=bank.questions.find((q:any)=>q.id===p.activeSession.items[0].questionId);
  await page.locator(`[data-option="${q.correctOptionId}"]`).click();
  await page.reload();await page.locator('[data-action=check]').click();
  await expect(page.locator('.feedback-title')).toContainText('Chính xác');
  p=await page.evaluate(key=>JSON.parse(localStorage.getItem(key)!),key);
  expect(p.records[q.id].lastOutcome).toBe('correct');
});

test('cross-chapter knowledge stays in its source chapter and can be practiced as a single question',async({page})=>{
  await page.goto('/#/mon/tthcm/chuong/2');
  await page.locator('[data-action=lesson-jump][data-section=c2-1930-1969]').click();
  const concept=page.locator('[data-lesson-concept=vietminh]');
  await concept.locator('.lesson-questions>summary').click();
  await concept.locator('[data-action=practice-question]').click();
  await expect(page).toHaveURL(/lam-bai/);
  const p=await page.evaluate(key=>JSON.parse(localStorage.getItem(key)!),key);
  expect(p.activeSession.items.map((i:any)=>i.questionId)).toEqual(['lms-g2-23']);
});

test('lesson controls and expanded content fit a phone viewport',async({page})=>{
  await page.setViewportSize({width:390,height:844});
  await page.goto('/#/mon/tthcm/chuong/6');
  await page.locator('[data-action=expand-lessons]').click();
  await expect(page.locator('[data-lesson-section][open]')).toHaveCount(8);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.locator('[data-action=collapse-lessons]').click();
  await expect(page.locator('[data-lesson-section][open]')).toHaveCount(0);
});
