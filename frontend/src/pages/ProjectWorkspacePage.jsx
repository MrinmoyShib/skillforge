import { useState, useEffect, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router';
import { projectService } from '../services/api/projectService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function ProjectWorkspacePage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();

  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Active milestone selection
  const [activeMilestoneIndex, setActiveMilestoneIndex] = useState(0);
  const [codeMap, setCodeMap] = useState({});

  // Verification state
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);

  // Fetch project details
  useEffect(() => {
    async function loadProject() {
      setLoading(true);
      try {
        const data = await projectService.getProjectBySlug(slug);
        setProject(data);

        // Populate initial code map from submitted code or starter code
        const initialCode = {};
        (data.milestones || []).forEach((m) => {
          initialCode[m.id] = (data.user_submitted_code && data.user_submitted_code[String(m.id)])
            || m.starter_code
            || '';
        });
        setCodeMap(initialCode);

        // Select the current incomplete milestone or the first milestone
        const milestones = data.milestones || [];
        const completedIds = data.user_completed_milestones || [];
        const nextIncompleteIdx = milestones.findIndex((m) => !completedIds.includes(m.id));
        if (nextIncompleteIdx !== -1) {
          setActiveMilestoneIndex(nextIncompleteIdx);
        } else if (milestones.length > 0) {
          setActiveMilestoneIndex(0);
        }
      } catch (err) {
        console.error('Failed to load project:', err);
        setError('Project not found or failed to load.');
      } finally {
        setLoading(false);
      }
    }
    loadProject();
  }, [slug]);

  const activeMilestone = useMemo(() => {
    if (!project || !project.milestones || project.milestones.length === 0) return null;
    return project.milestones[activeMilestoneIndex] || project.milestones[0];
  }, [project, activeMilestoneIndex]);

  const completedMilestoneIds = useMemo(() => {
    return project?.user_completed_milestones || [];
  }, [project]);

  const isMilestoneCompleted = (milestoneId) => {
    return completedMilestoneIds.includes(milestoneId);
  };

  const handleCodeChange = (newCode) => {
    if (!activeMilestone) return;
    setCodeMap((prev) => ({
      ...prev,
      [activeMilestone.id]: newCode,
    }));
  };

  const handleResetCode = () => {
    if (!activeMilestone) return;
    setCodeMap((prev) => ({
      ...prev,
      [activeMilestone.id]: activeMilestone.starter_code || '',
    }));
  };

  const handleVerify = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (!activeMilestone || isVerifying) return;

    const sourceCode = codeMap[activeMilestone.id] || '';
    if (!sourceCode.trim()) {
      alert('Source code cannot be empty.');
      return;
    }

    setIsVerifying(true);
    setVerificationResult(null);

    try {
      // Ensure project is started
      if (project.user_status === 'NOT_STARTED') {
        await projectService.startProject(project.slug);
      }

      const res = await projectService.verifyMilestone(project.slug, activeMilestone.id, sourceCode);
      setVerificationResult(res);

      if (res.passed) {
        // Refresh project data and user XP
        if (refreshUser) refreshUser();

        // Update local project progress
        setProject((prev) => {
          const updatedCompleted = Array.from(new Set([...(prev.user_completed_milestones || []), activeMilestone.id]));
          const isComplete = res.project_completed || updatedCompleted.length >= (prev.milestones || []).length;
          return {
            ...prev,
            user_status: isComplete ? 'COMPLETED' : 'IN_PROGRESS',
            user_completed_milestones: updatedCompleted,
            user_current_milestone_order: res.next_milestone_order || prev.user_current_milestone_order,
          };
        });

        if (res.project_completed) {
          setShowCelebration(true);
        } else if (activeMilestoneIndex + 1 < (project.milestones || []).length) {
          // Advance to next milestone after 1.5 seconds
          setTimeout(() => {
            setActiveMilestoneIndex((idx) => idx + 1);
          }, 1500);
        }
      }
    } catch (err) {
      console.error('Milestone verification error:', err);
      const msg = err?.response?.data?.detail || err?.response?.data?.message || 'Verification service error.';
      setVerificationResult({
        passed: false,
        message: msg,
        compile_output: err?.response?.data?.compile_output || msg,
      });
    } finally {
      setIsVerifying(false);
    }
  };

  // Keyboard shortcut: Ctrl+Enter / Cmd+Enter to verify
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleVerify();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleVerify]);

  const getLanguageInfo = (lang) => {
    switch (lang) {
      case 'python':
        return { label: 'Python 3', icon: '🐍', ext: 'py', color: 'text-emerald-400 border-emerald-500/30' };
      case 'javascript':
        return { label: 'JavaScript (Node.js)', icon: '🟨', ext: 'js', color: 'text-amber-400 border-amber-500/30' };
      case 'cpp':
        return { label: 'C++20 (GCC)', icon: '⚡', ext: 'cpp', color: 'text-cyan-400 border-cyan-500/30' };
      default:
        return { label: lang, icon: '💻', ext: 'txt', color: 'text-slate-400 border-slate-500/30' };
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-36">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="max-w-xl mx-auto py-24 text-center space-y-4">
        <span className="text-4xl">⚠️</span>
        <h2 className="text-xl font-bold text-white">Project Not Found</h2>
        <p className="text-sm text-slate-400">{error || 'The requested engineering project could not be located.'}</p>
        <Link
          to="/projects"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold"
        >
          Return to Projects Catalog
        </Link>
      </div>
    );
  }

  const langInfo = getLanguageInfo(project.language);

  return (
    <div className="w-full min-w-0 max-w-7xl mx-auto space-y-6 pb-20">
      {/* Top Breadcrumb & Project Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <Link to="/projects" className="hover:text-indigo-400 transition-colors">
              Projects
            </Link>
            <span>/</span>
            <span className="text-slate-200 font-semibold">{project.title}</span>
          </div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
              {project.title}
            </h1>
            <span className={`px-2.5 py-0.5 rounded-lg text-xs font-mono font-bold border ${langInfo.color}`}>
              {langInfo.icon} {langInfo.label}
            </span>
          </div>
        </div>

        {/* Status Capsule & Total XP Reward */}
        <div className="flex items-center gap-3 self-start md:self-auto">
          <div className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono flex items-center gap-2">
            <span className="text-slate-400">Project Reward:</span>
            <span className="text-cyan-400 font-bold">+{project.xp_reward} XP</span>
          </div>
          {project.user_status === 'COMPLETED' && (
            <span className="px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold flex items-center gap-1.5">
              <span>✓</span> Verified Complete
            </span>
          )}
        </div>
      </div>

      {/* Dual Pane Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Milestones Stepper & Milestone Specifications */}
        <div className="lg:col-span-5 space-y-5">
          {/* Milestone Stepper Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-sm space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
                Milestones Checklist
              </span>
              <span className="text-xs font-mono text-cyan-400">
                {completedMilestoneIds.length}/{(project.milestones || []).length} Completed
              </span>
            </div>

            <div className="space-y-2">
              {(project.milestones || []).map((milestone, idx) => {
                const isCompleted = isMilestoneCompleted(milestone.id);
                const isActive = activeMilestoneIndex === idx;

                return (
                  <button
                    key={milestone.id}
                    onClick={() => {
                      setActiveMilestoneIndex(idx);
                      setVerificationResult(null);
                    }}
                    className={`w-full text-left p-3 rounded-xl border transition-all flex items-center justify-between gap-3 ${isActive
                        ? 'bg-indigo-950/40 border-indigo-500/60 shadow-sm'
                        : isCompleted
                          ? 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700'
                          : 'bg-slate-950/30 border-slate-900 hover:border-slate-800 opacity-80'
                      }`}
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div
                        className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-mono font-bold flex-shrink-0 ${isCompleted
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                            : isActive
                              ? 'bg-indigo-600 text-white'
                              : 'bg-slate-800 text-slate-400'
                          }`}
                      >
                        {isCompleted ? '✓' : milestone.order}
                      </div>
                      <div className="min-w-0">
                        <h4 className={`text-xs font-bold truncate ${isActive ? 'text-white' : 'text-slate-300'}`}>
                          {milestone.title}
                        </h4>
                        <span className="text-[11px] font-mono text-slate-500">
                          +{milestone.xp_reward} XP
                        </span>
                      </div>
                    </div>

                    {isCompleted ? (
                      <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        Passed
                      </span>
                    ) : isActive ? (
                      <span className="text-[10px] font-mono font-bold text-indigo-300 uppercase bg-indigo-500/20 px-2 py-0.5 rounded border border-indigo-500/30">
                        Active
                      </span>
                    ) : null}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Milestone Documentation */}
          {activeMilestone && (
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-[11px] font-mono uppercase text-indigo-400 font-bold">
                    Milestone #{activeMilestone.order} Specifications
                  </span>
                  <h3 className="text-lg font-black text-white">{activeMilestone.title}</h3>
                </div>
                <div className="text-right font-mono">
                  <span className="text-xs text-slate-400 block">Milestone XP</span>
                  <span className="text-sm font-bold text-cyan-400">+{activeMilestone.xp_reward} XP</span>
                </div>
              </div>

              {/* Description & Requirements */}
              <div className="prose prose-invert prose-sm max-w-none text-slate-300 space-y-3 text-xs leading-relaxed">
                <div className="whitespace-pre-wrap font-sans text-slate-300 leading-relaxed bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/60">
                  {activeMilestone.description}
                </div>
              </div>

              {/* In-sandbox Verification Notice */}
              <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-[11px] text-slate-400 space-y-1.5">
                <div className="font-semibold text-slate-300 flex items-center gap-1.5">
                  <span>🔒</span> Isolated Sandbox Verification
                </div>
                <p>
                  When you click <strong>Verify Milestone</strong>, your solution is executed against our automated test harness in an isolated container. All assertions must pass with exit code 0.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Code Editor & Verification Console */}
        <div className="lg:col-span-7 space-y-4">
          {/* Code Editor Window */}
          <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
            {/* Editor Top Bar */}
            <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
                <span className="text-xs font-mono font-bold text-white">
                  {slug}_milestone_{activeMilestone?.order || 1}.{langInfo.ext}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700 flex items-center gap-1">
                  <span>{langInfo.icon}</span> {langInfo.label}
                </span>
              </div>
            </div>

            {/* Code Input Area */}
            <div className="p-4 bg-[#0d1117]">
              <textarea
                value={activeMilestone ? codeMap[activeMilestone.id] || '' : ''}
                onChange={(e) => handleCodeChange(e.target.value)}
                rows={22}
                spellCheck="false"
                className="w-full bg-transparent font-mono text-xs text-slate-200 leading-relaxed outline-none resize-y selection:bg-indigo-500 selection:text-white"
                placeholder={`// Implement Milestone #${activeMilestone?.order || 1} here...`}
              />
            </div>

            {/* Editor Action Bar */}
            <div className="px-4 py-3 bg-slate-900 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <button
                onClick={handleResetCode}
                className="text-xs text-slate-400 hover:text-white transition underline self-start"
              >
                Reset Starter Code
              </button>

              <div className="flex items-center gap-3">
                <span className="hidden sm:inline text-[11px] font-mono text-slate-500">
                  Ctrl+Enter to verify
                </span>
                <button
                  onClick={handleVerify}
                  disabled={isVerifying}
                  className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition disabled:opacity-50 flex items-center gap-2"
                >
                  {isVerifying ? (
                    <>
                      <Spinner size="sm" />
                      <span>Executing in Sandbox...</span>
                    </>
                  ) : (
                    <>
                      <span>Verify Milestone #{activeMilestone?.order || 1}</span>
                      <span>➔</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Verification Diagnostics Console */}
          {verificationResult && (
            <div
              className={`border rounded-2xl p-5 shadow-lg transition-all ${verificationResult.passed
                  ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300'
                  : 'bg-rose-950/20 border-rose-500/40 text-rose-300'
                }`}
            >
              <div className="flex items-center justify-between mb-3 border-b border-white/10 pb-2.5">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{verificationResult.passed ? '✅' : '❌'}</span>
                  <span className="text-xs font-mono font-black uppercase tracking-wider">
                    {verificationResult.passed ? 'Verification Succeeded' : 'Verification Failed'}
                  </span>
                </div>
                {verificationResult.execution_time && (
                  <span className="text-[11px] font-mono text-slate-400">
                    ⏱️ {(verificationResult.execution_time * 1000).toFixed(0)} ms
                  </span>
                )}
              </div>

              <p className="text-xs font-semibold mb-2">{verificationResult.message}</p>

              {verificationResult.compile_output && (
                <pre className="bg-black/60 p-3 rounded-xl font-mono text-[11px] text-slate-300 overflow-x-auto max-h-56 leading-relaxed border border-white/5">
                  {verificationResult.compile_output}
                </pre>
              )}

              {verificationResult.passed && verificationResult.xp_awarded > 0 && (
                <div className="mt-3 flex items-center justify-between text-xs font-mono bg-emerald-500/10 border border-emerald-500/30 px-3 py-2 rounded-xl text-emerald-300">
                  <span>🎉 Milestone Complete!</span>
                  <span className="font-bold">+{verificationResult.xp_awarded} XP Awarded</span>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Project Completion Celebration Modal */}
      {showCelebration && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="bg-gradient-to-b from-slate-900 to-indigo-950 border border-indigo-500/50 rounded-3xl p-8 max-w-lg w-full text-center space-y-6 shadow-2xl relative overflow-hidden animate-in fade-in zoom-in duration-300">
            <div className="text-5xl">🏆</div>
            <div className="space-y-2">
              <span className="text-xs font-mono uppercase tracking-widest text-cyan-400 font-bold">
                Project Milestone Certified
              </span>
              <h2 className="text-2xl sm:text-3xl font-black text-white">
                {project.title} Completed!
              </h2>
              <p className="text-sm text-slate-300">
                You have successfully implemented and verified all milestones for this production engineering project.
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-center space-y-1">
              <span className="text-xs font-mono text-slate-400">Total Project Reward</span>
              <div className="text-3xl font-black font-mono text-cyan-400">
                +{project.xp_reward} XP
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 pt-2">
              {user && (
                <Link
                  to={`/portfolio/${user.username}`}
                  className="flex-1 py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-colors shadow-md shadow-indigo-600/30"
                >
                  View in Public Portfolio ➔
                </Link>
              )}
              <button
                onClick={() => setShowCelebration(false)}
                className="py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
              >
                Close & Review Code
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

