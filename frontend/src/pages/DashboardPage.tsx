import { BookOpen, Target, Compass, TrendingUp, CheckCircle, ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"

export function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Welcome banner */}
      <div className="rounded-2xl bg-gradient-to-r from-secondary/40 via-surface-soft to-primary/20 p-6 md:p-8 border border-border">
        <div className="max-w-2xl">
          <Badge variant="default" className="mb-3">Kỳ học nền tảng</Badge>
          <h1 className="text-2xl md:text-3xl font-extrabold text-dark mb-2">
            Chào mừng trở lại với NextTech!
          </h1>
          <p className="text-gray-700 text-sm md:text-base mb-4">
            Lộ trình học tập cá nhân hóa được tối ưu dựa trên dữ liệu lý thuyết và bài tập lập trình của bạn.
          </p>
          <Link to="/learn">
            <Button className="gap-2">
              <span>Tiếp tục học bài gần nhất</span>
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </div>

      {/* Metrics grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Tiến độ chung</CardTitle>
            <BookOpen className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">65%</div>
            <Progress value={65} className="mt-2" />
            <p className="text-xs text-gray-500 mt-2">13/20 bài học hoàn thành</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Skill Mastery</CardTitle>
            <Target className="h-4 w-4 text-status-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">7.4 / 10</div>
            <div className="flex items-center gap-1.5 mt-2">
              <Badge variant="success">Ổn định</Badge>
              <span className="text-xs text-gray-500">4 kỹ năng thành thạo</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Gợi ý ôn tập</CardTitle>
            <Compass className="h-4 w-4 text-status-warning" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">2 mục</div>
            <p className="text-xs text-status-warning mt-2">Cần củng cố: Duyệt mảng</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Dự đoán bài tiếp theo</CardTitle>
            <TrendingUp className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">Khả quan</div>
            <p className="text-xs text-gray-500 mt-2">Xác suất thành công ~78%</p>
          </CardContent>
        </Card>
      </div>

      {/* Main sections */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Left: Active tasks */}
        <Card>
          <CardHeader>
            <CardTitle>Bài tập đang thực hiện</CardTitle>
            <CardDescription>Các nội dung đang đợi bạn hoàn thành</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-surface-soft transition-colors">
              <div className="flex items-center gap-3">
                <CheckCircle className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="font-semibold text-sm text-dark">Vòng lặp For & Duyệt mảng</p>
                  <p className="text-xs text-gray-500">Coding Exercise • Python</p>
                </div>
              </div>
              <Link to="/exercise/ex_01">
                <Button variant="outline" size="sm">Làm bài</Button>
              </Link>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-surface-soft transition-colors">
              <div className="flex items-center gap-3">
                <CheckCircle className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="font-semibold text-sm text-dark">Trắc nghiệm: Câu lệnh điều kiện</p>
                  <p className="text-xs text-gray-500">Quiz • 5 câu hỏi</p>
                </div>
              </div>
              <Link to="/quiz/qz_01">
                <Button variant="outline" size="sm">Làm quiz</Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Right: AI Recommendation teaser */}
        <Card className="border-primary/30 bg-surface-soft/30">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Gợi ý cá nhân hóa (AI Recommendation)</CardTitle>
              <Badge variant="default">AI Suggestion</Badge>
            </div>
            <CardDescription>Học liệu được chọn riêng theo điểm yếu hiện tại</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 rounded-xl bg-white border border-border shadow-sm">
              <p className="font-semibold text-sm text-dark">Kỹ năng: Duyệt mảng 1 chiều</p>
              <p className="text-xs text-gray-600 mt-1">
                <strong>Lý do:</strong> Tỷ lệ test case pass gần đây dưới 60%. Hệ thống khuyến nghị làm bài tập mức độ Dễ trước khi sang mảng 2 chiều.
              </p>
              <div className="mt-3 flex gap-2">
                <Link to="/recommendations">
                  <Button size="sm" variant="secondary">Xem chi tiết gợi ý</Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
