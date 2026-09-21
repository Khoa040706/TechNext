import { FileQuestion } from "lucide-react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"

export function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-6">
      <div className="h-16 w-16 rounded-full bg-secondary/40 text-primary flex items-center justify-center mb-4">
        <FileQuestion className="h-8 w-8" />
      </div>
      <h1 className="text-3xl font-extrabold text-dark mb-2">404 - Không tìm thấy trang</h1>
      <p className="text-gray-600 text-sm max-w-md mb-6">
        Đường dẫn bạn đang tìm kiếm không tồn tại hoặc đã được chuyển sang địa chỉ khác.
      </p>
      <Link to="/dashboard">
        <Button variant="default">Quay về trang tổng quan</Button>
      </Link>
    </div>
  )
}
