export type LessonDifficulty = "basic" | "intermediate" | "advanced";

export interface SampleCodeBlock {
  title: string;
  code: string;
  explanation: string;
}

export interface Lesson {
  slug: string;
  title: string;
  order: number;
  difficulty: LessonDifficulty;
  /** One-line hook for the lesson card */
  summary: string;
  /** Teaching paragraphs — beginner-friendly */
  explanation: string[];
  /** Mermaid diagram source (flowchart, graph, sequence, etc.) */
  mermaid: string;
  diagramCaption: string;
  sampleCode: SampleCodeBlock[];
  realWorldApplications: string[];
  keyTakeaways: string[];
  /** Question slugs in this module that practice this concept */
  relatedQuestionSlugs?: string[];
}

export interface ModuleCurriculum {
  topicSlug: string;
  /** Module-wide intro before subtopics */
  intro: {
    overview: string[];
    learningPath: string[];
    prerequisites: string[];
  };
  lessons: Lesson[];
}
