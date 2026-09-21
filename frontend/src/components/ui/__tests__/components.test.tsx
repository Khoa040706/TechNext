import { describe, it, expect, vi } from "vitest"
import { render, screen, fireEvent } from "@testing-library/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Select } from "@/components/ui/select"

describe("UI Primitives Smoke Tests", () => {
  it("renders Button and handles click events", () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Bắt đầu học</Button>)
    const button = screen.getByRole("button", { name: "Bắt đầu học" })
    expect(button).toBeInTheDocument()
    fireEvent.click(button)
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it("disables Button when isLoading is true", () => {
    render(<Button isLoading>Đang lưu</Button>)
    const button = screen.getByRole("button")
    expect(button).toBeDisabled()
  })

  it("renders Input and supports focus and change", () => {
    render(<Input placeholder="Nhập tên đăng nhập" />)
    const input = screen.getByPlaceholderText("Nhập tên đăng nhập") as HTMLInputElement
    expect(input).toBeInTheDocument()
    fireEvent.change(input, { target: { value: "student_01" } })
    expect(input.value).toBe("student_01")
    input.focus()
    expect(document.activeElement).toBe(input)
  })

  it("applies error styles on Input when hasError is true", () => {
    render(<Input hasError placeholder="Lỗi nhập" />)
    const input = screen.getByPlaceholderText("Lỗi nhập")
    expect(input.className).toContain("border-status-error")
  })

  it("renders Badge with various variants", () => {
    const { rerender } = render(<Badge variant="success">Hoàn thành</Badge>)
    expect(screen.getByText("Hoàn thành")).toBeInTheDocument()

    rerender(<Badge variant="error">Thất bại</Badge>)
    expect(screen.getByText("Thất bại")).toBeInTheDocument()
  })

  it("renders Card hierarchy correctly", () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Tiêu đề Card</CardTitle>
        </CardHeader>
        <CardContent>Nội dung chi tiết</CardContent>
      </Card>
    )
    expect(screen.getByText("Tiêu đề Card")).toBeInTheDocument()
    expect(screen.getByText("Nội dung chi tiết")).toBeInTheDocument()
  })

  it("renders Progress bar with appropriate role", () => {
    render(<Progress value={75} aria-label="Tiến độ học" />)
    const progress = screen.getByRole("progressbar")
    expect(progress).toBeInTheDocument()
  })

  it("renders Select and changes value", () => {
    render(
      <Select defaultValue="py" aria-label="Ngôn ngữ">
        <option value="py">Python</option>
        <option value="js">JavaScript</option>
      </Select>
    )
    const select = screen.getByRole("combobox") as HTMLSelectElement
    expect(select.value).toBe("py")
    fireEvent.change(select, { target: { value: "js" } })
    expect(select.value).toBe("js")
  })
})
