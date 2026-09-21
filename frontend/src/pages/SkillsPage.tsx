import { Target, TrendingUp, AlertCircle, CheckCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

const mockSkills = [
  { id: "sk_01", name: "Cú pháp & Biến căn bản", mastery: 92, level: "Thành thạo", status: "good" },
  { id: "sk_02", name: "Toán tử logic & Phép so sánh", mastery: 85, level: "Tốt", status: "good" },
  { id: "sk_03", name: "Cấu trúc rẽ nhánh If-Else", mastery: 74, level: "Khá", status: "good" },
  { id: "sk_04", name: "Vòng lặp For & While", mastery: 58, level: "Trung bình", status: "warning" },
  { id: "sk_05", name: "Duyệt mảng 1 chiều", mastery: 42, level: "Cần củng cố", status: "danger" },
  { id: "sk_06", name: "Tìm kiếm & Lọc trên mảng", mastery: 35, level: "Yếu", status: "danger" },
]

export function SkillsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-dark">Phân tích Kỹ năng & Mastery</h1>
        <p className="text-gray-600 text-sm mt-1">
          Ước lượng độ thành thạo kỹ năng dựa trên kết quả trắc nghiệm và tỷ lệ pass test case bài code.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="border-green-200 bg-green-50/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-semibold flex items-center gap-2 text-status-success">
              <CheckCircle className="h-4 w-4" />
              <span>Kỹ năng vững vàng</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">3 kỹ năng</div>
            <p className="text-xs text-gray-500 mt-1">Mastery &gt; 70%</p>
          </CardContent>
        </Card>

        <Card className="border-amber-200 bg-amber-50/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-semibold flex items-center gap-2 text-status-warning">
              <TrendingUp className="h-4 w-4" />
              <span>Đang tiến bộ</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">1 kỹ năng</div>
            <p className="text-xs text-gray-500 mt-1">Mastery 50% - 70%</p>
          </CardContent>
        </Card>

        <Card className="border-red-200 bg-red-50/30">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-semibold flex items-center gap-2 text-status-error">
              <AlertCircle className="h-4 w-4" />
              <span>Cần ôn tập gấp</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-dark">2 kỹ năng</div>
            <p className="text-xs text-gray-500 mt-1">Mastery &lt; 50%</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Chi tiết các kỹ năng quan sát được</CardTitle>
          <CardDescription>Bảng phân phối năng lực theo từng kỹ năng đo lường</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {mockSkills.map((skill) => (
            <div key={skill.id} className="p-4 rounded-xl border border-border bg-white space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <div className="flex items-center gap-2">
                  <Target className="h-4 w-4 text-primary" />
                  <span className="font-semibold text-sm text-dark">{skill.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-dark">{skill.mastery}%</span>
                  <Badge
                    variant={
                      skill.status === "good"
                        ? "success"
                        : skill.status === "warning"
                        ? "warning"
                        : "error"
                    }
                  >
                    {skill.level}
                  </Badge>
                </div>
              </div>
              <Progress value={skill.mastery} />
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
