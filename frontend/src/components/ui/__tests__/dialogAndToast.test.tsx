import { describe, it, expect } from "vitest"
import { render, screen, fireEvent, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { Dialog, DialogTrigger, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { ToastProvider, useToast } from "@/components/ui/toast"
import { Button } from "@/components/ui/button"

function ToastTester() {
  const { toast } = useToast()
  return (
    <Button onClick={() => toast({ title: "Thông báo thử nghiệm", description: "Nội dung toast", type: "success" })}>
      Kích hoạt Toast
    </Button>
  )
}

describe("Dialog, Tabs, and Toast Tests", () => {
  it("renders and opens Dialog modal when triggered", () => {
    render(
      <Dialog>
        <DialogTrigger asChild>
          <button>Mở hộp thoại</button>
        </DialogTrigger>
        <DialogContent>
          <DialogTitle>Xác nhận nộp bài</DialogTitle>
          <DialogDescription>Bạn có chắc chắn muốn nộp bài tập này không?</DialogDescription>
        </DialogContent>
      </Dialog>
    )

    const trigger = screen.getByText("Mở hộp thoại")
    expect(trigger).toBeInTheDocument()
    fireEvent.click(trigger)

    expect(screen.getByText("Xác nhận nộp bài")).toBeInTheDocument()
    expect(screen.getByText("Bạn có chắc chắn muốn nộp bài tập này không?")).toBeInTheDocument()
  })

  it("switches tabs correctly", async () => {
    const user = userEvent.setup()
    render(
      <Tabs defaultValue="tab1">
        <TabsList>
          <TabsTrigger value="tab1">Tab 1</TabsTrigger>
          <TabsTrigger value="tab2">Tab 2</TabsTrigger>
        </TabsList>
        <TabsContent value="tab1">Nội dung Tab 1</TabsContent>
        <TabsContent value="tab2">Nội dung Tab 2</TabsContent>
      </Tabs>
    )

    expect(screen.getByText("Nội dung Tab 1")).toBeInTheDocument()
    const tab2 = screen.getByRole("tab", { name: "Tab 2" })
    await user.click(tab2)

    await waitFor(() => {
      expect(screen.getByText("Nội dung Tab 2")).toBeInTheDocument()
    })
  })

  it("triggers and displays toast notification", () => {
    render(
      <ToastProvider>
        <ToastTester />
      </ToastProvider>
    )

    const button = screen.getByRole("button", { name: "Kích hoạt Toast" })
    fireEvent.click(button)

    expect(screen.getByText("Thông báo thử nghiệm")).toBeInTheDocument()
    expect(screen.getByText("Nội dung toast")).toBeInTheDocument()
  })
})
