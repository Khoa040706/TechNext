import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "outline" | "success" | "warning" | "error"
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variants = {
    default: "bg-primary/20 text-dark border-primary/30",
    secondary: "bg-secondary text-secondary-foreground border-border",
    outline: "text-dark border-border bg-white",
    success: "bg-green-100 text-status-success border-green-200",
    warning: "bg-amber-100 text-status-warning border-amber-200",
    error: "bg-red-100 text-status-error border-red-200",
  }

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        variants[variant],
        className
      )}
      {...props}
    />
  )
}

export { Badge }
