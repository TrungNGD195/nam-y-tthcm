import type { Bank, Concept, Deck, Progress, Question, Session, Subject } from '../../core/types.ts';
import { checkCurrent, createSession, finishSession, needsReview, normalize, scoreSession, selectQuestions, toggleBookmark } from '../../core/engine.ts';
import { emptyProgress, loadProgress, parseProgress, saveProgress, storageKey } from '../../core/storage.ts';
import { button, durationText, emphasize, esc, icon, link, pill, progressBar, promptText, referencesHtml, sourceDetails, sourceName, sourceLocation, renderBlocks } from '../../shared/ui.ts';

import { resolveRoute, scopeSubjectLinks, subjectHref } from '../../app/router.ts';
import { subjects } from '../../app/subjects.ts';
import { buildComprehensivePapers } from '../../core/comprehensive.ts';
import '../../shared/styles/comprehensive.css';

export type StudyController = { render: () => void; dispose: () => void };
export function mountStudy(subject: Subject, bank: Bank): StudyController {
const events = new AbortController();
const routeHash = (): string => { const route=resolveRoute(location.hash); return route.kind==='subject' && route.subjectId===subject.id ? route.localHash : '#/'; };
const collection = () => subject.collections.find(c => routeHash() === '#/' + c.id) ?? subject.collections[0];
const examSize = Math.min(subject.examSize ?? 20, bank.questions.length);
const comprehensiveSize=subject.comprehensiveExamSize;
const papers=comprehensiveSize?buildComprehensivePapers(bank.questions,comprehensiveSize,`${subject.id}:${bank.version}`):[];
const specialTags=new Set(subject.collections.flatMap(c=>c.tags));
const isSpecial=(q:Question)=>q.tags.some(tag=>specialTags.has(tag));

const qmap = new Map(bank.questions.map(q => [q.id, q]));
const app = document.querySelector<HTMLDivElement>('#app')!;
const dialog = document.querySelector<HTMLDialogElement>('#dialog')!;
const loaded = loadProgress(qmap, bank.version, subject.id);
let progress: Progress = loaded.progress;
let storageWarning = loaded.warning;
let menuOpen = false;
let count = 10;
let order: 'unseen' | 'random' = 'unseen';
let includeNumbers = false;
let numberTag = 'all';
let minutes = 0;
let keywordQuery = '';
let keywordFilter = 'all';
let keywordHidden = true;
let resultFilter = 'all';
const revealed = new Set<string>();
let pendingStart: { deck: Deck; mode: Session['mode']; minutes: number; specific?: Question[] } | null = null;
let returnFocus: HTMLElement | null = null;

function persist(): void {
  if (!saveProgress(progress) && !storageWarning) {
    storageWarning = 'Trình duyệt chưa cho lưu tiến độ. Bạn vẫn học bình thường; hãy xuất tiến độ trước khi đóng trang.';
    toast(storageWarning);
  }
}
function toast(message: string): void {
  const el = document.createElement('div');
  el.className = 'toast'; el.textContent = message;
  document.querySelector('#toasts')!.append(el);
  setTimeout(() => el.remove(), 5500);
}
function go(hash: string): void {
  const scoped=subjectHref(subject.id,hash);
  if (location.hash === scoped) render();
  else location.hash = scoped;
}
function openDialog(title: string, body: string, actions: string): void {
  returnFocus = document.activeElement as HTMLElement | null;
  dialog.innerHTML = `<h2 id="dialog-title">${esc(title)}</h2>${body}<div class="dialog-actions">${actions}</div>`;
  dialog.showModal();
}
dialog.addEventListener('close', () => { if (returnFocus?.isConnected) returnFocus.focus(); }, { signal: events.signal });

const countSeen = () => Object.values(progress.records).filter(r => r.seen > 0).length;
const reviewQuestions = () => bank.questions.filter(q => needsReview(progress.records[q.id]));
const chapterQuestions = (n: number, numbers = true) => bank.questions.filter(q => q.chapter === n && (numbers || !isSpecial(q)));
const conceptQuestions = (c: Concept) => bank.questions.filter(q => q.conceptId === c.id);
function conceptDone(c: Concept): boolean {
  return conceptQuestions(c).some(q => progress.records[q.id]?.lastOutcome === 'correct');
}
function coverage(chapter: number): { done: number; total: number } {
  const concepts = bank.concepts.filter(c => c.core && c.chapter === chapter && conceptQuestions(c).length);
  return { done: concepts.filter(conceptDone).length, total: concepts.length };
}
function breadcrumb(): string {
  const hash = routeHash();
  const chapterMatch = hash.match(/^#\/chuong\/(\d+)$/);
  if (chapterMatch) return `Chương ${chapterMatch[1]}`;
  const currentCollection=subject.collections.find(c=>hash==='#/'+c.id);if(currentCollection)return currentCollection.title;
  return ({ '#/': 'Tổng quan', '#/de-tong-hop': 'Luyện đề tổng hợp', '#/thi-thu': 'Thi thử', '#/can-on': 'Cần ôn', '#/keyword': 'Sổ keyword', '#/lam-bai': 'Đang làm bài', '#/ket-qua': 'Kết quả', '#/nguon': 'Nguồn & tiến độ' } as Record<string,string>)[hash] ?? 'Trang không tìm thấy';
}
function navItem(hash: string, name: string, symbol: string, badge = ''): string {
  const active = routeHash() === hash;
  return `<a href="${hash}" class="nav-link ${active ? 'active' : ''}" ${active ? 'aria-current="page"' : ''}>${icon(symbol)}<span>${name}</span>${badge ? `<span class="count">${badge}</span>` : ''}</a>`;
}
function shell(content: string): string {
  return `<button class="mobile-shade ${menuOpen ? 'visible' : ''}" data-action="menu" aria-label="Đóng menu"></button>
    <aside class="sidebar ${menuOpen ? 'open' : ''}" aria-label="Điều hướng học tập">
      <a href="#/" data-global class="brand" aria-label="Nắm ý — về tổng quan"><span class="brand-mark">${icon('book')}</span><span><span class="brand-name">Nắm ý<span style="color:#ad795d">.</span></span><span class="brand-sub" style="display:block">ÔN TẬP NHIỀU MÔN</span></span></a>
      <nav><a href="#/" data-global class="nav-link">${icon('back')}<span>Tất cả môn học</span></a>${navItem('#/', 'Tổng quan', 'home')}
      <p class="nav-label">Nội dung ôn tập</p>
      ${bank.chapters.map(c => `<a href="#/chuong/${c.number}" class="nav-link ${(routeHash() === `#/chuong/${c.number}`) ? 'active' : ''}" ${routeHash() === `#/chuong/${c.number}` ? 'aria-current="page"' : ''}><span class="chapter-index">${String(c.number).padStart(2,'0')}</span><span>${esc(c.shortTitle)}</span></a>`).join('')}
      <p class="nav-label">Luyện & ghi nhớ</p>
      ${papers.length?navItem('#/de-tong-hop','Luyện đề tổng hợp','target',String(comprehensiveSize)):''}${subject.collections.map(c=>navItem('#/'+c.id,c.title,c.icon)).join('')}${navItem('#/thi-thu',`Thi thử ${examSize} câu`,'target')}${navItem('#/can-on','Câu cần ôn','flag',String(reviewQuestions().length))}${navItem('#/keyword','Sổ keyword','layers')}
      </nav><div class="sidebar-footer">${navItem('#/nguon','Nguồn & tiến độ','info')}<div class="local-note"><span class="local-dot"></span>Miễn phí · Không cần đăng nhập</div></div>
    </aside>
    <div class="shell"><header class="topbar"><button class="icon-button menu-toggle" data-action="menu" aria-label="Mở menu" aria-expanded="${menuOpen}">${icon('menu')}</button><div class="breadcrumbs"><span class="bread-root">${esc(subject.name)}</span>${icon('chevron')}<strong>${esc(breadcrumb())}</strong></div><div class="topbar-right"><span class="status-label">${icon(storageWarning?'info':'check')}${storageWarning?'Kiểm tra trạng thái lưu':'Lưu trên trình duyệt'}</span><label class="subject-switch-label"><span class="sr-only">Đổi môn học</span><select id="subject-switch" aria-label="Đổi môn học">${subjects.map(s=>`<option value="${s.id}" ${s.id===subject.id?'selected':''}>${esc(s.shortName)}${s.status==='ready'?'':' (chờ tài liệu)'}</option>`).join('')}</select></label></div></header>
    ${storageWarning ? `<div class="warning-banner" role="status">${esc(storageWarning)}</div>` : ''}
    <main id="main" class="page" tabindex="-1">${content}</main></div>`;
}
function pageIntro(label: string, title: string, description: string, extra = ''): string {
  return `<div class="page-intro"><div class="eyebrow">${esc(label)}</div><div class="title-line"><h1>${esc(title)}</h1>${extra}</div><p>${esc(description)}</p></div>`;
}
function home(): string {
  const active = progress.activeSession;
  return `<div class="page-intro"><div class="intro-label">${icon('leaf')} Mỗi ngày một chút, vững hơn từng chương</div><div class="title-line"><h1>${esc(subject.name)}</h1>${pill('ÔN TẬP THEO CHƯƠNG')}</div><p>Chọn một chương bên dưới để bắt đầu học. Mọi chương đều mở sẵn.</p></div>
    ${active ? `<div class="continue-banner">${icon('clock')}<div class="grow"><strong>Bạn còn một bài đang làm</strong><p>${esc(active.deck.title)} · ${active.items.filter(i => i.checked || i.selectedOptionId).length}/${active.items.length} câu đã trả lời</p></div>${link('#/lam-bai','Tiếp tục '+icon('arrow'),'btn small')}</div>` : ''}
    <section class="quick-start"><div><span class="eyebrow">MỚI BẮT ĐẦU?</span><h2>Học từ chương đầu tiên</h2><p>Đọc ý chính → làm câu hỏi → nhớ keyword.</p></div>${link('#/chuong/'+bank.chapters[0].number,'Bắt đầu học '+icon('arrow'))}</section>
    ${papers.length?`<section class="quick-start comprehensive-start"><div><span class="eyebrow">ÔN CẢ MÔN</span><h2>Luyện đề tổng hợp ${comprehensiveSize} câu</h2><p>${papers.length} đề · Chia đều chương · Dùng đủ ${bank.questions.length} câu, có cả câu số liệu.</p></div>${link('#/de-tong-hop','Chọn đề để làm '+icon('arrow'))}</section>`:''}
    <div class="stats"><div class="stat"><div class="stat-icon">${icon('book')}</div><div><div class="stat-number">${bank.questions.length}</div><div class="stat-label">câu sẵn sàng để luyện</div></div></div><div class="stat"><div class="stat-icon">${icon('check')}</div><div><div class="stat-number">${countSeen()}<span style="font-size:13px;color:#a0a493;font-weight:400"> / ${bank.questions.length}</span></div><div class="stat-label">câu bạn đã gặp</div></div></div><a class="stat" href="#/can-on"><div class="stat-icon">${icon('flag')}</div><div><div class="stat-number">${reviewQuestions().length}</div><div class="stat-label">câu cần ôn lại</div></div></a></div>
    <div class="section-head"><h2>Ôn tập theo chương</h2><p>${bank.chapters.length} chương · Mở tự do · Không giới hạn lượt</p></div>
    <div class="chapter-grid">${bank.chapters.map(c => {
      const cover = coverage(c.number), qs = chapterQuestions(c.number), normal = qs.filter(q => !isSpecial(q)).length;
      return `<a class="chapter-card" href="#/chuong/${c.number}"><div class="card-top"><span class="chapter-symbol">${icon(c.icon)}</span><span class="chapter-label">CHƯƠNG ${String(c.number).padStart(2,'0')}</span></div><h3>${esc(c.title)}</h3><p>${esc(c.description)}</p><div class="card-bottom"><div class="progress-caption"><span>${cover.done ? `${cover.done}/${cover.total} ý cốt lõi đã luyện đúng` : 'Bắt đầu từ kiến thức cốt lõi'}</span><span>${Math.round(cover.done / Math.max(1,cover.total)*100)}%</span></div>${progressBar(cover.done/Math.max(1,cover.total)*100,'Độ phủ ý cốt lõi chương '+c.number)}<div class="card-link"><span>${normal} câu kiến thức · ${qs.length-normal} câu chuyên đề</span></div><span class="chapter-cta">Học chương này ${icon('arrow')}</span></div></a>`;
    }).join('')}</div>
    <div class="feature-grid">${subject.collections.map(c=>`<a class="feature-card" href="#/${c.id}">${icon(c.icon)}<div><h3>${esc(c.title)}</h3><p>${esc(c.description)}</p></div>${icon('arrow','feature-arrow')}</a>`).join('')}<a class="feature-card exam" href="#/thi-thu">${icon('target')}<div><h3>Thử sức với đề ${examSize} câu</h3><p>Đề mẫu và đề trộn để tự kiểm tra</p></div>${icon('arrow','feature-arrow')}</a></div>
    <div class="page-foot"><span>Nắm ý · Học hiểu để tự tin làm bài</span><a href="#/nguon">${esc(subject.sourceDescription ?? 'Theo tài liệu và ngân hàng của môn')} ${icon('chevron')}</a></div>`;
}

function countPicker(): string {
  return `<div class="field"><span class="field-label">Số câu mỗi lượt</span><div class="segmented" role="group" aria-label="Số câu">${[10,20,9999].map(n => `<button data-action="count" data-value="${n}" class="${count===n?'active':''}" aria-pressed="${count===n}">${n===9999?'Tất cả':n+' câu'}</button>`).join('')}</div></div>`;
}
function setupPanel(kind: 'chapter' | 'numbers' | 'review', chapter?: number): string {
  const deck: Deck = { kind:kind==='numbers'?'collection':kind, chapter, tag: numberTag, tags:kind==='numbers'?collection()?.tags:subject.collections.flatMap(c=>c.tags), includeNumbers, count, title:'', order };
  const available = selectQuestions(bank.questions,{...deck,count:9999},progress.records).length;
  const actual = Math.min(count, available);
  return `<aside class="panel setup-panel"><span class="eyebrow">LUYỆN TẬP</span><h3>Một lượt, một bước tiến</h3><p class="small muted">${available} câu phù hợp với lựa chọn của bạn.</p>${countPicker()}
    ${kind==='chapter'?`<div class="field"><label class="check-label"><input id="include-numbers" type="checkbox" ${includeNumbers?'checked':''}>Kèm câu trong chuyên đề riêng</label></div>`:''}
    ${kind==='numbers'?`<div class="field"><label for="number-tag">Nhóm câu chuyên đề</label><select id="number-tag">${[['all','Tất cả nhóm'],...(collection()?.filters??[]).map(f=>[f.tag,f.label])].map(([v,t])=>`<option value="${v}" ${numberTag===v?'selected':''}>${t}</option>`).join('')}</select></div>`:''}
    <div class="field"><label for="question-order">Cách chọn câu</label><select id="question-order"><option value="unseen" ${order==='unseen'?'selected':''}>Ưu tiên câu chưa gặp</option><option value="random" ${order==='random'?'selected':''}>Ngẫu nhiên toàn bộ</option></select></div>
    ${button('start',`${icon('arrow')} Luyện ${actual} câu`,'btn primary full',`data-kind="${kind}" ${chapter?`data-chapter="${chapter}"`:''} ${actual?'':'disabled'}`)}<p class="setup-note">Xem lời giải sau từng câu · Làm lại tùy ý</p></aside>`;
}
function conceptCard(c: Concept, index: number): string {
  return `<article class="concept-card"><span class="concept-number">Ý CỐT LÕI ${String(index+1).padStart(2,'0')}</span><h3>${esc(c.title)}</h3><p>${emphasize(c.summary,c.keywords)}</p><div class="keywords">${c.keywords.map(k=>`<span class="keyword-chip">${esc(k)}</span>`).join('')}</div>${c.confusionNote?`<div class="confusion"><strong>Dễ nhầm:</strong> ${esc(c.confusionNote)}</div>`:''}<details class="sources-detail"><summary>${icon('book')} Căn cứ kiến thức</summary>${referencesHtml(c.references,bank.sources)}</details></article>`;
}
function chapterPage(n: number): string {
  const c = bank.chapters.find(c=>c.number===n)!, cover=coverage(n);
  const concepts=bank.concepts.filter(x=>x.chapter===n&&x.core);
  return `${pageIntro(`CHƯƠNG ${String(n).padStart(2,'0')}`,c.title,c.description,pill(`${cover.done}/${cover.total} ý đã luyện đúng`,'green'))}
    <div class="chapter-layout"><section><div class="lesson-note">${icon('spark')} <strong>Trước khi làm bài:</strong> nắm những ý dưới đây, rồi thử một lượt ngắn. Bạn có thể bắt đầu luyện ngay nếu đã học qua.</div>${concepts.map(conceptCard).join('')}<p class="inline-note">${subject.collections.length?`Một số câu được tập hợp vào <a href="#/${subject.collections[0].id}" style="text-decoration:underline">chuyên đề riêng</a>. Bật lựa chọn kèm câu chuyên đề nếu muốn ôn đủ chương.`:'Các câu hỏi được tổ chức theo nội dung chương trong tài liệu.'}</p></section>${setupPanel('chapter',n)}</div>`;
}
function numbersPage(): string {
  const group=collection();
  const filtered = bank.questions.filter(q=>q.tags.some(tag=>group?.tags.includes(tag)) && (numberTag==='all'||q.tags.includes(numberTag)));
  const ids = [...new Set(filtered.map(q=>q.conceptId))];
  const cs = ids.map(id=>bank.concepts.find(c=>c.id===id)!).filter(Boolean);
  return `${pageIntro('CHUYÊN ĐỀ RIÊNG',group?.title??'Chuyên đề',group?.description??'',pill(`${filtered.length} câu`,'orange'))}<div class="chapter-layout"><section><div class="lesson-note">${icon('calendar')} ${subject.id==='tthcm'?'Nhớ <strong>sự kiện ↔ mốc số</strong>. Với câu “có mấy ý”, nhớ cả tên các ý.':'Đối chiếu ý chính, cách áp dụng và điểm dễ nhầm trước khi luyện.'}</div>${cs.map(conceptCard).join('')}</section>${setupPanel('numbers')}</div>`;
}
function examPage(): string {
  return `${pageIntro('TỰ KIỂM TRA',`Thử sức với ${examSize} câu`,'Tập đọc kỹ đề, chọn đáp án và xem lại những ý còn chưa chắc.')}
    <div class="filter-bar"><label for="exam-minutes" class="small muted">Thời gian tự chọn</label><select id="exam-minutes" class="filter-select">${[[0,'Không giới hạn'],[15,'15 phút'],[20,'20 phút'],[30,'30 phút']].map(([v,t])=>`<option value="${v}" ${minutes===v?'selected':''}>${t}</option>`).join('')}</select><span class="small muted">Đây là thời gian luyện tập do bạn chọn.</span></div>
    <div class="exam-cards">${bank.sampleQuestionIds.length?`<article class="panel exam-card"><div class="large-icon">${icon('book')}</div><div class="row wrap" style="margin-bottom:12px">${pill('ĐỀ MẪU','red')}${pill(`${examSize} CÂU`)}</div><h2>${esc(subject.sampleTitle??'Đề mẫu')}</h2><p>Luyện đề có trong tài liệu của môn; giữ thứ tự câu gốc để đối chiếu và làm quen cách hỏi.</p>${button('start',`Làm đề mẫu ${icon('arrow')}`,'btn primary full','data-kind="sample"')}</article>`:''}
    <article class="panel exam-card"><div class="large-icon" style="background:#edf1e8;color:#71815c">${icon('target')}</div><div class="row wrap" style="margin-bottom:12px">${pill('ĐỀ TRỘN','green')}${pill(`${examSize} CÂU`)}</div><h2>Mỗi lượt một bộ câu mới</h2><p>Trộn câu từ ${bank.chapters.length} chương và các chuyên đề của môn. Phân bổ giữa các chương, ưu tiên các ý khác nhau để kiểm tra rộng hơn.</p>${button('start',`Tạo đề trộn ${icon('arrow')}`,'btn full','data-kind="mixed"')}</article></div>
    <div class="exam-info">${icon('info')} Đáp án và lời giải chỉ hiện sau khi nộp bài. Đề trộn phục vụ luyện tập, chưa phải ma trận hoặc thời lượng thi chính thức của trường. Bạn có thể thi lại không giới hạn.</div>
    ${progress.history.length?`<div class="section-head"><h2>Những lượt gần đây</h2><p>Lưu riêng trên trình duyệt này</p></div><div class="panel"><ul class="history-list">${progress.history.slice(0,5).map(h=>`<li><span>${esc(h.title)}<br><small>${new Date(h.at).toLocaleString('vi-VN')}</small></span><span><strong>${h.correct}/${h.total}</strong>${h.assisted?` · ${h.assisted} gợi ý`:''}</span></li>`).join('')}</ul></div>`:''}`;
}
function comprehensivePage(): string {
  if(!papers.length)return `<div class="empty-state"><h1>Môn này chưa có bộ đề tổng hợp</h1>${link('#/','Về tổng quan')}</div>`;
  const active=progress.activeSession;
  return `${pageIntro('ÔN TẬP TOÀN MÔN',`Luyện đề tổng hợp ${comprehensiveSize} câu`,`${papers.length} đề cố định, bao phủ toàn bộ ${bank.questions.length} câu hỏi đang có, gồm cả câu số liệu. Bạn có thể chọn bất kỳ đề nào và làm lại không giới hạn.`)}
    ${active?.deck.kind==='comprehensive'?`<div class="continue-banner">${icon('clock')}<div class="grow"><strong>${esc(active.deck.title)}</strong><p>${active.items.filter(i=>i.selectedOptionId!==null).length}/${active.items.length} câu đã chọn · Bài đang làm được tự lưu.</p></div>${link('#/lam-bai','Tiếp tục đề này '+icon('arrow'),'btn small')}</div>`:''}
    <section class="comprehensive-overview"><div><strong>${papers.length}</strong><span>đề để luyện</span></div><div><strong>${comprehensiveSize}</strong><span>câu mỗi đề</span></div><div><strong>${Math.floor(comprehensiveSize!/bank.chapters.length)}–${Math.ceil(comprehensiveSize!/bank.chapters.length)}</strong><span>câu / chương / đề</span></div><div><strong>${countSeen()}/${bank.questions.length}</strong><span>câu đã gặp trên web</span></div></section>
    <div class="comprehensive-note">${icon('info')}<p>Số câu của các chương không bằng nhau, nên một số câu sẽ lặp giữa các đề để chia đều chương và dùng hết ngân hàng. <strong>Trong mỗi đề, 50 câu đều khác nhau.</strong> Đáp án, lời giải và keyword hiện sau khi nộp bài.</p></div>
    <div class="filter-bar"><label for="exam-minutes" class="small muted">Thời gian làm mỗi đề</label><select id="exam-minutes" class="filter-select">${[[0,'Không giới hạn'],[15,'15 phút'],[20,'20 phút'],[30,'30 phút'],[45,'45 phút'],[60,'60 phút'],[90,'90 phút']].map(([v,t])=>`<option value="${v}" ${minutes===v?'selected':''}>${t}</option>`).join('')}</select></div>
    <section class="comprehensive-grid" aria-label="Danh sách đề tổng hợp">${papers.map(paper=>{
      const seen=paper.questionIds.filter(id=>(progress.records[id]?.seen??0)>0).length;
      const last=progress.history.find(h=>h.title===paper.title&&h.mode==='exam');
      const continuing=active?.deck.kind==='comprehensive'&&active.deck.title===paper.title;
      return `<article class="comprehensive-card" data-paper="${paper.id}"><div class="row between"><span class="eyebrow">ĐỀ ${paper.id}</span>${pill(continuing?'ĐANG LÀM':last?'ĐÃ NỘP':'50 CÂU',last?'green':'')}</div><h2>Đề tổng hợp ${paper.id}</h2><div class="paper-chapters" aria-label="Số câu từng chương">${paper.chapterCounts.map(c=>`<span>Ch${c.chapter}: <strong>${c.count}</strong></span>`).join('')}</div><p class="small muted">Đã gặp ${seen}/50 câu${last?` · Lần nộp gần nhất: ${last.correct}/${last.total}`:''}</p>${continuing?link('#/lam-bai','Tiếp tục đề này '+icon('arrow'),'btn primary full'):button('start-paper','Làm đề này '+icon('arrow'),'btn primary full',`data-paper="${paper.id}"`)}</article>`;
    }).join('')}</section>`;
}
function reviewPage(): string {
  const qs = reviewQuestions();
  if (!qs.length) return `${pageIntro('ÔN LẠI','Những câu cần thêm một lần nhớ','Câu sai, bỏ qua, dùng gợi ý và câu bạn đánh dấu sẽ xuất hiện ở đây.')}<div class="empty-state">${icon('leaf')}<h2>Chưa có câu cần ôn</h2><p>Bắt đầu một lượt luyện. Khi có câu chưa chắc, Nắm ý sẽ giúp bạn tìm lại để ôn.</p>${link('#/','Chọn chương để học '+icon('arrow'))}</div>`;
  return `${pageIntro('ÔN LẠI','Thêm một lần, nhớ chắc hơn',`${qs.length} câu sai, bỏ qua, dùng gợi ý hoặc được bạn đánh dấu.`)}<div class="chapter-layout"><section class="review-list">${qs.map(q=>{
    const r=progress.records[q.id];
    return `<article class="review-item"><span class="chapter-index">0${q.chapter}</span><div class="grow"><small>CHƯƠNG ${q.chapter} · ${esc(q.topic)}</small><p>${promptText(q.prompt)}</p><div class="row wrap">${pill(r.lastOutcome==='assisted'?'Đã dùng gợi ý':r.lastOutcome==='skipped'?'Đã bỏ qua':r.lastOutcome==='incorrect'?'Cần luyện lại':'Đã đánh dấu','orange')}${r.bookmarked?pill('Đánh dấu'):''}</div></div>${button('bookmark',icon('flag'),'icon-button '+(r.bookmarked?'bookmark active':''),`data-id="${q.id}" aria-label="${r.bookmarked?'Bỏ đánh dấu':'Đánh dấu'} câu này" aria-pressed="${r.bookmarked}"`)}</article>`;
  }).join('')}</section>${setupPanel('review')}</div>`;
}
function keywordsPage(): string {
  const numericConcepts = new Set(bank.questions.filter(isSpecial).map(q=>q.conceptId));
  const cs=bank.concepts.filter(c=>conceptQuestions(c).length).filter(c=>(keywordFilter==='all'||keywordFilter==='numbers'&&numericConcepts.has(c.id)||String(c.chapter)===keywordFilter)&&normalize([c.title,c.summary,...c.keywords].join(' ')).includes(normalize(keywordQuery)));
  return `${pageIntro('GHI NHỚ CHỦ ĐỘNG','Đọc cụm gợi nhớ. Tự gọi ra ý chính.','Keyword giúp nhận ra kiến thức; luôn kiểm tra từ KHÔNG, SAI và ĐÚNG NHẤT trong đề.')}
    <div class="filter-bar"><div class="search-wrap">${icon('search')}<input id="keyword-search" class="search-input" type="search" value="${esc(keywordQuery)}" placeholder="Tìm ý chính, keyword, chủ đề…" aria-label="Tìm keyword"></div><select id="keyword-filter" class="filter-select" aria-label="Lọc keyword theo chương">${[['all','Tất cả chương'],...bank.chapters.map(c=>[String(c.number),`Chương ${c.number}`]),['numbers','Chuyên đề riêng']].map(([v,t])=>`<option value="${v}" ${v===keywordFilter?'selected':''}>${t}</option>`).join('')}</select>${button('hide-keywords',`${icon('eye')} ${keywordHidden?'Hiện tất cả':'Che tất cả'}`,'btn',`aria-pressed="${!keywordHidden}"`)}</div>
    <p class="small muted">${cs.length} cụm kiến thức · Tìm kiếm có dấu hoặc không dấu đều được.</p>
    ${cs.length?`<div class="keyword-grid">${cs.map(c=>{
      const show=!keywordHidden||revealed.has(c.id);
      const cue=conceptQuestions(c).sort((a,b)=>a.prompt.length-b.prompt.length)[0]?.prompt??c.title;
      return `<article class="keyword-card" data-concept="${c.id}">${pill('CHƯƠNG '+c.chapter)}<h3>${promptText(cue)}</h3>${show?`<div class="reveal"><strong>${esc(c.title)}</strong><br>${emphasize(c.summary,c.keywords)}<div class="keywords">${c.keywords.map(k=>`<span class="keyword-chip">${esc(k)}</span>`).join('')}</div>${c.confusionNote?`<div class="confusion">${esc(c.confusionNote)}</div>`:''}</div>`:'<p class="small muted" style="margin:17px 0 0">Bạn nhớ ý chính là gì? Thử nhẩm trước khi mở.</p>'}${button('reveal',`${icon('eye')} ${show?'Che ý chính':'Xem ý chính'}`,'btn small',`data-id="${c.id}" aria-expanded="${show}"`)}</article>`;
    }).join('')}</div>`:`<div class="empty-state">${icon('search')}<h2>Chưa tìm thấy cụm phù hợp</h2><p>Thử một từ ngắn hơn hoặc chọn tất cả chương.</p>${button('clear-search','Xóa bộ lọc','btn')}</div>`}`;
}

function feedback(q: Question, item: Session['items'][number]): string {
  const correct=item.selectedOptionId===q.correctOptionId;
  return `<section class="feedback ${correct?'':'wrong'}" aria-live="polite"><div class="feedback-title">${icon(correct?'check':'info')}${correct?(item.usedHint?'Đúng với gợi ý — thử nhớ lại ở lượt sau':'Chính xác. Chốt lại ý này nhé!'):item.selectedOptionId===null?'Chưa trả lời — cùng chốt kiến thức':'Chưa đúng. Nhớ điểm phân biệt này.'}</div><p class="correct-answer"><strong>Đáp án:</strong> ${esc(q.options.find(o=>o.id===q.correctOptionId)!.text)}</p><p>${emphasize(q.explanation,q.keywords)}</p>${renderBlocks(q.explanationBlocks)}<div class="keywords">${q.keywords.map(k=>`<span class="keyword-chip">${esc(k)}</span>`).join('')}</div>${q.confusionNote?`<div class="confusion"><strong>Dễ nhầm:</strong> ${esc(q.confusionNote)}</div>`:''}${sourceDetails(q,bank.sources)}</section>`;
}
function quizPage(): string {
  const s=progress.activeSession;
  if (!s) return `<div class="empty-state">${icon('book')}<h1>Bạn chưa có bài đang làm</h1><p>Chọn chương hoặc một đề để bắt đầu.</p>${link('#/','Chọn bộ câu hỏi')}</div>`;
  const item=s.items[s.cursor],q=qmap.get(item.questionId)!;
  const answered=s.items.filter(i=>s.mode==='practice'?i.checked:i.selectedOptionId!==null).length;
  const showAnswer=s.mode==='practice'&&item.checked;
  const record=progress.records[q.id];
  return `<div class="quiz-header"><div><div class="eyebrow">${s.mode==='practice'?'LUYỆN TẬP':'THI THỬ'} · ${esc(s.deck.title)}</div><h1>Từng câu một, vững từng ý.</h1><div class="quiz-top-meta">${s.mode==='practice'?'Lời giải hiện sau khi kiểm tra':'Đáp án được giữ kín đến khi nộp bài'} · ${s.items.length} câu</div></div>${button('save-exit','Lưu và thoát','btn')}</div>
    <div class="question-progress"><div class="progress-caption"><span>Đã trả lời ${answered}/${s.items.length}</span><span>${s.mode==='exam'&&s.deadline?`<span id="timer" class="quiz-timer" aria-label="Thời gian còn lại">${durationText(s.deadline-Date.now())}</span>`:`Câu ${s.cursor+1}/${s.items.length}`}</span></div>${progressBar(answered/s.items.length*100,'Tiến độ lượt làm')}</div>
    <div class="quiz-layout"><section class="panel question-card" data-quiz><div class="question-head"><div class="row wrap">${pill('CHƯƠNG '+q.chapter)}${q.tags.map(tag=>subject.collections.flatMap(c=>c.filters).find(f=>f.tag===tag)?.label).filter(Boolean).map(label=>pill(label!,'orange')).join('')}${q.originType==='converted'?pill('ĐÃ BIÊN TẬP'):''}</div>${button('bookmark',icon('flag'),'icon-button bookmark '+(record?.bookmarked?'active':''),`data-id="${q.id}" aria-label="${record?.bookmarked?'Bỏ đánh dấu':'Đánh dấu'} câu này" aria-pressed="${!!record?.bookmarked}"`)}</div>
    <h2 id="question-prompt" tabindex="-1">${promptText(q.prompt)}</h2>${renderBlocks(q.blocks)}<div class="options" role="radiogroup" aria-labelledby="question-prompt">${item.optionOrder.map((id,index)=>{
      const o=q.options.find(x=>x.id===id)!; const selected=item.selectedOptionId===id; const right=showAnswer&&id===q.correctOptionId;const wrong=showAnswer&&selected&&!right;
      return `<button type="button" data-action="choose" data-option="${id}" data-focus="option-${id}" class="option ${selected?'selected':''} ${right?'correct':''} ${wrong?'incorrect':''}" role="radio" aria-checked="${selected}" ${showAnswer?'disabled':''}><span class="option-letter">${String.fromCharCode(65+index)}</span><span class="option-text">${esc(o.text)}${renderBlocks(o.blocks)}</span>${right||wrong?icon(right?'check':'x','result-icon'):''}</button>`;
    }).join('')}</div>
    ${item.usedHint&&!showAnswer?`<div class="hint">${icon('spark')} Gợi ý nhận diện: <strong>${esc(q.keywords.join(' · '))}</strong><br><span class="small">Lượt có gợi ý được ghi nhận riêng.</span></div>`:''}
    ${showAnswer?feedback(q,item):''}
    <div class="question-actions"><div class="row">${button('previous',`${icon('back')} Trước`,'btn ghost',s.cursor===0?'disabled':'')}${s.mode==='practice'&&!item.checked?button('hint',`${icon('spark')} Gợi ý`,'btn ghost',item.usedHint?'disabled':''):''}</div><div class="row wrap">${s.mode==='practice'&&!item.checked?`${button('skip','Bỏ qua','btn ghost')}${button('check',`Kiểm tra ${icon('check')}`,'btn primary',item.selectedOptionId===null?'disabled':'')}`:button('next',`${s.cursor===s.items.length-1?(s.mode==='exam'?'Nộp bài':'Xem kết quả'):'Câu tiếp'} ${icon('arrow')}`)}</div></div><p class="shortcuts"><kbd>1</kbd>–<kbd>${q.options.length}</kbd> chọn đáp án <span style="margin:0 9px">·</span><kbd>Enter</kbd> ${s.mode==='practice'&&!item.checked?'kiểm tra':'câu tiếp'}</p></section>
    <aside class="panel question-nav"><h3>Các câu trong lượt</h3><div class="question-grid">${s.items.map((i,index)=>{
      const correct=i.checked&&i.selectedOptionId===qmap.get(i.questionId)?.correctOptionId;
      const state=i.checked?(correct?'right':'wrong'):i.selectedOptionId!==null?'answered':'';
      return `<button class="question-num ${state} ${index===s.cursor?'current':''} ${progress.records[i.questionId]?.bookmarked?'flagged':''}" data-action="jump" data-index="${index}" aria-label="Câu ${index+1}${i.checked?(correct?', đúng':', cần ôn'):i.selectedOptionId?', đã chọn':', chưa làm'}" ${index===s.cursor?'aria-current="step"':''}>${index+1}</button>`;
    }).join('')}</div><div class="nav-legend"><span></span> Đã trả lời<br><span class="empty-dot"></span> Chưa làm</div>${button('finish',s.mode==='exam'?'Nộp bài':'Kết thúc lượt','btn full small','style="margin-top:20px"')}<p class="setup-note">${s.mode==='exam'?'Kiểm tra lại trước khi nộp.':'Bạn có thể quay lại xem câu đã chấm.'}</p></aside></div>`;
}
function resultPage(): string {
  const s=progress.lastResult;
  if (!s) return `<div class="empty-state">${icon('target')}<h1>Chưa có kết quả</h1><p>Hoàn thành một lượt luyện để xem lại kiến thức.</p>${link('#/','Bắt đầu ôn')}</div>`;
  const score=scoreSession(s,qmap);
  const todo=s.items.filter(i=>i.selectedOptionId!==qmap.get(i.questionId)?.correctOptionId||i.usedHint||progress.records[i.questionId]?.bookmarked);
  const items=s.items.filter(i=>resultFilter==='all'||resultFilter==='wrong'&&i.selectedOptionId!==qmap.get(i.questionId)?.correctOptionId||resultFilter==='hint'&&i.usedHint);
  return `<div class="eyebrow">KẾT QUẢ · ${esc(s.deck.title)}</div><section class="panel result-hero"><div class="score-ring" style="--score:${score.correct/score.total*100}%"><div class="score-ring-inner"><strong>${(score.correct/score.total*10).toLocaleString('vi-VN',{maximumFractionDigits:1})}</strong><span>trên 10 điểm</span></div></div><div class="result-copy"><h1>${score.correct===score.total?'Một lượt làm rất vững!':'Bạn đã biết mình cần ôn gì.'}</h1><p>${score.correct===score.total?'Tiếp tục thử bộ khác và tự nhớ lại ở lượt sau.':'Xem lại keyword ở những câu chưa chắc, rồi thử thêm một lần.'}</p><div class="result-bits"><span><strong>${score.correct}/${score.total}</strong> câu đúng</span><span><strong>${score.incorrect}</strong> sai</span><span><strong>${score.skipped}</strong> bỏ qua</span><span><strong>${score.assisted}</strong> đúng có gợi ý</span><span>${icon('clock')} ${durationText((s.finishedAt??Date.now())-s.startedAt)}</span></div></div></section>
    <div class="result-actions">${todo.length?button('retry-review',`${icon('refresh')} Luyện ${todo.length} câu cần ôn`):pill('Không có câu cần ôn trong lượt này','green')}${button('retry',`${icon('refresh')} Luyện lại bộ này`,'btn')}${s.deck.kind==='comprehensive'?link('#/de-tong-hop','Chọn đề tổng hợp khác','btn'):''}${link('#/','Về tổng quan','btn ghost')}</div>
    <div class="filter-bar"><div class="tabs" role="tablist" aria-label="Lọc kết quả">${[['all','Tất cả'],['wrong','Sai & bỏ qua'],['hint','Dùng gợi ý']].map(([value,label])=>`<button class="tab" role="tab" aria-selected="${resultFilter===value}" data-action="result-filter" data-value="${value}">${label}</button>`).join('')}</div></div>
    ${items.length?items.map((i)=>{const q=qmap.get(i.questionId)!,correct=i.selectedOptionId===q.correctOptionId;const sourceIndex=s.items.indexOf(i)+1;return `<details class="result-item ${correct?'':'failed'}"><summary>${icon(correct?'check':'info')}<span class="grow"><span class="small muted">CÂU ${sourceIndex} · CHƯƠNG ${q.chapter}</span><br>${promptText(q.prompt)}</span>${icon('chevron')}</summary><div class="result-item-content">${!correct?`<p class="chosen-answer">Bạn chọn: ${i.selectedOptionId?esc(q.options.find(o=>o.id===i.selectedOptionId)?.text):'Chưa trả lời'}</p>`:''}${feedback(q,i)}</div></details>`}).join(''):`<div class="empty-state">${icon('check')}<h2>Không có câu trong nhóm này</h2><p>Chọn bộ lọc khác để xem lại các ý đã học.</p></div>`}`;
}
function sourcesPage(): string {
  const pending=bank.audit.filter(a=>a.status==='pending'||a.status==='disputed');
  return `${pageIntro('NỘI DUNG CÓ CĂN CỨ','Nguồn rõ ràng. Tiến độ của riêng bạn.','Câu hỏi bám ngân hàng trong môn, giải thích ngắn và có nơi để đối chiếu.')}
    <p class="sources-summary">Bản hiện tại có <strong>${bank.questions.length} câu chuẩn</strong> từ ${bank.audit.length} mục ngân hàng chính. Những mục thiếu đáp án hợp lệ hoặc còn mâu thuẫn được giữ riêng, không dùng để chấm điểm. Phần căn cứ trong lời giải là diễn giải nội dung tài liệu, không phải trích dẫn nguyên văn.</p>
    <div class="source-grid">${bank.sources.filter(s=>s.kind==='bank'||s.kind==='theory').map(s=>`<article class="source-card"><h3>${icon('book')} ${sourceName(s)}</h3><p>${s.locatorLabel==='mục'?'Nguồn trực tuyến':`${s.pages} ${s.locatorLabel==='câu'?'câu':'trang PDF'}`} · ${s.kind==='bank'?'Nguồn câu hỏi':'Căn cứ kiến thức'}</p></article>`).join('')}</div>
    <div class="section-head"><h2>Độ phủ ngân hàng chính</h2><p>Đếm mục nguồn, không nhân đôi câu trùng</p></div><div class="audit-table-wrap"><table><thead><tr><th>Nguồn</th><th>Tổng mục</th><th>Đưa vào</th><th>Gộp trùng</th><th>Chờ kiểm tra</th></tr></thead><tbody>${bank.sources.filter(s=>s.kind==='bank').map(s=>s.id).map(id=>{const items=bank.audit.filter(a=>a.sourceId===id);return `<tr><td>${esc(bank.sources.find(s=>s.id===id)?.shortTitle)}</td><td>${items.length}</td><td>${items.filter(a=>a.status==='published').length}</td><td>${items.filter(a=>a.status==='merged').length}</td><td>${items.filter(a=>a.status==='pending'||a.status==='disputed').length}</td></tr>`}).join('')}</tbody></table></div>
    <details class="panel" style="margin-top:18px"><summary style="cursor:pointer;font-size:13px;font-weight:600">${pending.length} mục chưa dùng để chấm — xem lý do</summary>${pending.map(a=>{const source=bank.sources.find(s=>s.id===a.sourceId);return `<div class="audit-pending"><strong>${sourceName(source)} · ${sourceLocation(source,a.pdfPage)} · chương ${a.chapter}${source?.locatorLabel==='câu'?'':` · câu ${a.number}`}</strong><br>${esc(a.reason)}</div>`;}).join('')}</details>
    <div class="section-head"><h2>Nguồn bổ sung</h2></div><div class="panel">${bank.supplements.map(s=>`<p class="small muted"><strong>${esc(bank.sources.find(x=>x.id===s.sourceId)?.shortTitle)}:</strong> ${esc(s.status)}</p>`).join('')}</div>
    <section class="panel storage-panel"><h2>Giữ lại hành trình học của bạn</h2><p>Tiến độ chỉ lưu trên trình duyệt hiện tại. Khi đổi máy, hãy xuất tệp rồi nhập ở thiết bị mới. Xóa dữ liệu trình duyệt có thể làm mất tiến độ nếu chưa sao lưu.</p><div class="row wrap">${button('export',`${icon('download')} Xuất tiến độ`,'btn')}${button('import',`${icon('upload')} Nhập tiến độ`,'btn')}${button('reset','Xóa tiến độ','btn ghost')}</div><input type="file" id="import-file" accept="application/json,.json" hidden><p class="small muted" style="margin-top:18px;margin-bottom:0">Ngân hàng ${esc(bank.version)} · Không cần tài khoản · Không gửi tiến độ lên máy chủ</p></section>`;
}

function render(): void {
  const focus=document.activeElement as HTMLInputElement | null;
  const id=focus?.id, focusKey=focus?.dataset.focus;
  const selection=focus?.tagName==='INPUT'&&focus.type==='search'?[focus.selectionStart,focus.selectionEnd]:null;
  const hash=routeHash();
  let content='';
  const match=hash.match(/^#\/chuong\/(\d+)$/);
  if(match && bank.chapters.some(c=>c.number===Number(match[1]))) content=chapterPage(Number(match[1]));
  else if(subject.collections.some(c=>hash==='#/'+c.id)) content=numbersPage();
  else switch(hash){
    case '#/':content=home();break;
    case '#/thi-thu':content=examPage();break;
    case '#/de-tong-hop':content=comprehensivePage();break;
    case '#/can-on':content=reviewPage();break;
    case '#/keyword':content=keywordsPage();break;
    case '#/lam-bai':content=quizPage();break;
    case '#/ket-qua':content=resultPage();break;
    case '#/nguon':content=sourcesPage();break;
    default:content=`<div class="empty-state">${icon('book')}<h1>Trang này chưa có</h1><p>Quay lại chọn một chương để tiếp tục học.</p>${link('#/','Về tổng quan')}</div>`;
  }
  app.innerHTML=scopeSubjectLinks(shell(content),subject.id);
  if(app.querySelector('[data-math]')) void import('../../shared/math.ts').then(module=>{if(!events.signal.aborted)module.renderMath(app);}).catch(()=>{if(!events.signal.aborted)toast('Chưa tải được kiểu chữ công thức. Biểu thức gốc vẫn được hiển thị.');});
  document.title=`${breadcrumb()} — ${subject.shortName} | Nắm ý`;
  if(id){const target=document.getElementById(id) as HTMLInputElement|null;if(target){target.focus({preventScroll:true});if(selection)target.setSelectionRange(selection[0],selection[1]);}}
  else if(focusKey) app.querySelector<HTMLElement>(`[data-focus="${CSS.escape(focusKey)}"]`)?.focus({preventScroll:true});
}

function begin(deck: Deck, mode: Session['mode'], timeLimit = minutes, specific?: Question[]): void {
  if(progress.activeSession){
    pendingStart={deck,mode,minutes:timeLimit,specific};
    openDialog('Bạn còn bài đang làm','<p>Tiếp tục bài cũ hoặc thay bằng lượt mới. Những câu đã được chấm vẫn giữ trong tiến độ.</p>',button('close-dialog','Hủy','btn ghost')+button('resume','Tiếp tục bài cũ','btn')+button('replace-session','Bắt đầu lượt mới'));
    return;
  }
  const qs=specific??selectQuestions(bank.questions,deck,progress.records,bank.sampleQuestionIds);
  if(!qs.length||(deck.kind==='comprehensive'&&qs.length!==deck.count)){toast('Chưa có đủ câu phù hợp. Hãy thử lựa chọn khác.');return;}
  progress.activeSession=createSession(qs,deck,mode,timeLimit);
  persist();go('#/lam-bai');window.scrollTo(0,0);
}
function submit(): void {
  progress=finishSession(progress,qmap);persist();resultFilter='all';dialog.close();go('#/ket-qua');window.scrollTo(0,0);
}
function confirmSubmit(): void {
  const s=progress.activeSession;if(!s)return;
  const unanswered=s.items.filter(i=>s.mode==='practice'?!i.checked:i.selectedOptionId===null).length;
  openDialog(s.mode==='exam'?'Nộp bài để xem kết quả?':'Kết thúc lượt luyện?',`<p>${unanswered?`Còn <strong>${unanswered} câu chưa hoàn thành</strong>. Những câu chưa trả lời sẽ được ghi nhận là bỏ qua để bạn ôn lại.`:'Bạn đã trả lời các câu. Cùng xem lại kết quả và keyword cần nhớ.'}</p>`,button('close-dialog','Tiếp tục làm','btn')+button('submit','Nộp & xem kết quả'));
}
function current(): {session: Session; item: Session['items'][number]; question: Question} | null {
  const session=progress.activeSession;if(!session)return null;
  const item=session.items[session.cursor],question=qmap.get(item.questionId);return question?{session,item,question}:null;
}
function choose(optionId: string): void {
  const c=current();if(!c||c.session.mode==='practice'&&c.item.checked||!c.question.options.some(o=>o.id===optionId))return;
  c.item.selectedOptionId=optionId;persist();render();
}
function nextQuestion(): void {
  const c=current();if(!c)return;
  if(c.session.mode==='practice'&&!c.item.checked)return;
  if(c.session.cursor===c.session.items.length-1){if(c.session.mode==='exam'||c.session.items.some(i=>!i.checked))confirmSubmit();else submit();}
  else{c.session.cursor++;persist();render();document.querySelector<HTMLElement>('#question-prompt')?.focus();window.scrollTo(0,0);}
}

document.addEventListener('click',event=>{
  const target=(event.target as Element).closest<HTMLElement>('[data-action]');
  if(!target){if((event.target as Element).closest('a[href^="#/"]'))menuOpen=false;return;}
  const action=target.dataset.action;
  switch(action){
    case 'skip-content':event.preventDefault();document.querySelector<HTMLElement>('#main')?.focus();break;
    case 'menu':menuOpen=!menuOpen;render();break;
    case 'count':count=Number(target.dataset.value);render();break;
    case 'start-paper':{
      const paper=papers.find(p=>p.id===target.dataset.paper);if(!paper)break;
      begin({kind:'comprehensive',count:paper.questionIds.length,title:paper.title,questionIds:[...paper.questionIds]},'exam');break;
    }
    case 'start':{
      const kind=target.dataset.kind as Deck['kind'];const chapter=target.dataset.chapter?Number(target.dataset.chapter):undefined;
      const title=kind==='chapter'?`Chương ${chapter}`:kind==='numbers'?(collection()?.title??'Chuyên đề'):kind==='sample'?(subject.sampleTitle??'Đề mẫu'):kind==='mixed'?`Đề trộn ${examSize} câu`:'Câu cần ôn';
      const deck:Deck={kind:kind==='numbers'?'collection':kind,tags:kind==='numbers'?collection()?.tags:subject.collections.flatMap(c=>c.tags),chapter,count:kind==='mixed'||kind==='sample'?examSize:count,includeNumbers,tag:numberTag,order,title};
      begin(deck,kind==='sample'||kind==='mixed'?'exam':'practice');break;
    }
    case 'close-dialog':dialog.close();pendingStart=null;break;
    case 'resume':dialog.close();pendingStart=null;go('#/lam-bai');break;
    case 'replace-session':{
      if(!pendingStart)break;const next=pendingStart;pendingStart=null;progress.activeSession=null;dialog.close();begin(next.deck,next.mode,next.minutes,next.specific);break;
    }
    case 'choose':choose(target.dataset.option!);break;
    case 'check':progress=checkCurrent(progress,qmap);persist();render();break;
    case 'skip':progress=checkCurrent(progress,qmap,true);persist();render();break;
    case 'hint':{const c=current();if(c&&c.session.mode==='practice'&&!c.item.checked){c.item.usedHint=true;persist();render();}break;}
    case 'bookmark':{const q=qmap.get(target.dataset.id!);if(q){progress=toggleBookmark(progress,q);persist();render();}break;}
    case 'previous':{const c=current();if(c&&c.session.cursor>0){c.session.cursor--;persist();render();}break;}
    case 'next':nextQuestion();break;
    case 'jump':{const c=current();const index=Number(target.dataset.index);if(c&&Number.isInteger(index)&&index>=0&&index<c.session.items.length){c.session.cursor=index;persist();render();document.querySelector<HTMLElement>('#question-prompt')?.focus();}break;}
    case 'save-exit':persist();go('#/');toast('Đã giữ bài đang làm. Bạn có thể tiếp tục bất cứ lúc nào.');break;
    case 'finish':confirmSubmit();break;
    case 'submit':submit();break;
    case 'result-filter':resultFilter=target.dataset.value!;render();break;
    case 'retry':{const s=progress.lastResult;if(s)begin({...s.deck},s.mode,0);break;}
    case 'retry-review':{
      const s=progress.lastResult;if(!s)break;
      const qs=s.items.filter(i=>i.selectedOptionId!==qmap.get(i.questionId)?.correctOptionId||i.usedHint||progress.records[i.questionId]?.bookmarked).map(i=>qmap.get(i.questionId)!);
      begin({kind:'review',count:qs.length,title:'Ôn lại lượt vừa làm',questionIds:qs.map(q=>q.id)},'practice',0,qs);break;
    }
    case 'reveal':{const id=target.dataset.id!;if(!keywordHidden){keywordHidden=true;for(const c of bank.concepts)revealed.add(c.id);}if(revealed.has(id))revealed.delete(id);else revealed.add(id);render();break;}
    case 'hide-keywords':keywordHidden=!keywordHidden;revealed.clear();render();break;
    case 'clear-search':keywordQuery='';keywordFilter='all';render();break;
    case 'export':{
      const blob=new Blob([JSON.stringify(progress,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`nam-y-tien-do-${subject.id}-${new Date().toISOString().slice(0,10)}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Đã xuất tệp tiến độ. Giữ tệp để chuyển sang máy khác.');break;
    }
    case 'import':document.querySelector<HTMLInputElement>('#import-file')?.click();break;
    case 'confirm-import':{
      if(importCandidate){progress=importCandidate;importCandidate=null;storageWarning='';persist();dialog.close();render();toast('Đã nhập tiến độ.');}break;
    }
    case 'reset':openDialog('Xóa tiến độ trên trình duyệt này?','<p>Thao tác sẽ xóa lịch sử, đánh dấu và bài đang làm. Bạn nên xuất một bản sao trước nếu muốn giữ lại.</p>',button('close-dialog','Giữ tiến độ','btn')+button('confirm-reset','Xóa tiến độ','btn danger'));break;
    case 'confirm-reset':progress=emptyProgress(bank.version,subject.id);persist();dialog.close();render();toast('Đã xóa tiến độ trên trình duyệt này.');break;
  }
}, { signal: events.signal });
let importCandidate: Progress | null = null;
document.addEventListener('change',async event=>{
  const el=event.target as HTMLInputElement|HTMLSelectElement;
  switch(el.id){
    case 'subject-switch':location.hash=subjectHref(el.value);break;
    case 'include-numbers':includeNumbers=(el as HTMLInputElement).checked;render();break;
    case 'number-tag':numberTag=el.value;render();break;
    case 'question-order':order=el.value==='random'?'random':'unseen';break;
    case 'exam-minutes':minutes=Number(el.value);break;
    case 'keyword-filter':keywordFilter=el.value;render();break;
    case 'import-file':{
      const file=(el as HTMLInputElement).files?.[0];if(!file)return;
      if(file.size>5_000_000){toast('Tệp quá lớn. Hãy dùng tệp JSON tiến độ dưới 5 MB.');el.value='';return;}
      try{const candidate=parseProgress(JSON.parse(await file.text()),qmap,bank.version,subject.id);importCandidate=candidate;openDialog('Thay tiến độ bằng tệp đã chọn?',`<p>Tệp chứa ${Object.values(candidate.records).filter(r=>r.seen).length} câu đã gặp. Tiến độ hiện tại sẽ được thay bằng nội dung tệp, không gộp tự động.</p>`,button('close-dialog','Hủy','btn')+button('confirm-import','Nhập tiến độ'));}
      catch{toast('Tệp không đúng định dạng tiến độ Nắm ý hoặc không thuộc môn này.');}
      el.value='';break;
    }
  }
}, { signal: events.signal });
document.addEventListener('input',event=>{const el=event.target as HTMLInputElement;if(el.id==='keyword-search'){keywordQuery=el.value;render();}}, { signal: events.signal });
document.addEventListener('keydown',event=>{
  if(event.repeat||event.altKey||event.ctrlKey||event.metaKey||dialog.open||routeHash()!=='#/lam-bai')return;
  const target=event.target as Element;
  if(target.closest('input,select,textarea,[contenteditable=true]'))return;
  const c=current();if(!c)return;
  if(/^[1-4]$/.test(event.key)){
    const id=c.item.optionOrder[Number(event.key)-1];if(id){event.preventDefault();choose(id);}return;
  }
  if(event.key==='Enter'){
    const action=target.closest<HTMLElement>('[data-action]')?.dataset.action;
    if(action&&!['choose','check','next'].includes(action))return;
    if(target.closest('a,summary'))return;
    event.preventDefault();
    if(c.session.mode==='practice'&&!c.item.checked){progress=checkCurrent(progress,qmap);persist();render();}
    else nextQuestion();
  }
}, { signal: events.signal });
function checkDeadline(): void {
  const s=progress.activeSession;
  if(!s||s.mode!=='exam'||!s.deadline)return;
  const remaining=s.deadline-Date.now();
  const el=document.querySelector('#timer');if(el){el.textContent=durationText(remaining);el.classList.toggle('urgent',remaining<60_000);}
  if(remaining<=0){submit();toast('Đã hết thời gian tự chọn. Bài được nộp và lưu kết quả.');}
}
window.addEventListener('storage',event=>{
  if(event.key===storageKey(subject.id))toast('Tiến độ vừa thay đổi ở tab khác. Tải lại trang nếu bạn muốn dùng bản mới nhất.');
}, { signal: events.signal });
render();checkDeadline();
const timer=setInterval(checkDeadline,1000);
return { render:()=>{menuOpen=false;render();checkDeadline();}, dispose:()=>{events.abort();clearInterval(timer);if(dialog.open)dialog.close();} };
}
