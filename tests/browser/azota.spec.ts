import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { createSession } from '../../src/core/engine.ts';
import { emptyProgress } from '../../src/core/storage.ts';
import type { Bank } from '../../src/core/types.ts';

const bank=JSON.parse(readFileSync(new URL('../../src/subjects/tthcm/bank.json',import.meta.url),'utf8')) as Bank;
const report=JSON.parse(readFileSync(new URL('../../content/tthcm/azota/reviewed.json',import.meta.url),'utf8'));
const key='nam-y:progress:v2:tthcm';

test('corrected date and aggregate answer grade by content after shuffling and reload',async({page})=>{
  const questions=['azota-e9lwce-070','azota-3eggrt-015'].map(id=>bank.questions.find(q=>q.id===report.questions.find((r:any)=>r.id===id).questionId)!);
  const progress=emptyProgress(bank.version);
  progress.activeSession=createSession(questions,{kind:'review',title:'Đối chiếu Azota',count:2},'practice');
  await page.addInitScript(({key,progress})=>{if(!localStorage.getItem(key))localStorage.setItem(key,JSON.stringify(progress));},{key,progress});
  await page.goto('/#/mon/tthcm/lam-bai');
  await expect(page.locator(`[data-option="${questions[0].correctOptionId}"]`)).toContainText('Tháng 4/1908');
  await page.locator(`[data-option="${questions[0].correctOptionId}"]`).click();
  await page.locator('[data-action=check]').click();
  await expect(page.locator('.feedback-title')).toContainText('Chính xác');
  await page.locator('.sources-detail summary').click();
  await expect(page.locator('.source-content')).toContainText('Câu 70');
  await expect(page.locator('.source-content')).toContainText('5/1908');
  await expect(page.locator('.source-content a[href="https://azota.vn/de-thi/e9lwce"]')).toBeVisible();
  await page.reload();
  await expect(page.locator('.feedback-title')).toContainText('Chính xác');
  await page.locator('[data-action=next]').click();
  await expect(page.locator(`[data-option="${questions[1].correctOptionId}"]`)).toContainText('Cả ba phương án còn lại');
  await page.locator(`[data-option="${questions[1].correctOptionId}"]`).click();
  await page.locator('[data-action=check]').click();
  await expect(page.locator('.feedback-title')).toContainText('Chính xác');
});

test('source page accounts for every capture and shows held items outside practice',async({page})=>{
  await page.goto('/#/mon/tthcm/nguon');
  await expect(page.locator('.sources-summary')).toContainText(String(bank.questions.length));
  await expect(page.locator('.sources-summary')).toContainText('755');
  await expect(page.locator('.audit-table-wrap tbody tr')).toHaveCount(9);
  const row=page.locator('.audit-table-wrap tbody tr').filter({hasText:'Azota rnaeqk'});
  await expect(row).toContainText('148');
  await page.getByText('15 mục chưa dùng để chấm — xem lý do',{exact:true}).click();
  await expect(page.locator('.audit-pending')).toHaveCount(15);
  await expect(page.locator('.audit-pending').filter({hasText:'thành tựu nổi bật nhất'})).toContainText('không nêu giai đoạn');
});
