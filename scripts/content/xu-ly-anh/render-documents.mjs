/** Render real PDFs first. rasterize_documents.py exports their pages for the web. */
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {chromium} from '@playwright/test';
import katex from 'katex';
import {exerciseHtml,printCss,sizingCss,teachingCss,canonical,escapeHtml} from './document-layout.mjs';

const root=resolve(dirname(fileURLToPath(import.meta.url)),'../../..');
const data=JSON.parse(await readFile(resolve(root,'src/subjects/xu-ly-anh/solutions.json'),'utf8'));
const out=resolve(root,'.analysis/solution-documents');await mkdir(out,{recursive:true});
const args=process.argv.slice(2),only=args.find(a=>a.startsWith('--only='))?.slice(7).split(',');
const collator=new Intl.Collator('en',{numeric:true});
const items=data.items.filter(i=>i.kind==='exercise'&&(!only||only.includes(i.id))).sort((a,b)=>a.area.localeCompare(b.area)||(a.area==='uyen'?a.chapter-b.chapter:a.points-b.points)||collator.compare(a.code,b.code));
const fontDir=resolve(root,'node_modules/katex/dist');
let katexCss=await readFile(resolve(fontDir,'katex.min.css'),'utf8');
const fontUrls=[...new Set([...katexCss.matchAll(/url\(([^)]+)\)/g)].map(m=>m[1]))];
for(const url of fontUrls){const binary=await readFile(resolve(fontDir,url));const ext=url.split('.').pop();katexCss=katexCss.replaceAll(`url(${url})`,`url(data:font/${ext};base64,${binary.toString('base64')})`);}
const browser=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROME_PATH|| (process.platform==='win32'?'C:/Program Files/Google/Chrome/Application/chrome.exe':undefined)});
const manifest={version:'2026.11.16.2',subjectId:'xu-ly-anh',dataVersion:data.version,items:[]};
try{
  const page=await browser.newPage({viewport:{width:795,height:1123}});
  const html=body=>`<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>${katexCss}\n${printCss}\n${sizingCss}\n${teachingCss}</style></head><body>${body}</body></html>`;
  async function print(body,id){
    const path=resolve(out,id+'.html');await writeFile(path,html(body));await page.goto(pathToFileURL(path).href);
    await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(img=>img.decode()));});
    // Long equations get several readable lines, never clipped or silently tiny.
    for(const locator of await page.locator('.equation').all()){
      const over=await locator.evaluate(el=>el.scrollWidth>el.clientWidth+1);
      if(over){
        const tex=await locator.getAttribute('data-tex');
        const parts=tex.split(/\\q?quad\s*/);
        if(parts.length>1){try{await locator.evaluate((el,html)=>el.innerHTML=html,parts.map(t=>`<div>${katex.renderToString(t,{displayMode:true,throwOnError:true,trust:false,output:'html'})}</div>`).join(''));}catch{ /* retain the valid complete equation */ }}
      }
    }
    const layout=await page.evaluate(()=>{
      const problems=[];
      for(const el of document.querySelectorAll('.equation,.data-table,.matrix-figure')){
        const natural=Math.max(el.scrollWidth,...[...el.children].map(child=>child.getBoundingClientRect().width));
        const available=el.clientWidth;
        if(natural>available+1){const ratio=available/natural;if(ratio<.72)problems.push({type:el.className,ratio});else el.style.fontSize=`${parseFloat(getComputedStyle(el).fontSize)*ratio}px`;}
      }
      return problems;
    });
    if(layout.length)throw new Error(id+': unreadable oversized content '+JSON.stringify(layout));
    await page.pdf({path:resolve(out,id+'.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,tagged:true,
      headerTemplate:'<div></div>',footerTemplate:`<div style="width:100%;text-align:center;font:9px Arial;color:#555">${escapeHtml(id==='cover'?'Nắm ý · Xử lý ảnh':'Bài '+items.find(i=>i.id===id).code)} · <span class="pageNumber"></span>/<span class="totalPages"></span></div>`});
  }
  await print('<section class="cover"><p>XỬ LÝ ẢNH · NẮM Ý</p><h1>67 bài tập<br>Đề và lời giải đối chiếu</h1><h2>giải ngân hàng · giải bài cô Uyên</h2><p>21 bài ngân hàng theo mức điểm.<br>46 bài cô Uyên theo chương 3–7.</p><p>Tách riêng từng câu (a), (b), (c) theo đề.<br>Mỗi bước: câu dẫn → công thức → ký hiệu → cách làm → thay số → kết quả.</p><p>Dùng mục lục dấu trang của PDF để chọn bài.<br>Đọc lưu ý tại bài khi dữ kiện hoặc đáp án nguồn cần hiệu chỉnh.</p><p class="byline">Đối chiếu giáo trình và slide được cung cấp.<br>Bản trình bày ngày 16/11/2026.</p></section>','cover');
  for(const item of items){
    const images=await Promise.all(item.images.map(async src=>'data:image/webp;base64,'+(await readFile(resolve(root,'public',src))).toString('base64')));
    await print(exerciseHtml(item,data.sources,images),item.id);
    manifest.items.push({id:item.id,code:item.code,title:item.title,area:item.area,chapter:item.chapter,points:item.points,contentHash:createHash('sha256').update(JSON.stringify(canonical(item))).digest('hex')});
    if(manifest.items.length%10===0)process.stdout.write(`PDFs: ${manifest.items.length}/${items.length}\n`);
  }
  await writeFile(resolve(out,only?'sample-manifest.json':'render-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
  process.stdout.write(`Rendered ${items.length} exercise PDFs. Next: python scripts/content/xu-ly-anh/rasterize_documents.py\n`);
}finally{await browser.close();}
