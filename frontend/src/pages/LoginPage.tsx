import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/components/ui/toast"
import { useNavigate } from "react-router-dom"

const loginSchema = z.object({
  email: z.string().email("Email không hợp lệ"),
  password: z.string().min(6, "Mật khẩu phải có ít nhất 6 ký tự"),
})

type LoginFormValues = z.infer<typeof loginSchema>

export function LoginPage() {
  const { toast } = useToast()
  const navigate = useNavigate()

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  const onSubmit = async (values: LoginFormValues) => {
    // Placeholder login flow for foundation phase
    toast({
      title: "Đăng nhập thử nghiệm",
      description: `Xin chào ${values.email}! Đang chuyển hướng vào Dashboard.`,
      type: "success",
    })
    navigate("/dashboard")
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4">
      <Card className="w-full max-w-md border-border shadow-md">
        <CardHeader className="text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-tr from-primary to-secondary text-white mb-3 shadow-sm">
            <Sparkles className="h-6 w-6 text-dark" />
          </div>
          <CardTitle className="text-2xl font-bold text-dark">Đăng nhập NextTech</CardTitle>
          <CardDescription>
            Hệ thống giáo dục cá nhân hóa lập trình và thuật toán
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
            <div>
              <label className="block text-sm font-medium text-dark mb-1">Email</label>
              <Input
                type="email"
                placeholder="sinhvien@example.com"
                hasError={!!errors.email}
                {...register("email")}
              />
              {errors.email && (
                <p className="text-xs text-status-error mt-1">{errors.email.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-dark mb-1">Mật khẩu</label>
              <Input
                type="password"
                placeholder="••••••••"
                hasError={!!errors.password}
                {...register("password")}
              />
              {errors.password && (
                <p className="text-xs text-status-error mt-1">{errors.password.message}</p>
              )}
            </div>

            <Button type="submit" className="w-full mt-2" isLoading={isSubmitting}>
              Đăng nhập
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
