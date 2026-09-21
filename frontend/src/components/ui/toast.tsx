import * as React from "react"
import { X, CheckCircle, AlertTriangle, AlertCircle, Info } from "lucide-react"
import { cn } from "@/lib/utils"

export type ToastType = "info" | "success" | "warning" | "error"

export interface ToastItem {
  id: string
  title?: string
  description: string
  type?: ToastType
}

interface ToastContextType {
  toasts: ToastItem[]
  toast: (options: Omit<ToastItem, "id">) => void
  dismiss: (id: string) => void
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastItem[]>([])

  const toast = React.useCallback((options: Omit<ToastItem, "id">) => {
    const id = Math.random().toString(36).substring(2, 9)
    const newToast: ToastItem = { ...options, id, type: options.type || "info" }
    setToasts((prev) => [...prev, newToast])

    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, 4000)
  }, [])

  const dismiss = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ toasts, toast, dismiss }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col space-y-2 max-w-sm w-full pointer-events-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={cn(
              "pointer-events-auto flex items-start gap-3 p-4 rounded-xl shadow-lg border transition-all animate-in slide-in-from-bottom-5",
              t.type === "success" && "bg-white border-green-300 text-dark",
              t.type === "error" && "bg-white border-red-300 text-dark",
              t.type === "warning" && "bg-white border-amber-300 text-dark",
              t.type === "info" && "bg-white border-border text-dark"
            )}
          >
            <div className="mt-0.5 shrink-0">
              {t.type === "success" && <CheckCircle className="h-5 w-5 text-status-success" />}
              {t.type === "error" && <AlertCircle className="h-5 w-5 text-status-error" />}
              {t.type === "warning" && <AlertTriangle className="h-5 w-5 text-status-warning" />}
              {t.type === "info" && <Info className="h-5 w-5 text-status-info" />}
            </div>
            <div className="flex-1 text-sm">
              {t.title && <p className="font-semibold text-dark">{t.title}</p>}
              <p className="text-gray-600">{t.description}</p>
            </div>
            <button
              onClick={() => dismiss(t.id)}
              className="text-gray-400 hover:text-dark p-0.5 rounded transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = React.useContext(ToastContext)
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider")
  }
  return context
}
