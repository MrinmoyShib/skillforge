import { useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router';
import { useAuth } from '../../context/AuthContext';

export default function AppLayout() {
  const { user, logout, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen w-full overflow-x-hidden bg-[var(--color-surface-dark)] text-[var(--color-text-primary)] flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <header className="sticky top-0 z-50 w-full border-b border-[var(--color-surface-hover)] bg-[var(--color-surface-card)]/90 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link to={user ? "/dashboard" : "/"} className="flex items-center gap-2.5 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center text-white font-black text-lg shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
                S
              </div>
              <span className="text-xl font-bold tracking-tight text-white group-hover:text-cyan-300 transition-colors">
                Skill<span className="text-[var(--color-brand-accent)]">Forge</span>
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
              {user && (
                <Link
                  to="/dashboard"
                  className={`transition-colors ${location.pathname === '/dashboard' ? 'text-white font-semibold' : 'text-[var(--color-text-secondary)] hover:text-white'}`}
                >
                  Dashboard
                </Link>
              )}
              <Link
                to="/problems"
                className={`transition-colors ${location.pathname.startsWith('/problems') ? 'text-white font-semibold' : 'text-[var(--color-text-secondary)] hover:text-white'}`}
              >
                Challenges
              </Link>
              <Link
                to="/projects"
                className={`transition-colors ${location.pathname.startsWith('/projects') ? 'text-white font-semibold' : 'text-[var(--color-text-secondary)] hover:text-white'}`}
              >
                Projects
              </Link>
              <Link
                to="/leaderboard"
                className={`transition-colors ${location.pathname === '/leaderboard' ? 'text-white font-semibold' : 'text-[var(--color-text-secondary)] hover:text-white'}`}
              >
                Leaderboard
              </Link>
              <Link
                to="/achievements"
                className={`transition-colors ${location.pathname === '/achievements' ? 'text-white font-semibold' : 'text-[var(--color-text-secondary)] hover:text-white'}`}
              >
                Achievements
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-3">
            {loading ? (
              <div className="w-8 h-8 rounded-full bg-slate-800 animate-pulse" />
            ) : user ? (
              <div className="flex items-center gap-3 sm:gap-4">
                {/* Level & XP Badges */}
                <div className="hidden sm:flex items-center gap-2 bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-full text-xs font-semibold">
                  <span className="text-cyan-400">Lvl {user.profile?.current_level ?? 1}</span>
                  <span className="text-slate-600">•</span>
                  <span className="text-indigo-400">{user.profile?.total_xp ?? 0} XP</span>
                </div>

                {/* User Avatar & Portfolio Link */}
                <Link
                  to={`/portfolio/${user.username}`}
                  title="View your public developer portfolio"
                  className="flex items-center gap-2 group hover:opacity-90 transition-opacity"
                >
                  <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-indigo-400/30 group-hover:ring-cyan-400/50 transition-all">
                    {(user.profile?.display_name || user.username || 'U')[0].toUpperCase()}
                  </div>
                  <span className="hidden lg:inline text-sm font-medium text-slate-200 group-hover:text-white">
                    {user.profile?.display_name || user.username}
                  </span>
                </Link>

                {/* Admin Studio Link (Staff Only) */}
                {user.is_staff && (
                  <Link
                    to="/admin"
                    title="Open SkillForge Admin Studio"
                    className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-red-500/20 via-orange-500/20 to-amber-500/20 hover:from-red-500/30 hover:to-amber-500/30 border border-red-500/40 text-red-300 hover:text-white text-xs font-mono font-bold tracking-wide shadow-md shadow-red-500/10 transition-all group"
                  >
                    <span className="w-2 h-2 rounded-full bg-red-400 animate-pulse"></span>
                    <span>Admin Studio</span>
                    <span className="text-red-400 group-hover:translate-x-0.5 transition-transform">➔</span>
                  </Link>
                )}

                {/* Settings Link */}
                <Link
                  to="/settings"
                  title="Account Settings"
                  className="hidden md:flex items-center justify-center p-2 rounded-lg border border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 hover:bg-slate-800 transition"
                >
                  <span className="text-sm">⚙️</span>
                </Link>

                {/* Desktop Logout Button */}
                <button
                  onClick={handleLogout}
                  className="hidden md:inline-block text-xs font-medium px-3 py-1.5 rounded-lg border border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 hover:bg-slate-800 transition"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="hidden sm:flex items-center gap-3">
                <Link
                  to="/login"
                  className="text-sm font-medium text-slate-300 hover:text-white px-3 py-1.5 rounded-lg hover:bg-slate-800/80 transition"
                >
                  Log In
                </Link>
                <Link
                  to="/register"
                  className="text-sm font-semibold bg-[var(--color-brand-primary)] hover:bg-[var(--color-brand-primary-hover)] text-white px-4 py-1.5 rounded-lg shadow-md shadow-indigo-500/20 transition"
                >
                  Get Started
                </Link>
              </div>
            )}

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-xl text-slate-300 hover:text-white bg-slate-800/80 border border-slate-700 hover:bg-slate-700 transition flex items-center justify-center"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Mobile Slide-Down Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-slate-800 bg-slate-950/95 px-4 pt-3 pb-5 space-y-3 backdrop-blur-xl shadow-2xl">
            {/* User Info on Mobile */}
            {user && (
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-indigo-400/30">
                    {(user.profile?.display_name || user.username || 'U')[0].toUpperCase()}
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-white">
                      {user.profile?.display_name || user.username}
                    </div>
                    <div className="text-[11px] text-cyan-400 font-mono">
                      Level {user.profile?.current_level ?? 1} • {user.profile?.total_xp ?? 0} XP
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout();
                  }}
                  className="text-xs px-2.5 py-1 rounded-lg border border-slate-700 bg-slate-800 text-slate-300 hover:text-white"
                >
                  Sign Out
                </button>
              </div>
            )}

            {/* Nav Links */}
            <div className="flex flex-col space-y-1">
              {user && (
                <Link
                  to="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname === '/dashboard' ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
                >
                  <span className="flex items-center gap-2.5">
                    <span>📊</span> Dashboard
                  </span>
                  <span className="text-[11px] text-emerald-400 font-mono font-semibold">My Stats</span>
                </Link>
              )}

              <Link
                to="/problems"
                onClick={() => setMobileMenuOpen(false)}
                className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname.startsWith('/problems') ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
              >
                <span className="flex items-center gap-2.5">
                  <span>💻</span> Challenges
                </span>
                <span className="text-[11px] text-cyan-400 font-mono font-semibold">Catalog</span>
              </Link>

              <Link
                to="/projects"
                onClick={() => setMobileMenuOpen(false)}
                className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname.startsWith('/projects') ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
              >
                <span className="flex items-center gap-2.5">
                  <span>🚀</span> Projects
                </span>
                <span className="text-[11px] text-indigo-400 font-mono font-semibold">Labs</span>
              </Link>

              {user && (
                <Link
                  to={`/portfolio/${user.username}`}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname.startsWith('/portfolio') ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
                >
                  <span className="flex items-center gap-2.5">
                    <span>👨‍💻</span> Portfolio
                  </span>
                  <span className="text-[11px] text-emerald-400 font-mono font-semibold">Public</span>
                </Link>
              )}

              {user && user.is_staff && (
                <Link
                  to="/admin"
                  onClick={() => setMobileMenuOpen(false)}
                  className="px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm bg-red-500/10 border border-red-500/30 text-red-300 hover:text-white font-bold font-mono"
                >
                  <span className="flex items-center gap-2.5">
                    <span>⚡</span> Admin Command Center
                  </span>
                  <span className="text-[11px] text-red-400 uppercase tracking-wider">Root</span>
                </Link>
              )}

              {user && (
                <Link
                  to="/settings"
                  onClick={() => setMobileMenuOpen(false)}
                  className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname === '/settings' ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
                >
                  <span className="flex items-center gap-2.5">
                    <span>⚙️</span> Settings
                  </span>
                  <span className="text-[11px] text-slate-400 font-mono font-semibold">Account</span>
                </Link>
              )}

              <Link
                to="/leaderboard"
                onClick={() => setMobileMenuOpen(false)}
                className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname === '/leaderboard' ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
              >
                <span className="flex items-center gap-2.5">
                  <span>🏆</span> Leaderboard
                </span>
                <span className="text-[11px] text-amber-400 font-mono font-semibold">Rankings</span>
              </Link>

              <Link
                to="/achievements"
                onClick={() => setMobileMenuOpen(false)}
                className={`px-3 py-2.5 rounded-xl transition flex items-center justify-between text-sm ${location.pathname === '/achievements' ? 'bg-indigo-600/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-200 hover:bg-slate-800/80'}`}
              >
                <span className="flex items-center gap-2.5">
                  <span>🎖️</span> Achievements
                </span>
                <span className="text-[11px] text-amber-400 font-mono font-semibold">Badges</span>
              </Link>
            </div>

            {/* Mobile Unauthenticated Action Buttons */}
            {!user && (
              <div className="pt-3 border-t border-slate-800 grid grid-cols-2 gap-2">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center text-sm font-medium text-slate-200 bg-slate-800 hover:bg-slate-700 py-2.5 rounded-xl transition"
                >
                  Log In
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center text-sm font-semibold bg-[var(--color-brand-primary)] hover:bg-[var(--color-brand-primary-hover)] text-white py-2.5 rounded-xl shadow-md shadow-indigo-500/20 transition"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        )}
      </header>

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 min-w-0">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-[var(--color-surface-hover)] bg-[var(--color-surface-card)] text-xs text-[var(--color-text-muted)] py-6 text-center">
        <p>© {new Date().getFullYear()} SkillForge. Built for developer learning and career advancement.</p>
      </footer>
    </div>
  );
}
