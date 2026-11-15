import { test,expect } from '@playwright/test';
import {readFileSync} from 'node:fs';
const documents=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/documents.json',import.meta.url),'utf8'));

test('desktop gives two obvious study entrances and all four point groups',async({page})=>{
  await page.goto('/#/mon/xu-ly-anh');
  await page.locator('.skip-link').focus();await page.locator('.skip-link').press('Enter');
  await expect(page.locator('#main')).toBeFocused();await expect(page).toHaveURL(/#\/mon\/xu-ly-anh$/);
  await expect(page.locator('.solution-area')).toHaveCount(2);
  for(const start of await page.locator('.solution-area .btn').all()){
    const box=await start.boundingBox();expect(box!.y+box!.height).toBeLessThan(768);
  }
  await expect(page.locator('.exam-map')).toContainText('Đạo đức');
  await expect(page.locator('.course-scope')).toContainText('Chưa thấy bộ câu hỏi/đáp án đạo đức');
  await page.screenshot({path:'test-results/image-processing-home.png',fullPage:true});
  await page.getByRole('link',{name:'Vào giải ngân hàng',exact:false}).click();
  await expect(page.locator('.solution-group')).toHaveCount(4);
  await expect(page.locator('.solution-group').first()).toContainText('14 câu/bài');
  await page.locator('.solution-group').first().click();await expect(page.locator('.solution-row')).toHaveCount(14);
  await page.locator('.solution-row').first().click();await expect(page.locator('.worked-answer')).toHaveCount(0);
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
  await expect(page.locator('.worked-answer mark').first()).toBeVisible();
  await page.getByRole('button',{name:'Cần ôn',exact:false}).click();
  await page.reload();await expect(page.getByRole('button',{name:'Cần ôn',exact:false})).toHaveAttribute('aria-pressed','true');
  await page.locator('.sidebar').getByRole('link',{name:'Cần ôn lại',exact:false}).click();
  await expect(page.locator('.solution-row')).toHaveCount(1);
});

test('chapter lists combine theory and calculations with accent-insensitive keyword search',async({page})=>{
  await page.goto('/#/mon/xu-ly-anh/co-uyen');await expect(page.locator('.solution-group')).toHaveCount(7);
  await page.locator('.solution-group').filter({hasText:'Chương 7'}).click();await expect(page.locator('.solution-row')).toHaveCount(19);
  await page.locator('#solution-kind').selectOption('exercise');await expect(page.locator('.solution-row')).toHaveCount(11);
  await page.locator('#solution-search').fill('phan xa');await expect(page.locator('.solution-row')).toHaveCount(1);
  await page.locator('.solution-row').click();await expect(page.locator('.solved-heading h1')).toContainText('bất đối xứng');
  const images=page.locator('.original-problem img');await expect(images).toHaveCount(1);
  await expect.poll(()=>images.first().evaluate((img:HTMLImageElement)=>img.complete&&img.naturalWidth>0)).toBe(true);
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
  const pages=page.locator('.answer-document-page img');
  await expect(pages).toHaveCount(documents.items['uyen-7-T2'].pages.length);
  await expect.poll(()=>pages.first().evaluate((img:HTMLImageElement)=>img.complete&&img.naturalWidth>=1200)).toBe(true);
  await expect(page.locator('.worked-answer .solution-step')).toHaveCount(0);
  await expect(page.getByRole('link',{name:'Xem PDF tại bài này'})).toHaveAttribute('href',new RegExp('#page='+documents.items['uyen-7-T2'].answerStartPage+'$'));
  await page.screenshot({path:'test-results/image-processing-worked.png',fullPage:true});
});

test('numerical worked answers display real PDF screenshots and expose source corrections',async({page})=>{
  const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
  for(const id of ['bank-3-3','bank-3-10','uyen-4-T3','uyen-6-T9','uyen-6-T11','uyen-7-T9']){
    await page.goto('/#/mon/xu-ly-anh/bai/'+id);
    await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
    const images=page.locator('.answer-document-page img');
    await expect(images).toHaveCount(documents.items[id].pages.length);
    await expect.poll(()=>images.first().evaluate((img:HTMLImageElement)=>img.complete&&img.naturalWidth>=1200)).toBe(true);
    const sources=await images.evaluateAll(els=>els.map(el=>(el as HTMLImageElement).getAttribute('src')));
    expect(sources.map(src=>src!.split('subjects/')[1])).toEqual(documents.items[id].pages.map((p:any)=>p.src.split('subjects/')[1]));
    await expect(page.locator('.worked-answer .solution-step,.worked-answer .katex')).toHaveCount(0);
    await page.locator('.solution-references summary').click();await expect(page.locator('.solution-references')).toContainText('trang PDF');
  }
  await page.goto('/#/mon/xu-ly-anh/bai/bank-3-10');
  await expect(page.locator('.source-correction')).toContainText('tập con');
  expect(errors).toEqual([]);
});

test('solution state stays separate from quiz progress when navigating between subjects',async({page})=>{
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-3-T1');
  await page.getByRole('button',{name:'Đã nắm',exact:false}).click();
  const state=await page.evaluate(()=>localStorage.getItem('nam-y:solutions:v1:xu-ly-anh'));
  await page.locator('.sidebar').getByRole('link',{name:'Tư tưởng Hồ Chí Minh',exact:true}).click();
  await expect(page.locator('.chapter-card')).toHaveCount(6);
  await page.locator('.brand').click();await page.locator('[data-subject=xu-ly-anh] .subject-primary').click();
  await expect(page.locator('.solution-shortcuts')).toContainText('1/168');
  expect(await page.evaluate(()=>localStorage.getItem('nam-y:solutions:v1:xu-ly-anh'))).toBe(state);
});

test('unavailable browser storage keeps study usable and reports unsaved marks',async({page})=>{
  await page.addInitScript(()=>{Storage.prototype.setItem=()=>{throw new DOMException('Quota exceeded','QuotaExceededError');};});
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-3-T1');
  await page.getByRole('button',{name:'Cần ôn',exact:false}).click();
  await expect(page.locator('.storage-notice')).toContainText('chưa lưu được');
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();await expect(page.locator('.worked-answer')).toBeVisible();
});

test('mobile can open menus and read wide matrices without page overflow',async({page})=>{
  await page.setViewportSize({width:390,height:844});
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-6-T11');
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();await expect(page.locator('.answer-document-page img').first()).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.getByRole('button',{name:'Mở menu',exact:true}).click();await expect(page.locator('.sidebar')).toHaveClass(/open/);
  await page.locator('.sidebar').getByRole('link',{name:'giải bài cô Uyên',exact:false}).click();await expect(page.locator('.solution-group')).toHaveCount(7);
});

test('PDF download and large-page links work while reveal and reading marks stay independent',async({page})=>{
  await page.goto('/#/mon/xu-ly-anh/bai/bank-3-1');
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
  const image=page.locator('.answer-document-page img').first();
  await expect.poll(()=>image.evaluate((img:HTMLImageElement)=>img.complete&&img.naturalWidth>0)).toBe(true);
  const large=page.locator('.answer-document-page>a').first();
  await expect(large).toHaveAttribute('href',(await image.getAttribute('src'))!);
  await expect(large).toHaveAttribute('target','_blank');
  const downloadPromise=page.waitForEvent('download');await page.getByRole('link',{name:'Tải PDF 67 bài'}).click();
  const download=await downloadPromise;expect(download.suggestedFilename()).toMatch(/\.pdf$/);expect(await download.failure()).toBeNull();
  await page.getByRole('button',{name:'Ẩn lời giải',exact:false}).click();await expect(page.locator('.answer-document-page')).toHaveCount(0);
  await page.getByRole('button',{name:'Đã nắm',exact:false}).click();await page.reload();
  await expect(page.getByRole('button',{name:'Đã nắm',exact:false})).toHaveAttribute('aria-pressed','true');
  await expect(page.locator('.answer-document-page')).toHaveCount(0);
});
