import { Settings, Plus, BookOpen, Target, CheckSquare, Code, Layers } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export function AdminPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="outline">Admin & Instructor Portal</Badge>
          </div>
          <h1 className="text-2xl font-bold text-dark">Quản trị Hệ thống & Nội dung</h1>
          <p className="text-gray-600 text-sm mt-1">
            Quản lý Topic, Skill, Lesson, Quiz, Coding Exercise và tài liệu học.
          </p>
        </div>
        <Button className="gap-2 shrink-0">
          <Plus className="h-4 w-4" />
          <span>Tạo nội dung mới</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="hover:border-primary/50 transition-colors">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-primary/10 text-primary">
                <BookOpen className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-base">Quản lý Topics</CardTitle>
                <CardDescription className="text-xs">5 chủ đề hiện có</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">Cấu hình thứ tự chủ đề và liên kết bài học.</p>
            <Button variant="outline" size="sm" className="w-full">Xem danh sách</Button>
          </CardContent>
        </Card>

        <Card className="hover:border-primary/50 transition-colors">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-secondary/30 text-dark">
                <Target className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-base">Quản lý Skills</CardTitle>
                <CardDescription className="text-xs">12 kỹ năng đo lường</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">Thiết lập điều kiện tiên quyết (prerequisites).</p>
            <Button variant="outline" size="sm" className="w-full">Xem danh sách</Button>
          </CardContent>
        </Card>

        <Card className="hover:border-primary/50 transition-colors">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-green-100 text-status-success">
                <CheckSquare className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-base">Quản lý Quizzes</CardTitle>
                <CardDescription className="text-xs">24 câu hỏi trắc nghiệm</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">Soạn câu hỏi và ánh xạ kỹ năng đánh giá.</p>
            <Button variant="outline" size="sm" className="w-full">Xem danh sách</Button>
          </CardContent>
        </Card>

        <Card className="hover:border-primary/50 transition-colors">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-blue-100 text-blue-600">
                <Code className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-base">Quản lý Coding Exercises</CardTitle>
                <CardDescription className="text-xs">18 bài tập Python</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">Quản lý test cases và thiết lập độ khó.</p>
            <Button variant="outline" size="sm" className="w-full">Xem danh sách</Button>
          </CardContent>
        </Card>

        <Card className="hover:border-primary/50 transition-colors">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-amber-100 text-status-warning">
                <Layers className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-base">Học liệu & Resources</CardTitle>
                <CardDescription className="text-xs">30 tài liệu tham khảo</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">Kho tài liệu phục vụ hệ thống gợi ý AI.</p>
            <Button variant="outline" size="sm" className="w-full">Xem danh sách</Button>
          </CardContent>
        </Card>

        <Card className="hover:border-primary/50 transition-colors">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-gray-100 text-gray-700">
                <Settings className="h-5 w-5" />
              </div>
              <div>
                <CardTitle className="text-base">Model Metadata</CardTitle>
                <CardDescription className="text-xs">ML Models & Experiment logs</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-xs text-gray-600 mb-4">Xem model version, feature order và metrics.</p>
            <Button variant="outline" size="sm" className="w-full">Xem cấu hình</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
