import { Link, Outlet, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'

export function Layout() {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/design', label: 'Design Pipeline' },
    { path: '/results', label: 'Results' },
    { path: '/editor', label: 'Code Editor' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Navigation */}
      <nav className="border-b bg-white/80 backdrop-blur-sm dark:bg-slate-900/80">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
                <span className="text-xl font-bold text-white">M</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                MetaMind
              </span>
            </Link>

            {/* Navigation Links */}
            <div className="flex space-x-1">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    "px-4 py-2 rounded-md text-sm font-medium transition-colors",
                    location.pathname === item.path
                      ? "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-100"
                  )}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t bg-white/80 backdrop-blur-sm dark:bg-slate-900/80 mt-auto">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between text-sm text-slate-600 dark:text-slate-400">
            <p>© 2024 MetaMind - Autonomous AI Pipeline Designer</p>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-slate-900 dark:hover:text-slate-100">
                Documentation
              </a>
              <a href="#" className="hover:text-slate-900 dark:hover:text-slate-100">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Made with Bob
