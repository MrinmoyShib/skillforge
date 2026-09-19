import React, { useState } from 'react';
import { NavLink, Outlet, Link } from 'react-router';
import { useAuth } from '../../context/AuthContext';

export default function AdminLayout() {
  const { user } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const navItems = [
    {
      name: 'Telemetry Hub',
      path: '/admin',
      end: true,
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      )
    },
    {
      name: 'Problem Studio',
      path: '/admin/problems',
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
      )
    },
    {
      name: 'Guided Projects',
      path: '/admin/projects',
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      )
    },
    {
      name: 'Developer Directory',
      path: '/admin/users',
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      )
    },
    {
      name: 'Submissions Audit',
      path: '/admin/submissions',
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
  ];

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col font-sans antialiased">
      {/* Top Admin Telemetry Strip */}
      <header className="h-16 bg-[#0f172a]/95 backdrop-blur border-b border-cyan-500/20 px-4 md:px-6 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-4">
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <Link to="/admin" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 via-indigo-600 to-fuchsia-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
              <span className="font-black text-white text-lg">⚡</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-black tracking-tight text-white text-base">SkillForge</span>
                <span className="text-[10px] font-mono uppercase tracking-widest px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/40 font-bold">
                  Root Admin
                </span>
              </div>
              <span className="text-[11px] font-mono text-slate-400 hidden sm:block">Command & Control Studio</span>
            </div>
          </Link>
        </div>

        {/* Right Header: System Status & User Actions */}
        <div className="flex items-center gap-3 md:gap-5">
          {/* Health Pill */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Cluster: Online</span>
          </div>

          {/* Admin User Chip */}
          <div className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-slate-800/80 border border-slate-700">
            <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white font-bold flex items-center justify-center text-xs">
              {user?.username?.[0]?.toUpperCase() || 'A'}
            </div>
            <div className="hidden sm:block text-left">
              <p className="text-xs font-bold text-white leading-tight">{user?.username}</p>
              <p className="text-[10px] text-cyan-400 font-mono">Super Admin</p>
            </div>
          </div>

          {/* Return to Student View */}
          <Link
            to="/dashboard"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 text-xs font-semibold transition-colors"
          >
            <span>Student App</span>
            <span className="text-slate-400">➔</span>
          </Link>
        </div>
      </header>

      {/* Body: Sidebar + Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <aside
          className={`fixed inset-y-0 left-0 pt-16 z-40 w-64 bg-[#0d1322] border-r border-slate-800 flex flex-col justify-between transition-transform duration-200 ease-in-out md:static md:translate-x-0 ${mobileOpen ? 'translate-x-0' : '-translate-x-full'
            }`}
        >
          <div className="p-4 space-y-1 overflow-y-auto">
            <div className="px-3 py-2 text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold">
              Navigation
            </div>
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.end}
                onClick={() => setMobileOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${isActive
                    ? 'bg-gradient-to-r from-cyan-500/20 to-indigo-500/10 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/10 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                {item.icon}
                <span>{item.name}</span>
              </NavLink>
            ))}

            <div className="pt-6 px-3 py-2 text-[11px] font-mono uppercase tracking-wider text-slate-400 font-bold">
              Database Backdoor
            </div>
            <a
              href={`${import.meta.env.VITE_API_BASE_URL?.replace('/api/v1', '') || ''}/admin/`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium text-amber-400/90 hover:text-amber-300 bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 transition-all group"
            >
              <div className="flex items-center gap-3">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                </svg>
                <span>Django DB Admin</span>
              </div>
              <svg className="w-4 h-4 text-amber-400/60 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>

          {/* Footer Info */}
          <div className="p-4 border-t border-slate-800/80 text-xs font-mono text-slate-400">
            <div className="flex items-center justify-between mb-1">
              <span>SkillForge Engine</span>
              <span className="text-cyan-400 font-semibold">v1.2.0</span>
            </div>
            <div className="text-[11px] text-slate-400">
              Isolation: Judge0 + Celery
            </div>
          </div>
        </aside>

        {/* Mobile Backdrop */}
        {mobileOpen && (
          <div
            onClick={() => setMobileOpen(false)}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 md:hidden"
          />
        )}

        {/* Main Workspace Area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8 bg-[#0b0f19]">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

