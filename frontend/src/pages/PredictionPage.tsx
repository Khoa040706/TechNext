import { TrendingUp, AlertTriangle, ArrowRight, Activity } from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export function PredictionPage() {
  const mockPrediction = {
    targetType: "next_exercise_success",
    targetName: "Bài tập tiếp theo: Thuật toán tìm kiếm nhị phân cơ bản",
    probability: 0.58,
    riskBand: "medium", // low, medium, high
    modelVersion: "v1.0.0-logistic-regression",
    explanation: {
      summary: "Khả năng hoàn thành bài tiếp theo hiện ở mức trung bình (58%). Bạn có thể gặp một số khó khăn ở phần xử lý chỉ số mảng.",
      topFactors: [
        { factor: "Tỷ lệ pass test case gần đây", impact: "-15%", direction: "negative" },
        { factor: "Số lần retry trên các bài tập mảng", impact: "-10%", direction: "negative" },
        { factor: "Điểm trắc nghiệm lý thuyết đạt 85%", impact: "+12%", direction: "positive" },
        { factor: "Đã hoàn thành các bài điều kiện tiên quyết", impact: "+8%", direction: "positive" },
      ],
      recommendedAction: "Nên ôn tập lại kiến thức 'Duyệt mảng' trong khoảng 10 phút và làm một bài tập mức Dễ trước khi bắt đầu bài này.",
    },
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <Badge variant="default">Student Performance Prediction</Badge>
          <span className="text-xs text-gray-500 font-mono">Model: {mockPrediction.modelVersion}</span>
        </div>
        <h1 className="text-2xl font-bold text-dark">Dự đoán kết quả & Giải thích (XAI)</h1>
        <p className="text-gray-600 text-sm mt-1">
          Hệ thống phân tích lịch sử học tập để cảnh báo sớm khó khăn và đưa ra giải thích minh bạch.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Prediction summary card */}
        <Card className="lg:col-span-1 border-primary/40 bg-white">
          <CardHeader>
            <CardTitle className="text-base">Xác suất thành công ước tính</CardTitle>
            <CardDescription>{mockPrediction.targetName}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6 text-center">
            <div className="py-4">
              <div className="text-5xl font-extrabold text-primary">
                {(mockPrediction.probability * 100).toFixed(0)}%
              </div>
              <div className="mt-3 flex justify-center">
                <Badge variant="warning" className="px-3 py-1 text-xs">
                  Mức độ rủi ro: Trung bình
                </Badge>
              </div>
            </div>

            <div className="text-xs text-gray-500 text-left bg-surface-soft p-3 rounded-xl border border-border">
              <p className="font-semibold text-dark mb-1 flex items-center gap-1">
                <Activity className="h-3.5 w-3.5 text-primary" /> Lưu ý phương pháp
              </p>
              Dự đoán dựa trên mô hình học máy được huấn luyện độc lập từ dữ liệu lịch sử làm bài và không đại diện cho điểm số học phần chính thức.
            </div>
          </CardContent>
        </Card>

        {/* XAI Explanation card */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-primary" />
              <CardTitle className="text-lg">Giải thích mô hình (Explainable AI - XAI)</CardTitle>
            </div>
            <CardDescription>
              Các yếu tố cốt lõi đóng góp vào kết quả dự đoán (Feature Attribution / SHAP values)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <p className="text-sm text-dark font-medium leading-relaxed bg-surface-soft p-4 rounded-xl border border-border">
              {mockPrediction.explanation.summary}
            </p>

            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3">
                Các yếu tố ảnh hưởng chính (Feature Weights)
              </h4>
              <div className="space-y-2.5">
                {mockPrediction.explanation.topFactors.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 rounded-lg border border-border bg-white text-xs"
                  >
                    <span className="font-medium text-dark">{item.factor}</span>
                    <Badge
                      variant={item.direction === "positive" ? "success" : "error"}
                      className="font-mono text-xs"
                    >
                      {item.impact}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-4">
              <div className="flex items-start gap-2.5">
                <AlertTriangle className="h-5 w-5 text-status-warning shrink-0 mt-0.5" />
                <div className="text-xs space-y-1">
                  <p className="font-bold text-dark">Hành động khuyến nghị (Next Action):</p>
                  <p className="text-gray-700 leading-relaxed">
                    {mockPrediction.explanation.recommendedAction}
                  </p>
                </div>
              </div>
              <div className="mt-4 flex justify-end">
                <Link to="/learn/top_04">
                  <Button size="sm" variant="default" className="gap-2">
                    <span>Thực hiện hành động đề xuất</span>
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
