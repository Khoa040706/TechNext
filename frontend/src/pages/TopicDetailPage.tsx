import { useParams, Link } from "react-router-dom"
import { ArrowLeft, CheckCircle, PlayCircle, Code } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export function TopicDetailPage() {
  const { topicId } = useParams<{ topicId: string }>()

  return (
    <div className="space-y-6">
      <Link to="/learn" className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-dark">
        <ArrowLeft className="h-4 w-4" />
        <span>Quay lại danh sách chủ đề</span>
      </Link>

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <Badge variant="default" className="mb-2">{topicId || "TOPIC"}</Badge>
          <h1 className="text-2xl font-bold text-dark">Chủ đề: Cấu trúc điều kiện & Logic</h1>
          <p className="text-gray-600 text-sm mt-1">
            Nắm vững mệnh đề if-else, điều kiện lồng nhau và toán tử logic trong Python.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-lg font-bold text-dark">Nội dung bài học</h2>
          
          <Card className="hover:border-primary/40 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between py-4">
              <div className="flex items-center gap-3">
                <CheckCircle className="h-5 w-5 text-status-success" />
                <div>
                  <CardTitle className="text-sm font-semibold">1. Khái niệm If - Else căn bản</CardTitle>
                  <p className="text-xs text-gray-500">Lý thuyết • 15 phút</p>
                </div>
              </div>
              <Button variant="outline" size="sm">Xem lại</Button>
            </CardHeader>
          </Card>

          <Card className="border-primary/40 hover:border-primary transition-colors">
            <CardHeader className="flex flex-row items-center justify-between py-4">
              <div className="flex items-center gap-3">
                <PlayCircle className="h-5 w-5 text-primary" />
                <div>
                  <CardTitle className="text-sm font-semibold">2. Mệnh đề Elif và điều kiện phức</CardTitle>
                  <p className="text-xs text-gray-500">Lý thuyết & Ví dụ • 20 phút</p>
                </div>
              </div>
              <Button variant="default" size="sm">Học tiếp</Button>
            </CardHeader>
          </Card>
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-bold text-dark">Bài kiểm tra & Code</h2>
          
          <Card>
            <CardHeader className="py-4">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <Code className="h-4 w-4 text-primary" />
                <span>Coding Exercise</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-xs text-gray-600">Kiểm tra năm nhuận và phân loại điểm số.</p>
              <Link to="/exercise/ex_conditionals_01">
                <Button variant="outline" size="sm" className="w-full">
                  Làm bài code
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="py-4">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-primary" />
                <span>Kiểm tra nhanh (Quiz)</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-xs text-gray-600">5 câu trắc nghiệm lý thuyết mệnh đề điều kiện.</p>
              <Link to="/quiz/qz_conditionals_01">
                <Button variant="secondary" size="sm" className="w-full">
                  Làm Quiz
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
