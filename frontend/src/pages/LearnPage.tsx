import { BookOpen, Clock } from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

const mockTopics = [
  { id: "top_01", title: "Variables & Data Types", lessons: 4, exercises: 2, status: "completed" },
  { id: "top_02", title: "Conditionals & Logic", lessons: 5, exercises: 3, status: "in_progress" },
  { id: "top_03", title: "Loops & Iterations", lessons: 6, exercises: 4, status: "locked" },
  { id: "top_04", title: "Arrays & Lists", lessons: 8, exercises: 6, status: "locked" },
  { id: "top_05", title: "Functions & Scope", lessons: 5, exercises: 4, status: "locked" },
]

export function LearnPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-dark">Lộ trình học tập</h1>
        <p className="text-gray-600 text-sm mt-1">
          Các chủ đề lập trình và thuật toán nền tảng được sắp xếp theo mức độ thích ứng.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockTopics.map((topic) => (
          <Card key={topic.id} className="flex flex-col justify-between hover:border-primary/50 transition-colors">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-medium text-gray-500 uppercase">{topic.id}</span>
                {topic.status === "completed" && <Badge variant="success">Hoàn thành</Badge>}
                {topic.status === "in_progress" && <Badge variant="warning">Đang học</Badge>}
                {topic.status === "locked" && <Badge variant="outline">Chưa mở</Badge>}
              </div>
              <CardTitle className="text-base">{topic.title}</CardTitle>
              <CardDescription className="flex items-center gap-4 text-xs mt-2">
                <span className="flex items-center gap-1">
                  <BookOpen className="h-3.5 w-3.5" />
                  {topic.lessons} bài học
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5" />
                  {topic.exercises} bài tập
                </span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link to={`/learn/${topic.id}`}>
                <Button
                  variant={topic.status === "locked" ? "outline" : "default"}
                  className="w-full"
                  disabled={topic.status === "locked"}
                >
                  {topic.status === "completed" ? "Ôn tập lại" : topic.status === "in_progress" ? "Tiếp tục học" : "Chưa đủ điều kiện"}
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
