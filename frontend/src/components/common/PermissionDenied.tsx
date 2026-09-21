import { ShieldAlert } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useNavigate } from "react-router-dom"

interface PermissionDeniedProps {
  title?: string
  message?: string
  className?: string
}

export function PermissionDenied({
  title = "Không có quyền truy cập",
  message = "Bạn không có quyền xem trang hoặc tài nguyên này. Vui lòng liên hệ quản trị viên hoặc quay về trang chủ.",
  className,
}: PermissionDeniedProps) {
  const navigate = useNavigate()

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center p-12 text-center rounded-xl border border-amber-200 bg-amber-50/50 my-8",
        className
      )}
      role="alert"
    >
      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-amber-100 text-status-warning mb-4">
        <ShieldAlert className="h-7 w-7" />
      </div>
      <h3 className="text-lg font-bold text-dark mb-2">{title}</h3>
      <p className="text-sm text-gray-600 max-w-md mb-6">{message}</p>
      <Button onClick={() => navigate("/dashboard")} variant="default" size="sm">
        Về trang tổng quan
      </Button>
    </div>
  )
}
