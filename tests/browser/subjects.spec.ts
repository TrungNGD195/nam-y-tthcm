import { test,expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8'));
const currentKey='nam-y:progress:v2:tthcm';

test('entry page makes the available learning action visible without loading question data',async({page})=>{
  await page.setViewportSize({width:1366,height:768});
  const requests:string[]=[];page.on('request',r=>requests.push(r.url()));
  await page.goto('/');await expect(page.locator('.subject-card')).toHaveCount(3);
  const start=page.locator('[data-subject=tthcm]').getByRole('link',{name:'Vào học',exact:false});
  await expect(start).toBeVisible();const box=await start.boundingBox();expect(box!.y+box!.height).toBeLessThan(768);
  expect(requests.some(url=>/\/assets\/bank-/.test(url))).toBe(false);
  await expect(page.locator('.awaiting-button')).toHaveCount(1);
  await page.screenshot({path:'test-results/subjects-desktop.png',fullPage:true});
  await start.click();await expect(page.locator('.chapter-card')).toHaveCount(6);
  await expect(page.locator('.chapter-cta').first()).toHaveText(/Học chương này/);
  await page.locator('.chapter-card').first().click();await expect(page.locator('[data-action=start]')).toBeVisible();
});

test('switching subjects keeps progress and cannot mix the subject contexts',async({page})=>{
  await page.goto('/#/mon/tthcm/chuong/1');await page.locator('[data-action=start]').click();
  await page.locator('[data-action=skip]').click();
  const original=await page.evaluate(key=>localStorage.getItem(key),currentKey);
  await page.selectOption('#subject-switch','xu-ly-anh');
  await expect(page.locator('.solution-areas')).toBeVisible();
  await expect(page.locator('.question-card')).toHaveCount(0);
  expect(await page.evaluate(key=>localStorage.getItem(key),currentKey)).toBe(original);
  expect(await page.evaluate(()=>localStorage.getItem('nam-y:progress:v2:xu-ly-anh'))).toBeNull();
  await page.locator('.brand').click();await page.locator('[data-subject=tthcm] .resume-link').click();
  await expect(page.locator('.feedback')).toBeVisible();
  await page.locator('[data-action=next]').click();await page.locator('[data-action=skip]').click();
  const restored=await page.evaluate(key=>JSON.parse(localStorage.getItem(key)!),currentKey);
  expect(Object.values(restored.records).reduce((sum:number,r:any)=>sum+r.seen,0)).toBe(2);
});

test('old URLs and saved data migrate, including an unfinished shuffled question',async({page})=>{
  const q=bank.questions[0];
  const legacy={schemaVersion:1,bankVersion:bank.version,records:{},history:[],lastResult:null,activeSession:{id:'old-session',mode:'practice',status:'active',deck:{kind:'chapter',chapter:1,count:1,title:'Chương 1'},items:[{questionId:q.id,revision:q.revision,optionOrder:q.options.map((o:any)=>o.id).reverse(),selectedOptionId:null,checked:false,recorded:false,usedHint:false}],cursor:0,startedAt:Date.now(),deadline:null,finishedAt:null}};
  await page.addInitScript(data=>{if(!localStorage.getItem('nam-y:progress:v1'))localStorage.setItem('nam-y:progress:v1',JSON.stringify(data));},legacy);
  await page.goto('/#/lam-bai');await expect(page).toHaveURL(/mon\/tthcm\/lam-bai/);
  await expect(page.locator('#question-prompt')).toHaveText(q.prompt);
  const ids=await page.locator('[data-action=choose]').evaluateAll(els=>els.map(el=>(el as HTMLElement).dataset.option));
  expect(ids).toEqual(legacy.activeSession.items[0].optionOrder);
  await page.locator(`[data-option="${q.correctOptionId}"]`).click();await page.locator('[data-action=check]').click();
  await page.reload();await expect(page.locator('.feedback')).toBeVisible();
  const p=await page.evaluate(key=>JSON.parse(localStorage.getItem(key)!),currentKey);expect(p.records[q.id].seen).toBe(1);
  expect(await page.evaluate(()=>localStorage.getItem('nam-y:progress:v1'))).toBe(JSON.stringify(legacy));
});

test('mobile catalog is usable and pending subjects have an honest empty state',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto('/');
  await expect(page.locator('.subject-card')).toHaveCount(3);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  await page.locator('[data-subject=khoa-hoc-du-lieu] .subject-info-link').click();
  await expect(page.locator('.awaiting-panel')).toContainText('Chưa có câu hỏi để ôn');
  await page.screenshot({path:'test-results/subject-pending-mobile.png',fullPage:true});
});
