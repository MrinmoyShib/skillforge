import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router';
import { portfolioService } from '../services/api/portfolioService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';
import { formatDate } from '../utils/formatters';
import { sanitizeUrl } from '../utils/urlSanitizer';

export default function PortfolioPage() {
  const { username } = useParams();
  const { user: currentUser } = useAuth();

  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [shareModalOpen, setShareModalOpen] = useState(false);

  useEffect(() => {
    async function loadPortfolio() {
      setLoading(true);
      try {
        const data = await portfolioService.getPortfolio(username);
        setPortfolio(data);
      } catch (err) {
        console.error('Failed to load portfolio:', err);
        setError('Developer profile not found or could not be loaded.');
      } finally {
        setLoading(false);
      }
    }
    loadPortfolio();
  }, [username]);

  const shareUrl = typeof window !== 'undefined' ? window.location.href : '';

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const getBadgeColor = (badgeType) => {
    switch (badgeType) {
      case 'gold':
        return 'border-amber-400/50 bg-amber-500/10 text-amber-300';
      case 'silver':
        return 'border-slate-300/50 bg-slate-400/10 text-slate-200';
      case 'bronze':
        return 'border-amber-700/50 bg-amber-800/10 text-amber-500';
      default:
        return 'border-indigo-500/50 bg-indigo-500/10 text-indigo-300';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-36">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !portfolio) {
    return (
      <div className="max-w-xl mx-auto py-24 text-center space-y-4">
        <span className="text-4xl">👨‍💻</span>
        <h2 className="text-xl font-bold text-white">Developer Not Found</h2>
        <p className="text-sm text-slate-400">{error || 'No developer exists with this username.'}</p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold"
        >
          Return Home
        </Link>
      </div>
    );
  }

  const { user, achievements, recent_activity } = portfolio;
  const isOwner = currentUser && currentUser.username === user.username;

  return (
    <div className="w-full min-w-0 max-w-5xl mx-auto space-y-10 pb-24">
      {/* 1. Developer Hero Card */}
      <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl">
        {/* Background glow */}
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-5">
            {/* Avatar */}
            {user.avatar_url ? (
              <img
                src={user.avatar_url}
                alt={user.display_name || user.username}
                className="w-20 h-20 rounded-2xl object-cover border-2 border-indigo-500/40 shadow-lg shadow-indigo-500/30 flex-shrink-0"
              />
            ) : (
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center text-3xl font-black text-white shadow-lg shadow-indigo-500/30 flex-shrink-0">
                {user.display_name ? user.display_name.charAt(0).toUpperCase() : user.username.charAt(0).toUpperCase()}
              </div>
            )}

            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2.5">
                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                  {user.display_name || user.username}
                </h1>
                <span className="text-xs font-mono text-slate-400 font-medium">
                  @{user.username}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  Level {user.current_level} • {user.level_title}
                </span>
              </div>

              <p className="text-slate-300 text-sm max-w-xl leading-relaxed">
                {user.bio || 'Competitive programmer & full-stack software engineer.'}
              </p>

              {/* Social & Contact Pills */}
              <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 pt-1 font-mono">
                <span>📅 Joined {formatDate(user.joined_at)}</span>

                {user.phone_number && (
                  <span className="flex items-center gap-1 text-slate-300">
                    <span>📞</span> {user.phone_number}
                  </span>
                )}

                {user.github_url && sanitizeUrl(user.github_url) && (
                  <a
                    href={sanitizeUrl(user.github_url)}
                    target="_blank"
                    rel="noreferrer"
                    className="text-indigo-400 hover:text-indigo-300 transition-colors flex items-center gap-1 bg-slate-950/60 px-2 py-0.5 rounded border border-slate-800"
                  >
                    <span>🔗</span> GitHub
                  </a>
                )}

                {user.linkedin_url && sanitizeUrl(user.linkedin_url) && (
                  <a
                    href={sanitizeUrl(user.linkedin_url)}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:text-cyan-300 transition-colors flex items-center gap-1 bg-slate-950/60 px-2 py-0.5 rounded border border-slate-800"
                  >
                    <span>🔗</span> LinkedIn
                  </a>
                )}

                {user.twitter_url && sanitizeUrl(user.twitter_url) && (
                  <a
                    href={sanitizeUrl(user.twitter_url)}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sky-400 hover:text-sky-300 transition-colors flex items-center gap-1 bg-slate-950/60 px-2 py-0.5 rounded border border-slate-800"
                  >
                    <span>🐦</span> X
                  </a>
                )}

                {user.website_url && sanitizeUrl(user.website_url) && (
                  <a
                    href={sanitizeUrl(user.website_url)}
                    target="_blank"
                    rel="noreferrer"
                    className="text-emerald-400 hover:text-emerald-300 transition-colors flex items-center gap-1 bg-slate-950/60 px-2 py-0.5 rounded border border-slate-800"
                  >
                    <span>🌐</span> Portfolio
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Action CTAs: Share + Edit Profile (if owner) */}
          <div className="self-start md:self-auto flex flex-wrap items-center gap-3">
            {isOwner && (
              <Link
                to="/settings"
                className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition-all flex items-center gap-2"
              >
                <span>⚙️</span>
                <span>Edit Profile & Settings</span>
              </Link>
            )}

            <button
              onClick={() => setShareModalOpen(true)}
              className="px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-white text-xs font-semibold border border-slate-700/60 shadow-sm transition-all flex items-center gap-2"
            >
              <span>🔗</span>
              <span>Share Profile</span>
            </button>
          </div>
        </div>

        {/* Telemetry Stat Strip */}
        <div className="mt-8 pt-6 border-t border-slate-800/80 grid grid-cols-3 gap-4">
          <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 text-center">
            <span className="text-xs font-mono uppercase text-slate-400 tracking-wider block mb-1">
              Total XP
            </span>
            <span className="text-2xl font-black font-mono text-cyan-400">
              {user.total_xp.toLocaleString()}
            </span>
          </div>

          <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 text-center">
            <span className="text-xs font-mono uppercase text-slate-400 tracking-wider block mb-1">
              Problems Solved
            </span>
            <span className="text-2xl font-black font-mono text-emerald-400">
              {user.problems_solved_count}
            </span>
          </div>

          <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4 text-center">
            <span className="text-xs font-mono uppercase text-slate-400 tracking-wider block mb-1">
              Daily Streak
            </span>
            <span className="text-2xl font-black font-mono text-amber-400 flex items-center justify-center gap-1">
              <span>🔥</span> {user.current_streak_days}d
            </span>
          </div>
        </div>
      </div>

      {/* 2. Platform Achievements & Badges Showcase */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <span>🎖️</span> Earned Credentials & Badges
        </h2>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
          {(!achievements || achievements.length === 0) ? (
            <p className="text-xs text-slate-400 py-6 text-center">No badges unlocked yet.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {achievements.map((ach) => {
                const badgeClass = getBadgeColor(ach.badge_type);
                return (
                  <div
                    key={ach.code}
                    className={`p-3.5 rounded-xl border flex items-start gap-3 ${badgeClass}`}
                  >
                    <span className="text-2xl flex-shrink-0">{ach.icon}</span>
                    <div className="min-w-0">
                      <h4 className="text-xs font-bold text-white truncate">{ach.name}</h4>
                      <p className="text-[11px] text-slate-300 line-clamp-2 mt-0.5">
                        {ach.description}
                      </p>
                      <span className="text-[10px] font-mono text-slate-400 block mt-1">
                        {formatDate(ach.unlocked_at)}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* 3. Proof of Work Activity Feed */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <span>📜</span> Proof of Work Activity Stream
        </h2>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
          {(!recent_activity || recent_activity.length === 0) ? (
            <p className="text-xs text-slate-400 py-4 text-center">No recent activity recorded.</p>
          ) : (
            <div className="space-y-3">
              {recent_activity.map((act) => (
                <div
                  key={act.id}
                  className="flex items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs font-mono"
                >
                  <div className="flex items-center gap-2.5 text-slate-300">
                    <span className="text-emerald-400">●</span>
                    <span>{act.description}</span>
                  </div>
                  <span className="text-slate-500 text-[11px]">
                    {formatDate(act.created_at)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Share Profile Modal */}
      {shareModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-7 max-w-md w-full space-y-5 shadow-2xl relative animate-in fade-in zoom-in duration-200">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <span>🚀</span> Share Developer Profile
              </h3>
              <button
                onClick={() => setShareModalOpen(false)}
                className="text-slate-400 hover:text-white text-sm"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Share {user.display_name || user.username}&apos;s verified developer credentials and portfolio across platforms:
            </p>

            {/* Social Share Grid */}
            <div className="grid grid-cols-2 gap-3">
              {/* WhatsApp */}
              <a
                href={`https://api.whatsapp.com/send?text=${encodeURIComponent(`Check out ${user.display_name || user.username}'s developer portfolio on SkillForge: ${shareUrl}`)}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2.5 p-3 rounded-xl bg-emerald-950/40 hover:bg-emerald-900/50 border border-emerald-500/40 text-emerald-300 text-xs font-semibold transition"
              >
                <span className="text-base">💬</span>
                <span>WhatsApp</span>
              </a>

              {/* LinkedIn */}
              <a
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2.5 p-3 rounded-xl bg-sky-950/40 hover:bg-sky-900/50 border border-sky-500/40 text-sky-300 text-xs font-semibold transition"
              >
                <span className="text-base">💼</span>
                <span>LinkedIn</span>
              </a>

              {/* Twitter / X */}
              <a
                href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(`Check out ${user.display_name || user.username}'s developer profile on SkillForge!`)}&url=${encodeURIComponent(shareUrl)}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2.5 p-3 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold transition"
              >
                <span className="text-base">🐦</span>
                <span>Twitter / X</span>
              </a>

              {/* Gmail / Email */}
              <a
                href={`mailto:?subject=${encodeURIComponent(`SkillForge Developer Portfolio - ${user.display_name || user.username}`)}&body=${encodeURIComponent(`Check out ${user.display_name || user.username}'s verified portfolio on SkillForge:\n${shareUrl}`)}`}
                className="flex items-center gap-2.5 p-3 rounded-xl bg-rose-950/40 hover:bg-rose-900/50 border border-rose-500/40 text-rose-300 text-xs font-semibold transition"
              >
                <span className="text-base">✉️</span>
                <span>Email / Gmail</span>
              </a>
            </div>

            {/* Direct Copy Link Field */}
            <div className="pt-2">
              <div className="flex items-center gap-2 bg-slate-950 p-2 rounded-xl border border-slate-800">
                <input
                  type="text"
                  readOnly
                  value={shareUrl}
                  className="bg-transparent text-xs text-slate-300 flex-1 outline-none px-2 font-mono truncate"
                />
                <button
                  onClick={handleCopyLink}
                  className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition flex items-center gap-1.5 flex-shrink-0"
                >
                  <span>{copied ? '✓' : '📋'}</span>
                  <span>{copied ? 'Copied!' : 'Copy'}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
