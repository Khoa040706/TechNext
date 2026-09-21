import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, CheckCircle2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/components/ui/toast"

export function QuizPage() {
  const { quizId } = useParams<{ quizId: string }>()
  const { toast } = useToast()
  const [selectedOption, setSelectedOption] = useState<number | null>(null)
  const [submitted, setSubmitted] = useState(false)

  const mockQuestion = {
    text: "Trong Python, kết quả của biểu thức (True and not False) or False là gì?",
    options: ["True", "False", "None", "Báo lỗi cú pháp"],
    correctIndex: 0,
    explanation: "Biểu thức 'not False' là True, do đó 'True and True' là True. 'True or False' trả về True.",
  }

  const handleSubmit = () => {
    if (selectedOption === null) return
    setSubmitted(true)
    const isCorrect = selectedOption === mockQuestion.correctIndex
    toast({
      title: isCorrect ? "Chính xác!" : "Chưa chính xác",
      description: isCorrect ? "Bạn đã chọn đúng đáp án." : "Xem lời giải thích chi tiết bên dưới.",
      type: isCorrect ? "success" : "warning",
    })
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <Link to="/learn" className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-dark">
        <ArrowLeft className="h-4 w-4" />
        <span>Quay lại bài học</span>
      </Link>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <Badge variant="secondary">Mã quiz: {quizId || "qz_demo"}</Badge>
            <span className="text-xs text-gray-500 font-medium">Câu hỏi 1 / 1</span>
          </div>
          <CardTitle className="text-lg mt-3">{mockQuestion.text}</CardTitle>
          <CardDescription>Chọn một phương án chính xác nhất</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            {mockQuestion.options.map((opt, idx) => {
              const isSelected = selectedOption === idx
              const isCorrect = submitted && idx === mockQuestion.correctIndex
              const isWrong = submitted && isSelected && idx !== mockQuestion.correctIndex

              return (
                <button
                  key={idx}
                  type="button"
                  onClick={() => !submitted && setSelectedOption(idx)}
                  className={`w-full flex items-center justify-between p-4 rounded-xl border text-left text-sm transition-all ${
                    isCorrect
                      ? "border-green-400 bg-green-50 text-status-success font-medium"
                      : isWrong
                      ? "border-red-400 bg-red-50 text-status-error font-medium"
                      : isSelected
                      ? "border-primary bg-primary/10 text-dark font-medium"
                      : "border-border bg-white text-dark hover:bg-surface-soft"
                  }`}
                >
                  <span>{String.fromCharCode(65 + idx)}. {opt}</span>
                  {isCorrect && <CheckCircle2 className="h-4 w-4 text-status-success" />}
                </button>
              )
            })}
          </div>

          {submitted && (
            <div className="p-4 rounded-xl bg-surface-soft border border-border mt-4 text-xs text-gray-700">
              <strong className="block text-dark mb-1">Giải thích:</strong>
              {mockQuestion.explanation}
            </div>
          )}

          <div className="flex justify-end pt-4">
            {!submitted ? (
              <Button onClick={handleSubmit} disabled={selectedOption === null}>
                Gửi đáp án
              </Button>
            ) : (
              <Button onClick={() => { setSubmitted(false); setSelectedOption(null) }} variant="outline">
                Làm lại câu hỏi
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
