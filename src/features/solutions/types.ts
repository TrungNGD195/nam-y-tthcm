import type { ContentBlock } from '../../core/types.ts';

export type SolutionStep = { lead: string; formula?: string; substitution?: string; result?: string; text?: string; blocks?: ContentBlock[] };
export type SolvedItem = {
  id: string; revision: number; code: string; area: 'bank' | 'uyen'; sourceId: string; sourcePages: number[];
  kind: 'theory' | 'exercise'; points: number | null; chapter: number; title: string; prompt: string;
  originalText: string; images: string[]; keywords: string[]; steps: SolutionStep[]; note: string;
  references: { sourceId: string; pdfPage: number; section: string }[];
  answerStyle?: 'complete'; answerBasis?: 'checked-key' | 'course-theory';
};
export type Solutions = {
  subjectId: string; version: string; updatedAt: string; chapters: { number: number; title: string }[];
  items: SolvedItem[];
  sources: { id: string; title: string; path: string; pages: number; sha256: string }[];
  coverage: { bank: number; uyen: number; theory: number; exercises: number; bankPoints: Record<string, number>; englishTheory: string };
  exam: { ethics: string; theory: string; exercises: string; note: string };
  documents?: SolutionDocuments;
};
export type ReadingMark = { revision: number; state: 'known' | 'review' };
export type SolutionDocuments = {
  subjectId:string; version:string; dataVersion:string; renderFingerprint:string;
  book:{src:string;pages:number;sha256:string};
  items:Record<string,{contentHash:string;pdfStartPage:number;pdfEndPage:number;answerStartPage:number;textSrc:string;
    pages:{src:string;width:number;height:number;pdfPage:number;sha256:string}[]}>;
};
