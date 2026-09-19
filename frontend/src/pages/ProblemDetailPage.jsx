import { useState, useEffect, useRef } from 'react';
import { useParams, Link, useNavigate } from 'react-router';
import { problemService } from '../services/api/problemService';
import { submissionService } from '../services/api/submissionService';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/feedback/Spinner';

export default function ProblemDetailPage() {
  const { slug } = useParams();
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();

  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [code, setCode] = useState('');
  const [activeTab, setActiveTab] = useState('statement'); // 'statement' | 'history'
  const [sampleCaseIndex, setSampleCaseIndex] = useState(0);

  // Submissions & Evaluation States
  const [activeSubmission, setActiveSubmission] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [history, setHistory] = useState([]);
  const [selectedResultIndex, setSelectedResultIndex] = useState(0);

  const pollIntervalRef = useRef(null);

  useEffect(() => {
    const fetchDetail = async () => {
      setLoading(true);
      try {
        const data = await problemService.getProblemBySlug(slug);
        setProblem(data);
        setCode(
          data.starter_code ||
          '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your solution here\n    return 0;\n}\n'
        );
      } catch {
        setError('Challenge not found or failed to load.');
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [slug]);

  const fetchHistory = async () => {
    if (!problem || !user) return;
    try {
      const res = await submissionService.getSubmissionsForProblem(problem.id);
      setHistory(res?.results || []);
    } catch (err) {
      console.error('Failed to fetch submission history:', err);
    }
  };

  useEffect(() => {
    if (problem && user && activeTab === 'history') {
      fetchHistory();
    }
  }, [problem, user, activeTab]);

  // Clean up polling timer on unmount
  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    };
  }, []);

  const handleRunCode = async (isSampleRun = false) => {
    if (!user) {
      navigate('/login');
      return;
    }

    if (!code.trim()) return;

    setIsEvaluating(true);
    setActiveSubmission(null);
    setSelectedResultIndex(0);

    try {
      const initialSub = await submissionService.createSubmission({
        problem_id: problem.id,
        source_code: code,
        language: problem.language || (problem.slug?.startsWith('py-') ? 'python' : problem.slug?.startsWith('js-') ? 'javascript' : 'cpp'),
        is_sample_run: isSampleRun,
      });

      setActiveSubmission(initialSub);

      // Poll until terminal status reached
      pollIntervalRef.current = setInterval(async () => {
        try {
          const updated = await submissionService.getSubmission(initialSub.id);
          setActiveSubmission(updated);

          if (updated.status !== 'PENDING' && updated.status !== 'PROCESSING') {
            clearInterval(pollIntervalRef.current);
            setIsEvaluating(false);

            // If solve was accepted, refresh user profile to update level and XP
            if (updated.status === 'ACCEPTED' && !isSampleRun) {
              refreshUser();
            }

            // Refresh history
            fetchHistory();
          }
        } catch {
          clearInterval(pollIntervalRef.current);
          setIsEvaluating(false);
        }
      }, 1000);
    } catch (err) {
      setIsEvaluating(false);
      const msg = err?.response?.data?.detail || 'Failed to dispatch submission.';
      alert(msg);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh]">
        <Spinner />
        <p className="text-xs text-slate-400 mt-3 font-mono">Loading problem statement...</p>
      </div>
    );
  }

  if (error || !problem) {
    return (
      <div className="text-center py-20 bg-[var(--color-surface-card)] rounded-2xl border border-slate-800 p-8 max-w-lg mx-auto">
        <div className="text-4xl mb-3">⚠️</div>
        <h2 className="text-xl font-bold text-white">{error || 'Problem not found'}</h2>
        <p className="text-xs text-slate-400 mt-2">The requested challenge might have been moved or unpublished.</p>
        <Link to="/problems" className="inline-block mt-6 px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold">
          Back to Challenges
        </Link>
      </div>
    );
  }

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

  const getVerdictColor = (status) => {
    switch (status) {
      case 'ACCEPTED':
        return 'text-emerald-400 bg-emerald-950/60 border-emerald-800';
      case 'WRONG_ANSWER':
        return 'text-rose-400 bg-rose-950/60 border-rose-800';
      case 'COMPILATION_ERROR':
        return 'text-amber-400 bg-amber-950/60 border-amber-800';
      case 'TIME_LIMIT_EXCEEDED':
        return 'text-orange-400 bg-orange-950/60 border-orange-800';
      case 'PROCESSING':
      case 'PENDING':
        return 'text-cyan-400 bg-cyan-950/60 border-cyan-800';
      default:
        return 'text-slate-300 bg-slate-800 border-slate-700';
    }
  };

  const getLanguageInfo = (lang, prob = null) => {
    const raw = (
      lang ||
      prob?.language ||
      prob?.category?.slug ||
      (prob?.slug?.startsWith('py-') ? 'python' : '') ||
      (prob?.slug?.startsWith('js-') ? 'javascript' : '') ||
      (prob?.slug?.startsWith('cpp-') ? 'cpp' : '') ||
      ''
    ).toLowerCase();

    if (raw.includes('python') || raw.startsWith('py')) {
      return {
        label: 'Python 3.8+',
        icon: '🐍',
        badgeClass: 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60',
        filename: 'solution.py',
        placeholder: 'Write your Python 3 solution here...',
      };
    }
    if (raw.includes('javascript') || raw.includes('node') || raw.startsWith('js')) {
      return {
        label: 'JavaScript (Node.js)',
        icon: '🟨',
        badgeClass: 'bg-amber-950/60 text-amber-300 border-amber-800/60',
        filename: 'solution.js',
        placeholder: 'Write your JavaScript (Node.js) solution here...',
      };
    }
    return {
      label: 'C++ (GCC 9.2)',
      icon: '⚡',
      badgeClass: 'bg-cyan-950/60 text-cyan-300 border-cyan-800/60',
      filename: 'solution.cpp',
      placeholder: 'Write your C++ solution here...',
    };
  };

  const sampleCases = problem.sample_test_cases || [];
  const langInfo = getLanguageInfo(problem.language, problem);

  return (
    <div className="space-y-6 w-full min-w-0">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <Link to="/problems" className="text-slate-400 hover:text-white transition p-1.5 rounded-lg hover:bg-slate-800">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-black text-white tracking-tight">{problem.title}</h1>
            <div className="flex items-center gap-2 mt-1">
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${langInfo.badgeClass} flex items-center gap-1`}>
                <span>{langInfo.icon}</span> {langInfo.label}
              </span>
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${getDifficultyBadge(problem.difficulty)}`}>
                {problem.difficulty}
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-800 border border-slate-700 text-slate-300">
                Tier {problem.challenge_level}
              </span>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold text-amber-400 bg-amber-950/40 border border-amber-800/40">
                +{problem.xp_reward} XP
              </span>
              <span className="text-xs text-slate-400 font-medium">in {problem.category?.name}</span>
            </div>
          </div>
        </div>

        {/* Tab Toggle (Statement vs Submissions) */}
        <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800 self-start sm:self-auto text-xs font-semibold">
          <button
            onClick={() => setActiveTab('statement')}
            className={`px-3 py-1.5 rounded-lg transition ${activeTab === 'statement' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
          >
            Problem Statement
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-3 py-1.5 rounded-lg transition ${activeTab === 'history' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
          >
            Submissions {history.length > 0 && `(${history.length})`}
          </button>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start w-full min-w-0">
        {/* Left Column: Problem Details OR Submission History */}
        <div className="lg:col-span-6 space-y-6 w-full min-w-0">
          {activeTab === 'statement' ? (
            <>
              {/* Problem Description Card */}
              <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 space-y-6 shadow-sm">
                <div>
                  <h2 className="text-xs uppercase font-bold text-cyan-400 tracking-wider mb-2">Description</h2>
                  <div className="text-sm text-slate-200 leading-relaxed whitespace-pre-line">
                    {problem.description}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-800">
                  <div>
                    <h3 className="text-xs uppercase font-bold text-slate-400 tracking-wider mb-1.5">Input Format</h3>
                    <div className="text-xs text-slate-300 whitespace-pre-line bg-slate-900/80 p-3 rounded-xl border border-slate-800 font-mono">
                      {problem.input_format || 'Standard input stream (cin)'}
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xs uppercase font-bold text-slate-400 tracking-wider mb-1.5">Output Format</h3>
                    <div className="text-xs text-slate-300 whitespace-pre-line bg-slate-900/80 p-3 rounded-xl border border-slate-800 font-mono">
                      {problem.output_format || 'Standard output stream (cout)'}
                    </div>
                  </div>
                </div>

                {problem.constraints && (
                  <div className="pt-4 border-t border-slate-800">
                    <h3 className="text-xs uppercase font-bold text-slate-400 tracking-wider mb-1.5">Constraints</h3>
                    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-3 text-xs text-amber-300/90 font-mono whitespace-pre-line">
                      {problem.constraints}
                    </div>
                  </div>
                )}

                <div className="flex items-center gap-6 pt-4 border-t border-slate-800 text-xs text-slate-400 font-mono">
                  <div>⏱️ Time Limit: <span className="text-white font-bold">{problem.time_limit_seconds}s</span></div>
                  <div>💾 Memory Limit: <span className="text-white font-bold">{Math.round(problem.memory_limit_kb / 1024)} MB</span></div>
                </div>
              </div>

              {/* Sample Cases */}
              {sampleCases.length > 0 && (
                <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 space-y-4 shadow-sm">
                  <h2 className="text-xs uppercase font-bold text-cyan-400 tracking-wider">
                    Sample Test Cases
                  </h2>

                  <div className="flex gap-2 border-b border-slate-800 pb-2">
                    {sampleCases.map((c, idx) => (
                      <button
                        key={c.id}
                        onClick={() => setSampleCaseIndex(idx)}
                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${sampleCaseIndex === idx
                          ? 'bg-indigo-600 text-white'
                          : 'text-slate-400 hover:text-white bg-slate-800'
                          }`}
                      >
                        Sample Case {idx + 1}
                      </button>
                    ))}
                  </div>

                  {sampleCases[sampleCaseIndex] && (
                    <div className="space-y-3 pt-1">
                      <div>
                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Input:</span>
                        <pre className="mt-1 p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-emerald-300 overflow-x-auto">
                          {sampleCases[sampleCaseIndex].input_data}
                        </pre>
                      </div>
                      <div>
                        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Expected Output:</span>
                        <pre className="mt-1 p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-cyan-300 overflow-x-auto">
                          {sampleCases[sampleCaseIndex].expected_output}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </>
          ) : (
            /* Submissions History Tab */
            <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-6 space-y-4 shadow-sm">
              <h2 className="text-sm font-bold text-white mb-2">Past Submissions on this Challenge</h2>
              {!user ? (
                <p className="text-xs text-slate-400">Please log in to view your submissions.</p>
              ) : history.length === 0 ? (
                <p className="text-xs text-slate-400 py-8 text-center">No submissions yet for this problem.</p>
              ) : (
                <div className="space-y-2">
                  {history.map((sub) => (
                    <div
                      key={sub.id}
                      className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between text-xs"
                    >
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded font-bold uppercase border text-[10px] ${getVerdictColor(sub.status)}`}>
                          {sub.status}
                        </span>
                        <span className="text-slate-400 font-mono">
                          {sub.passed_test_cases_count}/{sub.total_test_cases_count} cases
                        </span>
                        {sub.is_sample_run && (
                          <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">Sample Run</span>
                        )}
                      </div>
                      <div className="text-slate-500 font-mono text-[11px]">
                        {new Date(sub.created_at).toLocaleTimeString()}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Code Editor & Execution Results Drawer */}
        <div className="lg:col-span-6 space-y-4 w-full min-w-0">
          {/* Editor Window */}
          <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl w-full">
            {/* Editor Top Bar */}
            <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
                <span className="text-xs font-mono font-bold text-white">{langInfo.filename}</span>
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
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={18}
                spellCheck="false"
                className="w-full bg-transparent font-mono text-xs text-slate-200 leading-relaxed outline-none resize-y selection:bg-indigo-500 selection:text-white"
                placeholder={langInfo.placeholder}
              />
            </div>

            {/* Editor Action Bar */}
            <div className="px-4 py-3 bg-slate-900 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <button
                onClick={() => setCode(problem.starter_code)}
                className="text-xs text-slate-400 hover:text-white transition underline self-start"
              >
                Reset Starter Code
              </button>

              <div className="flex flex-wrap items-center gap-2 sm:gap-3 w-full sm:w-auto">
                <button
                  onClick={() => handleRunCode(true)}
                  disabled={isEvaluating}
                  className="flex-1 sm:flex-none px-3.5 sm:px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  <span>Run Sample Tests</span>
                </button>

                <button
                  onClick={() => handleRunCode(false)}
                  disabled={isEvaluating}
                  className="flex-1 sm:flex-none px-4 sm:px-5 py-2 rounded-xl bg-[var(--color-brand-primary)] hover:bg-[var(--color-brand-primary-hover)] text-white text-xs font-bold shadow-md shadow-indigo-500/25 transition disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {isEvaluating ? (
                    <>
                      <svg className="animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      <span>Evaluating...</span>
                    </>
                  ) : (
                    <>
                      <span>Submit Code</span>
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                      </svg>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Live Evaluation Results Drawer */}
          {(isEvaluating || activeSubmission) && (
            <div className="bg-[var(--color-surface-card)] border border-[var(--color-surface-hover)] rounded-2xl p-5 shadow-xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-white">Execution Verdict:</span>
                  {isEvaluating ? (
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-800 animate-pulse">
                      Running in Sandbox...
                    </span>
                  ) : (
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold border ${getVerdictColor(activeSubmission?.status)}`}>
                      {activeSubmission?.status}
                    </span>
                  )}
                </div>

                {activeSubmission && !isEvaluating && (
                  <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
                    {activeSubmission.execution_time != null && (
                      <span>⏱️ {activeSubmission.execution_time}s</span>
                    )}
                    {activeSubmission.memory_usage != null && (
                      <span>💾 {activeSubmission.memory_usage} KB</span>
                    )}
                    <span>
                      Passed: <strong className="text-white">{activeSubmission.passed_test_cases_count}/{activeSubmission.total_test_cases_count}</strong>
                    </span>
                  </div>
                )}
              </div>

              {/* Status Specific Banners */}
              {activeSubmission?.status === 'ACCEPTED' && !isEvaluating && (
                <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 text-xs font-semibold flex items-center justify-between">
                  <span>🎉 All test cases passed successfully!</span>
                  {!activeSubmission.is_sample_run && (
                    <span className="font-mono bg-emerald-900/60 px-2 py-0.5 rounded text-emerald-200">
                      +{problem.xp_reward} XP Earned
                    </span>
                  )}
                </div>
              )}

              {/* Compilation Error Output */}
              {activeSubmission?.compile_output && (
                <div>
                  <span className="text-[11px] font-bold text-rose-400 uppercase tracking-wider">Compiler Diagnostic:</span>
                  <pre className="mt-1 p-3 rounded-xl bg-slate-950 border border-rose-900/50 font-mono text-xs text-rose-300 overflow-x-auto whitespace-pre-wrap">
                    {activeSubmission.compile_output}
                  </pre>
                </div>
              )}

              {/* Per-Test-Case Results Tabs */}
              {activeSubmission?.results?.length > 0 && (
                <div className="space-y-3 pt-2">
                  <div className="flex flex-wrap gap-1.5 border-b border-slate-800 pb-2">
                    {activeSubmission.results.map((r, idx) => (
                      <button
                        key={r.id}
                        onClick={() => setSelectedResultIndex(idx)}
                        className={`px-2.5 py-1 rounded-lg text-xs font-mono font-semibold transition ${selectedResultIndex === idx
                          ? 'bg-indigo-600 text-white shadow-sm'
                          : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
                          }`}
                      >
                        Case {idx + 1}: {r.status === 'ACCEPTED' ? '✓' : '✗'}
                      </button>
                    ))}
                  </div>

                  {activeSubmission.results[selectedResultIndex] && (
                    <div className="space-y-2 text-xs">
                      <div className="flex items-center justify-between text-slate-400 text-[11px] font-mono">
                        <span>Status: <strong className={activeSubmission.results[selectedResultIndex].status === 'ACCEPTED' ? 'text-emerald-400' : 'text-rose-400'}>{activeSubmission.results[selectedResultIndex].status}</strong></span>
                        {activeSubmission.results[selectedResultIndex].execution_time != null && (
                          <span>{activeSubmission.results[selectedResultIndex].execution_time}s</span>
                        )}
                      </div>

                      <div>
                        <span className="text-[11px] text-slate-400 font-bold uppercase">Input:</span>
                        <pre className="mt-0.5 p-2 rounded-lg bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-300 overflow-x-auto">
                          {activeSubmission.results[selectedResultIndex].input_data}
                        </pre>
                      </div>

                      <div>
                        <span className="text-[11px] text-slate-400 font-bold uppercase">Expected:</span>
                        <pre className="mt-0.5 p-2 rounded-lg bg-slate-950 border border-slate-800 font-mono text-[11px] text-cyan-300 overflow-x-auto">
                          {activeSubmission.results[selectedResultIndex].expected_output}
                        </pre>
                      </div>

                      {activeSubmission.results[selectedResultIndex].actual_output && (
                        <div>
                          <span className="text-[11px] text-slate-400 font-bold uppercase">Your Output:</span>
                          <pre className="mt-0.5 p-2 rounded-lg bg-slate-950 border border-slate-800 font-mono text-[11px] text-emerald-300 overflow-x-auto">
                            {activeSubmission.results[selectedResultIndex].actual_output}
                          </pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
