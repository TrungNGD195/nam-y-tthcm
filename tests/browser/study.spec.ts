import { test, expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
const bank=JSON.parse(readFileSync(new URL('../../src/data/bank.json',import.meta.url),'utf8'));
const qmap=new Map<string,any>(bank.questions.map((q:any)=>[q.id,q]));
const key='nam-y:progress:v1';
const readProgress=(page:Page)=>page.evaluate(key=>JSON.parse(localStorage.getItem(key)!),key);

test('practice: hint, independent grading, reload, result and review',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/#/chuong/2');
  await page.locator('[data-action=start]').click();
  await expect(page).toHaveURL(/lam-bai/);
  let p=await readProgress(page);
  const first=p.activeSession.items[0];const q=qmap.get(first.questionId)!;
  const optionOrder=await page.locator('[data-action=choose]').evaluateAll(els=>els.map(el=>(el as HTMLElement).dataset.option));
  await page.locator('[data-action=hint]').click();
  await page.locator(`[data-option="${q.correctOptionId}"]`).click();
  await page.keyboard.press('Enter');
  await expect(page.locator('.feedback-title')).toContainText('Đúng với gợi ý');
  await page.keyboard.down('Enter'); // Held key must not skip a question.
  await page.keyboard.up('Enter');
  await page.reload();
  p=await readProgress(page);
  // The extra deliberate press above may advance one item, but the first stays graded exactly once.
  expect(p.records[first.questionId].seen).toBe(1);
  expect(p.records[first.questionId].lastOutcome).toBe('assisted');
  expect(p.activeSession.items[0].optionOrder).toEqual(optionOrder);
  const cursor=p.activeSession.cursor;const second=qmap.get(p.activeSession.items[cursor].questionId)!;
  if(cursor===0){await page.locator('[data-action=next]').click();}
  const current=(await readProgress(page)).activeSession;
  const next=qmap.get(current.items[current.cursor].questionId)!;
  const incorrect=next.options.find((o:any)=>o.id!==next.correctOptionId).id;
  await page.locator(`[data-option="${incorrect}"]`).click();
  await page.locator('[data-action=check]').click();
  await expect(page.locator('.feedback-title')).toContainText('Chưa đúng');
  await page.locator('[data-action=finish]').click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.locator('[data-action=submit]').click();
  await expect(page).toHaveURL(/ket-qua/);
  expect((await readProgress(page)).history).toHaveLength(1);
  await page.locator('[data-action=result-filter][data-value=wrong]').click();
  await expect(page.locator('.result-item')).not.toHaveCount(0);
  await page.goto('/#/can-on');
  await expect(page.locator('.review-item')).toHaveCount(10);
  expect(second).toBeTruthy();
  expect(errors).toEqual([]);
});

test('quiz keyboard Enter is a separate action; key repeat cannot auto advance',async({page})=>{
  await page.goto('/#/chuong/1');await page.locator('[data-action=start]').click();
  await page.keyboard.press('1');
  await page.keyboard.down('Enter');
  await expect(page.locator('.feedback')).toBeVisible();
  await page.keyboard.down('Enter');
  expect((await readProgress(page)).activeSession.cursor).toBe(0);
  await page.keyboard.up('Enter');
  await page.keyboard.press('Enter');
  expect((await readProgress(page)).activeSession.cursor).toBe(1);
});

test('exam hides answers, saves choices and auto-submits on original deadline',async({page})=>{
  await page.clock.install();
  await page.goto('/#/thi-thu');await page.selectOption('#exam-minutes','15');
  await page.locator('[data-kind=sample]').click();
  await expect(page.locator('[data-action=hint]')).toHaveCount(0);
  await expect(page.locator('.feedback')).toHaveCount(0);
  let p=await readProgress(page);expect(p.activeSession.items).toHaveLength(20);
  const q=qmap.get(p.activeSession.items[0].questionId)!;
  await page.locator(`[data-option="${q.correctOptionId}"]`).click();
  p=await readProgress(page);expect(Object.keys(p.records)).toHaveLength(0);const deadline=p.activeSession.deadline;
  await page.reload();
  p=await readProgress(page);expect(p.activeSession.deadline).toBe(deadline);
  await expect(page.locator(`[data-option="${q.correctOptionId}"]`)).toHaveAttribute('aria-checked','true');
  await page.clock.fastForward(16*60_000);
  await expect(page).toHaveURL(/ket-qua/);
  p=await readProgress(page);expect(p.history).toHaveLength(1);expect(p.history[0].correct).toBe(1);expect(p.activeSession).toBeNull();
  await page.reload();expect((await readProgress(page)).history).toHaveLength(1);
});

