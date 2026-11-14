import registry from '../subjects/catalog.json';
import type { Bank, Subject } from '../core/types.ts';
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
