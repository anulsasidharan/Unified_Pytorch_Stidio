import { BookMarked, BookOpen, Bot, Code2, Home, LineChart, LogIn, LogOut, Upload } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/store/authStore';
import { useState } from 'react';
import { AuthDialog } from '@/components/auth/AuthDialog';

const navItems = [
  { label: 'Home', icon: Home, to: '/' },
  { label: 'Learn', icon: BookOpen, to: '/learn' },
  { label: 'Practice', icon: Code2, to: '/practice' },
  { label: 'Track', icon: LineChart, to: '/track' },
  { label: 'Revision', icon: BookMarked, to: '/revision' },
  { label: 'Import', icon: Upload, to: '/import' },
  { label: 'Assistant', icon: Bot, to: '/assistant' },
] as const;

export function Navbar() {
  const user = useAuthStore((s) => s.user);
  const clearAuth = useAuthStore((s) => s.clearAuth);
  const [authOpen, setAuthOpen] = useState(false);

  return (
    <>
      <AuthDialog open={authOpen} onOpenChange={setAuthOpen} />
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          <NavLink to="/" className="flex items-center gap-2 font-semibold tracking-tight">
            <Code2 className="h-5 w-5 text-primary" />
            <span>DSA Studio</span>
          </NavLink>
          <nav className="hidden items-center gap-1 md:flex">
            {navItems.map(({ label, icon: Icon, to }) => (
              <NavLink
                key={label}
                to={to}
                className={({ isActive }) =>
                  cn(
                    'inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground',
                    isActive && 'bg-accent text-accent-foreground',
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            {user ? (
              <>
                <span className="hidden text-sm text-muted-foreground sm:inline">{user.username}</span>
                <Button variant="ghost" size="sm" onClick={clearAuth}>
                  <LogOut className="h-4 w-4" />
                  <span className="sr-only sm:not-sr-only sm:ml-1">Logout</span>
                </Button>
              </>
            ) : (
              <Button variant="outline" size="sm" onClick={() => setAuthOpen(true)}>
                <LogIn className="h-4 w-4" />
                <span className="ml-1">Sign in</span>
              </Button>
            )}
          </div>
        </div>
      </header>
    </>
  );
}
