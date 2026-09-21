import { describe, it, expect, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import { LoadingState } from "@/components/common/LoadingState"
import { EmptyState } from "@/components/common/EmptyState"
import { ErrorState } from "@/components/common/ErrorState"
import { PermissionDenied } from "@/components/common/PermissionDenied"

describe("State Patterns Component Tests", () => {
  it("renders LoadingState with spinner and message", () => {
    render(<LoadingState message="Đang nạp bài tập..." />)
    expect(screen.getByRole("status")).toBeInTheDocument()
    expect(screen.getByText("Đang nạp bài tập...")).toBeInTheDocument()
  })

  it("renders LoadingState skeleton variant", () => {
    render(<LoadingState variant="skeleton" message="Đang tải dữ liệu..." />)
    expect(screen.getByRole("status")).toBeInTheDocument()
  })

  it("renders EmptyState and triggers action", () => {
    const handleAction = vi.fn()
    render(
      <EmptyState
        title="Chưa có gợi ý"
        description="Hãy hoàn thành bài học đầu tiên."
        actionLabel="Học ngay"
        onAction={handleAction}
      />
    )
    expect(screen.getByText("Chưa có gợi ý")).toBeInTheDocument()
    expect(screen.getByText("Hãy hoàn thành bài học đầu tiên.")).toBeInTheDocument()
    const button = screen.getByRole("button", { name: "Học ngay" })
    fireEvent.click(button)
    expect(handleAction).toHaveBeenCalledTimes(1)
  })

  it("renders ErrorState and triggers retry", () => {
    const handleRetry = vi.fn()
    render(
      <ErrorState
        title="Lỗi tải danh sách"
        message="Vui lòng kiểm tra kết nối mạng."
        onRetry={handleRetry}
      />
    )
    expect(screen.getByRole("alert")).toBeInTheDocument()
    expect(screen.getByText("Lỗi tải danh sách")).toBeInTheDocument()
    const retryBtn = screen.getByRole("button", { name: /Thử lại/i })
    fireEvent.click(retryBtn)
    expect(handleRetry).toHaveBeenCalledTimes(1)
  })

  it("renders PermissionDenied notice", () => {
    render(
      <BrowserRouter>
        <PermissionDenied />
      </BrowserRouter>
    )
    expect(screen.getByText("Không có quyền truy cập")).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Về trang tổng quan" })).toBeInTheDocument()
  })
})
