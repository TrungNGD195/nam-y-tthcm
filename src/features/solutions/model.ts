import type { ReadingMark, SolvedItem } from './types.ts';

export const readingKey = (subjectId: string): string => `nam-y:solutions:v1:${subjectId}`;
export const normalize = (text: string): string => text.normalize('NFD').replace(/\p{M}/gu, '').replace(/đ/g,'d').replace(/Đ/g,'D').toLowerCase();
export function parseMarks(raw: string | null, items: SolvedItem[]): Record<string, ReadingMark> {
  try {
    const data: unknown = JSON.parse(raw ?? '{}');
    if (!data || typeof data !== 'object' || Array.isArray(data)) return {};
    const result: Record<string, ReadingMark> = {};
    for (const item of items) {
      const entry = (data as Record<string, Partial<ReadingMark>>)[item.id];
      if (entry && entry.revision === item.revision && ['known','review'].includes(entry.state ?? '')) result[item.id] = { revision: item.revision, state: entry.state! };
    }
    return result;
  } catch { return {}; }
}
export function filterItems(items: SolvedItem[], query: string, kind: string, state: string, marks: Record<string, ReadingMark>): SolvedItem[] {
  const words=normalize(query).trim().split(/\s+/).filter(Boolean);
  return items.filter(item => (kind==='all'||item.kind===kind) && (state==='all'||(state==='new'?!marks[item.id]:marks[item.id]?.state===state)) && words.every(word=>normalize(`${item.code} ${item.title} ${item.prompt} ${item.keywords.join(' ')}`).includes(word)));
}
