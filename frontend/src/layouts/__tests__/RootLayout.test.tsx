import { describe, it, expect } from "vitest"
import { render, screen } from "@testing-library/react"
import { MemoryRouter, Routes, Route } from "react-router-dom"
import { RootLayout } from "@/layouts/RootLayout"

describe("App Shell & RootLayout Navigation Tests", () => {
  it("renders header, sidebar, and child content in main container", () => {
    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <Routes>
          <Route path="/" element={<RootLayout />}>
            <Route path="dashboard" element={<div>Trang Dashboard Nội Dung</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    )

    // Check Header branding
    expect(screen.getByText("Next")).toBeInTheDocument()
    expect(screen.getByText("Tech")).toBeInTheDocument()

    // Check Sidebar links
    expect(screen.getByText("Tổng quan")).toBeInTheDocument()
    expect(screen.getByText("Học tập")).toBeInTheDocument()
    expect(screen.getByText("Kỹ năng & Mastery")).toBeInTheDocument()
    expect(screen.getByText("Gợi ý học tập")).toBeInTheDocument()
    expect(screen.getByText("Dự đoán & XAI")).toBeInTheDocument()
    expect(screen.getByText("Quản trị")).toBeInTheDocument()

    // Check Child content rendered inside main container
    expect(screen.getByText("Trang Dashboard Nội Dung")).toBeInTheDocument()
  })
})
