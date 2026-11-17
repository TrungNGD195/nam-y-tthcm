import { test,expect } from '@playwright/test';
import {readFileSync} from 'node:fs';
const documents=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/documents.json',import.meta.url),'utf8'));
const solutions=JSON.parse(readFileSync(new URL('../../src/subjects/xu-ly-anh/solutions.json',import.meta.url),'utf8'));

test('theory renders complete responses, corrected formulas, true-false reasons and MATLAB code',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  for(const id of ['bank-2-2','bank-2-6','uyen-6-L9','uyen-7-L5']){
    const item=solutions.items.find((i:any)=>i.id===id);
    await page.goto('/#/mon/xu-ly-anh/bai/'+id);
    await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
    await expect(page.locator('.theory-answer h2')).toHaveText('Câu trả lời');
    await expect(page.locator('.theory-answer-part')).toHaveCount(item.steps.length);
    for(let n=0;n<item.steps.length;n++){
      await expect(page.locator('.theory-answer-part>p').nth(n)).toHaveText(item.steps[n].text);
    }
    await expect(page.locator('.theory-answer .solution-step,.katex-error')).toHaveCount(0);
    await expect(page.locator('.recall-keywords mark').first()).toBeVisible();
    if(id==='bank-2-2'){
      await expect(page.locator('.source-correction')).toContainText('225');
      await expect(page.locator('.theory-answer .katex').first()).toBeVisible();
      await page.screenshot({path:'test-results/theory-complete-answer.png',fullPage:true});
    }
    if(id==='uyen-7-L5')await expect(page.locator('.theory-answer pre')).toContainText('padarray');
  }
  expect(errors).toEqual([]);
});

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
  await expect(page.locator('.focused-question-part')).toHaveCount(1);
  await page.locator('.source-original>summary').click();
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

test('exercise subpart buttons jump to their PDF heading and text exports explain each step',async({page})=>{
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-6-T11');
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
  const buttons=page.locator('.answer-part-nav button');await expect(buttons).toHaveCount(4);
  const target=documents.items['uyen-6-T11'].parts.at(-1);
  await buttons.last().click();
  const img=page.locator(`.answer-document-page[data-document-page="${target.pdfPage}"] img`);
  await expect.poll(()=>img.evaluate((el:HTMLImageElement)=>el.complete&&el.naturalWidth>0)).toBe(true);
  await expect.poll(async()=>Math.abs(await img.evaluate((el:HTMLImageElement,offset:number)=>el.getBoundingClientRect().top+el.getBoundingClientRect().height*offset-16,target.top))).toBeLessThan(5);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  const href=await page.getByRole('link',{name:'Bản văn bản',exact:true}).getAttribute('href');
  const res=await page.request.get(href!);expect(res.ok()).toBe(true);
  const text=await res.text();
  for(const label of ['Câu (a)','Câu (g)','Ký hiệu:','Cách làm:','Thay số / thực hiện:'])expect(text).toContain(label);
  await page.screenshot({path:'test-results/worked-subpart.png'});
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-7-L8');
  await expect(page.locator('.prompt-subpart')).toHaveCount(7);
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
  await expect(page.locator('.theory-statement')).toHaveCount(7);
});

test('later exercises ask only the new focus, provide earlier computations and retain all original problems',async({page})=>{
  await page.goto('/#/mon/xu-ly-anh/co-uyen/chuong/6');
  await page.locator('#solution-kind').selectOption('exercise');await expect(page.locator('.solution-row')).toHaveCount(12);
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-6-T2');
  await expect(page.locator('.focused-question-part h4')).toHaveText(['Câu (b)','Câu (c)']);
  await expect(page.locator('.supplied-data')).toContainText('n₂=61 bit');
  await expect(page.locator('.source-original')).not.toHaveAttribute('open');
  await page.locator('.focus-context a').first().click();
  await expect(page).toHaveURL(/uyen-6-T1$/);await expect(page.locator('.original-problem img').first()).toBeVisible();
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-5-T6');
  await expect(page.locator('.focused-question-part h4')).toHaveText(['Câu (c)']);
  await expect(page.locator('.focused-givens table')).toHaveCount(3);
  await expect(page.locator('.focused-requirements')).toContainText('plateau');
  await page.locator('.source-original>summary').click();
  await expect(page.locator('.source-original img').first()).toBeVisible();
  await page.locator('.source-original .original-transcript>summary').click();
  await expect(page.locator('.original-transcript pre')).toContainText('Tính biểu đồ tần suất');
  await page.locator('.source-original>summary').click();
  await page.getByRole('button',{name:'Mở lời giải',exact:false}).click();
  await expect(page.locator('.answer-part-nav button')).toHaveCount(1);
  await expect(page.locator('.answer-part-nav')).toContainText('Câu (c)');
  await page.goto('/#/mon/xu-ly-anh/bai/uyen-6-T11');
  await expect(page.locator('.focused-question-part h4')).toHaveText(['Câu (a)','Câu (e)','Câu (f)','Câu (g)']);
  await page.screenshot({path:'test-results/focused-exercise-question.png',fullPage:true});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
