export type ChapterNumber = 1 | 2 | 3 | 4 | 5 | 6;
export type NumberTag = 'date' | 'congress' | 'count';
export type Reference = { sourceId: string; pdfPage: number; section: string; evidence: string };
export type Source = { id: string; title: string; shortTitle: string; kind: 'bank' | 'theory' | 'supplement'; pages: number };
export type Concept = {
  id: string; chapter: ChapterNumber; title: string; summary: string;
  keywords: string[]; confusionNote: string; references: Reference[]; core: boolean;
};
export type Question = {
  id: string; revision: number; chapter: ChapterNumber; topic: string; conceptId: string;
  tags: NumberTag[]; prompt: string; options: { id: string; text: string }[];
  correctOptionId: string; shufflePolicy: 'safe' | 'fixed'; originType: 'original' | 'converted';
  explanation: string; keywords: string[]; confusionNote: string;
  sources: { sourceId: string; pdfPage: number; originalNumber: number; group: string }[];
  theoryReferences: Reference[]; editorialNote: string; reviewStatus: 'verified';
};
export type Chapter = { number: ChapterNumber; title: string; shortTitle: string; description: string; icon: string };
export type AuditEntry = { id: string; sourceId: string; number: number; chapter: number; pdfPage: number; status: 'published' | 'merged' | 'pending' | 'disputed'; questionId?: string; reason: string };
export type Bank = {
  version: string; updatedAt: string; chapters: Chapter[]; concepts: Concept[]; questions: Question[];
  sources: Source[]; sampleQuestionIds: string[]; audit: AuditEntry[];
  supplements: { sourceId: string; status: string }[];
};
export type Outcome = 'correct' | 'incorrect' | 'assisted' | 'skipped';
export type RecordEntry = {
  revision: number; seen: number; correct: number; incorrect: number;
  lastOutcome: Outcome | null; lastAt: number | null; bookmarked: boolean;
};
export type SessionItem = {
  questionId: string; revision: number; optionOrder: string[];
  selectedOptionId: string | null; checked: boolean; usedHint: boolean; recorded: boolean;
};
export type Deck = { kind: 'chapter' | 'numbers' | 'review' | 'mixed' | 'sample'; chapter?: number; tag?: string; includeNumbers?: boolean; order?: 'unseen' | 'random'; count: number; title: string; questionIds?: string[] };
export type Session = {
  id: string; mode: 'practice' | 'exam'; status: 'active' | 'finished'; deck: Deck;
  items: SessionItem[]; cursor: number; startedAt: number; deadline: number | null; finishedAt: number | null;
};
export type HistoryEntry = { id: string; title: string; at: number; total: number; correct: number; assisted: number; mode: 'practice' | 'exam' };
export type Progress = {
  schemaVersion: 1; bankVersion: string; records: Record<string, RecordEntry>;
  activeSession: Session | null; lastResult: Session | null; history: HistoryEntry[];
};
