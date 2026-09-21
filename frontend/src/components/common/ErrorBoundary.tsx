import { Component, ErrorInfo, ReactNode } from "react"
import { AlertTriangle, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error in component:", error, errorInfo)
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null })
    window.location.reload()
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="min-h-screen flex items-center justify-center p-6 bg-surface-soft">
          <div className="max-w-md w-full bg-white rounded-2xl border border-red-200 p-8 shadow-sm text-center">
            <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center text-status-error">
              <AlertTriangle className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-bold text-dark mb-2">Đã có lỗi xảy ra</h2>
            <p className="text-sm text-gray-600 mb-6">
              Hệ thống gặp sự cố không mong muốn khi tải giao diện. Bạn có thể tải lại trang để thử lại.
            </p>
            {this.state.error && (
              <pre className="text-xs bg-gray-50 p-3 rounded-lg text-left text-gray-700 overflow-x-auto mb-6 max-h-32 border border-border">
                {this.state.error.message}
              </pre>
            )}
            <Button onClick={this.handleReset} className="w-full gap-2">
              <RefreshCw className="w-4 h-4" />
              Tải lại ứng dụng
            </Button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
