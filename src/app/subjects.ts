import registry from '../subjects/catalog.json';
import type { Bank, Subject } from '../core/types.ts';
import type { Solutions, SolutionDocuments } from '../features/solutions/types.ts';
export const subjects = registry as Subject[];
export const getSubject = (id: string): Subject | undefined => subjects.find(s => s.id === id);
const loaders = import.meta.glob<{ default: Bank }>('../subjects/*/bank.json');
const cache = new Map<string, Promise<Bank>>();
export function loadBank(subject: Subject): Promise<Bank> {
  if (subject.status !== 'ready') return Promise.reject(new Error('Môn này đang chờ tài liệu.'));
  if (!cache.has(subject.id)) {
    const loader = loaders[`../subjects/${subject.id}/bank.json`];
    if (!loader) return Promise.reject(new Error('Chưa tìm thấy ngân hàng của môn học.'));
    cache.set(subject.id, loader().then(module => {
      if (module.default.subjectId !== subject.id) throw new Error('Ngân hàng không khớp với môn học.');
      return module.default;
    }).catch(error => { cache.delete(subject.id); throw error; }));
  }
  return cache.get(subject.id)!;
}
const solutionLoaders = import.meta.glob<{ default: Solutions }>('../subjects/*/solutions.json');
const documentLoaders = import.meta.glob<{ default: SolutionDocuments }>('../subjects/*/documents.json');
const solutionCache = new Map<string, Promise<Solutions>>();
export function loadSolutions(subject: Subject): Promise<Solutions> {
  if (subject.status !== 'ready' || subject.learningMode !== 'solutions') return Promise.reject(new Error('Môn không dùng bộ lời giải.'));
  if (!solutionCache.has(subject.id)) {
    const loader=solutionLoaders[`../subjects/${subject.id}/solutions.json`];
    if (!loader) return Promise.reject(new Error('Chưa có bộ lời giải.'));
    const documentLoader=documentLoaders[`../subjects/${subject.id}/documents.json`];
    if(subject.solutionPresentation==='documents'&&!documentLoader)return Promise.reject(new Error('Chưa có bản PDF lời giải của môn.'));
    solutionCache.set(subject.id,Promise.all([loader(),documentLoader?.()]).then(([module,documents])=>{
      if(module.default.subjectId!==subject.id)throw new Error('Bộ lời giải không khớp môn.');
      if(documents&&documents.default.subjectId!==subject.id)throw new Error('Bản PDF không khớp môn.');
      return {...module.default,documents:documents?.default};
    }).catch(error=>{solutionCache.delete(subject.id);throw error;}));
  }
  return solutionCache.get(subject.id)!;
}
