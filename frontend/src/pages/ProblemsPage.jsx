import { useState, useEffect, useCallback } from 'react';
import { Link, useSearchParams } from 'react-router';
import { problemService } from '../services/api/problemService';
import { progressService } from '../services/api/progressService';
import { useAuth } from '../context/AuthContext';
import { getLanguageInfo } from '../utils/languageUtils';

export default function ProblemsPage() {
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const [problems, setProblems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [solvedIds, setSolvedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);

  // Pagination
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  // Filter States (initialize category from URL param if present)
  const initialCategory = searchParams.get('track') || searchParams.get('category') || '';
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(initialCategory);
  const [selectedLevel, setSelectedLevel] = useState('');

  // Synchronize category state when URL search param changes
  useEffect(() => {
    const urlTrack = searchParams.get('track') || searchParams.get('category') || '';
    if (urlTrack !== selectedCategory) {
      setSelectedCategory(urlTrack);
      setPage(1);
    }
  }, [searchParams]);

  const handleTrackSelect = (trackSlug) => {
    setSelectedCategory(trackSlug);
    setPage(1);
    const newParams = new URLSearchParams(searchParams);
    if (trackSlug) {
      newParams.set('track', trackSlug);
      newParams.delete('category');
    } else {
      newParams.delete('track');
      newParams.delete('category');
    }
    setSearchParams(newParams);
  };

  const fetchCategories = async () => {
    try {
      const res = await problemService.getCategories();
      setCategories(res || []);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const fetchProblems = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page,
        page_size: pageSize,
      };
      if (searchTerm.trim()) params.search = searchTerm.trim();
      if (selectedDifficulty) params.difficulty = selectedDifficulty;
      if (selectedCategory) params.category = selectedCategory;
      if (selectedLevel) params.level = selectedLevel;

      const res = await problemService.getProblems(params);
      setProblems(res?.results || []);
      setTotalCount(res?.count || 0);
    } catch (err) {
      console.error('Failed to fetch problems:', err);
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, searchTerm, selectedDifficulty, selectedCategory, selectedLevel]);

  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    const fetchSolved = async () => {
      if (!user) {
        setSolvedIds([]);
        return;
      }
      try {
        const res = await progressService.getSolvedProblemIds();
        setSolvedIds(res?.solved_problem_ids || []);
      } catch (err) {
        console.error('Failed to fetch solved problems:', err);
      }
    };
    fetchSolved();
  }, [user]);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchProblems();
    }, 150);
    return () => clearTimeout(timer);
  }, [fetchProblems]);

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



  const totalPages = Math.ceil(totalCount / pageSize) || 1;

  return (
    <div className="space-y-8 w-full min-w-0">
      {/* Catalog Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight flex items-center gap-3">
            <span>💻</span> Coding Challenges
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Master 100 progressive algorithms across Python, JavaScript, and C++ with zero duplicate problems.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-semibold px-3.5 py-1.5 rounded-full bg-slate-800/80 border border-slate-700 text-slate-300">
            <span className="text-cyan-400 font-bold font-mono">{totalCount}</span> Challenges Available
          </div>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-5 space-y-4 shadow-lg w-full min-w-0">
        {/* Track Filter Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800">
          <span className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider pr-1 shrink-0">
            Language Track:
          </span>
          <button
            onClick={() => handleTrackSelect('')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition shrink-0 ${selectedCategory === ''
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-white bg-slate-900 border border-slate-800'
              }`}
          >
            All Tracks (300)
          </button>
          <button
            onClick={() => handleTrackSelect('python')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition shrink-0 flex items-center gap-1.5 ${selectedCategory === 'python'
              ? 'bg-emerald-600 text-white shadow-sm'
              : 'text-slate-300 hover:text-white bg-slate-900 border border-slate-800'
              }`}
          >
            <span>🐍</span> Python Track (100)
          </button>
          <button
            onClick={() => handleTrackSelect('javascript')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition shrink-0 flex items-center gap-1.5 ${selectedCategory === 'javascript'
              ? 'bg-amber-600 text-white shadow-sm'
              : 'text-slate-300 hover:text-white bg-slate-900 border border-slate-800'
              }`}
          >
            <span>🟨</span> JavaScript Track (100)
          </button>
          <button
            onClick={() => handleTrackSelect('cpp')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition shrink-0 flex items-center gap-1.5 ${selectedCategory === 'cpp'
              ? 'bg-cyan-600 text-white shadow-sm'
              : 'text-slate-300 hover:text-white bg-slate-900 border border-slate-800'
              }`}
          >
            <span>⚡</span> C++ Track (100)
          </button>
        </div>

        {/* Search Bar */}
        <div className="relative w-full">
          <svg className="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search problems by title, algorithm, data structure, or tags..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setPage(1);
            }}
            className="w-full pl-11 pr-4 py-2.5 rounded-xl bg-[var(--color-surface-dark)] border border-slate-700 text-white placeholder-slate-500 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition"
          />
        </div>

        {/* Filter Controls Row */}
        <div className="flex flex-wrap items-center gap-3 pt-2 text-xs w-full">
          {/* Difficulty Dropdown */}
          <select
            value={selectedDifficulty}
            onChange={(e) => {
              setSelectedDifficulty(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 rounded-xl bg-[var(--color-surface-dark)] border border-slate-700 text-slate-200 outline-none focus:border-indigo-500 font-medium"
          >
            <option value="">All Difficulties</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          {/* Level Filter Tabs */}
          <div className="flex items-center gap-1 bg-[var(--color-surface-dark)] p-1 rounded-xl border border-slate-800 max-w-full overflow-x-auto">
            <button
              onClick={() => {
                setSelectedLevel('');
                setPage(1);
              }}
              className={`px-3 py-1 rounded-lg font-medium transition ${selectedLevel === '' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
                }`}
            >
              All Tiers
            </button>
            {[1, 2, 3, 4, 5].map((lvl) => (
              <button
                key={lvl}
                onClick={() => {
                  setSelectedLevel(selectedLevel === String(lvl) ? '' : String(lvl));
                  setPage(1);
                }}
                className={`px-2.5 py-1 rounded-lg font-medium transition ${selectedLevel === String(lvl)
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
                  }`}
              >
                Level {lvl}
              </button>
            ))}
          </div>

          {/* Page Size Selector */}
          <div className="flex items-center gap-1 ml-auto text-slate-400">
            <span>Per page:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setPage(1);
              }}
              className="px-2 py-1 rounded-lg bg-[var(--color-surface-dark)] border border-slate-800 text-slate-300 outline-none focus:border-indigo-500"
            >
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>

          {/* Reset Filters */}
          {(searchTerm || selectedDifficulty || selectedCategory || selectedLevel) && (
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedDifficulty('');
                setSelectedLevel('');
                handleTrackSelect('');
              }}
              className="text-slate-400 hover:text-red-400 underline font-medium"
            >
              Reset All Filters
            </button>
          )}
        </div>
      </div>

      {/* Problems List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((n) => (
            <div key={n} className="h-20 rounded-xl bg-slate-800/40 animate-pulse" />
          ))}
        </div>
      ) : problems.length === 0 ? (
        <div className="text-center py-16 bg-[var(--color-surface-card)] border border-slate-800 rounded-2xl p-8">
          <div className="text-4xl mb-3">🔍</div>
          <h3 className="text-lg font-bold text-white">No challenges match your filters</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Try adjusting your search terms or resetting the difficulty and tier filters.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {problems.map((problem) => {
            const isSolved = solvedIds.includes(problem.id);
            return (
              <div
                key={problem.id}
                className={`group bg-[var(--color-surface-card)] border ${isSolved
                  ? 'border-emerald-800/40 hover:border-emerald-600/60'
                  : 'border-[var(--color-surface-hover)] hover:border-indigo-500/50'
                  } rounded-2xl p-5 transition-all shadow-sm hover:shadow-md flex flex-col sm:flex-row sm:items-center justify-between gap-4`}
              >
                <div className="space-y-2">
                  <div className="flex flex-wrap items-center gap-2">
                    {(() => {
                      const langInfo = getLanguageInfo(problem.language || selectedCategory, problem);
                      return (
                        <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${langInfo.badgeClass} flex items-center gap-1`}>
                          <span>{langInfo.icon}</span> {langInfo.label}
                        </span>
                      );
                    })()}
                    <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase border ${getDifficultyBadge(problem.difficulty)}`}>
                      {problem.difficulty}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-slate-800 border border-slate-700 text-slate-300">
                      Tier {problem.challenge_level}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold text-amber-400 bg-amber-950/40 border border-amber-800/40">
                      +{problem.xp_reward} XP
                    </span>
                    {isSolved && (
                      <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-950/80 border border-emerald-600/60 text-emerald-300 flex items-center gap-1 shadow-sm">
                        <span>✓</span> Solved
                      </span>
                    )}
                    <span className="text-xs text-slate-400 font-medium">
                      in <strong className="text-slate-300">{problem.category?.name}</strong>
                    </span>
                  </div>

                  <Link
                    to={`/problems/${problem.slug}`}
                    className="block text-lg font-bold text-white group-hover:text-indigo-400 transition-colors"
                  >
                    {problem.title}
                  </Link>

                  {problem.tags?.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {problem.tags.map((t) => (
                        <span
                          key={t.id}
                          className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-[10px] font-mono text-slate-400"
                        >
                          #{t.name}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <Link
                    to={`/problems/${problem.slug}`}
                    className={`px-4 py-2 rounded-xl font-semibold text-xs transition flex items-center gap-2 shadow-sm ${isSolved
                      ? 'bg-emerald-950/60 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/60'
                      : 'bg-slate-800 hover:bg-indigo-600 text-white'
                      }`}
                  >
                    <span>{isSolved ? 'Review / Practice' : 'Solve'}</span>
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Pagination Controls */}
      {totalCount > 0 && (
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
          <div>
            Showing <strong className="text-white">{(page - 1) * pageSize + 1}</strong> to{' '}
            <strong className="text-white">{Math.min(page * pageSize, totalCount)}</strong> of{' '}
            <strong className="text-white">{totalCount}</strong> challenges
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
              disabled={page <= 1}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              ← Previous
            </button>

            <span className="px-3 py-1.5 font-mono text-slate-300">
              Page {page} of {totalPages}
            </span>

            <button
              onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
              disabled={page >= totalPages}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed transition"
            >
              Next →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