test('keyword search ignores diacritics and focus survives typing',async({page})=>{
  await page.goto('/#/keyword');
  await page.locator('#keyword-search').pressSequentially('khong tu');
  const card=page.locator('.keyword-card[data-concept=confucius]');
  await expect(card).toBeVisible();
  await expect(card.locator('h3')).toContainText('Khổng Tử');
  await expect(page.locator('#keyword-search')).toBeFocused();
  await expect(card.locator('.reveal')).toHaveCount(0);
  await card.locator('[data-action=reveal]').click();
  await expect(card.locator('.reveal')).toContainText('tu dưỡng đạo đức cá nhân');
  await page.locator('#keyword-search').fill('KHÔNG CÓ CỤM NÀY 1234');
  await expect(page.locator('.empty-state')).toBeVisible();
  await page.locator('[data-action=clear-search]').click();
  expect(await page.locator('.keyword-card').count()).toBeGreaterThan(30);
});

test('progress export/import round trip and invalid JSON are handled',async({page})=>{
  await page.goto('/#/chuong/1');await page.locator('[data-action=start]').click();
  await page.locator('[data-action=skip]').click();
  const original=await readProgress(page);
  await page.goto('/#/nguon');
  const downloaded=page.waitForEvent('download');await page.locator('[data-action=export]').click();
  expect((await downloaded).suggestedFilename()).toMatch(/nam-y-tien-do/);
  await page.locator('[data-action=reset]').click();await page.locator('[data-action=confirm-reset]').click();
  expect(Object.keys((await readProgress(page)).records)).toHaveLength(0);
  await page.locator('#import-file').setInputFiles({name:'progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(original))});
  await page.locator('[data-action=confirm-import]').click();
  expect((await readProgress(page)).records).toEqual(original.records);
  await page.locator('#import-file').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{oops')});
  await expect(page.locator('#toasts')).toContainText('không đúng định dạng');
});

test('blocked localStorage still permits a full practice interaction',async({page})=>{
  await page.addInitScript(()=>{Storage.prototype.setItem=function(){throw new Error('Storage blocked');};});
  await page.goto('/#/chuong/1');await page.locator('[data-action=start]').click();
  await expect(page.locator('.warning-banner')).toContainText('chưa cho lưu');
  await page.locator('[data-action=skip]').click();
  await expect(page.locator('.feedback')).toBeVisible();
  await page.locator('[data-action=save-exit]').click();
  await expect(page.locator('.continue-banner')).toBeVisible();
});

for(const viewport of [{width:1366,height:768},{width:1920,height:1080},{width:390,height:844},{width:683,height:384}]){
  test(`layout and navigation at ${viewport.width}×${viewport.height}`,async({page})=>{
    await page.setViewportSize(viewport);await page.goto('/#/');
    await expect(page.locator('.chapter-card')).toHaveCount(6);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
    await page.screenshot({path:`test-results/home-${viewport.width}.png`,fullPage:true});
    if(viewport.width<900){await page.getByRole('button',{name:'Mở menu',exact:true}).click();await expect(page.locator('.sidebar')).toHaveClass(/open/);}
    await page.locator('.sidebar a[href="#/con-so"]').click();
    await expect(page.locator('h1')).toHaveText('Con số cần nhớ');
    await page.selectOption('#number-tag','count');
    await page.locator('[data-action=start]').click();
    await expect(page.locator('.question-card')).toBeVisible();
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
    await page.screenshot({path:`test-results/question-${viewport.width}.png`,fullPage:true});
    await page.reload();await expect(page.locator('.question-card')).toBeVisible();
  });
}
