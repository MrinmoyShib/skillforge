import { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router';
import { projectService } from '../services/api/projectService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function ProjectsPage() {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function loadProjects() {
      setLoading(true);
      try {
        const data = await projectService.getProjects();
        const projectList = Array.isArray(data) ? data : (data?.results || []);
        setProjects(projectList);
      } catch (err) {
        console.error('Failed to load projects:', err);
      } finally {
        setLoading(false);
      }
    }
    loadProjects();
  }, []);

  // Filter logic
  const filteredProjects = useMemo(() => {
    return projects.filter((p) => {
      // Language filter
      if (selectedLanguage !== 'all' && p.language !== selectedLanguage) return false;

      // Difficulty filter
      if (selectedDifficulty !== 'all' && p.difficulty !== selectedDifficulty) return false;

      // Status filter
      if (selectedStatus !== 'all' && p.user_status !== selectedStatus) return false;

      // Search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesTitle = p.title.toLowerCase().includes(q);
        const matchesDesc = (p.short_description || '').toLowerCase().includes(q);
        const matchesTech = (p.technologies || []).some((t) => t.toLowerCase().includes(q));
        return matchesTitle || matchesDesc || matchesTech;
      }

      return true;
    });
  }, [projects, selectedLanguage, selectedDifficulty, selectedStatus, searchQuery]);

  // Telemetry stats
  const stats = useMemo(() => {
    const total = projects.length;
    const completed = projects.filter((p) => p.user_status === 'COMPLETED').length;
    const inProgress = projects.filter((p) => p.user_status === 'IN_PROGRESS').length;
    const totalXP = projects.reduce((acc, p) => acc + (p.xp_reward || 0), 0);
    const earnedXP = projects
      .filter((p) => p.user_status === 'COMPLETED')
      .reduce((acc, p) => acc + (p.xp_reward || 0), 0);

    return { total, completed, inProgress, totalXP, earnedXP };
  }, [projects]);

  const getLanguageBadge = (lang) => {
    switch (lang) {
      case 'python':
        return { label: 'Python', icon: '🐍', color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30' };
      case 'javascript':
        return { label: 'JavaScript', icon: '🟨', color: 'text-amber-400 bg-amber-500/10 border-amber-500/30' };
      case 'cpp':
        return { label: 'C++', icon: '⚡', color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30' };
      default:
        return { label: lang, icon: '💻', color: 'text-slate-400 bg-slate-500/10 border-slate-500/30' };
    }
  };

  const getDifficultyBadge = (diff) => {
    switch (diff) {
      case 'easy':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'medium':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'hard':
        return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
      default:
        return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'COMPLETED':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Verified Complete
          </span>
        );
      case 'IN_PROGRESS':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold font-mono text-amber-400 bg-amber-500/10 border border-amber-500/30">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span> In Progress
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold font-mono text-slate-400 bg-slate-800/80 border border-slate-700/50">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span> Not Started
          </span>
        );
    }
  };

  return (
    <div className="space-y-8 w-full min-w-0 max-w-7xl mx-auto pb-16">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-slate-800 pb-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-mono font-semibold">
            <span>🚀</span> Guided Engineering Labs
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
            Production Software Projects
          </h1>
          <p className="text-slate-400 text-sm max-w-2xl">
            Build real-world systems, compilers, async schedulers, and network daemons across Python, JavaScript, and C++.
            Every milestone is verified inside isolated sandboxes with automated test harnesses.
          </p>
        </div>

        {/* Telemetry Capsule */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 bg-slate-900/90 border border-slate-800 p-4 rounded-2xl">
          <div className="text-center px-3">
            <span className="block text-2xl font-black font-mono text-white">{stats.total}</span>
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Projects</span>
          </div>
          <div className="text-center px-3 border-x border-slate-800">
            <span className="block text-2xl font-black font-mono text-cyan-400">+{stats.totalXP}</span>
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Available XP</span>
          </div>
          <div className="text-center px-3 col-span-2 sm:col-span-1">
            <span className="block text-2xl font-black font-mono text-emerald-400">
              {stats.completed}/{stats.total}
            </span>
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Completed</span>
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800/80 backdrop-blur-sm">
        {/* Search */}
        <div className="relative flex-1">
          <input
            type="text"
            placeholder="Search projects by title, architecture, or technology..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-2.5 pl-10 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
          />
          <span className="absolute left-3.5 top-3 text-slate-500 text-sm">🔍</span>
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3.5 top-2.5 text-slate-500 hover:text-white text-sm"
            >
              ✕
            </button>
          )}
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Language Selector */}
          <div className="flex items-center bg-slate-950/80 border border-slate-800 rounded-xl p-1 text-xs">
            {[
              { id: 'all', label: 'All Tracks' },
              { id: 'python', label: '🐍 Python' },
              { id: 'javascript', label: '🟨 JS' },
              { id: 'cpp', label: '⚡ C++' },
            ].map((lang) => (
              <button
                key={lang.id}
                onClick={() => setSelectedLanguage(lang.id)}
                className={`px-3 py-1.5 rounded-lg font-medium transition-all ${selectedLanguage === lang.id
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
                  }`}
              >
                {lang.label}
              </button>
            ))}
          </div>

          {/* Difficulty Dropdown */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="bg-slate-950/80 border border-slate-800 text-slate-300 text-xs rounded-xl px-3 py-2 focus:outline-none focus:border-indigo-500 font-medium"
          >
            <option value="all">All Difficulties</option>
            <option value="easy">🟢 Easy</option>
            <option value="medium">🟡 Medium</option>
            <option value="hard">🔴 Hard</option>
          </select>

          {/* Status Dropdown (if logged in) */}
          {user && (
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-slate-950/80 border border-slate-800 text-slate-300 text-xs rounded-xl px-3 py-2 focus:outline-none focus:border-indigo-500 font-medium"
            >
              <option value="all">All Progress</option>
              <option value="NOT_STARTED">Not Started</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
            </select>
          )}
        </div>
      </div>

      {/* Projects Grid */}
      {loading ? (
        <div className="flex justify-center items-center py-24">
          <Spinner size="lg" />
        </div>
      ) : filteredProjects.length === 0 ? (
        <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-12 text-center space-y-3">
          <span className="text-4xl">🛠️</span>
          <h3 className="text-lg font-bold text-white">No Guided Projects Found</h3>
          <p className="text-sm text-slate-400 max-w-md mx-auto">
            No projects matched your selected filters. Try clearing your search query or selecting all language tracks.
          </p>
          <button
            onClick={() => {
              setSelectedLanguage('all');
              setSelectedDifficulty('all');
              setSelectedStatus('all');
              setSearchQuery('');
            }}
            className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition-colors mt-2"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => {
            const langBadge = getLanguageBadge(project.language);
            const diffClass = getDifficultyBadge(project.difficulty);

            return (
              <div
                key={project.id}
                className="group flex flex-col justify-between bg-slate-900/80 hover:bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-6 transition-all duration-300 hover:shadow-xl hover:shadow-indigo-950/20 relative overflow-hidden"
              >
                {/* Top Ambient Glow */}
                <div className="absolute -top-12 -right-12 w-28 h-28 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/10 transition-colors pointer-events-none" />

                <div className="space-y-4">
                  {/* Card Header: Language Badge + Difficulty + Status */}
                  <div className="flex items-center justify-between gap-2">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-bold font-mono border ${langBadge.color}`}
                    >
                      <span>{langBadge.icon}</span> {langBadge.label}
                    </span>

                    <span
                      className={`text-[11px] font-mono font-bold uppercase px-2 py-0.5 rounded border ${diffClass}`}
                    >
                      {project.difficulty}
                    </span>
                  </div>

                  {/* Title & Short Description */}
                  <div>
                    <h2 className="text-xl font-bold text-white group-hover:text-indigo-300 transition-colors leading-snug">
                      {project.title}
                    </h2>
                    <p className="text-slate-400 text-xs line-clamp-3 mt-2 leading-relaxed">
                      {project.short_description}
                    </p>
                  </div>

                  {/* Tech Stack Pills */}
                  {project.technologies && project.technologies.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {project.technologies.map((tech) => (
                        <span
                          key={tech}
                          className="px-2 py-0.5 rounded-md text-[11px] font-mono text-slate-300 bg-slate-950/80 border border-slate-800"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Card Footer: Metadata & Action CTA */}
                <div className="mt-6 pt-5 border-t border-slate-800/80 space-y-4">
                  <div className="flex items-center justify-between text-xs font-mono text-slate-400">
                    <span className="flex items-center gap-1">
                      <span>📋</span> {project.milestones_count || 0} Milestones
                    </span>
                    <span className="flex items-center gap-1 text-cyan-400 font-bold">
                      <span>⚡</span> +{project.xp_reward} XP
                    </span>
                    <span className="flex items-center gap-1">
                      <span>⏱️</span> {project.estimated_minutes}m
                    </span>
                  </div>

                  <div className="flex items-center justify-between gap-3 pt-1">
                    <div>{getStatusBadge(project.user_status)}</div>

                    <Link
                      to={`/projects/${project.slug}`}
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all shadow-md shadow-indigo-600/20 hover:translate-x-0.5"
                    >
                      {project.user_status === 'COMPLETED'
                        ? 'Review Lab'
                        : project.user_status === 'IN_PROGRESS'
                          ? 'Continue Lab'
                          : 'Launch Lab'}{' '}
                      ➔
                    </Link>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

