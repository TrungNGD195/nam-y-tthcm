export type ChapterNumber = number;
export type NumberTag = string;
export type Collection = { id: string; title: string; description: string; icon: string; tags: string[]; filters: {tag: string; label: string}[] };
export type Subject = {
  id: string; name: string; shortName: string; description: string; icon: string;
  accent: string; accentLight: string; status: 'ready' | 'awaiting-materials';
  learningMode?: 'quiz' | 'solutions';
  questionCount?: number; chapterCount?: number; examSize?: number; sampleTitle?: string;
  sourceDescription?: string; collections: Collection[];
};
export type ContentBlock =
  | { type: 'image'; src: string; alt: string; caption?: string }
  | { type: 'matrix'; rows: (string | number)[][]; caption?: string }
  | { type: 'table'; headers: string[]; rows: (string | number)[][]; caption?: string }
  | { type: 'code'; code: string; language?: string }
  | { type: 'formula'; tex: string; display?: boolean };
export type Reference = { sourceId: string; pdfPage: number; section: string; evidence: string };
export type Source = { id: string; title: string; shortTitle: string; kind: 'bank' | 'theory' | 'supplement'; pages: number; url?: string; locatorLabel?: 'câu' | 'mục' };
export type Concept = {
  id: string; chapter: ChapterNumber; title: string; summary: string;
  keywords: string[]; confusionNote: string; references: Reference[]; core: boolean;
};
export type Question = {
  id: string; revision: number; chapter: ChapterNumber; topic: string; conceptId: string;
  tags: NumberTag[]; prompt: string; blocks?: ContentBlock[]; explanationBlocks?: ContentBlock[]; options: { id: string; text: string; blocks?: ContentBlock[] }[];
  correctOptionId: string; shufflePolicy: 'safe' | 'fixed'; originType: 'original' | 'converted';
  explanation: string; keywords: string[]; confusionNote: string;
  sources: { sourceId: string; pdfPage: number; originalNumber: number; group: string }[];
  theoryReferences: Reference[]; editorialNote: string; reviewStatus: 'verified';
};
export type Chapter = { number: ChapterNumber; title: string; shortTitle: string; description: string; icon: string };
export type AuditEntry = { id: string; sourceId: string; number: number; chapter: number; pdfPage: number; status: 'published' | 'merged' | 'pending' | 'disputed'; questionId?: string; reason: string };
export type Bank = {
  subjectId: string;
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
export type Deck = { kind: 'chapter' | 'numbers' | 'review' | 'mixed' | 'sample' | 'collection'; chapter?: number; tag?: string; tags?: string[]; includeNumbers?: boolean; order?: 'unseen' | 'random'; count: number; title: string; questionIds?: string[] };
export type Session = {
  id: string; mode: 'practice' | 'exam'; status: 'active' | 'finished'; deck: Deck;
  items: SessionItem[]; cursor: number; startedAt: number; deadline: number | null; finishedAt: number | null;
};
export type HistoryEntry = { id: string; title: string; at: number; total: number; correct: number; assisted: number; mode: 'practice' | 'exam' };
export type Progress = {
  schemaVersion: 2; subjectId: string; bankVersion: string; records: Record<string, RecordEntry>;
  activeSession: Session | null; lastResult: Session | null; history: HistoryEntry[];
};
