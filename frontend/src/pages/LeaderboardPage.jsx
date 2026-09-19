import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router';
import { leaderboardService } from '../services/api/leaderboardService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function LeaderboardPage() {
  const { user } = useAuth();
  const [leaderboard, setLeaderboard] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [currentUserRank, setCurrentUserRank] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('xp'); // 'xp' | 'solved'
  const [searchQuery, setSearchQuery] = useState('');

  const fetchLeaderboard = useCallback(async () => {
    setLoading(true);
    try {
      const data = await leaderboardService.getLeaderboard({ sort: sortBy, limit: 50 });
      setLeaderboard(data?.results || []);
      setTotalCount(data?.total_count || 0);
      setCurrentUserRank(data?.current_user_rank);
    } catch (err) {
      console.error('Failed to load leaderboard:', err);
    } finally {
      setLoading(false);
    }
  }, [sortBy]);

  useEffect(() => {
    fetchLeaderboard();
  }, [fetchLeaderboard]);

  const filteredResults = leaderboard.filter((entry) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      entry.username.toLowerCase().includes(q) ||
      entry.display_name.toLowerCase().includes(q)
    );
  });

  const topThree = leaderboard.slice(0, 3);

  const getRankBadgeClass = (rank) => {
    if (rank === 1) return 'bg-amber-500/20 text-amber-300 border-amber-500/40 ring-2 ring-amber-500/20';
    if (rank === 2) return 'bg-slate-300/20 text-slate-200 border-slate-400/40';
    if (rank === 3) return 'bg-amber-700/20 text-amber-500 border-amber-700/40';
    return 'bg-slate-900 text-slate-400 border-slate-800';
  };

  return (
    <div className="space-y-8 w-full min-w-0">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <span>🏆</span> Global Leaderboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Top competitive programmers ranked by verified telemetry and problem mastery.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-slate-300 w-fit">
          <span className="text-cyan-400 font-bold">{totalCount}</span> Active Competitors
        </div>
      </div>

      {/* Authenticated User Standing Banner */}
      {user && currentUserRank && (
        <div className="bg-gradient-to-r from-indigo-950/60 via-slate-900 to-indigo-950/40 border border-indigo-500/30 rounded-2xl p-4 sm:p-5 flex items-center justify-between shadow-lg">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-lg font-black text-indigo-300">
              #{currentUserRank}
            </div>
            <div>
              <div className="text-sm font-bold text-white flex items-center gap-2">
                <span>Your Global Standing</span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-indigo-600/30 text-indigo-300 border border-indigo-500/30">
                  Current Rank
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Keep solving calibrated problems to climb the ranks and earn new badges.
              </p>
            </div>
          </div>

          <Link
            to="/dashboard"
            className="hidden sm:inline-block px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition"
          >
            My Stats
          </Link>
        </div>
      )}

      {/* Top 3 Podium (Only shown if at least 3 users exist) */}
      {!loading && topThree.length >= 3 && !searchQuery && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          {/* 2nd Place */}
          <div className="order-2 md:order-1 bg-[var(--color-surface-card)] border border-slate-400/20 rounded-2xl p-5 text-center flex flex-col justify-between relative overflow-hidden shadow-md">
            <div className="w-12 h-12 mx-auto rounded-full bg-slate-800 border-2 border-slate-400/40 flex items-center justify-center text-xl mb-3">
              🥈
            </div>
            <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-widest">2nd Place</div>
            <h3 className="text-base font-bold text-white mt-1">{topThree[1].display_name}</h3>
            <p className="text-xs text-slate-400 font-mono">@{topThree[1].username}</p>
            <div className="mt-4 pt-3 border-t border-slate-800 flex justify-center gap-4 text-xs font-mono">
              <div>
                <span className="text-cyan-400 font-bold">{topThree[1].total_xp}</span>
                <span className="text-slate-500 text-[10px] block">XP</span>
              </div>
              <div>
                <span className="text-emerald-400 font-bold">{topThree[1].problems_solved_count}</span>
                <span className="text-slate-500 text-[10px] block">SOLVED</span>
              </div>
            </div>
          </div>

          {/* 1st Place (Center, Elevated) */}
          <div className="order-1 md:order-2 bg-gradient-to-b from-amber-950/40 via-slate-900 to-slate-950 border border-amber-500/40 rounded-2xl p-6 text-center flex flex-col justify-between relative overflow-hidden shadow-xl ring-1 ring-amber-500/20 md:-translate-y-2">
            <div className="w-14 h-14 mx-auto rounded-full bg-amber-500/20 border-2 border-amber-400 flex items-center justify-center text-2xl mb-3 shadow-lg shadow-amber-500/10">
              🥇
            </div>
            <div className="text-xs font-mono font-black text-amber-400 uppercase tracking-widest">Grand Champion</div>
            <h3 className="text-lg font-black text-white mt-1">{topThree[0].display_name}</h3>
            <p className="text-xs text-slate-400 font-mono">@{topThree[0].username}</p>
            <div className="mt-4 pt-3 border-t border-amber-500/20 flex justify-center gap-6 text-xs font-mono">
              <div>
                <span className="text-cyan-300 font-black text-sm">{topThree[0].total_xp.toLocaleString()}</span>
                <span className="text-slate-400 text-[10px] block">TOTAL XP</span>
              </div>
              <div>
                <span className="text-emerald-300 font-black text-sm">{topThree[0].problems_solved_count}</span>
                <span className="text-slate-400 text-[10px] block">PROBLEMS</span>
              </div>
            </div>
          </div>

          {/* 3rd Place */}
          <div className="order-3 md:order-3 bg-[var(--color-surface-card)] border border-amber-800/20 rounded-2xl p-5 text-center flex flex-col justify-between relative overflow-hidden shadow-md">
            <div className="w-12 h-12 mx-auto rounded-full bg-slate-800 border-2 border-amber-700/40 flex items-center justify-center text-xl mb-3">
              🥉
            </div>
            <div className="text-xs font-mono font-bold text-amber-600 uppercase tracking-widest">3rd Place</div>
            <h3 className="text-base font-bold text-white mt-1">{topThree[2].display_name}</h3>
            <p className="text-xs text-slate-400 font-mono">@{topThree[2].username}</p>
            <div className="mt-4 pt-3 border-t border-slate-800 flex justify-center gap-4 text-xs font-mono">
              <div>
                <span className="text-cyan-400 font-bold">{topThree[2].total_xp}</span>
                <span className="text-slate-500 text-[10px] block">XP</span>
              </div>
              <div>
                <span className="text-emerald-400 font-bold">{topThree[2].problems_solved_count}</span>
                <span className="text-slate-500 text-[10px] block">SOLVED</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filter and Search Toolbar */}
      <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
        {/* Sort Tabs */}
        <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs font-semibold self-start sm:self-auto">
          <button
            onClick={() => setSortBy('xp')}
            className={`px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 ${sortBy === 'xp' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
          >
            <span>⚡</span> Ranked by XP
          </button>
          <button
            onClick={() => setSortBy('solved')}
            className={`px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 ${sortBy === 'solved' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
          >
            <span>💡</span> Ranked by Solved
          </button>
        </div>

        {/* Search Bar */}
        <div className="relative w-full sm:w-72">
          <svg className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search competitor..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 outline-none focus:border-indigo-500 transition"
          />
        </div>
      </div>

      {/* Rankings Table */}
      <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl overflow-hidden shadow-sm">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-3">
            <Spinner />
            <p className="text-xs font-mono text-slate-400">Loading standings...</p>
          </div>
        ) : filteredResults.length === 0 ? (
          <div className="text-center py-16 text-slate-400 text-xs">
            No competitors match your query.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/90 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-4 w-16">Rank</th>
                  <th className="py-3.5 px-4">Developer</th>
                  <th className="py-3.5 px-4">Tier</th>
                  <th className="py-3.5 px-4 text-right">Verified XP</th>
                  <th className="py-3.5 px-4 text-right">Solved</th>
                  <th className="py-3.5 px-4 text-right hidden sm:table-cell">Streak</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                {filteredResults.map((entry) => (
                  <tr
                    key={entry.user_id}
                    className={`transition-colors hover:bg-slate-800/40 ${entry.is_current_user ? 'bg-indigo-950/30' : ''
                      }`}
                  >
                    <td className="py-3.5 px-4">
                      <span className={`inline-flex items-center justify-center w-7 h-7 rounded-lg font-mono font-bold text-xs border ${getRankBadgeClass(entry.rank)}`}>
                        {entry.rank}
                      </span>
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white text-xs font-bold ring-2 ring-indigo-400/20 shrink-0">
                          {entry.avatar_initial}
                        </div>
                        <div className="min-w-0">
                          <div className="font-bold text-white flex items-center gap-2 truncate">
                            <span>{entry.display_name}</span>
                            {entry.is_current_user && (
                              <span className="text-[10px] font-mono font-bold px-1.5 py-0.2 rounded bg-indigo-600 text-white">
                                YOU
                              </span>
                            )}
                          </div>
                          <div className="text-[11px] text-slate-400 font-mono">@{entry.username}</div>
                        </div>
                      </div>
                    </td>

                    <td className="py-3.5 px-4">
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-slate-800 border border-slate-700 text-slate-300">
                        Lvl {entry.level} • {entry.level_title}
                      </span>
                    </td>

                    <td className="py-3.5 px-4 text-right font-mono font-bold text-cyan-400 text-sm">
                      {entry.total_xp.toLocaleString()}
                    </td>

                    <td className="py-3.5 px-4 text-right font-mono text-emerald-400">
                      {entry.problems_solved_count}
                    </td>

                    <td className="py-3.5 px-4 text-right font-mono text-amber-400 hidden sm:table-cell">
                      {entry.current_streak_days > 0 ? `🔥 ${entry.current_streak_days}d` : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

