import { Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface LoadingStateProps {
  message?: string
  className?: string
  variant?: "spinner" | "skeleton"
}

export function LoadingState({
  message = "Đang tải dữ liệu...",
  className,
  variant = "spinner",
}: LoadingStateProps) {
  if (variant === "skeleton") {
    return (
      <div className={cn("space-y-3 p-4 w-full animate-pulse", className)} role="status" aria-label={message}>
        <div className="h-6 bg-border-soft rounded-md w-1/3" />
        <div className="h-4 bg-border-soft rounded-md w-full" />
        <div className="h-4 bg-border-soft rounded-md w-4/5" />
        <div className="h-24 bg-border-soft rounded-xl w-full mt-4" />
      </div>
    )
  }

  return (
    <div
      className={cn("flex flex-col items-center justify-center py-12 px-4 text-center", className)}
      role="status"
      aria-label={message}
    >
      <Loader2 className="h-8 w-8 animate-spin text-primary mb-3" />
      <p className="text-sm font-medium text-dark/70">{message}</p>
    </div>
  )
}
