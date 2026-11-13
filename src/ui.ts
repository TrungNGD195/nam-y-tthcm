import type { Question, Reference, Source } from './types.ts';

export const esc = (value: unknown): string => String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]!);

const paths: Record<string, string> = {
  book: '<path d="M12 7c-2-2-5-3-9-2v15c4-1 7 0 9 2m0-15c2-2 5-3 9-2v15c-4-1-7 0-9 2V7Z"/>',
  home: '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
  arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
  back: '<path d="M19 12H5m5-5-5 5 5 5"/>',
  spark: '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 11h18m-13 4h1m6 0h1"/>',
  flag: '<path d="M5 21V4m0 0c5-4 9 4 14 0v11c-5 4-9-4-14 0"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  x: '<path d="m6 6 12 12M6 18 18 6"/>',
  menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.01"/>',
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
  download: '<path d="M12 3v12m-4-4 4 4 4-4M4 16v4h16v-4"/>',
  upload: '<path d="M12 15V3m-4 4 4-4 4 4M4 16v4h16v-4"/>',
  leaf: '<path d="M20 3C7 2 2 8 5 15s14 7 15-12ZM5 21 16 9"/>',
  layers: '<path d="m12 3 10 5-10 5L2 8l10-5ZM2 12l10 5 10-5M2 16l10 5 10-5"/>',
  people: '<circle cx="9" cy="8" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3m1-16a3 3 0 0 1 0 6m3 10v-3a6 6 0 0 0-3-5"/>',
  building: '<path d="m3 8 9-5 9 5H3Zm2 3v7m7-7v7m7-7v7M3 21h18"/>',
  heart: '<path d="M20 5c-3-3-6-1-8 1-2-2-5-4-8-1-6 6 8 15 8 15S26 11 20 5Z"/>',
  globe: '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
  eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
  refresh: '<path d="M20 8a8 8 0 1 0 0 8M20 3v5h-5"/>',
  chevron: '<path d="m9 5 7 7-7 7"/>',
};

export const icon = (name: string, className = ''): string => `<svg class="icon ${esc(className)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name] ?? paths.book}</svg>`;
export const button = (action: string, label: string, className = 'btn primary', extra = ''): string => `<button type="button" class="${className}" data-action="${action}" ${extra}>${label}</button>`;
export const link = (href: string, label: string, className = 'btn primary'): string => `<a href="${esc(href)}" class="${className}">${label}</a>`;
export const pill = (text: string, cls = ''): string => `<span class="pill ${cls}">${esc(text)}</span>`;
export function progressBar(value: number, label: string): string {
  const percent = Math.min(100, Math.max(0, Math.round(value)));
  return `<div class="progress-track" role="progressbar" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100" aria-label="${esc(label)}"><span style="width:${percent}%"></span></div>`;
}
export function emphasize(text: string, keywords: string[] = []): string {
  const sorted = [...new Set(keywords)].filter(Boolean).sort((a,b) => b.length-a.length);
  if (!sorted.length) return esc(text);
  const pattern = sorted.map(s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
  return text.split(new RegExp(`(${pattern})`, 'gi')).map(part => sorted.some(word => word.toLocaleLowerCase('vi') === part.toLocaleLowerCase('vi')) ? `<mark>${esc(part)}</mark>` : esc(part)).join('');
}
export const promptText = (text: string): string => emphasize(text, ['không phải', 'không nằm', 'không thuộc', 'không thể hiện', 'không đúng', 'đúng nhất', 'phương án sai', 'lần đầu tiên']);

export function referencesHtml(refs: Reference[], sources: Source[]): string {
  return refs.map(ref => `<div class="reference"><strong>${esc(sources.find(s => s.id === ref.sourceId)?.shortTitle ?? ref.sourceId)}</strong><span>Trang PDF ${ref.pdfPage} · ${esc(ref.section)}</span><p>${esc(ref.evidence)}</p></div>`).join('');
}
export function sourceDetails(q: Question, sources: Source[]): string {
  return `<details class="sources-detail"><summary>${icon('book')} Xem nguồn đối chiếu</summary><div class="source-content">${q.sources.map(s => `<p class="source-line">${esc(sources.find(x => x.id === s.sourceId)?.shortTitle ?? s.sourceId)} · trang PDF ${s.pdfPage} · ${esc(s.group)} · câu ${s.originalNumber}</p>`).join('')}${referencesHtml(q.theoryReferences, sources)}${q.editorialNote ? `<p class="editorial-note">Biên tập: ${esc(q.editorialNote)}</p>` : ''}</div></details>`;
}
export const durationText = (milliseconds: number): string => {
  const seconds = Math.max(0, Math.floor(milliseconds / 1000));
  return `${Math.floor(seconds / 60).toString().padStart(2,'0')}:${(seconds % 60).toString().padStart(2,'0')}`;
};
