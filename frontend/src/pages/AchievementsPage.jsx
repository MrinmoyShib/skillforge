import { useState, useEffect, useMemo } from 'react';
import { achievementService } from '../services/api/achievementService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';
import { formatDate } from '../utils/formatters';

export default function AchievementsPage() {
  const { user } = useAuth();
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all' | 'unlocked' | 'locked'
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function loadAchievements() {
      setLoading(true);
      try {
        const data = await achievementService.getAchievements();
        setAchievements(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error('Failed to load achievements:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAchievements();
  }, []);

  // Summary Metrics
  const metrics = useMemo(() => {
    const total = achievements.length;
    const unlocked = achievements.filter((a) => a.is_unlocked).length;
    const locked = total - unlocked;
    const totalXPEarned = achievements
      .filter((a) => a.is_unlocked)
      .reduce((sum, a) => sum + (a.xp_bonus || 0), 0);
    const totalXPAvailable = achievements.reduce(
      (sum, a) => sum + (a.xp_bonus || 0),
      0
    );
    const percentComplete = total > 0 ? Math.round((unlocked / total) * 100) : 0;

    return { total, unlocked, locked, totalXPEarned, totalXPAvailable, percentComplete };
  }, [achievements]);

  // Filtered List
  const filteredAchievements = useMemo(() => {
    return achievements.filter((item) => {
      // Status filter
      if (filter === 'unlocked' && !item.is_unlocked) return false;
      if (filter === 'locked' && item.is_unlocked) return false;

      // Search filter
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesName = item.name.toLowerCase().includes(q);
        const matchesDesc = item.description.toLowerCase().includes(q);
        return matchesName || matchesDesc;
      }
      return true;
    });
  }, [achievements, filter, searchQuery]);

  return (
    <div className="space-y-8 w-full min-w-0">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <span>🎖️</span> Platform Achievements
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Earn verified developer badges, bonus XP, and career-advancement credentials.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-slate-300 w-fit">
          <span className="text-amber-400 font-bold">{metrics.unlocked}</span> of{' '}
          <span className="text-slate-400 font-bold">{metrics.total}</span> Badges Unlocked
        </div>
      </div>

      {/* Progress Telemetry Card */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-5 sm:p-6 shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 flex-1">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
                Mastery Completion
              </span>
              <span className="text-sm font-black font-mono text-cyan-400">
                {metrics.percentComplete}%
              </span>
            </div>
            {/* Progress bar */}
            <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-slate-700/50">
              <div
                className="bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400 h-full rounded-full transition-all duration-500 shadow-sm"
                style={{ width: `${metrics.percentComplete}%` }}
              />
            </div>
          </div>

          <div className="flex items-center gap-6 border-t md:border-t-0 md:border-l border-slate-800 pt-4 md:pt-0 md:pl-8">
            <div>
              <div className="text-xl sm:text-2xl font-black text-amber-400 font-mono">
                +{metrics.totalXPEarned}
              </div>
              <div className="text-[11px] uppercase tracking-wider text-slate-400 font-mono">
                XP Claimed
              </div>
            </div>
            <div>
              <div className="text-xl sm:text-2xl font-black text-slate-200 font-mono">
                {metrics.totalXPAvailable}
              </div>
              <div className="text-[11px] uppercase tracking-wider text-slate-400 font-mono">
                Total Available XP
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filter and Search Controls */}
      <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
        {/* Tabs */}
        <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs font-semibold self-start sm:self-auto">
          <button
            onClick={() => setFilter('all')}
            className={`px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 ${filter === 'all'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
              }`}
          >
            <span>All</span>
            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono">
              {metrics.total}
            </span>
          </button>
          <button
            onClick={() => setFilter('unlocked')}
            className={`px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 ${filter === 'unlocked'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
              }`}
          >
            <span>Unlocked</span>
            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono">
              {metrics.unlocked}
            </span>
          </button>
          <button
            onClick={() => setFilter('locked')}
            className={`px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 ${filter === 'locked'
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-white'
              }`}
          >
            <span>Locked</span>
            <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono">
              {metrics.locked}
            </span>
          </button>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <svg
            className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          <input
            type="text"
            placeholder="Search badges..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 outline-none focus:border-indigo-500 transition"
          />
        </div>
      </div>

      {/* Badges Grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 space-y-3">
          <Spinner />
          <p className="text-xs font-mono text-slate-400">Loading achievements...</p>
        </div>
      ) : filteredAchievements.length === 0 ? (
        <div className="text-center py-16 text-slate-400 text-xs bg-[var(--color-surface-card)] border border-slate-800 rounded-2xl">
          No achievements match your selected filter.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredAchievements.map((badge) => {
            const isUnlocked = badge.is_unlocked;
            return (
              <div
                key={badge.id}
                className={`relative rounded-2xl p-5 flex flex-col justify-between transition-all duration-300 ${isUnlocked
                    ? 'bg-gradient-to-b from-slate-900 via-slate-900/90 to-slate-950 border border-amber-500/40 shadow-lg shadow-amber-500/5 hover:border-amber-400 hover:scale-[1.01]'
                    : 'bg-slate-900/60 border border-slate-800 hover:border-slate-700 opacity-80'
                  }`}
              >
                <div>
                  {/* Card Header: Icon & XP Badge */}
                  <div className="flex items-start justify-between gap-3 mb-4">
                    <div
                      className={`w-14 h-14 rounded-2xl flex items-center justify-center text-3xl shrink-0 transition-transform ${isUnlocked
                          ? 'bg-gradient-to-tr from-amber-500/20 to-indigo-500/20 border border-amber-500/40 shadow-md ring-2 ring-amber-500/20'
                          : 'bg-slate-800 border border-slate-700 text-slate-500 grayscale'
                        }`}
                    >
                      {badge.icon || '🏆'}
                    </div>

                    <div className="flex flex-col items-end gap-1.5">
                      <span
                        className={`text-xs font-mono font-bold px-2.5 py-1 rounded-lg border ${isUnlocked
                            ? 'bg-amber-500/10 text-amber-300 border-amber-500/30'
                            : 'bg-slate-800 text-slate-400 border-slate-700'
                          }`}
                      >
                        +{badge.xp_bonus} XP
                      </span>
                      {isUnlocked ? (
                        <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-400">
                          <span>✓</span> Unlocked
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-[11px] font-mono text-slate-500">
                          <span>🔒</span> Locked
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Title & Description */}
                  <h3 className="text-base font-bold text-white tracking-tight">
                    {badge.name}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
                    {badge.description}
                  </p>
                </div>

                {/* Card Footer: Progress or Unlock Date */}
                <div className="mt-5 pt-4 border-t border-slate-800/80">
                  {isUnlocked ? (
                    <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                      <span>Unlocked On</span>
                      <span className="text-slate-200 font-semibold">
                        {badge.earned_at ? formatDate(badge.earned_at) : 'Active'}
                      </span>
                    </div>
                  ) : (
                    <div className="space-y-1.5">
                      <div className="flex items-center justify-between text-[11px] font-mono">
                        <span className="text-slate-400">Progress</span>
                        <span className="text-cyan-400 font-bold">
                          {badge.current_progress} / {badge.criteria_value} (
                          {Math.round(badge.progress_percent)}%)
                        </span>
                      </div>
                      <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                        <div
                          className="bg-cyan-500 h-full rounded-full transition-all duration-300"
                          style={{ width: `${Math.min(badge.progress_percent, 100)}%` }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

