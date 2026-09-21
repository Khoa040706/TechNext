import { lazy, Suspense, type ReactNode } from "react"
import { createBrowserRouter, Navigate } from "react-router-dom"
import { RootLayout } from "@/layouts/RootLayout"
import { LoadingState } from "@/components/common/LoadingState"

const LoginPage = lazy(() => import("@/pages/LoginPage").then((m) => ({ default: m.LoginPage })))
const DashboardPage = lazy(() => import("@/pages/DashboardPage").then((m) => ({ default: m.DashboardPage })))
const LearnPage = lazy(() => import("@/pages/LearnPage").then((m) => ({ default: m.LearnPage })))
const TopicDetailPage = lazy(() => import("@/pages/TopicDetailPage").then((m) => ({ default: m.TopicDetailPage })))
const QuizPage = lazy(() => import("@/pages/QuizPage").then((m) => ({ default: m.QuizPage })))
const ExercisePage = lazy(() => import("@/pages/ExercisePage").then((m) => ({ default: m.ExercisePage })))
const SkillsPage = lazy(() => import("@/pages/SkillsPage").then((m) => ({ default: m.SkillsPage })))
const RecommendationsPage = lazy(() => import("@/pages/RecommendationsPage").then((m) => ({ default: m.RecommendationsPage })))
const PredictionPage = lazy(() => import("@/pages/PredictionPage").then((m) => ({ default: m.PredictionPage })))
const AdminPage = lazy(() => import("@/pages/AdminPage").then((m) => ({ default: m.AdminPage })))
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage").then((m) => ({ default: m.NotFoundPage })))

function withSuspense(component: ReactNode) {
  return <Suspense fallback={<LoadingState className="py-24" />}>{component}</Suspense>
}

export const router = createBrowserRouter([
  {
    path: "/login",
    element: withSuspense(<LoginPage />),
  },
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: "dashboard",
        element: withSuspense(<DashboardPage />),
      },
      {
        path: "learn",
        element: withSuspense(<LearnPage />),
      },
      {
        path: "learn/:topicId",
        element: withSuspense(<TopicDetailPage />),
      },
      {
        path: "quiz/:quizId",
        element: withSuspense(<QuizPage />),
      },
      {
        path: "exercise/:exerciseId",
        element: withSuspense(<ExercisePage />),
      },
      {
        path: "skills",
        element: withSuspense(<SkillsPage />),
      },
      {
        path: "recommendations",
        element: withSuspense(<RecommendationsPage />),
      },
      {
        path: "prediction",
        element: withSuspense(<PredictionPage />),
      },
      {
        path: "admin/*",
        element: withSuspense(<AdminPage />),
      },
      {
        path: "*",
        element: withSuspense(<NotFoundPage />),
      },
    ],
  },
])
