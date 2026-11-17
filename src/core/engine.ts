import type { Deck, Progress, Question, RecordEntry, Session, SessionItem } from './types.ts';

export const normalize = (text: string): string => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();

export function shuffle<T>(items: readonly T[], random: () => number = Math.random): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export function needsReview(record?: RecordEntry): boolean {
  return !!record && (record.bookmarked || ['incorrect', 'skipped', 'assisted'].includes(record.lastOutcome ?? ''));
}

export function selectQuestions(questions: Question[], deck: Deck, records: Progress['records'], sampleIds: string[] = [], random: () => number = Math.random): Question[] {
  let pool = questions;
  if (deck.kind === 'comprehensive') {
    const map=new Map(questions.map(q=>[q.id,q]));
    return (deck.questionIds??[]).map(id=>map.get(id)).filter((q):q is Question=>!!q);
  }
  if (deck.kind === 'sample') return sampleIds.map(id => questions.find(q => q.id === id)).filter((q): q is Question => !!q);
  if (deck.kind === 'chapter') pool = pool.filter(q => q.chapter === deck.chapter && (deck.includeNumbers || !q.tags.some(tag => (deck.tags ?? q.tags).includes(tag))));
  if (deck.kind === 'numbers') pool = pool.filter(q => q.tags.length && (!deck.tag || deck.tag === 'all' || q.tags.includes(deck.tag as Question['tags'][number])));
  if (deck.kind === 'collection') pool = pool.filter(q => q.tags.some(tag => deck.tags?.includes(tag)) && (!deck.tag || deck.tag === 'all' || q.tags.includes(deck.tag)));
  if (deck.kind === 'review') pool = pool.filter(q => deck.questionIds ? deck.questionIds.includes(q.id) : needsReview(records[q.id]));
  let ordered = shuffle(pool, random);
  if (deck.order === 'unseen') ordered.sort((a, b) => (records[a.id]?.seen ?? 0) - (records[b.id]?.seen ?? 0));
  if (deck.kind === 'review') ordered.sort((a, b) => (records[b.id]?.incorrect ?? 0) - (records[a.id]?.incorrect ?? 0));
  if (deck.kind !== 'mixed') return ordered.slice(0, deck.count);

  // Round-robin chapters; prefer another concept before repeating one.
  const chapters = [...new Set(ordered.map(q => q.chapter))].sort((a,b) => a-b);
  const buckets = chapters.map(chapter => ordered.filter(q => q.chapter === chapter));
  const selected: Question[] = [];
  const concepts = new Set<string>();
  while (selected.length < deck.count && buckets.some(bucket => bucket.length)) {
    for (const bucket of buckets) {
      if (!bucket.length || selected.length >= deck.count) continue;
      const fresh = bucket.findIndex(q => !concepts.has(q.conceptId));
      const [q] = bucket.splice(fresh < 0 ? 0 : fresh, 1);
      selected.push(q);
      concepts.add(q.conceptId);
    }
  }
  if (selected.length && !selected.some(q => q.tags.length)) {
    const numeric = ordered.find(q => q.tags.length);
    if (numeric) {
      const replaceIndex = selected.findIndex(q => q.chapter === numeric.chapter);
      selected[replaceIndex < 0 ? selected.length - 1 : replaceIndex] = numeric;
    }
  }
  return selected;
}

export function createSession(questions: Question[], deck: Deck, mode: Session['mode'], minutes = 0, now = Date.now(), random: () => number = Math.random): Session {
  return {
    id: globalThis.crypto?.randomUUID?.() ?? `session-${now}-${random().toString(36).slice(2)}`,
    mode, status: 'active', deck, cursor: 0, startedAt: now,
    deadline: mode === 'exam' && minutes > 0 ? now + minutes * 60_000 : null, finishedAt: null,
    items: questions.map(q => ({
      questionId: q.id, revision: q.revision,
      optionOrder: q.shufflePolicy === 'fixed' ? q.options.map(o => o.id) : shuffle(q.options.map(o => o.id), random),
      selectedOptionId: null, checked: false, usedHint: false, recorded: false,
    })),
  };
}

export function emptyRecord(q: Question): RecordEntry {
  return { revision: q.revision, seen: 0, correct: 0, incorrect: 0, lastOutcome: null, lastAt: null, bookmarked: false };
}

function recordItem(progress: Progress, item: SessionItem, q: Question, now: number): void {
  if (item.recorded) return;
  const record = progress.records[q.id] ?? emptyRecord(q);
  const correct = item.selectedOptionId === q.correctOptionId;
  record.seen++;
  record.lastAt = now;
  record.lastOutcome = item.selectedOptionId === null ? 'skipped' : !correct ? 'incorrect' : item.usedHint ? 'assisted' : 'correct';
  if (correct && !item.usedHint) record.correct++;
  if (!correct) record.incorrect++;
  progress.records[q.id] = record;
  item.recorded = true;
  item.checked = true;
}

export function checkCurrent(progress: Progress, questions: Map<string, Question>, skip = false, now = Date.now()): Progress {
  const next = structuredClone(progress);
  const session = next.activeSession;
  if (!session || (session.mode !== 'practice' && session.examFeedback !== 'immediate') || session.status !== 'active') return next;
  const item = session.items[session.cursor];
  const q = questions.get(item.questionId);
  if (!q || item.checked || (!skip && item.selectedOptionId === null)) return next;
  if (skip) item.selectedOptionId = null;
  recordItem(next, item, q, now);
  return next;
}

export function enableImmediateExamFeedback(progress: Progress, questions: Map<string, Question>, now = Date.now()): Progress {
  if (!progress.activeSession || progress.activeSession.mode !== 'exam') return progress;
  const next = structuredClone(progress), session = next.activeSession!;
  session.examFeedback = 'immediate';
  // Previously saved choices receive feedback without changing the paper or its deadline.
  for (const item of session.items) {
    const q = questions.get(item.questionId);
    if (q && item.selectedOptionId !== null) recordItem(next, item, q, now);
  }
  return next;
}

export function finishSession(progress: Progress, questions: Map<string, Question>, now = Date.now()): Progress {
  if (!progress.activeSession) return progress;
  const next = structuredClone(progress);
  const session = next.activeSession!;
  for (const item of session.items) {
    const q = questions.get(item.questionId);
    if (q) recordItem(next, item, q, now);
  }
  session.status = 'finished';
  session.finishedAt = now;
  const counts = scoreSession(session, questions);
  next.history = [{ id: session.id, title: session.deck.title, at: now, total: counts.total, correct: counts.correct, assisted: counts.assisted, mode: session.mode,...(session.deck.paperKey?{paperKey:session.deck.paperKey}:{}) }, ...next.history.filter(h => h.id !== session.id)].slice(0, 50);
  next.lastResult = session;
  next.activeSession = null;
  return next;
}

export function scoreSession(session: Session, questions: Map<string, Question>) {
  let correct = 0, assisted = 0, skipped = 0;
  for (const item of session.items) {
    if (item.selectedOptionId === null) skipped++;
    else if (item.selectedOptionId === questions.get(item.questionId)?.correctOptionId) {
      correct++;
      if (item.usedHint) assisted++;
    }
  }
  return { total: session.items.length, correct, assisted, independent: correct - assisted, skipped, incorrect: session.items.length - correct - skipped };
}

export function toggleBookmark(progress: Progress, q: Question): Progress {
  const next = structuredClone(progress);
  const record = next.records[q.id] ?? emptyRecord(q);
  record.bookmarked = !record.bookmarked;
  next.records[q.id] = record;
  return next;
}
