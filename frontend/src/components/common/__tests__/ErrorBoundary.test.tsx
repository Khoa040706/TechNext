import { describe, it, expect, vi, beforeAll, afterAll } from "vitest"
import { render, screen } from "@testing-library/react"
import { ErrorBoundary } from "@/components/common/ErrorBoundary"

const ProblemChild = () => {
  throw new Error("Cố tình ném lỗi kiểm thử ErrorBoundary")
}

describe("ErrorBoundary Component Test", () => {
  const originalConsoleError = console.error

  beforeAll(() => {
    // Suppress console.error output during deliberate error throwing
    console.error = vi.fn()
  })

  afterAll(() => {
    console.error = originalConsoleError
  })

  it("catches render errors and shows graceful error screen", () => {
    render(
      <ErrorBoundary>
        <ProblemChild />
      </ErrorBoundary>
    )

    expect(screen.getByText("Đã có lỗi xảy ra")).toBeInTheDocument()
    expect(
      screen.getByText(/Hệ thống gặp sự cố không mong muốn/i)
    ).toBeInTheDocument()
    expect(screen.getByText("Cố tình ném lỗi kiểm thử ErrorBoundary")).toBeInTheDocument()
  })

  it("renders children normally when there is no error", () => {
    render(
      <ErrorBoundary>
        <div>Nội dung an toàn</div>
      </ErrorBoundary>
    )

    expect(screen.getByText("Nội dung an toàn")).toBeInTheDocument()
  })
})
