import React, { useEffect, useState } from 'react';
import adminService from '../../services/api/adminService';
import Spinner from '../../components/feedback/Spinner';

export default function AdminProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [modalTab, setModalTab] = useState('general'); // 'general' | 'milestones'
  const [saving, setSaving] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    slug: '',
    language: 'python',
    difficulty: 'medium',
    challenge_level: 2,
    short_description: '',
    description: '',
    xp_reward: 150,
    estimated_minutes: 60,
    order: 1,
    is_published: true,
    milestones: [
      {
        order: 1,
        title: 'Initial Architecture Setup',
        description: 'Set up the core data structure.',
        starter_code: '',
        test_harness_code: '',
        xp_reward: 50,
        hints: []
      }
    ]
  });

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data = await adminService.getProjects();
      setProjects(data.results || data);
      setError(null);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load guided projects.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleOpenCreate = () => {
    setEditingProject(null);
    setFormData({
      title: '',
      slug: '',
      language: 'python',
      difficulty: 'medium',
      challenge_level: 2,
      short_description: '',
      description: '',
      xp_reward: 150,
      estimated_minutes: 60,
      order: projects.length + 1,
      is_published: true,
      milestones: [
        {
          order: 1,
          title: 'Initial Architecture Setup',
          description: 'Set up the core data structure.',
          starter_code: '',
          test_harness_code: '',
          xp_reward: 50,
          hints: []
        }
      ]
    });
    setModalTab('general');
    setModalOpen(true);
  };

  const handleOpenEdit = async (project) => {
    try {
      setLoading(true);
      const detail = await adminService.getProject(project.id);
      setEditingProject(detail);
      setFormData({
        title: detail.title,
        slug: detail.slug,
        language: detail.language,
        difficulty: detail.difficulty,
        challenge_level: detail.challenge_level,
        short_description: detail.short_description || '',
        description: detail.description || '',
        xp_reward: detail.xp_reward,
        estimated_minutes: detail.estimated_minutes,
        order: detail.order,
        is_published: detail.is_published,
        milestones: detail.milestones?.length ? detail.milestones : [
          {
            order: 1,
            title: 'Milestone 1',
            description: '',
            starter_code: '',
            test_harness_code: '',
            xp_reward: 50,
            hints: []
          }
        ]
      });
      setModalTab('general');
      setModalOpen(true);
    } catch (err) {
      alert('Failed to load project details: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePublish = async (project) => {
    try {
      const updated = await adminService.updateProject(project.id, {
        is_published: !project.is_published
      });
      setProjects(projects.map(p => p.id === project.id ? { ...p, is_published: updated.is_published } : p));
    } catch (err) {
      alert('Failed to update project: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const handleDeleteProject = async (project) => {
    if (!window.confirm(`Are you sure you want to permanently delete project "${project.title}"?`)) {
      return;
    }
    try {
      await adminService.deleteProject(project.id);
      setProjects(projects.filter(p => p.id !== project.id));
    } catch (err) {
      alert('Failed to delete project: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const handleSaveProject = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      if (editingProject) {
        await adminService.updateProject(editingProject.id, formData);
      } else {
        await adminService.createProject(formData);
      }
      setModalOpen(false);
      fetchProjects();
    } catch (err) {
      alert('Failed to save project: ' + JSON.stringify(err?.response?.data || err.message));
    } finally {
      setSaving(false);
    }
  };

  const addMilestone = () => {
    setFormData({
      ...formData,
      milestones: [
        ...formData.milestones,
        {
          order: formData.milestones.length + 1,
          title: `Milestone ${formData.milestones.length + 1}`,
          description: '',
          starter_code: '',
          test_harness_code: '',
          xp_reward: 50,
          hints: []
        }
      ]
    });
  };

  const removeMilestone = (index) => {
    setFormData({
      ...formData,
      milestones: formData.milestones.filter((_, i) => i !== index)
    });
  };

  const updateMilestone = (index, field, value) => {
    const updated = [...formData.milestones];
    updated[index][field] = value;
    setFormData({ ...formData, milestones: updated });
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#131b2e] p-6 rounded-2xl border border-cyan-500/20 shadow-xl">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
            <span>Guided Projects Curator</span>
            <span className="text-xs font-mono font-normal text-indigo-400 px-2.5 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/30">
              {projects.length} Engineering Labs
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Build hands-on, multi-step engineering projects with automated verification test harnesses.
          </p>
        </div>
        <button
          onClick={handleOpenCreate}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-sm font-bold shadow-lg shadow-cyan-500/20 transition-all self-start sm:self-auto"
        >
          <span>+ Create Project</span>
        </button>
      </div>

      {/* Projects Grid */}
      {loading && projects.length === 0 ? (
        <div className="p-12 flex justify-center">
          <Spinner size="lg" />
        </div>
      ) : projects.length === 0 ? (
        <div className="p-12 text-center text-slate-400 font-mono text-sm bg-[#131b2e] rounded-2xl border border-slate-800">
          No guided projects configured yet. Click "+ Create Project" to author your first engineering lab.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.id}
              className="bg-[#131b2e] border border-slate-800 hover:border-cyan-500/40 rounded-2xl p-6 flex flex-col justify-between transition-all group shadow-lg"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="font-mono text-xs px-2.5 py-0.5 rounded-md bg-slate-900 border border-slate-700 text-cyan-300 font-semibold">
                    {project.language === 'python' ? '🐍 Python' : project.language === 'javascript' ? '🟨 JavaScript' : '⚡ C++'}
                  </span>
                  <button
                    onClick={() => handleTogglePublish(project)}
                    className={`px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold transition-all ${project.is_published
                        ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40'
                        : 'bg-slate-800 text-slate-400 border border-slate-700'
                      }`}
                  >
                    {project.is_published ? '● Live' : '○ Draft'}
                  </button>
                </div>

                <h3 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
                  {project.title}
                </h3>
                <p className="text-xs text-slate-400 mt-2 line-clamp-2">
                  {project.short_description || 'No description provided.'}
                </p>

                <div className="mt-4 pt-4 border-t border-slate-800/80 grid grid-cols-3 gap-2 text-center font-mono">
                  <div className="bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                    <span className="block text-[10px] text-slate-400 uppercase">Milestones</span>
                    <span className="text-xs font-bold text-white">{project.milestones_count || 0}</span>
                  </div>
                  <div className="bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                    <span className="block text-[10px] text-slate-400 uppercase">XP Reward</span>
                    <span className="text-xs font-bold text-indigo-400">+{project.xp_reward}</span>
                  </div>
                  <div className="bg-slate-900/60 p-2 rounded-lg border border-slate-800">
                    <span className="block text-[10px] text-slate-400 uppercase">Difficulty</span>
                    <span className="text-xs font-bold text-emerald-400 capitalize">{project.difficulty}</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between gap-2">
                <button
                  onClick={() => handleOpenEdit(project)}
                  className="flex-1 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
                >
                  Edit Milestones & Code
                </button>
                <button
                  onClick={() => handleDeleteProject(project)}
                  className="px-3 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-semibold border border-red-500/30 transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create / Edit Project Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
          <div className="bg-[#131b2e] border border-cyan-500/30 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col shadow-2xl">
            {/* Header */}
            <div className="p-5 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-white">
                  {editingProject ? `Edit Project: ${editingProject.title}` : 'Create Guided Project'}
                </h2>
                <p className="text-xs text-slate-400">Configure engineering specifications and verification milestones</p>
              </div>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-white p-2 text-xl">
                ✕
              </button>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-slate-800 px-5 gap-4 text-xs font-mono bg-slate-900/60">
              <button
                onClick={() => setModalTab('general')}
                className={`py-3 border-b-2 font-bold transition-all ${modalTab === 'general' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
              >
                1. Project Brief & Parameters
              </button>
              <button
                onClick={() => setModalTab('milestones')}
                className={`py-3 border-b-2 font-bold transition-all ${modalTab === 'milestones' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
              >
                2. Milestones & Test Harnesses ({formData.milestones.length})
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {modalTab === 'general' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Project Title *</label>
                    <input
                      type="text"
                      required
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      placeholder="e.g. Build an Asynchronous Redis Clone"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Slug</label>
                    <input
                      type="text"
                      value={formData.slug}
                      onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                      placeholder="e.g. async-redis-clone"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Language Track</label>
                    <select
                      value={formData.language}
                      onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    >
                      <option value="python">Python</option>
                      <option value="javascript">JavaScript</option>
                      <option value="cpp">C++</option>
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
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Completion Bonus XP</label>
                    <input
                      type="number"
                      value={formData.xp_reward}
                      onChange={(e) => setFormData({ ...formData, xp_reward: parseInt(e.target.value) || 150 })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div className="col-span-2">
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Short Description</label>
                    <input
                      type="text"
                      value={formData.short_description}
                      onChange={(e) => setFormData({ ...formData, short_description: e.target.value })}
                      placeholder="Brief overview displayed on the project card..."
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div className="col-span-2">
                    <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Full Project Specification (Markdown)</label>
                    <textarea
                      rows={6}
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Detailed architectural brief, goals, background, and deliverables..."
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white font-mono focus:outline-none focus:border-cyan-500"
                    />
                  </div>

                  <div className="col-span-2 flex items-center gap-3">
                    <input
                      type="checkbox"
                      id="project_published"
                      checked={formData.is_published}
                      onChange={(e) => setFormData({ ...formData, is_published: e.target.checked })}
                      className="w-4 h-4 rounded text-cyan-600 bg-slate-900 border-slate-700"
                    />
                    <label htmlFor="project_published" className="text-sm text-white font-medium">
                      Publish project immediately
                    </label>
                  </div>
                </div>
              )}

              {modalTab === 'milestones' && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-slate-400">
                      Each milestone represents a verified checkpoint executed inside the sandbox.
                    </p>
                    <button
                      type="button"
                      onClick={addMilestone}
                      className="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 text-xs font-semibold"
                    >
                      + Add Milestone
                    </button>
                  </div>

                  {formData.milestones.map((m, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono font-bold text-white">
                          Milestone #{m.order}: {m.title || 'Untitled'}
                        </span>
                        {formData.milestones.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removeMilestone(idx)}
                            className="text-red-400 hover:text-red-300 text-xs font-mono"
                          >
                            Remove
                          </button>
                        )}
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div className="sm:col-span-2">
                          <label className="block text-[11px] font-mono text-slate-400 mb-1">Title</label>
                          <input
                            type="text"
                            value={m.title}
                            onChange={(e) => updateMilestone(idx, 'title', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-cyan-500"
                          />
                        </div>
                        <div>
                          <label className="block text-[11px] font-mono text-slate-400 mb-1">XP Reward</label>
                          <input
                            type="number"
                            value={m.xp_reward}
                            onChange={(e) => updateMilestone(idx, 'xp_reward', parseInt(e.target.value) || 50)}
                            className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-cyan-500"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-[11px] font-mono text-slate-400 mb-1">Milestone Description & Requirements</label>
                        <textarea
                          rows={3}
                          value={m.description}
                          onChange={(e) => updateMilestone(idx, 'description', e.target.value)}
                          className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
                        />
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div>
                          <label className="block text-[11px] font-mono text-slate-400 mb-1">Starter Code Skeleton</label>
                          <textarea
                            rows={4}
                            value={m.starter_code}
                            onChange={(e) => updateMilestone(idx, 'starter_code', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
                          />
                        </div>
                        <div>
                          <label className="block text-[11px] font-mono text-slate-400 mb-1">Test Harness Verification Code</label>
                          <textarea
                            rows={4}
                            value={m.test_harness_code}
                            onChange={(e) => updateMilestone(idx, 'test_harness_code', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white font-mono focus:outline-none focus:border-cyan-500"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
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
                onClick={handleSaveProject}
                disabled={saving}
                className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 disabled:opacity-50"
              >
                {saving ? 'Saving...' : editingProject ? 'Update Project' : 'Create Project'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

