import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8'));
const qmap=new Map<string,any>(bank.questions.map((q:any)=>[q.id,q]));
const key='nam-y:progress:v2:tthcm';
const progress=(page:any)=>page.evaluate((key:string)=>JSON.parse(localStorage.getItem(key)!),key);

test('comprehensive papers are discoverable, complete, balanced and support full exam flow',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/#/mon/tthcm');
  await page.locator('.comprehensive-start').getByRole('link',{name:'Chọn đề để làm',exact:false}).click();
  await expect(page.locator('.comprehensive-card')).toHaveCount(11);
  await expect(page.locator('.comprehensive-overview')).toContainText('506');
  await expect(page.locator('.comprehensive-note')).toContainText('Mỗi câu chỉ xuất hiện một lần');
  for(const card of await page.locator('.comprehensive-card').all())await expect(card.locator('.paper-chapters span')).toHaveCount(6);
  await page.screenshot({path:'test-results/comprehensive-desktop.png',fullPage:true});
  await page.selectOption('#exam-minutes','60');
  await page.locator('[data-action=start-paper][data-paper="01"]').click();
  await expect(page.locator('.question-num')).toHaveCount(50);
  await expect(page.locator('.feedback')).toHaveCount(0);await expect(page.locator('[data-action=hint]')).toHaveCount(0);
  let p=await progress(page);const ids=p.activeSession.items.map((i:any)=>i.questionId);const deadline=p.activeSession.deadline;
  expect(new Set(ids).size).toBe(50);expect(p.activeSession.deck.kind).toBe('comprehensive');
  await page.locator(`[data-option="${qmap.get(ids[0])!.correctOptionId}"]`).click();
  await page.reload();await expect(page.locator('.question-num')).toHaveCount(50);
  p=await progress(page);expect(p.activeSession.deadline).toBe(deadline);expect(p.activeSession.items.map((i:any)=>i.questionId)).toEqual(ids);
  await expect(page.locator(`[data-option="${qmap.get(ids[0])!.correctOptionId}"]`)).toHaveAttribute('aria-checked','true');
  await page.locator('[data-action=jump][data-index="49"]').click();
  await page.locator(`[data-option="${qmap.get(ids[49])!.correctOptionId}"]`).click();
  await page.locator('[data-action=finish]').click();await page.locator('[data-action=submit]').click();
  await expect(page.locator('.result-item')).toHaveCount(50);
  p=await progress(page);expect(p.lastResult.items).toHaveLength(50);expect(p.history[0].correct).toBe(2);
  await page.getByRole('link',{name:'Chọn đề tổng hợp khác',exact:true}).click();
  await expect(page.locator('.comprehensive-card[data-paper="01"]')).toContainText('2/50');
  await page.locator('[data-action=start-paper][data-paper="01"]').click();await expect(page.locator('.question-num')).toHaveCount(50);
  expect((await progress(page)).activeSession.items.map((i:any)=>i.questionId)).toEqual(ids);
  expect(errors).toEqual([]);
});

test('unfinished paper can resume or be retained when another paper is selected',async({page})=>{
  await page.goto('/#/mon/tthcm/de-tong-hop');await page.locator('[data-action=start-paper][data-paper="10"]').click();
  await expect(page.locator('.question-num')).toHaveCount(50);const original=await progress(page);
  await page.locator('[data-action=save-exit]').click();await page.locator('.sidebar').getByRole('link',{name:'Luyện đề tổng hợp',exact:false}).click();
  await expect(page.locator('.continue-banner')).toContainText('Đề tổng hợp 10');
  await page.locator('[data-action=start-paper][data-paper="02"]').click();await expect(page.getByRole('dialog')).toBeVisible();
  await page.locator('[data-action=close-dialog]').click();expect((await progress(page)).activeSession.id).toBe(original.activeSession.id);
  await page.locator('[data-action=start-paper][data-paper="02"]').click();await page.locator('[data-action=replace-session]').click();
  await expect(page.locator('.question-num')).toHaveCount(50);const next=(await progress(page)).activeSession;expect(next.deck.title).toContain('02');
  expect(next.items.some((item:any)=>original.activeSession.items.some((old:any)=>old.questionId===item.questionId))).toBe(false);
});

test('mobile can study the short final paper without repeated padding',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto('/#/mon/tthcm/de-tong-hop');
  await expect(page.locator('.comprehensive-card')).toHaveCount(11);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await expect(page.locator('.comprehensive-card[data-paper="11"]')).toContainText('6 CÂU');
  await page.locator('[data-action=start-paper][data-paper="11"]').click();await expect(page.locator('.question-num')).toHaveCount(6);
  await page.locator('[data-action=jump][data-index="5"]').click();await expect(page.locator('.question-num.current')).toHaveText('6');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
