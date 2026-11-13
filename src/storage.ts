import type { Progress, Question, RecordEntry, Session, SessionItem } from './types.ts';

export const STORAGE_KEY = 'nam-y:progress:v1';
export const emptyProgress = (bankVersion: string): Progress => ({ schemaVersion: 1, bankVersion, records: {}, activeSession: null, lastResult: null, history: [] });

const object = (value: unknown): value is Record<string, unknown> => typeof value === 'object' && value !== null && !Array.isArray(value);
const integer = (n: unknown): n is number => typeof n === 'number' && Number.isSafeInteger(n) && n >= 0;
const time = (n: unknown): n is number => typeof n === 'number' && Number.isFinite(n) && n >= 0;

function sanitizeSession(value: unknown, questions: Map<string, Question>, status: Session['status']): Session | null {
  if (!object(value) || value.status !== status || !['practice', 'exam'].includes(String(value.mode)) || typeof value.id !== 'string' || value.id.length > 120 || !object(value.deck)) return null;
  if (!Array.isArray(value.items) || value.items.length < 1 || value.items.length > questions.size || !integer(value.cursor) || value.cursor >= value.items.length || !time(value.startedAt)) return null;
  const deck = value.deck;
  if (!['chapter', 'numbers', 'review', 'mixed', 'sample'].includes(String(deck.kind)) || typeof deck.title !== 'string' || deck.title.length > 200 || !integer(deck.count) || !deck.count) return null;
  if (deck.kind === 'chapter' && (!integer(deck.chapter) || deck.chapter < 1 || deck.chapter > 6)) return null;
  const ids = new Set<string>();
  const items: SessionItem[] = [];
  for (const raw of value.items) {
    if (!object(raw) || typeof raw.questionId !== 'string' || ids.has(raw.questionId)) return null;
    const q = questions.get(raw.questionId);
    if (!q || raw.revision !== q.revision || !Array.isArray(raw.optionOrder) || raw.optionOrder.length !== q.options.length || new Set(raw.optionOrder).size !== q.options.length || raw.optionOrder.some(id => !q.options.some(o => o.id === id))) return null;
    if (raw.selectedOptionId !== null && !q.options.some(o => o.id === raw.selectedOptionId)) return null;
    if (typeof raw.checked !== 'boolean' || typeof raw.usedHint !== 'boolean' || typeof raw.recorded !== 'boolean' || raw.checked !== raw.recorded) return null;
    if (value.mode === 'exam' && (raw.usedHint || (status === 'active' && raw.checked))) return null;
    if (status === 'finished' && !raw.checked) return null;
    ids.add(q.id);
    items.push({ questionId: q.id, revision: q.revision, optionOrder: [...raw.optionOrder] as string[], selectedOptionId: raw.selectedOptionId as string | null, checked: raw.checked, usedHint: raw.usedHint, recorded: raw.recorded });
  }
  if (value.deadline !== null && (!time(value.deadline) || value.deadline < value.startedAt || value.deadline > value.startedAt + 180 * 60_000)) return null;
  if (status === 'finished' && !time(value.finishedAt)) return null;
  return {
    id: value.id, mode: value.mode as Session['mode'], status, items, cursor: value.cursor, startedAt: value.startedAt,
    deadline: value.deadline as number | null, finishedAt: status === 'finished' ? value.finishedAt as number : null,
    deck: { kind: deck.kind as Session['deck']['kind'], title: deck.title, count: deck.count,
      ...(integer(deck.chapter) ? { chapter: deck.chapter } : {}),
      ...(typeof deck.tag === 'string' && ['all','date','congress','count'].includes(deck.tag) ? { tag: deck.tag } : {}),
      ...(Array.isArray(deck.questionIds) && deck.questionIds.length <= questions.size && deck.questionIds.every(id => typeof id === 'string' && questions.has(id)) ? { questionIds: [...new Set(deck.questionIds)] as string[] } : {}),
      includeNumbers: deck.includeNumbers === true, order: deck.order === 'random' ? 'random' : 'unseen' },
  };
}

export function parseProgress(input: unknown, questions: Map<string, Question>, bankVersion: string): Progress {
  if (!object(input) || input.schemaVersion !== 1 || !object(input.records) || !Array.isArray(input.history)) throw new Error('Tệp không đúng định dạng tiến độ Nắm ý.');
  const next = emptyProgress(bankVersion);
  for (const [id, raw] of Object.entries(input.records)) {
    const q = questions.get(id);
    if (!q || !object(raw) || raw.revision !== q.revision) continue;
    if (![raw.seen, raw.correct, raw.incorrect].every(integer) || (raw.correct as number) + (raw.incorrect as number) > (raw.seen as number) || typeof raw.bookmarked !== 'boolean') continue;
    if (raw.lastOutcome !== null && !['correct','incorrect','skipped','assisted'].includes(String(raw.lastOutcome))) continue;
    if (raw.lastAt !== null && !time(raw.lastAt)) continue;
    next.records[id] = { revision: q.revision, seen: raw.seen as number, correct: raw.correct as number, incorrect: raw.incorrect as number, lastOutcome: raw.lastOutcome as RecordEntry['lastOutcome'], lastAt: raw.lastAt as number | null, bookmarked: raw.bookmarked };
  }
  next.activeSession = sanitizeSession(input.activeSession, questions, 'active');
  next.lastResult = sanitizeSession(input.lastResult, questions, 'finished');
  next.history = input.history.filter(object).filter(h => typeof h.id === 'string' && typeof h.title === 'string' && h.title.length <= 200 && time(h.at) && integer(h.total) && integer(h.correct) && integer(h.assisted) && h.correct <= h.total && h.assisted <= h.correct && ['practice','exam'].includes(String(h.mode))).slice(0, 50).map(h => ({ id: String(h.id).slice(0,120), title: String(h.title), at: h.at as number, total: h.total as number, correct: h.correct as number, assisted: h.assisted as number, mode: h.mode as 'practice' | 'exam' }));
  return next;
}

export function loadProgress(questions: Map<string, Question>, bankVersion: string): { progress: Progress; warning: string } {
  try {
    const text = localStorage.getItem(STORAGE_KEY);
    if (!text) return { progress: emptyProgress(bankVersion), warning: '' };
    const raw = JSON.parse(text);
    const progress = parseProgress(raw, questions, bankVersion);
    const changedSession = raw.activeSession && !progress.activeSession;
    return { progress, warning: changedSession ? 'Bài đang làm không còn phù hợp với ngân hàng hiện tại. Các kết quả còn hợp lệ vẫn được giữ.' : '' };
  } catch {
    return { progress: emptyProgress(bankVersion), warning: 'Không đọc được tiến độ đã lưu. Bạn vẫn có thể học; hãy xuất tiến độ mới khi cần.' };
  }
}

export function saveProgress(progress: Progress): boolean {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(progress)); return true; }
  catch { return false; }
}
