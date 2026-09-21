import {
  LayoutDashboard,
  BookOpen,
  Target,
  Compass,
  TrendingUp,
  Settings,
  X,
} from "lucide-react"
import { NavLink } from "react-router-dom"
import { useUiStore } from "@/stores/useUiStore"
import { cn } from "@/lib/utils"

const navigation = [
  { name: "Tổng quan", href: "/dashboard", icon: LayoutDashboard },
  { name: "Học tập", href: "/learn", icon: BookOpen },
  { name: "Kỹ năng & Mastery", href: "/skills", icon: Target },
  { name: "Gợi ý học tập", href: "/recommendations", icon: Compass },
  { name: "Dự đoán & XAI", href: "/prediction", icon: TrendingUp },
  { name: "Quản trị", href: "/admin", icon: Settings },
]

export function Sidebar() {
  const { mobileMenuOpen, setMobileMenuOpen } = useUiStore()

  return (
    <>
      {/* Mobile backdrop */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm md:hidden"
          onClick={() => setMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar container */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-border bg-white transition-transform duration-200 ease-in-out md:static md:translate-x-0",
          mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Mobile header inside sidebar */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-border md:hidden">
          <span className="font-bold text-dark">Menu điều hướng</span>
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="p-1 rounded-lg text-dark hover:bg-surface-soft"
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation items */}
        <div className="flex-1 overflow-y-auto p-4 space-y-1">
          <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-gray-400">
            Học tập cá nhân hóa
          </div>

          {navigation.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.href}
                to={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary/20 text-dark font-semibold border-l-4 border-primary"
                      : "text-gray-600 hover:bg-surface-soft hover:text-dark"
                  )
                }
              >
                <Icon className="h-5 w-5 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            )
          })}
        </div>

        {/* Footer info in sidebar */}
        <div className="p-4 border-t border-border text-xs text-gray-500">
          <p className="font-semibold text-dark">NextTech V1</p>
          <p>Personalized Education</p>
        </div>
      </aside>
    </>
  )
}
