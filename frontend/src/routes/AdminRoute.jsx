import React from 'react';
import { Navigate, Outlet, Link } from 'react-router';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function AdminRoute({ children }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#0b0f19]">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!user.is_staff) {
    return (
      <div className="min-h-screen bg-[#0b0f19] flex items-center justify-center p-6 text-white font-mono">
        <div className="max-w-md w-full bg-[#131b2e] border border-red-500/40 rounded-2xl p-8 text-center shadow-2xl shadow-red-950/30">
          <div className="w-16 h-16 bg-red-500/10 border border-red-500/30 text-red-400 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-5">
            🛑
          </div>
          <h1 className="text-2xl font-black tracking-tight text-white mb-2">Access Denied</h1>
          <p className="text-sm text-slate-400 mb-6 leading-relaxed">
            Staff privileges are required to access the SkillForge Command Center. Your account (<span className="text-cyan-400 font-semibold">{user.username}</span>) does not have administrator authorization.
          </p>
          <Link
            to="/dashboard"
            className="inline-flex items-center justify-center px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 text-white font-bold text-sm tracking-wide shadow-lg shadow-cyan-500/20 hover:brightness-110 transition-all"
          >
            ← Return to Student Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return children ? children : <Outlet />;
}

