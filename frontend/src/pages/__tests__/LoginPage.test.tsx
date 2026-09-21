import { describe, it, expect } from "vitest"
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import { BrowserRouter } from "react-router-dom"
import { LoginPage } from "@/pages/LoginPage"
import { ToastProvider } from "@/components/ui/toast"

describe("LoginPage Form & Zod Validation Tests", () => {
  it("renders login form with inputs and submit button", () => {
    render(
      <BrowserRouter>
        <ToastProvider>
          <LoginPage />
        </ToastProvider>
      </BrowserRouter>
    )

    expect(screen.getByText("Đăng nhập NextTech")).toBeInTheDocument()
    expect(screen.getByPlaceholderText("sinhvien@example.com")).toBeInTheDocument()
    expect(screen.getByPlaceholderText("••••••••")).toBeInTheDocument()
    expect(screen.getByRole("button", { name: "Đăng nhập" })).toBeInTheDocument()
  })

  it("validates invalid email and short password with Zod error messages", async () => {
    render(
      <BrowserRouter>
        <ToastProvider>
          <LoginPage />
        </ToastProvider>
      </BrowserRouter>
    )

    const emailInput = screen.getByPlaceholderText("sinhvien@example.com")
    const passwordInput = screen.getByPlaceholderText("••••••••")
    const submitBtn = screen.getByRole("button", { name: "Đăng nhập" })

    fireEvent.change(emailInput, { target: { value: "not-an-email" } })
    fireEvent.change(passwordInput, { target: { value: "123" } })
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(screen.getByText("Email không hợp lệ")).toBeInTheDocument()
      expect(screen.getByText("Mật khẩu phải có ít nhất 6 ký tự")).toBeInTheDocument()
    })
  })
})
