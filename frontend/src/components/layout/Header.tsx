import { Menu, Sparkles, User } from "lucide-react"
import { Link } from "react-router-dom"
import { useUiStore } from "@/stores/useUiStore"
import { Button } from "@/components/ui/button"

export function Header() {
  const { toggleMobileMenu } = useUiStore()

  return (
    <header className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-border bg-white px-4 md:px-6 shadow-sm">
      <div className="flex items-center gap-3">
        <button
          onClick={toggleMobileMenu}
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-border text-dark hover:bg-surface-soft md:hidden"
          aria-label="Toggle mobile menu"
        >
          <Menu className="h-5 w-5" />
        </button>

        {/* NextTech Brand Logo - Concept 04 */}
        <Link to="/dashboard" className="flex items-center gap-2 font-bold text-dark text-xl group">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-primary to-secondary text-white shadow-sm group-hover:scale-105 transition-transform">
            <Sparkles className="h-5 w-5 text-dark" />
          </div>
          <span className="tracking-tight">
            Next<span className="text-primary">Tech</span>
          </span>
        </Link>
      </div>

      <div className="flex items-center gap-3">
        <Link to="/login">
          <Button variant="outline" size="sm" className="gap-2">
            <User className="h-4 w-4" />
            <span>Tài khoản</span>
          </Button>
        </Link>
      </div>
    </header>
  )
}
