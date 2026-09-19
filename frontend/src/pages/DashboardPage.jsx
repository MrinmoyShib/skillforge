import { useState, useEffect } from 'react';
import { Link } from 'react-router';
import { dashboardService } from '../services/api/dashboardService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTrackTab, setActiveTrackTab] = useState('all');

  const fetchDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await dashboardService.getDashboardData();
      setData(res);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
      setError('Unable to load dashboard data. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[55vh] space-y-3">
        <Spinner />
        <p className="text-xs font-mono text-slate-400">Loading your developer telemetry...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-[var(--color-surface-card)] border border-slate-800 rounded-2xl p-8 max-w-lg mx-auto text-center space-y-4 shadow-xl">
        <div className="text-4xl">⚠️</div>
        <h2 className="text-xl font-bold text-white">Dashboard Unavailable</h2>
        <p className="text-xs text-slate-400">{error || 'Something went wrong while aggregating metrics.'}</p>
        <button
          onClick={fetchDashboard}
          className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition shadow-md"
        >
          Try Again
        </button>
      </div>
    );
  }

  const { stats, category_mastery, recent_submissions, recommended_problems, recent_activity, enrolled_projects } = data;

  const getVerdictBadge = (status) => {
    switch (status) {
      case 'ACCEPTED':
        return 'text-emerald-300 bg-emerald-950/60 border-emerald-800/60';
      case 'WRONG_ANSWER':
        return 'text-rose-300 bg-rose-950/60 border-rose-800/60';
      case 'COMPILATION_ERROR':
        return 'text-amber-300 bg-amber-950/60 border-amber-800/60';
      case 'TIME_LIMIT_EXCEEDED':
        return 'text-orange-300 bg-orange-950/60 border-orange-800/60';
      default:
        return 'text-slate-300 bg-slate-800 border-slate-700';
    }
  };

  const getDifficultyBadge = (diff) => {
    switch (diff) {
      case 'easy':
        return 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60';
      case 'medium':
        return 'bg-amber-950/60 text-amber-300 border-amber-800/60';
      case 'hard':
        return 'bg-rose-950/60 text-rose-300 border-rose-800/60';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  const getLanguageInfo = (lang, item = null) => {
    const raw = (
      lang ||
      item?.language ||
      item?.slug ||
      item?.category_slug ||
      item?.problem_slug ||
      ''
    ).toLowerCase();

    if (raw.includes('python') || raw.startsWith('py') || raw.includes('/py-') || raw.includes('py-')) {
      return {
        label: 'Python 3',
        icon: '🐍',
        badgeClass: 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60',
        gradientClass: 'from-emerald-500 to-teal-400',
        accentText: 'text-emerald-400',
        borderHover: 'hover:border-emerald-500/50',
        bgHighlight: 'bg-emerald-950/30',
      };
    }
    if (raw.includes('javascript') || raw.includes('node') || raw.startsWith('js') || raw.includes('/js-') || raw.includes('js-')) {
      return {
        label: 'JavaScript',
        icon: '🟨',
        badgeClass: 'bg-amber-950/60 text-amber-300 border-amber-800/60',
        gradientClass: 'from-amber-500 to-yellow-400',
        accentText: 'text-amber-400',
        borderHover: 'hover:border-amber-500/50',
        bgHighlight: 'bg-amber-950/30',
      };
    }
    return {
      label: 'C++',
      icon: '⚡',
      badgeClass: 'bg-cyan-950/60 text-cyan-300 border-cyan-800/60',
      gradientClass: 'from-cyan-500 to-indigo-400',
      accentText: 'text-cyan-400',
      borderHover: 'hover:border-cyan-500/50',
      bgHighlight: 'bg-cyan-950/30',
    };
  };

  const TRACK_SLUGS = ['python', 'javascript', 'cpp'];
  const trackCategories = category_mastery.filter(c => TRACK_SLUGS.includes(c.slug));
  const filteredTracks = activeTrackTab === 'all'
    ? (trackCategories.length > 0
      ? trackCategories
      : category_mastery.filter(c => !['arrays', 'strings', 'math-logic', 'control-flow'].includes(c.slug)))
    : category_mastery.filter(c => c.slug === activeTrackTab);

  return (
    <div className="space-y-8 w-full min-w-0">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-indigo-950/90 via-slate-900 to-slate-950 border border-indigo-500/20 rounded-2xl p-6 sm:p-8 relative overflow-hidden shadow-xl">
        <div className="absolute right-0 top-0 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-semibold mb-3">
              <span>🚀</span> Level {stats.current_level} • {stats.level_title}
            </div>
            <h1 className="text-2xl sm:text-4xl font-black text-white tracking-tight">
              Welcome back, {stats.display_name}!
            </h1>
            <p className="text-slate-400 text-xs sm:text-sm mt-2 max-w-xl leading-relaxed">
              SkillForge now features 100 curated challenges across Python, JavaScript, and C++.
              Master algorithms from Beginner foundations to Grandmaster complexity with zero duplicate problems.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              to="/problems"
              className="px-5 py-2.5 rounded-xl bg-[var(--color-brand-primary)] hover:bg-[var(--color-brand-primary-hover)] text-white font-bold text-xs sm:text-sm shadow-md shadow-indigo-500/25 transition flex items-center gap-2"
            >
              <span>Explore Challenges</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </Link>
          </div>
        </div>
      </div>

      {/* Key Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {/* Level Card */}
        <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-5 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider">
            <span>Current Tier</span>
            <span className="text-lg">🏆</span>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline gap-2">
              <span className="text-2xl sm:text-3xl font-black text-white">Level {stats.current_level}</span>
              <span className="text-xs text-indigo-400 font-semibold">{stats.level_title}</span>
            </div>
            <div className="mt-3">
              <div className="flex justify-between text-[11px] text-slate-400 mb-1 font-mono">
                <span>Next Milestone</span>
                <span>{stats.next_level_xp ? `${stats.total_xp} / ${stats.next_level_xp} XP` : 'Max Tier Reached'}</span>
              </div>
              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full transition-all duration-500"
                  style={{ width: `${stats.progress_percent}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Total XP Card */}
        <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-5 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider">
            <span>Experience Points</span>
            <span className="text-lg">⚡</span>
          </div>
          <div className="mt-4">
            <div className="text-2xl sm:text-3xl font-black text-cyan-400 font-mono">
              {stats.total_xp.toLocaleString()}
            </div>
            <p className="text-xs text-slate-400 mt-2">Verified lifetime engineering XP</p>
          </div>
        </div>

        {/* Challenges Mastered Card */}
        <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-5 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider">
            <span>Problems Solved</span>
            <span className="text-lg">💡</span>
          </div>
          <div className="mt-4">
            <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">
              {stats.problems_solved_count}
            </div>
            <p className="text-xs text-slate-400 mt-2">Unique challenges mastered</p>
          </div>
        </div>

        {/* Daily Streak Card */}
        <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-5 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider">
            <span>Daily Streak</span>
            <span className="text-lg">🔥</span>
          </div>
          <div className="mt-4">
            <div className="text-2xl sm:text-3xl font-black text-amber-400 font-mono">
              {stats.current_streak_days} {stats.current_streak_days === 1 ? 'Day' : 'Days'}
            </div>
            <p className="text-xs text-slate-400 mt-2">
              {stats.current_streak_days > 0 ? 'Consistent practice streak' : 'Solve a challenge today to ignite streak!'}
            </p>
          </div>
        </div>
      </div>

      {/* Language Track Mastery Visualizer Section */}
      <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span>🎯</span> Language Track Mastery
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Track your solved challenges, remaining problems, and XP points earned across Python, JavaScript, and C++
            </p>
          </div>

          {/* Interactive Track Switcher */}
          <div className="flex items-center gap-1.5 bg-slate-900/90 p-1 rounded-xl border border-slate-800 shrink-0">
            <button
              onClick={() => setActiveTrackTab('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeTrackTab === 'all'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
                }`}
            >
              All Tracks
            </button>
            <button
              onClick={() => setActiveTrackTab('python')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${activeTrackTab === 'python'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
                }`}
            >
              <span>🐍</span> Python
            </button>
            <button
              onClick={() => setActiveTrackTab('javascript')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${activeTrackTab === 'javascript'
                ? 'bg-amber-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
                }`}
            >
              <span>🟨</span> JavaScript
            </button>
            <button
              onClick={() => setActiveTrackTab('cpp')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${activeTrackTab === 'cpp'
                ? 'bg-cyan-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
                }`}
            >
              <span>⚡</span> C++
            </button>
          </div>
        </div>

        {/* Track Cards Grid */}
        <div className={`grid grid-cols-1 ${activeTrackTab === 'all' ? 'md:grid-cols-3' : 'md:grid-cols-1'} gap-5`}>
          {filteredTracks.map((cat) => {
            const langInfo = getLanguageInfo(cat.slug, cat);
            const remaining = cat.remaining_problems ?? Math.max(0, cat.total_problems - cat.solved_problems);
            const pointsGot = cat.xp_earned ?? 0;

            return (
              <div
                key={cat.id}
                className={`p-5 rounded-2xl bg-slate-900/70 border border-slate-800/90 ${langInfo.borderHover} transition flex flex-col justify-between space-y-5 shadow-sm`}
              >
                {/* Header */}
                <div className="space-y-4">
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-3">
                      <div className="text-3xl p-2 rounded-xl bg-slate-950 border border-slate-800 shadow-inner flex items-center justify-center">
                        {langInfo.icon}
                      </div>
                      <div>
                        <h3 className="text-base font-bold text-white flex items-center gap-2">
                          {cat.name}
                        </h3>
                        <p className="text-xs text-slate-400">
                          {cat.total_problems} Curated Challenges
                        </p>
                      </div>
                    </div>
                    <div className="text-right font-mono">
                      <span className={`text-lg font-black ${langInfo.accentText}`}>
                        {cat.mastery_percent}%
                      </span>
                      <p className="text-[10px] uppercase font-mono tracking-wider text-slate-500 font-bold">
                        Mastery
                      </p>
                    </div>
                  </div>

                  {/* Main Progress Bar */}
                  <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                    <div
                      className={`h-full bg-gradient-to-r ${langInfo.gradientClass} rounded-full transition-all duration-500`}
                      style={{ width: `${cat.mastery_percent}%` }}
                    />
                  </div>

                  {/* Dedicated Metric Boxes: Solved, Remaining, Points Got */}
                  <div className="grid grid-cols-3 gap-2.5 pt-1">
                    {/* Box 1: Solved */}
                    <div className="bg-slate-950/80 border border-emerald-900/50 rounded-xl p-3 text-center flex flex-col justify-center shadow-inner">
                      <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">
                        Solved
                      </div>
                      <div className="text-xl sm:text-2xl font-black text-white font-mono mt-0.5">
                        {cat.solved_problems}
                      </div>
                      <div className="text-[10px] text-slate-400 mt-0.5">
                        of {cat.total_problems}
                      </div>
                    </div>

                    {/* Box 2: Remaining */}
                    <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-center flex flex-col justify-center shadow-inner">
                      <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">
                        Remaining
                      </div>
                      <div className="text-xl sm:text-2xl font-black text-slate-200 font-mono mt-0.5">
                        {remaining}
                      </div>
                      <div className="text-[10px] text-slate-500 mt-0.5">
                        to solve
                      </div>
                    </div>

                    {/* Box 3: Points Got */}
                    <div className="bg-slate-950/80 border border-amber-900/50 rounded-xl p-3 text-center flex flex-col justify-center shadow-inner">
                      <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-400">
                        Points Got
                      </div>
                      <div className="text-xl sm:text-2xl font-black text-amber-300 font-mono mt-0.5 truncate">
                        +{pointsGot}
                      </div>
                      <div className="text-[10px] text-slate-400 mt-0.5">
                        XP points
                      </div>
                    </div>
                  </div>
                </div>

                {/* Card Action Footer */}
                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-3">
                  <Link
                    to={`/problems?track=${cat.slug}`}
                    className="text-xs font-mono text-slate-400 hover:text-white transition flex items-center gap-1"
                  >
                    <span>Catalog ({cat.total_problems})</span>
                    <span>→</span>
                  </Link>

                  {cat.next_unsolved_slug ? (
                    <Link
                      to={`/problems/${cat.next_unsolved_slug}`}
                      className={`px-3.5 py-1.5 rounded-xl font-bold text-xs transition flex items-center gap-1.5 shadow-sm ${cat.slug === 'python'
                        ? 'bg-emerald-600 hover:bg-emerald-500 text-white'
                        : cat.slug === 'javascript'
                          ? 'bg-amber-600 hover:bg-amber-500 text-white'
                          : 'bg-cyan-600 hover:bg-cyan-500 text-white'
                        }`}
                    >
                      <span>{cat.solved_problems > 0 ? 'Continue Track' : 'Start Track'}</span>
                      <span>→</span>
                    </Link>
                  ) : (
                    <span className="px-3 py-1.5 rounded-xl bg-emerald-950/80 border border-emerald-800/80 text-emerald-300 text-xs font-bold flex items-center gap-1">
                      <span>✓</span> Track Mastered
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Verified Engineering Projects Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <span>🚀</span> Verified Engineering Projects
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Multi-milestone production systems with automated in-sandbox verification
            </p>
          </div>
          <Link
            to="/projects"
            className="text-xs font-mono text-indigo-400 hover:text-indigo-300 font-semibold transition flex items-center gap-1 self-start sm:self-auto"
          >
            <span>Browse Project Catalog</span>
            <span>→</span>
          </Link>
        </div>

        {(!enrolled_projects || enrolled_projects.length === 0) ? (
          <div className="bg-gradient-to-r from-indigo-950/30 via-slate-900/60 to-indigo-950/30 border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center sm:text-left">
              <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-[11px] font-mono font-semibold">
                <span>⚡</span> Hands-On Real World Labs
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white">
                No active engineering projects yet
              </h3>
              <p className="text-xs text-slate-400 max-w-md">
                Build HTTP routers, memory allocators, async workers, and rate limiters with automated test harnesses.
              </p>
            </div>
            <Link
              to="/projects"
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-md shadow-indigo-600/30 flex items-center gap-2 flex-shrink-0"
            >
              <span>Explore Projects</span>
              <span>➔</span>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {enrolled_projects.map((proj) => {
              const langInfo = getLanguageInfo(proj.language, proj);
              const isCompleted = proj.status === 'COMPLETED';

              return (
                <div
                  key={proj.id}
                  className="bg-[var(--color-surface-card)] border border-slate-800 hover:border-slate-700 rounded-2xl p-5 space-y-4 shadow-sm transition flex flex-col justify-between"
                >
                  <div className="space-y-2.5">
                    <div className="flex items-center justify-between">
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-lg text-xs font-mono font-bold bg-slate-950 border border-slate-800 text-white">
                        <span>{langInfo.icon}</span> {langInfo.label}
                      </span>
                      {isCompleted ? (
                        <span className="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
                          ✓ Verified
                        </span>
                      ) : (
                        <span className="text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full animate-pulse">
                          In Progress
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-white truncate">{proj.title}</h3>

                    {/* Progress Bar */}
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                        <span>Milestones</span>
                        <span className="text-cyan-400 font-semibold">
                          {proj.completed_milestones_count}/{proj.total_milestones_count}
                        </span>
                      </div>
                      <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden border border-slate-800">
                        <div
                          className="bg-gradient-to-r from-indigo-500 to-cyan-400 h-full rounded-full transition-all duration-500"
                          style={{ width: `${proj.progress_percent}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-3">
                    <span className="text-xs font-mono text-cyan-400 font-bold">
                      +{proj.xp_reward} XP
                    </span>

                    <Link
                      to={`/projects/${proj.slug}`}
                      className="px-3.5 py-1.5 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 hover:text-white text-xs font-bold transition flex items-center gap-1"
                    >
                      <span>{isCompleted ? 'Review Lab' : 'Continue Lab'}</span>
                      <span>➔</span>
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Main Grid: Recommended Challenges & Recent Submissions */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Recommended Challenges (7 cols) */}
        <div className="lg:col-span-7 bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 shadow-sm space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <span>💡</span> Recommended Next Steps
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Earliest unsolved challenges in each language track
              </p>
            </div>
            <Link to="/problems" className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold transition">
              Browse All →
            </Link>
          </div>

          <div className="space-y-3">
            {recommended_problems?.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-400">
                <span>🎉</span> All current problems mastered! Excellent engineering progress.
              </div>
            ) : (
              recommended_problems.map((prob) => {
                const langInfo = getLanguageInfo(prob.language, prob);
                return (
                  <div
                    key={prob.id}
                    className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/50 transition flex items-center justify-between gap-4"
                  >
                    <div className="min-w-0 space-y-1.5">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${langInfo.badgeClass} flex items-center gap-1`}>
                          <span>{langInfo.icon}</span> {langInfo.label}
                        </span>
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${getDifficultyBadge(prob.difficulty)}`}>
                          {prob.difficulty}
                        </span>
                        <span className="text-[10px] font-mono text-amber-400 bg-amber-950/40 border border-amber-800/30 px-1.5 rounded font-bold">
                          +{prob.xp_reward} XP
                        </span>
                        <span className="text-[10px] text-slate-400 font-mono">
                          Tier {prob.challenge_level}
                        </span>
                      </div>
                      <Link
                        to={`/problems/${prob.slug}`}
                        className="block text-sm font-bold text-white hover:text-indigo-400 truncate"
                      >
                        {prob.title}
                      </Link>
                    </div>

                    <Link
                      to={`/problems/${prob.slug}`}
                      className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shrink-0 transition shadow-sm"
                    >
                      Solve Now
                    </Link>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right: Milestone Log (5 cols) */}
        <div className="lg:col-span-5 bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 shadow-sm space-y-4">
          <div className="border-b border-slate-800 pb-4">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <span>📜</span> Milestone Activity Log
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Recent progression history</p>
          </div>

          <div className="space-y-3">
            {recent_activity?.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">No milestones yet. Solve your first challenge to generate telemetry!</p>
            ) : (
              recent_activity.map((act) => (
                <div key={act.id} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/60 space-y-1">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className={`font-bold font-mono uppercase ${act.activity_type === 'LEVEL_UP' ? 'text-cyan-400' : 'text-emerald-400'
                      }`}>
                      {act.activity_type === 'LEVEL_UP' ? '⭐ Level Up' : '✓ Solved'}
                    </span>
                    <span className="text-slate-500 font-mono text-[10px]">
                      {new Date(act.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <p className="text-xs text-slate-200 font-medium leading-snug">
                    {act.description}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Recent Submissions Full-Width Table */}
      <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <span>⚡</span> Recent Submissions
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">Live execution outcomes and sandbox verdicts</p>
          </div>
        </div>

        {recent_submissions?.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">
            No submissions recorded yet. Head over to <Link to="/problems" className="text-indigo-400 underline">Challenges</Link> to run code in the sandbox!
          </div>
        ) : (
          <div className="divide-y divide-slate-800/80">
            {recent_submissions.map((sub) => {
              const langInfo = getLanguageInfo(sub.language, sub);
              return (
                <div key={sub.id} className="py-3 flex items-center justify-between gap-4 text-xs">
                  <div className="min-w-0 space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${langInfo.badgeClass}`}>
                        {langInfo.icon} {langInfo.label}
                      </span>
                      <Link
                        to={`/problems/${sub.problem_slug}`}
                        className="font-semibold text-white hover:text-indigo-400 truncate block"
                      >
                        {sub.problem_title}
                      </Link>
                    </div>
                    <div className="flex items-center gap-2 text-[11px] text-slate-500 font-mono">
                      <span>{sub.passed_cases}/{sub.total_cases} test cases</span>
                      {sub.execution_time != null && <span>• {sub.execution_time}s</span>}
                      {sub.memory_usage != null && <span>• {sub.memory_usage} KB</span>}
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <span className={`px-2.5 py-0.5 rounded-md font-mono text-[10px] font-bold uppercase border ${getVerdictBadge(sub.status)}`}>
                      {sub.status}
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono hidden sm:inline">
                      {new Date(sub.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
