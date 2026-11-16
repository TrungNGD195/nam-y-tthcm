import '../../shared/styles/solutions.css';
import type { Subject } from '../../core/types.ts';
import type { ReadingMark, Solutions, SolvedItem } from './types.ts';
import { subjects } from '../../app/subjects.ts';
import { resolveRoute, subjectHref } from '../../app/router.ts';
import { catalogShell } from '../subjects/catalog.ts';
import { esc, emphasize, icon, link, pill, renderBlocks } from '../../shared/ui.ts';
import { filterItems, parseMarks, readingKey } from './model.ts';

export function mountSolutions(subject: Subject, data: Solutions): {render:()=>void;dispose:()=>void} {
  const app=document.querySelector<HTMLDivElement>('#app')!;
  let disposed=false, marks: Record<string, ReadingMark>={}, storageAvailable=true;
  try { marks=parseMarks(localStorage.getItem(readingKey(subject.id)),data.items); } catch { storageAvailable=false; }
  let revealed=false,lastItem='',query='',kind='all',state='all',listContext='';
  const href=(path='')=>subjectHref(subject.id,'#/'+path);
  const itemMap=new Map(data.items.map(item=>[item.id,item]));
  const chapterName=(n:number)=>data.chapters.find(c=>c.number===n)?.title??'';
  const areaName=(area:string)=>area==='bank'?'giải ngân hàng':'giải bài cô Uyên';
  const groupHref=(item:SolvedItem)=>item.area==='bank'?href(`ngan-hang/${item.points}`):href(`co-uyen/chuong/${item.chapter}`);
  function markLabel(item:SolvedItem):string {return marks[item.id]?.state==='known'?'Đã nắm':marks[item.id]?.state==='review'?'Cần ôn':'Chưa đánh dấu';}
  function route():string {
    const current=resolveRoute(location.hash);
    return current.kind==='subject'?current.localHash.replace(/^#\/?/,''):'';
  }
  function exam():string {
    return `<section class="exam-map" aria-label="Cấu trúc đề thi"><div><strong>01</strong><span>Đạo đức<small>Chưa có bộ câu hỏi riêng</small></span></div><div><strong>02</strong><span>Lý thuyết<small>Nhớ ý chính & keyword</small></span></div><div><strong>03–04</strong><span>Bài tập chương 3–7<small>Viết công thức trước khi tính</small></span></div></section>`;
  }
  function landing():string {
    const known=data.items.filter(i=>marks[i.id]?.state==='known').length;
    const review=data.items.filter(i=>marks[i.id]?.state==='review').length;
    return `<div class="solution-intro"><span class="eyebrow">XỬ LÝ ẢNH · ÔN TỰ LUẬN</span><h1>Chọn bộ bài để bắt đầu học.</h1><p>Đọc đề, tự trả lời rồi mở lời giải. Mỗi bài tính đều có công thức, thay số và kết quả.</p></div>
      <section class="solution-areas" aria-label="Hai khu vực ôn tập"><article class="solution-area"><span class="area-symbol">${icon('book')}</span><span class="eyebrow">BỘ 01 · ${data.coverage.bank} CÂU/BÀI</span><h2>giải ngân hàng</h2><p>Theo ngân hàng trong bộ Xử lý ảnh.<br>Chia riêng <strong>1 · 2 · 3 · 4 điểm</strong>.</p>${link(href('ngan-hang'),'Vào giải ngân hàng '+icon('arrow'),'btn primary full')}</article><article class="solution-area"><span class="area-symbol">${icon('layers')}</span><span class="eyebrow">BỘ 02 · ${data.coverage.uyen} CÂU/BÀI</span><h2>giải bài cô Uyên</h2><p>Theo bộ Ôn tập, chia theo chương.<br>Ưu tiên bài tập <strong>chương 3–7</strong>.</p>${link(href('co-uyen'),'Vào giải bài cô Uyên '+icon('arrow'),'btn primary full')}</article></section>
      ${exam()}<p class="course-scope">${esc(data.exam.note)}</p><div class="solution-shortcuts">${link(href('can-on'),`${icon('flag')} Cần ôn (${review})`,'btn')}<span>${known}/${data.items.length} bài đã tự đánh dấu nắm được</span>${link(href('nguon'),'Nguồn & quy ước tính','text-link')}</div><div class="solution-how">1. Chọn bộ / chương <span>→</span> 2. Tự làm trước <span>→</span> 3. Đối chiếu lời giải <span>→</span> 4. Đánh dấu để ôn lại</div>`;
  }
  function groups(area:'bank'|'uyen'):string {
    const groups=area==='bank'?[1,2,3,4]:[3,4,5,6,7,2,8];
    return `<div class="solution-intro">${link(href(),icon('back')+' Trang Xử lý ảnh','text-link')}<h1>${areaName(area)}</h1><p>${area==='bank'?'Chọn mức điểm theo ngân hàng gốc. Mỗi phần có đề và lời giải riêng.':'Chọn chương để ôn lý thuyết và bài tính cùng nhau. Chương 2, 8 chứa lý thuyết bổ sung có trong bộ Ôn tập.'}</p></div><section class="solution-groups" aria-label="Chọn phần để học">${groups.map(n=>{
      const items=data.items.filter(i=>i.area===area&&(area==='bank'?i.points:i.chapter)===n);
      const known=items.filter(i=>marks[i.id]?.state==='known').length;
      const exercises=items.filter(i=>i.kind==='exercise').length;
      return `<a class="solution-group" href="${area==='bank'?href('ngan-hang/'+n):href('co-uyen/chuong/'+n)}"><span class="group-number">${area==='bank'?n+' điểm':'Chương '+n}</span><h2>${area==='bank'?(n<3?'Câu hỏi lý thuyết':'Bài tập tính toán'):esc(chapterName(n))}</h2><p>${items.length} câu/bài · ${exercises?exercises+' bài tính': 'Lý thuyết'}${known?' · '+known+' đã nắm':''}</p><span class="group-start">Học phần này ${icon('arrow')}</span></a>`;
    }).join('')}</section>`;
  }
  function list(title:string,items:SolvedItem[],context:string):string {
    if(listContext!==context){query='';kind='all';state=context==='review'?'review':'all';listContext=context;}
    return `${link(href(context.startsWith('bank')?'ngan-hang':context.startsWith('uyen')?'co-uyen':''),icon('back')+' Chọn phần khác','text-link')}<h1 class="solution-list-title">${esc(title)}</h1><div class="solution-filters"><label class="solution-search">${icon('search')}<span class="sr-only">Tìm câu hoặc keyword</span><input id="solution-search" type="search" placeholder="Tìm mã câu, nội dung hoặc keyword…" value="${esc(query)}"></label><label><span class="sr-only">Loại câu</span><select id="solution-kind"><option value="all">Lý thuyết & bài tập</option><option value="theory" ${kind==='theory'?'selected':''}>Lý thuyết</option><option value="exercise" ${kind==='exercise'?'selected':''}>Bài tập tính toán</option></select></label><label><span class="sr-only">Trạng thái ôn tập</span><select id="solution-state">${[['all','Mọi trạng thái'],['new','Chưa đánh dấu'],['review','Cần ôn'],['known','Đã nắm']].map(([v,t])=>`<option value="${v}" ${state===v?'selected':''}>${t}</option>`).join('')}</select></label></div><div id="solution-results" data-ids="${items.map(i=>i.id).join(',')}">${rows(items)}</div>`;
  }
  function rows(items:SolvedItem[]):string {
    const visible=filterItems(items,query,kind,state,marks);
    return `<p class="solution-count" role="status">${visible.length}/${items.length} câu/bài · Chọn một câu để đọc đề và tự làm.</p><div class="solution-rows">${visible.map(item=>`<a class="solution-row" href="${href('bai/'+item.id)}"><span class="item-code">${esc(item.code.replace('-bs',' bổ sung'))}</span><div><h2>${esc(item.title)}</h2><p>${esc(item.keywords.join(' · '))}</p></div><span class="row-status">${pill(item.kind==='theory'?'Lý thuyết':'Bài tính')}${marks[item.id]?pill(markLabel(item),marks[item.id].state==='known'?'green':''):''}</span><span class="read-item">Đọc đề ${icon('chevron')}</span></a>`).join('')||'<div class="empty-state"><h2>Không có câu phù hợp</h2><p>Thử đổi từ tìm kiếm hoặc bộ lọc.</p></div>'}</div>`;
  }
  function theoryParts(item:SolvedItem):{label:string;text:string}[]{
    return [...item.prompt.matchAll(/\(([a-g])\)\s*([\s\S]*?)(?=\([a-g]\)|$)/g)].map(m=>({label:m[1],text:m[2].trim()}));
  }
  function theoryPromptHtml(item:SolvedItem):string {
    const parts=theoryParts(item);
    if(!parts.length)return `<p class="theory-prompt">${esc(item.prompt)}</p>`;
    return `<p class="theory-prompt">${esc(item.prompt.split(/\([a-g]\)/)[0].trim())}</p>${parts.map(p=>`<p class="prompt-subpart"><strong>(${p.label})</strong> ${esc(p.text)}</p>`).join('')}`;
  }
  function solutionHtml(item:SolvedItem):string {
    if(item.kind==='exercise')return documentHtml(item);
    const parts=theoryParts(item);
    return `<section class="worked-answer theory-answer" id="worked-answer" tabindex="-1" aria-label="Câu trả lời lý thuyết"><div class="answer-heading"><span class="eyebrow">LÝ THUYẾT</span><h2>Câu trả lời</h2></div>
      <div class="theory-response">${item.steps.map(s=>{const part=parts.find(p=>s.lead.startsWith(`(${p.label})`));return `<section class="theory-answer-part">${part?`<blockquote class="theory-statement"><strong>Đề (${part.label}):</strong> ${esc(part.text)}</blockquote>`:''}<h3>${esc(s.lead)}</h3><p>${emphasize(s.text??'',item.keywords)}</p>${s.formula?renderBlocks([{type:'formula',tex:s.formula}]):''}${renderBlocks(s.blocks)}</section>`;}).join('')}</div>
      <div class="recall-keywords">${icon('spark')}<strong>Keyword cần nhớ:</strong> ${item.keywords.map(k=>`<mark>${esc(k)}</mark>`).join(' ')}</div>
      <p class="self-check-note">Đối chiếu câu trả lời trước khi tự đánh dấu Cần ôn hoặc Đã nắm.</p></section>`;
  }
  function documentHtml(item:SolvedItem):string {
    const collection=data.documents,doc=collection?.items[item.id];
    if(!collection||!doc)return `<section class="worked-answer" id="worked-answer" role="status"><p>Chưa tải được bản PDF lời giải. Hãy tải lại trang.</p></section>`;
    const url=(src:string)=>import.meta.env.BASE_URL+src;
    return `<section class="worked-answer document-answer" id="worked-answer" tabindex="-1" aria-label="Lời giải dạng trang PDF"><div class="answer-heading"><span class="eyebrow">LỜI GIẢI ĐÃ DÀN TRANG</span><h2>Đọc bài giải như trên giấy</h2><p>${doc.pages.length} trang lời giải · Công thức → thay số → kết quả. Bấm vào trang để xem ảnh lớn.</p></div>
      <div class="document-toolbar"><a class="btn" href="${esc(url(collection.book.src))}#page=${doc.answerStartPage}" target="_blank" rel="noopener">${icon('book')} Xem PDF tại bài này</a><a class="btn" href="${esc(url(collection.book.src))}" download="Xu-ly-anh-67-bai-tap-va-loi-giai.pdf">Tải PDF 67 bài</a><a class="text-link" href="${esc(url(doc.textSrc))}" target="_blank" rel="noopener">Bản văn bản</a></div>
      <nav class="answer-part-nav" aria-label="Chọn câu trong bài giải">${doc.parts.map(part=>`<button type="button" class="btn small" data-solution-action="answer-part" data-page="${part.pdfPage}" data-offset="${part.top}">${esc(part.title)}</button>`).join('')}</nav>
      <div class="answer-document-pages">${doc.pages.map((page,index)=>`<figure class="answer-document-page" data-document-page="${page.pdfPage}"><a href="${esc(url(page.src))}" target="_blank" rel="noopener" title="Mở trang lời giải cỡ lớn"><img src="${esc(url(page.src))}" width="${page.width}" height="${page.height}" alt="Lời giải bài ${esc(item.code)} — trang ${index+1}/${doc.pages.length}; bản văn bản và PDF ở ngay phía trên" loading="${index?'lazy':'eager'}" decoding="async"></a><figcaption>Trang lời giải ${index+1}/${doc.pages.length} · Trang ${page.pdfPage} trong PDF tổng hợp</figcaption></figure>`).join('')}</div>
      <p class="self-check-note">Đối chiếu cách làm rồi tự đánh dấu Cần ôn hoặc Đã nắm.</p></section>`;
  }
  function itemPage(item:SolvedItem):string {
    if(lastItem!==item.id){revealed=false;lastItem=item.id;}
    const siblings=data.items.filter(i=>i.area===item.area&&(item.area==='bank'?i.points===item.points:i.chapter===item.chapter));
    const at=siblings.findIndex(i=>i.id===item.id);
    const refHtml=item.references.map(ref=>`<li><strong>${esc(data.sources.find(s=>s.id===ref.sourceId)?.title??ref.sourceId)}</strong> · trang PDF ${ref.pdfPage}<span>${esc(ref.section)}</span></li>`).join('');
    return `<div class="solution-breadcrumb">${link(groupHref(item),icon('back')+' '+areaName(item.area)+(item.area==='bank'?' · '+item.points+' điểm':' · Chương '+item.chapter),'text-link')}<span>${at+1}/${siblings.length}</span></div><article class="solved-item" data-item-id="${item.id}"><div class="solved-heading">${pill(item.kind==='theory'?'LÝ THUYẾT':'BÀI TẬP TÍNH TOÁN')}<span class="muted">Câu/bài ${esc(item.code.replace('-bs',' bổ sung'))}</span><h1>${esc(item.title)}</h1></div><section class="original-problem" aria-label="Đề bài"><h2>Đề bài</h2>${item.kind==='theory'?theoryPromptHtml(item):`<p class="small muted">Giữ nguyên dữ kiện và các ý hỏi từ tài liệu.</p>${item.images.map((src,index)=>`<figure><img src="${esc(import.meta.env.BASE_URL+src)}" alt="Đề gốc bài ${esc(item.code)}, phần ${index+1}; bản chép văn bản ở ngay dưới" ${index?'loading="lazy"':''}></figure>`).join('')}<details class="original-transcript"><summary>Bản chép văn bản của đề</summary><pre>${esc(item.originalText)}</pre></details>`}</section>${item.note?`<aside class="source-correction"><strong>Lưu ý dữ kiện / quy ước</strong><p>${esc(item.note)}</p></aside>`:''}<div class="answer-toggle"><button class="btn primary" data-solution-action="reveal" aria-expanded="${revealed}" aria-controls="worked-answer">${icon(revealed?'eye':'book')} ${revealed?'Ẩn lời giải':'Mở lời giải'}</button><span>Hãy thử tự trả lời trước khi xem.</span></div>${revealed?solutionHtml(item):'<div id="worked-answer" hidden></div>'}<div class="reading-marks" aria-label="Tự đánh giá"><strong>Tự đánh giá:</strong><button class="btn ${marks[item.id]?.state==='review'?'selected':''}" data-solution-action="mark" data-state="review" aria-pressed="${marks[item.id]?.state==='review'}">${icon('flag')} Cần ôn</button><button class="btn ${marks[item.id]?.state==='known'?'selected':''}" data-solution-action="mark" data-state="known" aria-pressed="${marks[item.id]?.state==='known'}">${icon('check')} Đã nắm</button><span role="status" class="small muted">${markLabel(item)}</span></div><details class="solution-references"><summary>${icon('book')} Nguồn đối chiếu</summary><ul>${refHtml}</ul></details></article><nav class="item-pagination" aria-label="Bài trước và sau">${at>0?link(href('bai/'+siblings[at-1].id),icon('back')+' Bài trước','btn'):'<span></span>'}${link(groupHref(item),'Danh sách bài','btn')}${at<siblings.length-1?link(href('bai/'+siblings[at+1].id),'Bài tiếp '+icon('arrow'),'btn primary'):'<span></span>'}</nav>`;
  }
  function sourcesPage():string {
    return `${link(href(),icon('back')+' Trang Xử lý ảnh','text-link')}<h1>Nguồn & quy ước tính</h1><section class="source-panel"><h2>168 câu/bài từ đúng hai bộ tài liệu</h2><p>Ngân hàng: 51 mục; cô Uyên: 117 mục. Bản Theory Questions.pdf trùng 28 câu của Lý thuyết.pdf nên không tính hai lần.</p><p>Chương trên web theo slide và bộ cô Uyên. Số chương của giáo trình PTIT khác; mỗi lời giải ghi trang PDF để tra chính xác.</p><ul><li>Nhân chập thực hành: đặt tâm, không lật mặt nạ, ngoài ảnh bằng 0; giữ đáp ứng có dấu nếu đề yêu cầu cộng.</li><li>Khuếch tán lỗi: đặt lại sai số ở đầu dòng, dùng đúng ngưỡng của từng bài.</li><li>Cân bằng histogram: phân biệt công thức giáo trình và công thức slide.</li><li>Phân vị đối xứng nền: chương 3 lấy mức cuối không vượt p%; chương 5 lấy mức đầu đạt p%, theo quy ước ghi trong từng bộ.</li><li>SE không đối xứng: phân biệt giãn theo hit B và giãn chuẩn dùng B phản xạ.</li><li>RLC/Huffman/LZW: nêu quy ước, không tính chi phí bảng mã/header khi đề chưa yêu cầu.</li></ul><p>${esc(data.exam.note)}</p></section><section class="source-panel"><h2>Các mục có lưu ý nguồn</h2><ul>${data.items.filter(i=>i.note).map(i=>`<li><a href="${href('bai/'+i.id)}">${esc(i.id)} — ${esc(i.title)}</a><p>${esc(i.note)}</p></li>`).join('')}</ul></section><section class="source-panel"><h2>Danh mục tài liệu</h2>${data.sources.map(s=>`<p><strong>${esc(s.title)}</strong> · ${s.pages} trang <small>${esc(s.path)}</small></p>`).join('')}</section>`;
  }
  function render():void {
    if(disposed)return;
    const path=route();let content='';let match:RegExpMatchArray|null;
    if(!path)content=landing();
    else if(path==='ngan-hang')content=groups('bank');
    else if(path==='co-uyen')content=groups('uyen');
    else if(path==='can-on')content=list('Những bài cần ôn lại',data.items,'review');
    else if(path==='nguon')content=sourcesPage();
    else if((match=path.match(/^ngan-hang\/([1-4])$/)))content=list(`giải ngân hàng · ${match[1]} điểm`,data.items.filter(i=>i.area==='bank'&&i.points===Number(match![1])),'bank'+match[1]);
    else if((match=path.match(/^co-uyen\/chuong\/(\d+)$/))&&data.chapters.some(c=>c.number===Number(match![1])))content=list(`Chương ${match[1]} · ${chapterName(Number(match[1]))}`,data.items.filter(i=>i.area==='uyen'&&i.chapter===Number(match![1])),'uyen'+match[1]);
    else if(path.startsWith('bai/')&&itemMap.has(path.slice(4)))content=itemPage(itemMap.get(path.slice(4))!);
    else content=`<div class="empty-state"><h1>Không tìm thấy phần này</h1>${link(href(),'Về môn Xử lý ảnh')}</div>`;
    document.title=`${path.startsWith('bai/')?itemMap.get(path.slice(4))?.title+' — ':''}${subject.name} — Nắm ý`;
    app.innerHTML=catalogShell(`<div class="solutions-page">${!storageAvailable?'<p class="storage-notice" role="status">Trình duyệt chưa lưu được tự đánh giá. Bạn vẫn đọc và làm bài bình thường.</p>':''}${content}</div>`,subjects,subject.id);
    const nav=app.querySelector('aside nav');
    nav?.insertAdjacentHTML('beforeend',`<p class="nav-label">XỬ LÝ ẢNH</p><a class="nav-link ${path.startsWith('ngan-hang')?'active':''}" href="${href('ngan-hang')}">${icon('book')}giải ngân hàng</a><a class="nav-link ${path.startsWith('co-uyen')?'active':''}" href="${href('co-uyen')}">${icon('layers')}giải bài cô Uyên</a><a class="nav-link ${path==='can-on'?'active':''}" href="${href('can-on')}">${icon('flag')}Cần ôn lại</a>`);
    if(app.querySelector('[data-math]'))void import('../../shared/math.ts').then(m=>{if(!disposed)m.renderMath(app);});
  }
  function updateResults():void {
    const results=app.querySelector<HTMLElement>('#solution-results');
    if(results)results.innerHTML=rows((results.dataset.ids??'').split(',').map(id=>itemMap.get(id)).filter((i):i is SolvedItem=>!!i));
  }
  function onClick(event:Event):void {
    const target=(event.target as Element).closest<HTMLElement>('[data-solution-action],[data-action]');if(!target)return;
    if(target.dataset.action==='menu'){
      const sidebar=app.querySelector('.sidebar');const open=!sidebar?.classList.contains('open');sidebar?.classList.toggle('open',open);app.querySelector('.mobile-shade')?.classList.toggle('visible',open);app.querySelector('.menu-toggle')?.setAttribute('aria-expanded',String(open));return;
    }
    const item=itemMap.get(route().replace(/^bai\//,''));if(!item)return;
    if(target.dataset.solutionAction==='answer-part'){
      const num=Number(target.dataset.page);if(!Number.isInteger(num))return;
      const figure=app.querySelector<HTMLElement>(`.answer-document-page[data-document-page="${num}"]`);
      if(figure){const offset=Number(target.dataset.offset);const img=figure.querySelector('img')!;const bounds=img.getBoundingClientRect();window.scrollTo({top:window.scrollY+bounds.top+bounds.height*(Number.isFinite(offset)&&offset>=0&&offset<1?offset:0)-16,behavior:'smooth'});}return;
    }
    if(target.dataset.solutionAction==='reveal'){
      const y=window.scrollY;revealed=!revealed;render();window.scrollTo(0,y);
      app.querySelector<HTMLElement>('[data-solution-action=reveal]')?.focus({preventScroll:true});
    }
    if(target.dataset.solutionAction==='mark'){
      const next=target.dataset.state as 'known'|'review';if(!['known','review'].includes(next))return;
      if(marks[item.id]?.state===next)delete marks[item.id];else marks[item.id]={revision:item.revision,state:next};
      try { localStorage.setItem(readingKey(subject.id),JSON.stringify(marks));storageAvailable=true; } catch { storageAvailable=false; }
      const y=window.scrollY;render();window.scrollTo(0,y);app.querySelector<HTMLElement>(`[data-state="${next}"]`)?.focus({preventScroll:true});
    }
  }
  function onInput(event:Event):void {
    const el=event.target as HTMLInputElement;
    if(el.id==='solution-search'){query=el.value;updateResults();}
    if(el.id==='solution-kind'){kind=el.value;updateResults();}
    if(el.id==='solution-state'){state=el.value;updateResults();}
  }
  app.addEventListener('click',onClick);app.addEventListener('input',onInput);
  render();
  return {render,dispose:()=>{disposed=true;app.removeEventListener('click',onClick);app.removeEventListener('input',onInput);}};
}
