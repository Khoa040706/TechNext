/**
 * NextTech Query Key Factory
 * Đảm bảo key nhất quán trên toàn bộ frontend cho TanStack Query cache & invalidation
 */
export const queryKeys = {
  auth: {
    me: () => ["auth", "me"] as const,
    profile: () => ["auth", "profile"] as const,
  },
  dashboard: {
    overview: () => ["dashboard", "overview"] as const,
  },
  topics: {
    all: () => ["topics"] as const,
    detail: (id: string) => ["topics", id] as const,
  },
  lessons: {
    detail: (id: string) => ["lessons", id] as const,
  },
  quizzes: {
    detail: (id: string) => ["quizzes", id] as const,
    attempts: (id: string) => ["quizzes", id, "attempts"] as const,
  },
  exercises: {
    all: () => ["exercises"] as const,
    detail: (id: string) => ["exercises", id] as const,
    submissions: (id: string) => ["exercises", id, "submissions"] as const,
  },
  mastery: {
    current: () => ["mastery", "current"] as const,
    history: () => ["mastery", "history"] as const,
  },
  learningPath: {
    current: () => ["learning-path", "current"] as const,
  },
  recommendations: {
    list: () => ["recommendations", "list"] as const,
  },
  predictions: {
    latest: () => ["predictions", "latest"] as const,
    explanation: (predictionId: string) => ["predictions", predictionId, "explanation"] as const,
  },
  admin: {
    analytics: () => ["admin", "analytics"] as const,
    topics: () => ["admin", "topics"] as const,
    skills: () => ["admin", "skills"] as const,
    quizzes: () => ["admin", "quizzes"] as const,
    exercises: () => ["admin", "exercises"] as const,
    resources: () => ["admin", "resources"] as const,
  },
} as const
