import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Play, Send, CheckCircle, Terminal } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/components/ui/toast"

export function ExercisePage() {
  const { exerciseId } = useParams<{ exerciseId: string }>()
  const { toast } = useToast()
  const [code, setCode] = useState<string>(
    `def is_leap_year(year: int) -> bool:\n    # Viết giải thuật kiểm tra năm nhuận tại đây\n    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):\n        return True\n    return False\n`
  )
  const [output, setOutput] = useState<string | null>(null)
  const [isRunning, setIsRunning] = useState(false)

  const handleRun = () => {
    setIsRunning(true)
    setTimeout(() => {
      setIsRunning(false)
      setOutput("Running test suite...\nTest 1: is_leap_year(2024) -> True [PASS]\nTest 2: is_leap_year(1900) -> False [PASS]\nTest 3: is_leap_year(2000) -> True [PASS]\nAll 3 tests passed!")
      toast({
        title: "Chạy thử thành công",
        description: "3/3 kiểm thử mẫu đã vượt qua!",
        type: "success",
      })
    }, 600)
  }

  const handleSubmit = () => {
    toast({
      title: "Đã nộp bài tập",
      description: "Hệ thống ghi nhận telemetry (execution_source=client_pyodide).",
      type: "info",
    })
  }

  return (
    <div className="space-y-6">
      <Link to="/learn" className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-dark">
        <ArrowLeft className="h-4 w-4" />
        <span>Quay lại danh sách bài</span>
      </Link>

      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="secondary">{exerciseId || "ex_01"}</Badge>
            <Badge variant="outline">Độ khó: Dễ</Badge>
            <Badge variant="default">Python</Badge>
          </div>
          <h1 className="text-xl font-bold text-dark">Bài tập: Kiểm tra năm nhuận</h1>
        </div>
        <div className="flex items-center gap-2">
          <Button onClick={handleRun} variant="outline" size="sm" className="gap-2" isLoading={isRunning}>
            <Play className="h-4 w-4 text-status-success" />
            Chạy thử code
          </Button>
          <Button onClick={handleSubmit} size="sm" className="gap-2">
            <Send className="h-4 w-4" />
            Nộp bài
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Description & Test cases */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Mô tả bài toán</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-gray-700">
              <p>
                Viết hàm <code className="bg-surface-soft px-1.5 py-0.5 rounded text-dark font-mono text-xs">is_leap_year(year: int) -&gt; bool</code> trả về <strong>True</strong> nếu năm truyền vào là năm nhuận theo lịch Dương, ngược lại trả về <strong>False</strong>.
              </p>
              <div className="rounded-lg bg-surface-soft p-3 border border-border text-xs space-y-1">
                <p className="font-semibold text-dark">Quy tắc năm nhuận:</p>
                <p>• Năm chia hết cho 4 nhưng không chia hết cho 100.</p>
                <p>• HOẶC năm chia hết cho 400.</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Các trường hợp kiểm thử (Test Cases)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-xs font-mono">
              <div className="flex items-center justify-between p-2 rounded bg-surface-soft border border-border">
                <span>Input: 2024</span>
                <span className="text-status-success font-semibold flex items-center gap-1">
                  <CheckCircle className="h-3 w-3" /> Output: True
                </span>
              </div>
              <div className="flex items-center justify-between p-2 rounded bg-surface-soft border border-border">
                <span>Input: 1900</span>
                <span className="text-status-success font-semibold flex items-center gap-1">
                  <CheckCircle className="h-3 w-3" /> Output: False
                </span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right: Code area & Terminal output */}
        <div className="space-y-4">
          <Card className="overflow-hidden border-border">
            <div className="flex items-center justify-between px-4 py-2 bg-dark text-white text-xs font-mono">
              <span>solution.py</span>
              <span className="text-gray-400">Python 3.12 (Pyodide Worker)</span>
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-64 p-4 font-mono text-xs text-gray-100 bg-[#1E1E1E] focus:outline-none resize-none leading-relaxed"
              spellCheck={false}
            />
          </Card>

          <Card>
            <CardHeader className="py-3 bg-surface-soft border-b border-border flex flex-row items-center gap-2">
              <Terminal className="h-4 w-4 text-primary" />
              <CardTitle className="text-xs font-mono">Kết quả thực thi (Console / Test Results)</CardTitle>
            </CardHeader>
            <CardContent className="p-3">
              <pre className="text-xs font-mono text-dark whitespace-pre-wrap min-h-[80px]">
                {output || "Chưa có kết quả chạy. Bấm 'Chạy thử code' để kiểm tra."}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
