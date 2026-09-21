import { BookOpen, Code, ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

const mockRecommendations = [
  {
    id: "rec_01",
    type: "theory",
    targetSkill: "Duyệt mảng 1 chiều",
    title: "Tóm tắt trực quan: Cách duyệt mảng và tránh lỗi Index Out of Range",
    difficulty: "Dễ",
    score: 0.89,
    reason: "Bạn vừa gặp 2 lỗi IndexError trong lần nộp code bài tập mảng gần nhất.",
    actionLink: "/learn/top_04",
    actionLabel: "Đọc tài liệu ôn tập",
  },
  {
    id: "rec_02",
    type: "exercise",
    targetSkill: "Vòng lặp For & While",
    title: "Bài tập rèn luyện: Tính tổng các số chẵn trong danh sách",
    difficulty: "Dễ",
    score: 0.82,
    reason: "Kỹ năng vòng lặp đang ở mức 58%, cần thêm 1 bài thực hành thành công để củng cố.",
    actionLink: "/exercise/ex_for_sum",
    actionLabel: "Thực hành ngay",
  },
]

export function RecommendationsPage() {
  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <Badge variant="default">AI Recommendation</Badge>
          <span className="text-xs text-gray-500 font-mono">Rule + Collaborative Baseline</span>
        </div>
        <h1 className="text-2xl font-bold text-dark">Gợi ý học tập theo năng lực</h1>
        <p className="text-gray-600 text-sm mt-1">
          Các tài liệu, bài giảng và bài tập được hệ thống đề xuất dựa trên điểm yếu hiện tại của bạn.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {mockRecommendations.map((rec) => (
          <Card key={rec.id} className="border-border hover:border-primary/50 transition-colors">
            <CardHeader>
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  {rec.type === "theory" ? (
                    <Badge variant="outline" className="gap-1">
                      <BookOpen className="h-3 w-3" /> Lý thuyết
                    </Badge>
                  ) : (
                    <Badge variant="outline" className="gap-1">
                      <Code className="h-3 w-3" /> Bài tập code
                    </Badge>
                  )}
                  <span className="text-xs font-semibold text-primary">Kỹ năng: {rec.targetSkill}</span>
                </div>
                <Badge variant="secondary">Độ khó: {rec.difficulty}</Badge>
              </div>
              <CardTitle className="text-base text-dark">{rec.title}</CardTitle>
              <CardDescription className="text-xs mt-1">
                Độ tương thích khuyến nghị: <strong>{(rec.score * 100).toFixed(0)}%</strong>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-xl bg-surface-soft p-3.5 border border-border text-xs text-gray-700">
                <span className="font-semibold text-dark block mb-0.5">Vì sao NextTech gợi ý mục này?</span>
                {rec.reason}
              </div>
              <div className="flex justify-end">
                <Link to={rec.actionLink}>
                  <Button size="sm" className="gap-2">
                    <span>{rec.actionLabel}</span>
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
