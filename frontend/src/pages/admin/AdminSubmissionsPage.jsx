import React, { useEffect, useState } from 'react';
import adminService from '../../services/api/adminService';
import Spinner from '../../components/feedback/Spinner';

export default function AdminSubmissionsPage() {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [statusFilter, setStatusFilter] = useState('');
  const [languageFilter, setLanguageFilter] = useState('');
  const [usernameFilter, setUsernameFilter] = useState('');
  const [problemFilter, setProblemFilter] = useState('');

  // Code Inspector Modal
  const [inspectingSub, setInspectingSub] = useState(null);
  const [inspectLoading, setInspectLoading] = useState(false);
  const [rejudgingId, setRejudgingId] = useState(null);

  const fetchSubmissions = async () => {
    try {
      setLoading(true);
      const params = {};
      if (statusFilter) params.status = statusFilter;
      if (languageFilter) params.language = languageFilter;
      if (usernameFilter) params.username = usernameFilter;
      if (problemFilter) params.problem_slug = problemFilter;

      const data = await adminService.getSubmissions(params);
      setSubmissions(data.results || data);
      setError(null);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load submissions audit log.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSubmissions();
  }, [statusFilter, languageFilter, usernameFilter, problemFilter]);

  const handleInspect = async (subId) => {
    try {
      setInspectLoading(true);
      const detail = await adminService.getSubmission(subId);
      setInspectingSub(detail);
    } catch (err) {
      alert('Failed to load submission details: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setInspectLoading(false);
    }
  };

  const handleRejudge = async (subId) => {
    try {
      setRejudgingId(subId);
      const updated = await adminService.rejudgeSubmission(subId);
      setSubmissions(submissions.map(s => s.id === subId ? {
        ...s,
        status: updated.status,
        execution_time: updated.execution_time,
        memory_usage: updated.memory_usage,
        passed_test_cases_count: updated.passed_test_cases_count,
        total_test_cases_count: updated.total_test_cases_count,
      } : s));

      if (inspectingSub?.id === subId) {
        setInspectingSub(updated);
      }
    } catch (err) {
      alert('Re-judge failed: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setRejudgingId(null);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#131b2e] p-6 rounded-2xl border border-cyan-500/20 shadow-xl">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
            <span>Submissions Audit Stream</span>
            <span className="text-xs font-mono font-normal text-cyan-400 px-2.5 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30">
              Global Stream
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Audit developer code submissions, inspect sandbox outputs, and trigger re-judges.
          </p>
        </div>
        <button
          onClick={fetchSubmissions}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold self-start sm:self-auto transition-all"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh Stream</span>
        </button>
      </div>

      {/* Filters Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 bg-[#131b2e] p-4 rounded-2xl border border-slate-800">
        <input
          type="text"
          placeholder="Filter by username..."
          value={usernameFilter}
          onChange={(e) => setUsernameFilter(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
        />

        <input
          type="text"
          placeholder="Filter by problem slug..."
          value={problemFilter}
          onChange={(e) => setProblemFilter(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
        />

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Verdicts</option>
          <option value="ACCEPTED">ACCEPTED (Passed)</option>
          <option value="WRONG_ANSWER">WRONG_ANSWER</option>
          <option value="TIME_LIMIT_EXCEEDED">TIME_LIMIT_EXCEEDED</option>
          <option value="COMPILATION_ERROR">COMPILATION_ERROR</option>
          <option value="RUNTIME_ERROR">RUNTIME_ERROR</option>
          <option value="PENDING">PENDING</option>
        </select>

        <select
          value={languageFilter}
          onChange={(e) => setLanguageFilter(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Languages</option>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      {/* Submissions Stream Table */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        {loading && submissions.length === 0 ? (
          <div className="p-12 flex justify-center">
            <Spinner size="lg" />
          </div>
        ) : submissions.length === 0 ? (
          <div className="p-12 text-center text-slate-400 font-mono text-sm">
            No submissions found matching the criteria.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/80 text-xs font-mono uppercase tracking-wider text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3.5">ID & Timestamp</th>
                  <th className="px-4 py-3.5">Developer</th>
                  <th className="px-4 py-3.5">Challenge</th>
                  <th className="px-4 py-3.5">Track</th>
                  <th className="px-4 py-3.5">Verdict</th>
                  <th className="px-4 py-3.5">Pass Ratio</th>
                  <th className="px-4 py-3.5">Runtime</th>
                  <th className="px-4 py-3.5">Memory</th>
                  <th className="px-5 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {submissions.map((sub) => (
                  <tr key={sub.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-5 py-3.5 font-mono text-xs text-slate-400">
                      <div className="text-white font-bold">#{sub.id}</div>
                      <div>{new Date(sub.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</div>
                    </td>
                    <td className="px-4 py-3.5 font-semibold text-white">
                      @{sub.username}
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="font-semibold text-white">{sub.problem_title}</div>
                      <div className="text-xs font-mono text-slate-500">{sub.problem_slug}</div>
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-cyan-300">
                      {sub.language === 'python' ? '🐍 Python' : sub.language === 'javascript' ? '🟨 JS' : '⚡ C++'}
                    </td>
                    <td className="px-4 py-3.5">
                      <span className={`inline-block px-2.5 py-0.5 rounded text-[11px] font-bold font-mono ${sub.status === 'ACCEPTED'
                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                          : sub.status === 'COMPILATION_ERROR'
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            : 'bg-red-500/20 text-red-400 border border-red-500/30'
                        }`}>
                        {sub.status}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-slate-300">
                      {sub.passed_test_cases_count} / {sub.total_test_cases_count}
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-slate-400">
                      {sub.execution_time != null ? `${sub.execution_time}s` : '—'}
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-slate-400">
                      {sub.memory_usage ? `${Math.round(sub.memory_usage / 1024)} MB` : '—'}
                    </td>
                    <td className="px-5 py-3.5 text-right space-x-2">
                      <button
                        onClick={() => handleInspect(sub.id)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
                      >
                        Inspect Code
                      </button>
                      <button
                        onClick={() => handleRejudge(sub.id)}
                        disabled={rejudgingId === sub.id}
                        className="px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 text-xs font-semibold border border-cyan-500/30 transition-colors disabled:opacity-50"
                      >
                        {rejudgingId === sub.id ? 'Judging...' : 'Re-Judge ⚡'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Code Inspector Modal */}
      {inspectingSub && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
          <div className="bg-[#131b2e] border border-cyan-500/30 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col shadow-2xl">
            {/* Header */}
            <div className="p-5 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center gap-3">
                  <span>Submission #{inspectingSub.id}</span>
                  <span className={`px-2.5 py-0.5 rounded text-xs font-mono font-bold ${inspectingSub.status === 'ACCEPTED'
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : 'bg-red-500/20 text-red-400'
                    }`}>
                    {inspectingSub.status}
                  </span>
                </h2>
                <p className="text-xs text-slate-400 font-mono">
                  By @{inspectingSub.username} on "{inspectingSub.problem_title}" ({inspectingSub.language})
                </p>
              </div>
              <button
                onClick={() => setInspectingSub(null)}
                className="text-slate-400 hover:text-white p-2 text-xl"
              >
                ✕
              </button>
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-5">
              {/* Telemetry Strip */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 uppercase text-[10px] block">Execution Time</span>
                  <span className="text-white font-bold text-sm">{inspectingSub.execution_time != null ? `${inspectingSub.execution_time}s` : '—'}</span>
                </div>
                <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 uppercase text-[10px] block">Memory</span>
                  <span className="text-white font-bold text-sm">{inspectingSub.memory_usage ? `${Math.round(inspectingSub.memory_usage / 1024)} MB` : '—'}</span>
                </div>
                <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 uppercase text-[10px] block">Test Cases</span>
                  <span className="text-white font-bold text-sm">{inspectingSub.passed_test_cases_count} / {inspectingSub.total_test_cases_count}</span>
                </div>
                <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 uppercase text-[10px] block">Submitted At</span>
                  <span className="text-white font-bold text-sm">{new Date(inspectingSub.created_at).toLocaleDateString()}</span>
                </div>
              </div>

              {/* Source Code */}
              <div>
                <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Submitted Source Code</h3>
                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-cyan-200 overflow-x-auto max-h-64">
                  {inspectingSub.source_code}
                </pre>
              </div>

              {/* Compiler / Error Output */}
              {(inspectingSub.compile_output || inspectingSub.error_message) && (
                <div>
                  <h3 className="text-xs font-mono uppercase tracking-wider text-amber-400 mb-2">Compiler / Execution Errors</h3>
                  <pre className="p-4 rounded-xl bg-red-950/20 border border-red-500/30 font-mono text-xs text-red-300 overflow-x-auto">
                    {inspectingSub.compile_output || inspectingSub.error_message}
                  </pre>
                </div>
              )}

              {/* Test Cases Results */}
              {inspectingSub.results?.length > 0 && (
                <div>
                  <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">
                    Evaluation Test Cases ({inspectingSub.results.length})
                  </h3>
                  <div className="space-y-2">
                    {inspectingSub.results.map((r, i) => (
                      <div
                        key={i}
                        className={`p-3.5 rounded-xl border text-xs font-mono ${r.status === 'ACCEPTED'
                            ? 'bg-emerald-500/5 border-emerald-500/20 text-slate-300'
                            : 'bg-red-500/5 border-red-500/20 text-slate-300'
                          }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-bold text-white">
                            Case #{r.order} {r.is_sample ? '(Sample)' : '(Hidden)'}
                          </span>
                          <span className={`font-bold ${r.status === 'ACCEPTED' ? 'text-emerald-400' : 'text-red-400'}`}>
                            {r.status} ({r.execution_time}s)
                          </span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                          <div>
                            <span className="text-slate-500 block">Expected:</span>
                            <pre className="p-1.5 rounded bg-slate-950/60 border border-slate-800 overflow-x-auto">{r.expected_output}</pre>
                          </div>
                          <div>
                            <span className="text-slate-500 block">Actual Output:</span>
                            <pre className="p-1.5 rounded bg-slate-950/60 border border-slate-800 overflow-x-auto">{r.actual_output || '(none)'}</pre>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Footer Actions */}
            <div className="p-5 border-t border-slate-800 flex items-center justify-between bg-slate-900/40">
              <button
                type="button"
                onClick={() => setInspectingSub(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
              >
                Close
              </button>
              <button
                type="button"
                onClick={() => handleRejudge(inspectingSub.id)}
                disabled={rejudgingId === inspectingSub.id}
                className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 disabled:opacity-50"
              >
                {rejudgingId === inspectingSub.id ? 'Re-Judging in Sandbox...' : 'Re-Judge Submission ⚡'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

