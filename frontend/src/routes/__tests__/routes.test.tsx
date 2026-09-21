import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { RouterProvider, createMemoryRouter } from "react-router-dom"
import { QueryClientProvider } from "@tanstack/react-query"
import { queryClient } from "@/lib/query-client"
import { ToastProvider } from "@/components/ui/toast"
import { RootLayout } from "@/layouts/RootLayout"
import { LoginPage } from "@/pages/LoginPage"
import { DashboardPage } from "@/pages/DashboardPage"
import { LearnPage } from "@/pages/LearnPage"
import { TopicDetailPage } from "@/pages/TopicDetailPage"
import { QuizPage } from "@/pages/QuizPage"
import { ExercisePage } from "@/pages/ExercisePage"
import { SkillsPage } from "@/pages/SkillsPage"
import { RecommendationsPage } from "@/pages/RecommendationsPage"
import { PredictionPage } from "@/pages/PredictionPage"
import { AdminPage } from "@/pages/AdminPage"
import { NotFoundPage } from "@/pages/NotFoundPage"

function renderWithRouter(initialRoute: string) {
  const routes = [
    {
      path: "/login",
      element: <LoginPage />,
    },
    {
      path: "/",
      element: <RootLayout />,
      children: [
        { path: "dashboard", element: <DashboardPage /> },
        { path: "learn", element: <LearnPage /> },
        { path: "learn/:topicId", element: <TopicDetailPage /> },
        { path: "quiz/:quizId", element: <QuizPage /> },
        { path: "exercise/:exerciseId", element: <ExercisePage /> },
        { path: "skills", element: <SkillsPage /> },
        { path: "recommendations", element: <RecommendationsPage /> },
        { path: "prediction", element: <PredictionPage /> },
        { path: "admin/*", element: <AdminPage /> },
        { path: "*", element: <NotFoundPage /> },
      ],
    },
  ]

  const memoryRouter = createMemoryRouter(routes, {
    initialEntries: [initialRoute],
  })

  return render(
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <RouterProvider router={memoryRouter} />
      </ToastProvider>
    </QueryClientProvider>
  )
}

describe("Comprehensive Route Rendering Tests", () => {
  it("renders /login route", () => {
    renderWithRouter("/login")
    expect(screen.getByText("Đăng nhập NextTech")).toBeInTheDocument()
  })

  it("renders /dashboard route", () => {
    renderWithRouter("/dashboard")
    expect(screen.getByText(/Chào mừng trở lại với NextTech/i)).toBeInTheDocument()
    expect(screen.getByText("Skill Mastery")).toBeInTheDocument()
  })

  it("renders /learn route", () => {
    renderWithRouter("/learn")
    expect(screen.getByText("Lộ trình học tập")).toBeInTheDocument()
    expect(screen.getByText("Variables & Data Types")).toBeInTheDocument()
  })

  it("renders /learn/:topicId route", () => {
    renderWithRouter("/learn/top_02")
    expect(screen.getByText(/Chủ đề: Cấu trúc điều kiện & Logic/i)).toBeInTheDocument()
  })

  it("renders /quiz/:quizId route", () => {
    renderWithRouter("/quiz/qz_01")
    expect(screen.getByText(/Mã quiz: qz_01/i)).toBeInTheDocument()
    expect(screen.getByText(/Trong Python, kết quả của biểu thức/i)).toBeInTheDocument()
  })

  it("renders /exercise/:exerciseId route", () => {
    renderWithRouter("/exercise/ex_01")
    expect(screen.getByText(/Bài tập: Kiểm tra năm nhuận/i)).toBeInTheDocument()
    expect(screen.getByText(/Quy tắc năm nhuận/i)).toBeInTheDocument()
  })

  it("renders /skills route", () => {
    renderWithRouter("/skills")
    expect(screen.getByText("Phân tích Kỹ năng & Mastery")).toBeInTheDocument()
    expect(screen.getByText("Cú pháp & Biến căn bản")).toBeInTheDocument()
  })

  it("renders /recommendations route", () => {
    renderWithRouter("/recommendations")
    expect(screen.getByText("Gợi ý học tập theo năng lực")).toBeInTheDocument()
    expect(screen.getByText(/Tóm tắt trực quan/i)).toBeInTheDocument()
  })

  it("renders /prediction route", () => {
    renderWithRouter("/prediction")
    expect(screen.getByText("Dự đoán kết quả & Giải thích (XAI)")).toBeInTheDocument()
    expect(screen.getByText(/Xác suất thành công ước tính/i)).toBeInTheDocument()
  })

  it("renders /admin route", () => {
    renderWithRouter("/admin")
    expect(screen.getByText("Quản trị Hệ thống & Nội dung")).toBeInTheDocument()
    expect(screen.getByText("Quản lý Topics")).toBeInTheDocument()
  })

  it("renders 404 for unknown route", () => {
    renderWithRouter("/random-unknown-path")
    expect(screen.getByText("404 - Không tìm thấy trang")).toBeInTheDocument()
  })
})
