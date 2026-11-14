import '../shared/styles/base.css';
import '../shared/styles/multisubject.css';
import { subjects, getSubject, loadBank, loadSolutions } from './subjects.ts';
import { legacyRedirect, resolveRoute } from './router.ts';
import { awaitingPage, catalogPage, catalogShell } from '../features/subjects/catalog.ts';
import { icon, link } from '../shared/ui.ts';
import type { StudyController } from '../features/study/controller.ts';

const app=document.querySelector<HTMLDivElement>('#app')!;
let active: { id: string; controller: StudyController } | null=null;
let generation=0;

async function renderApp(): Promise<void> {
  const oldLink=legacyRedirect(location.hash);
  if(oldLink)history.replaceState(null,'',oldLink);
  const route=resolveRoute(location.hash),token=++generation;
  if(route.kind==='subject'&&active?.id===route.subjectId){active.controller.render();return;}
  active?.controller.dispose();active=null;
  const subject=route.kind==='subject'?getSubject(route.subjectId):undefined;
  document.documentElement.style.setProperty('--accent',subject?.accent??'#853e44');
  document.documentElement.style.setProperty('--accent-light',subject?.accentLight??'#f6edeb');
  if(route.kind==='catalog'){
    document.title='Nắm ý — Chọn môn để bắt đầu ôn tập';
    app.innerHTML=catalogShell(catalogPage(subjects),subjects);return;
  }
  if(!subject){
    document.title='Không tìm thấy — Nắm ý';
    app.innerHTML=catalogShell(`<div class="empty-state">${icon('book')}<h1>Không tìm thấy môn hoặc trang này</h1><p>Chọn một môn trong danh sách để tiếp tục học.</p>${link('#/','Về danh sách môn')}</div>`,subjects);return;
  }
  document.title=`${subject.name} — Nắm ý`;
  if(subject.status!=='ready'){
    app.innerHTML=catalogShell(awaitingPage(subject),subjects,subject.id);return;
  }
  app.innerHTML=catalogShell('<div class="empty-state" role="status">Đang mở nội dung môn học…</div>',subjects,subject.id);
  try{
    if(subject.learningMode==='solutions'){
      const [data,module]=await Promise.all([loadSolutions(subject),import('../features/solutions/controller.ts')]);
      if(token!==generation)return;
      active={id:subject.id,controller:module.mountSolutions(subject,data)};return;
    }
    const [bank,module]=await Promise.all([loadBank(subject),import('../features/study/controller.ts')]);
    if(token!==generation)return;
    const controller=module.mountStudy(subject,bank);
    // A stored expired exam can navigate while mounting; the next hash event handles it.
    active={id:subject.id,controller};
  }catch{
    if(token!==generation)return;
    app.innerHTML=catalogShell(`<div class="empty-state">${icon('info')}<h1>Chưa tải được môn học</h1><p>Kiểm tra kết nối rồi thử mở lại. Tiến độ đã lưu vẫn được giữ.</p><button class="btn primary" data-action="retry-load">Thử lại</button> ${link('#/','Chọn môn khác','btn')}</div>`,subjects,subject.id);
  }
}

document.addEventListener('click',event=>{
  const action=(event.target as Element).closest<HTMLElement>('[data-action]')?.dataset.action;
  if(action==='retry-load'){void renderApp();return;}
  if(action==='skip-content'){event.preventDefault();document.querySelector<HTMLElement>('#main')?.focus();return;}
  if(active)return;
  if(action==='menu'){
    const sidebar=document.querySelector('.sidebar'),open=!sidebar?.classList.contains('open');
    sidebar?.classList.toggle('open',open);document.querySelector('.mobile-shade')?.classList.toggle('visible',open);
    document.querySelector('.menu-toggle')?.setAttribute('aria-expanded',String(open));
  }
});
window.addEventListener('hashchange',()=>{void renderApp();window.scrollTo(0,0);});
void renderApp();
