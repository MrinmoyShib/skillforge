import React, { useEffect, useState } from 'react';
import adminService from '../../services/api/adminService';
import Spinner from '../../components/feedback/Spinner';
import { useToast } from '../../components/feedback/Toast';

export default function AdminProblemsPage() {
  const toast = useToast();
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [search, setSearch] = useState('');
  const [language, setLanguage] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [isPublished, setIsPublished] = useState('');

  // Edit / Create Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProblem, setEditingProblem] = useState(null);
  const [modalTab, setModalTab] = useState('general'); // 'general' | 'statement' | 'testcases' | 'verify'
  const [saving, setSaving] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    description: '',
    language: 'python',
    difficulty: 'easy',
    challenge_level: 1,
    xp_reward: 50,
    time_limit_seconds: 2.0,
    memory_limit_kb: 262144,
    is_published: false,
    starter_code: '',
    constraints: '',
    input_format: '',
    output_format: '',
    category_slug: 'algorithms',
    test_cases: [
      { input_data: '', expected_output: '', is_sample: true, order: 1 }
    ]
  });

  // Verify Solution state
  const [verifyCode, setVerifyCode] = useState('');
  const [verifying, setVerifying] = useState(false);
  const [verifyResult, setVerifyResult] = useState(null);

  const fetchProblems = async () => {
    try {
      setLoading(true);
      const params = {};
      if (search) params.search = search;
      if (language) params.language = language;
      if (difficulty) params.difficulty = difficulty;
      if (isPublished !== '') params.is_published = isPublished;

      const data = await adminService.getProblems(params);
      setProblems(data.results || data);
      setError(null);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load problems.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProblems();
  }, [search, language, difficulty, isPublished]);

  const handleOpenCreate = () => {
    setEditingProblem(null);
    setFormData({
      title: '',
      slug: '',
      description: '',
      language: 'python',
      difficulty: 'easy',
      challenge_level: 1,
      xp_reward: 50,
      time_limit_seconds: 2.0,
      memory_limit_kb: 262144,
      is_published: false,
      starter_code: '',
      constraints: '',
      input_format: '',
      output_format: '',
      category_slug: 'algorithms',
      test_cases: [
        { input_data: '', expected_output: '', is_sample: true, order: 1 }
      ]
    });
    setVerifyCode('');
    setVerifyResult(null);
    setModalTab('general');
    setModalOpen(true);
  };

  const handleOpenEdit = async (problem) => {
    try {
      setLoading(true);
      const detail = await adminService.getProblem(problem.id);
      setEditingProblem(detail);
      setFormData({
        title: detail.title,
        slug: detail.slug,
        description: detail.description || '',
        language: detail.language,
        difficulty: detail.difficulty,
        challenge_level: detail.challenge_level,
        xp_reward: detail.xp_reward,
        time_limit_seconds: detail.time_limit_seconds,
        memory_limit_kb: detail.memory_limit_kb,
        is_published: detail.is_published,
        starter_code: detail.starter_code || '',
        constraints: detail.constraints || '',
        input_format: detail.input_format || '',
        output_format: detail.output_format || '',
        category_id: detail.category_id,
        test_cases: detail.test_cases?.length ? detail.test_cases : [
          { input_data: '', expected_output: '', is_sample: true, order: 1 }
        ]
      });
      setVerifyCode(detail.starter_code || '');
      setVerifyResult(null);
      setModalTab('general');
      setModalOpen(true);
    } catch (err) {
      toast.error('Failed to load problem details: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePublish = async (problem) => {
    try {
      const updated = await adminService.updateProblem(problem.id, {
        is_published: !problem.is_published
      });
      setProblems(problems.map(p => p.id === problem.id ? { ...p, is_published: updated.is_published } : p));
    } catch (err) {
      toast.error('Failed to toggle publish status: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const handleDelete = async (problem) => {
    // TODO: replace with confirmation modal
    if (!window.confirm(`Are you sure you want to permanently delete challenge "${problem.title}"?`)) {
      return;
    }
    try {
      await adminService.deleteProblem(problem.id);
      setProblems(problems.filter(p => p.id !== problem.id));
      toast.success('Challenge deleted successfully.');
    } catch (err) {
      toast.error('Failed to delete problem: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const handleSaveProblem = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      if (editingProblem) {
        await adminService.updateProblem(editingProblem.id, formData);
        toast.success('Challenge updated successfully.');
      } else {
        await adminService.createProblem(formData);
        toast.success('Challenge created successfully.');
      }
      setModalOpen(false);
      fetchProblems();
    } catch (err) {
      toast.error('Failed to save challenge: ' + JSON.stringify(err?.response?.data || err.message));
    } finally {
      setSaving(false);
    }
  };

  const handleRunVerify = async () => {
    if (!editingProblem) {
      toast.warning('Please save the challenge first before running sandbox verification.');
      return;
    }
    if (!verifyCode.trim()) {
      toast.warning('Please enter solution code to verify.');
      return;
    }

    try {
      setVerifying(true);
      const res = await adminService.verifyProblem(editingProblem.id, {
        source_code: verifyCode,
        language: formData.language
      });
      setVerifyResult(res);
      if (res.all_passed) {
        toast.success('All test cases passed!');
      } else {
        toast.warning('Some test cases failed.');
      }
    } catch (err) {
      toast.error('Verification failed: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setVerifying(false);
    }
  };

  // Test case handlers
  const addTestCase = () => {
    setFormData({
      ...formData,
      test_cases: [
        ...formData.test_cases,
        { input_data: '', expected_output: '', is_sample: false, order: formData.test_cases.length + 1 }
      ]
    });
  };

  const removeTestCase = (index) => {
    setFormData({
      ...formData,
      test_cases: formData.test_cases.filter((_, i) => i !== index)
    });
  };

  const updateTestCase = (index, field, value) => {
    const updated = [...formData.test_cases];
    updated[index][field] = value;
    setFormData({ ...formData, test_cases: updated });
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#131b2e] p-6 rounded-2xl border border-cyan-500/20 shadow-xl">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
            <span>Problem Studio</span>
            <span className="text-xs font-mono font-normal text-cyan-400 px-2.5 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30">
              {problems.length} Challenges
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Author, publish, manage test cases, and sandbox-verify algorithmic challenges across all language tracks.
          </p>
        </div>
        <button
          onClick={handleOpenCreate}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-sm font-bold shadow-lg shadow-cyan-500/20 transition-all self-start sm:self-auto"
        >
          <span>+ Create Challenge</span>
        </button>
      </div>

      {/* Filters Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 bg-[#131b2e] p-4 rounded-2xl border border-slate-800">
        <input
          type="text"
          placeholder="Search by title, slug..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
        />

        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Language Tracks</option>
          <option value="python">🐍 Python</option>
          <option value="javascript">🟨 JavaScript</option>
          <option value="cpp">⚡ C++</option>
        </select>

        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        <select
          value={isPublished}
          onChange={(e) => setIsPublished(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Statuses</option>
          <option value="true">Published</option>
          <option value="false">Draft</option>
        </select>
      </div>

      {/* Problems Catalog Table */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        {loading && problems.length === 0 ? (
          <div className="p-12 flex justify-center">
            <Spinner size="lg" />
          </div>
        ) : problems.length === 0 ? (
          <div className="p-12 text-center text-slate-400 font-mono text-sm">
            No challenges found matching the selected filters.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/80 text-xs font-mono uppercase tracking-wider text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3.5">Challenge Title</th>
                  <th className="px-4 py-3.5">Track</th>
                  <th className="px-4 py-3.5">Difficulty</th>
                  <th className="px-4 py-3.5">Tier</th>
                  <th className="px-4 py-3.5">XP</th>
                  <th className="px-4 py-3.5">Test Cases</th>
                  <th className="px-4 py-3.5">Solves</th>
                  <th className="px-4 py-3.5">Status</th>
                  <th className="px-5 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {problems.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-5 py-3.5 font-semibold text-white">
                      <div>{p.title}</div>
                      <div className="text-xs font-mono text-slate-400">{p.slug}</div>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className="inline-flex items-center gap-1 font-mono text-xs text-cyan-300">
                        {p.language === 'python' ? '🐍 Python' : p.language === 'javascript' ? '🟨 JS' : '⚡ C++'}
                      </span>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className={`inline-block px-2 py-0.5 rounded text-[11px] font-bold uppercase font-mono ${p.difficulty === 'easy' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                          p.difficulty === 'medium' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                            'bg-red-500/20 text-red-400 border border-red-500/30'
                        }`}>
                        {p.difficulty}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-slate-300">
                      L{p.challenge_level}
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-indigo-300 font-bold">
                      +{p.xp_reward}
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-slate-400">
                      {p.test_cases_count} cases
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-emerald-400">
                      {p.solves_count}
                    </td>
                    <td className="px-4 py-3.5">
                      <button
                        onClick={() => handleTogglePublish(p)}
                        className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold transition-all ${p.is_published
                            ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 hover:bg-cyan-500/30'
                            : 'bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700'
                          }`}
                      >
                        {p.is_published ? '● Published' : '○ Draft'}
                      </button>
                    </td>
                    <td className="px-5 py-3.5 text-right space-x-2">
                      <button
                        onClick={() => handleOpenEdit(p)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
                      >
                        Studio / Edit
                      </button>
                      <button
                        onClick={() => handleDelete(p)}
                        className="px-2.5 py-1 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-semibold border border-red-500/30 transition-colors"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create / Edit Problem Studio Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
          <div className="bg-[#131b2e] border border-cyan-500/30 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col shadow-2xl">
            {/* Modal Header */}
            <div className="p-5 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-white">
                  {editingProblem ? `Editing Challenge: ${editingProblem.title}` : 'Author New Challenge'}
                </h2>
                <p className="text-xs text-slate-400">Configure parameters, test cases, and sandbox verification</p>
              </div>
              <button
                onClick={() => setModalOpen(false)}
                className="text-slate-400 hover:text-white p-2 text-xl"
              >
                ✕
              </button>
            </div>

            {/* Modal Tabs */}
            <div className="flex border-b border-slate-800 px-5 gap-4 text-xs font-mono bg-slate-900/60">
              <button
                onClick={() => setModalTab('general')}
                className={`py-3 border-b-2 font-bold transition-all ${modalTab === 'general' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
              >
                1. General Parameters
              </button>
              <button
                onClick={() => setModalTab('statement')}
                className={`py-3 border-b-2 font-bold transition-all ${modalTab === 'statement' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
              >
                2. Statement & Starter Code
              </button>
              <button
                onClick={() => setModalTab('testcases')}
                className={`py-3 border-b-2 font-bold transition-all ${modalTab === 'testcases' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
              >
                3. Test Cases ({formData.test_cases.length})
              </button>
              {editingProblem && (
                <button
                  onClick={() => setModalTab('verify')}
                  className={`py-3 border-b-2 font-bold transition-all ${modalTab === 'verify' ? 'border-emerald-400 text-emerald-300' : 'border-transparent text-slate-400 hover:text-slate-200'
                    }`}
                >
                  4. Sandbox Verify ⚡
                </button>
              )}
            </div>

            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-6">
              {/* Tab 1: General Info */}
              {modalTab === 'general' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Challenge Title *</label>
                    <input
                      type="text"
                      required
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      placeholder="e.g. Invert Binary Tree"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Slug (auto-generated if blank)</label>
                    <input
                      type="text"
                      value={formData.slug}
                      onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                      placeholder="e.g. invert-binary-tree"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Language Track *</label>
                    <select
                      value={formData.language}
                      onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    >
                      <option value="python">Python 3</option>
                      <option value="javascript">JavaScript</option>
                      <option value="cpp">C++ 20</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Difficulty</label>
                    <select
                      value={formData.difficulty}
                      onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    >
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Progression Tier (1-5)</label>
                    <input
                      type="number"
                      min="1"
                      max="5"
                      value={formData.challenge_level}
                      onChange={(e) => setFormData({ ...formData, challenge_level: parseInt(e.target.value) || 1 })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">XP Reward</label>
                    <input
                      type="number"
                      value={formData.xp_reward}
                      onChange={(e) => setFormData({ ...formData, xp_reward: parseInt(e.target.value) || 50 })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Time Limit (Seconds)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.time_limit_seconds}
                      onChange={(e) => setFormData({ ...formData, time_limit_seconds: parseFloat(e.target.value) || 2.0 })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div className="col-span-2 flex items-center gap-3 pt-3">
                    <input
                      type="checkbox"
                      id="is_published"
                      checked={formData.is_published}
                      onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                      className="w-4 h-4 rounded text-cyan-600 bg-slate-900 border-slate-700"
                    />
                    <label htmlFor="is_published" className="text-sm text-white font-medium">
                      Publish immediately (visible to all students in catalog)
                    </label>
                  </div>
                </div>
              )}

              {/* Tab 2: Statement & Starter Code */}
              {modalTab === 'statement' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Markdown Description</label>
                    <textarea
                      rows={6}
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Enter problem statement with examples in Markdown..."
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white font-mono focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Starter Code Boilerplate</label>
                    <textarea
                      rows={6}
                      value={formData.starter_code}
                      onChange={(e) => setFormData({ ...formData, starter_code: e.target.value })}
                      placeholder="Initial starter code provided to student..."
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white font-mono focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                      <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Constraints</label>
                      <textarea
                        rows={3}
                        value={formData.constraints}
                        onChange={(e) => setFormData({ ...formData, constraints: e.target.value })}
                        placeholder="1 <= N <= 10^5"
                        className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Input Format</label>
                      <textarea
                        rows={3}
                        value={formData.input_format}
                        onChange={(e) => setFormData({ ...formData, input_format: e.target.value })}
                        placeholder="First line contains N..."
                        className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Output Format</label>
                      <textarea
                        rows={3}
                        value={formData.output_format}
                        onChange={(e) => setFormData({ ...formData, output_format: e.target.value })}
                        placeholder="Print the single integer result..."
                        className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Tab 3: Test Cases */}
              {modalTab === 'testcases' && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-slate-400">
                      Sample test cases are visible to students. Hidden test cases are masked for anti-leak protection.
                    </p>
                    <button
                      type="button"
                      onClick={addTestCase}
                      className="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 text-xs font-semibold"
                    >
                      + Add Test Case
                    </button>
                  </div>

                  <div className="space-y-4">
                    {formData.test_cases.map((tc, idx) => (
                      <div key={idx} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-mono font-bold text-white">
                            Case #{idx + 1} {tc.is_sample ? '(Sample / Public)' : '(Hidden / Evaluation)'}
                          </span>
                          <div className="flex items-center gap-3">
                            <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                              <input
                                type="checkbox"
                                checked={tc.is_sample}
                                onChange={(e) => updateTestCase(idx, 'is_sample', e.target.checked)}
                                className="w-3.5 h-3.5 text-cyan-500"
                              />
                              <span>Sample</span>
                            </label>
                            {formData.test_cases.length > 1 && (
                              <button
                                type="button"
                                onClick={() => removeTestCase(idx)}
                                className="text-red-400 hover:text-red-300 text-xs font-mono"
                              >
                                Remove
                              </button>
                            )}
                          </div>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                          <div>
                            <label className="block text-[11px] font-mono text-slate-400 mb-1">Standard Input (stdin)</label>
                            <textarea
                              rows={3}
                              value={tc.input_data}
                              onChange={(e) => updateTestCase(idx, 'input_data', e.target.value)}
                              placeholder="e.g. 5\n"
                              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-cyan-500"
                            />
                          </div>
                          <div>
                            <label className="block text-[11px] font-mono text-slate-400 mb-1">Expected Output (stdout)</label>
                            <textarea
                              rows={3}
                              value={tc.expected_output}
                              onChange={(e) => updateTestCase(idx, 'expected_output', e.target.value)}
                              placeholder="e.g. 10\n"
                              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-cyan-500"
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tab 4: Sandbox Verify */}
              {modalTab === 'verify' && editingProblem && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-bold text-white">In-Studio Solution Tester</h3>
                      <p className="text-xs text-slate-400">
                        Paste a reference solution to test against all {formData.test_cases.length} test cases in the sandbox.
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={handleRunVerify}
                      disabled={verifying}
                      className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-emerald-500/20 disabled:opacity-50"
                    >
                      {verifying ? 'Running Sandbox...' : 'Run Verification ⚡'}
                    </button>
                  </div>

                  <textarea
                    rows={8}
                    value={verifyCode}
                    onChange={(e) => setVerifyCode(e.target.value)}
                    placeholder="Paste reference solution code here..."
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-emerald-500"
                  />

                  {verifyResult && (
                    <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono font-bold uppercase tracking-wider">
                          Result:{' '}
                          <strong className={verifyResult.all_passed ? 'text-emerald-400' : 'text-red-400'}>
                            {verifyResult.all_passed ? '✓ ALL TESTS PASSED' : `✕ ${verifyResult.passed_count}/${verifyResult.total_count} PASSED`}
                          </strong>
                        </span>
                      </div>

                      <div className="space-y-2 max-h-60 overflow-y-auto">
                        {verifyResult.results?.map((res, i) => (
                          <div
                            key={i}
                            className={`p-3 rounded-lg border text-xs font-mono flex items-center justify-between ${res.status === 'ACCEPTED'
                                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                                : 'bg-red-500/10 border-red-500/30 text-red-300'
                              }`}
                          >
                            <span>Case #{res.order} ({res.is_sample ? 'Sample' : 'Hidden'})</span>
                            <span>{res.status} ({res.execution_time}s)</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-5 border-t border-slate-800 flex items-center justify-end gap-3 bg-slate-900/40">
              <button
                type="button"
                onClick={() => setModalOpen(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSaveProblem}
                disabled={saving}
                className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 disabled:opacity-50"
              >
                {saving ? 'Saving...' : editingProblem ? 'Update Challenge' : 'Create Challenge'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

