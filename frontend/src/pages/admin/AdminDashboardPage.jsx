import React, { useEffect, useState } from 'react';
import { Link } from 'react-router';
import adminService from '../../services/api/adminService';
import Spinner from '../../components/feedback/Spinner';

export default function AdminDashboardPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTelemetry = async () => {
    try {
      setLoading(true);
      const data = await adminService.getAnalytics();
      setAnalytics(data);
      setError(null);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to fetch platform telemetry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTelemetry();
  }, []);

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-500/10 border border-red-500/30 rounded-2xl text-red-400 font-mono">
        <p className="font-bold mb-2">Error Loading Telemetry</p>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchTelemetry}
          className="mt-4 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded-lg text-xs font-semibold"
        >
          Retry
        </button>
      </div>
    );
  }

  const {
    total_users,
    active_users,
    staff_users,
    total_problems,
    published_problems,
    draft_problems,
    total_test_cases,
    total_projects,
    total_milestones_completed,
    total_submissions,
    accepted_submissions,
    acceptance_rate,
    solves_by_language,
    system_health,
  } = analytics;

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-[#131b2e] via-[#162035] to-[#131b2e] p-6 rounded-2xl border border-cyan-500/20 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-black text-white tracking-tight">Platform Telemetry Hub</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 text-xs font-mono font-bold">
              Real-time
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Global developer activity, execution cluster health, and challenge authoring status.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchTelemetry}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition-all"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Refresh</span>
          </button>
          <Link
            to="/admin/problems"
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 transition-all"
          >
            <span>+ New Challenge</span>
          </Link>
        </div>
      </div>

      {/* System Health Strip */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">PostgreSQL DB</span>
            <p className="text-base font-bold text-white mt-1 capitalize">{system_health.database}</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-lg">
            🗄️
          </div>
        </div>

        <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">Execution Sandbox</span>
            <p className="text-base font-bold text-white mt-1 capitalize">{system_health.sandbox}</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-lg">
            ⚡
          </div>
        </div>

        <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-5 flex items-center justify-between">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">Redis Broker</span>
            <p className="text-base font-bold text-white mt-1 capitalize">{system_health.redis}</p>
          </div>
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center text-lg">
            📡
          </div>
        </div>
      </div>

      {/* KPI Counters Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Total Users */}
        <div className="bg-[#131b2e] border border-slate-800 hover:border-cyan-500/40 rounded-2xl p-6 transition-all group">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">Developers</span>
            <span className="text-xl">👥</span>
          </div>
          <div className="text-3xl font-black text-white tracking-tight">{total_users.toLocaleString()}</div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Active (7d): <strong className="text-emerald-400">{active_users}</strong></span>
            <span>Staff: <strong className="text-indigo-400">{staff_users}</strong></span>
          </div>
        </div>

        {/* Problems Catalog */}
        <div className="bg-[#131b2e] border border-slate-800 hover:border-cyan-500/40 rounded-2xl p-6 transition-all group">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">Challenges</span>
            <span className="text-xl">💻</span>
          </div>
          <div className="text-3xl font-black text-white tracking-tight">{total_problems.toLocaleString()}</div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Published: <strong className="text-cyan-400">{published_problems}</strong></span>
            <span>Draft: <strong className="text-amber-400">{draft_problems}</strong></span>
          </div>
        </div>

        {/* Total Submissions */}
        <div className="bg-[#131b2e] border border-slate-800 hover:border-cyan-500/40 rounded-2xl p-6 transition-all group">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">Submissions</span>
            <span className="text-xl">📜</span>
          </div>
          <div className="text-3xl font-black text-white tracking-tight">{total_submissions.toLocaleString()}</div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Accepted: <strong className="text-emerald-400">{accepted_submissions}</strong></span>
            <span>Rate: <strong className="text-cyan-400">{acceptance_rate}%</strong></span>
          </div>
        </div>

        {/* Guided Projects */}
        <div className="bg-[#131b2e] border border-slate-800 hover:border-cyan-500/40 rounded-2xl p-6 transition-all group">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-400">Guided Projects</span>
            <span className="text-xl">🚀</span>
          </div>
          <div className="text-3xl font-black text-white tracking-tight">{total_projects.toLocaleString()}</div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Milestones: <strong className="text-indigo-400">{total_milestones_completed}</strong></span>
            <span>Test Cases: <strong className="text-slate-200">{total_test_cases}</strong></span>
          </div>
        </div>
      </div>

      {/* Language Solves Distribution & Quick Control */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Language Solves Breakdown */}
        <div className="lg:col-span-2 bg-[#131b2e] border border-slate-800 rounded-2xl p-6">
          <h2 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <span>Solves Distribution by Track</span>
            <span className="text-xs font-normal text-slate-400 font-mono">(Accepted submissions)</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Python */}
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-sky-400 flex items-center gap-1.5">
                  <span>🐍</span> Python Track
                </span>
              </div>
              <div className="text-2xl font-black text-white font-mono">
                {solves_by_language.python.toLocaleString()}
              </div>
              <span className="text-[11px] text-slate-400 mt-2 font-mono">Verified Solves</span>
            </div>

            {/* JavaScript */}
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-yellow-400 flex items-center gap-1.5">
                  <span>🟨</span> JavaScript Track
                </span>
              </div>
              <div className="text-2xl font-black text-white font-mono">
                {solves_by_language.javascript.toLocaleString()}
              </div>
              <span className="text-[11px] text-slate-400 mt-2 font-mono">Verified Solves</span>
            </div>

            {/* C++ */}
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-sm text-indigo-400 flex items-center gap-1.5">
                  <span>⚡</span> C++ Track
                </span>
              </div>
              <div className="text-2xl font-black text-white font-mono">
                {solves_by_language.cpp.toLocaleString()}
              </div>
              <span className="text-[11px] text-slate-400 mt-2 font-mono">Verified Solves</span>
            </div>
          </div>
        </div>

        {/* Quick Actions Panel */}
        <div className="bg-[#131b2e] border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h2 className="text-base font-bold text-white mb-4">Command Shortcuts</h2>
            <div className="space-y-2.5">
              <Link
                to="/admin/problems"
                className="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-sm text-slate-200 hover:text-white transition-all group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-cyan-400">💻</span>
                  <span>Problem Studio & Test Cases</span>
                </div>
                <span className="text-slate-400 group-hover:translate-x-0.5 transition-transform">→</span>
              </Link>

              <Link
                to="/admin/users"
                className="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-sm text-slate-200 hover:text-white transition-all group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-emerald-400">👥</span>
                  <span>Moderate Users & Adjust XP</span>
                </div>
                <span className="text-slate-400 group-hover:translate-x-0.5 transition-transform">→</span>
              </Link>

              <Link
                to="/admin/submissions"
                className="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-sm text-slate-200 hover:text-white transition-all group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-indigo-400">📜</span>
                  <span>Audit Submissions & Re-Judge</span>
                </div>
                <span className="text-slate-400 group-hover:translate-x-0.5 transition-transform">→</span>
              </Link>

              <Link
                to="/admin/projects"
                className="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-sm text-slate-200 hover:text-white transition-all group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-fuchsia-400">🚀</span>
                  <span>Curate Guided Projects</span>
                </div>
                <span className="text-slate-400 group-hover:translate-x-0.5 transition-transform">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

