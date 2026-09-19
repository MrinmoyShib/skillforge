import React, { useEffect, useState } from 'react';
import adminService from '../../services/api/adminService';
import Spinner from '../../components/feedback/Spinner';

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [search, setSearch] = useState('');
  const [isStaff, setIsStaff] = useState('');
  const [isActive, setIsActive] = useState('');

  // Selected User for Intel Drawer
  const [selectedUser, setSelectedUser] = useState(null);
  const [intelLoading, setIntelLoading] = useState(false);

  // XP Adjust Modal
  const [xpModalUser, setXpModalUser] = useState(null);
  const [xpDelta, setXpDelta] = useState(100);
  const [xpReason, setXpReason] = useState('Admin manual XP reward');
  const [xpSaving, setXpSaving] = useState(false);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const params = {};
      if (search) params.search = search;
      if (isStaff !== '') params.is_staff = isStaff;
      if (isActive !== '') params.is_active = isActive;

      const data = await adminService.getUsers(params);
      setUsers(data.results || data);
      setError(null);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to fetch developer directory.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [search, isStaff, isActive]);

  const handleInspectUser = async (userId) => {
    try {
      setIntelLoading(true);
      const detail = await adminService.getUser(userId);
      setSelectedUser(detail);
    } catch (err) {
      alert('Failed to load student telemetry: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setIntelLoading(false);
    }
  };

  const handleToggleStaff = async (user) => {
    try {
      const updated = await adminService.updateUser(user.id, {
        is_staff: !user.is_staff
      });
      setUsers(users.map(u => u.id === user.id ? { ...u, is_staff: updated.is_staff } : u));
      if (selectedUser?.id === user.id) {
        setSelectedUser({ ...selectedUser, is_staff: updated.is_staff });
      }
    } catch (err) {
      alert('Failed to update staff status: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const handleToggleActive = async (user) => {
    try {
      const updated = await adminService.updateUser(user.id, {
        is_active: !user.is_active
      });
      setUsers(users.map(u => u.id === user.id ? { ...u, is_active: updated.is_active } : u));
      if (selectedUser?.id === user.id) {
        setSelectedUser({ ...selectedUser, is_active: updated.is_active });
      }
    } catch (err) {
      alert('Failed to toggle active status: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const handleOpenXpModal = (user) => {
    setXpModalUser(user);
    setXpDelta(100);
    setXpReason('Admin manual adjustment');
  };

  const handleSaveXp = async (e) => {
    e.preventDefault();
    if (!xpModalUser) return;
    try {
      setXpSaving(true);
      const updated = await adminService.adjustUserXP(xpModalUser.id, {
        xp_delta: parseInt(xpDelta),
        reason: xpReason
      });
      setUsers(users.map(u => u.id === xpModalUser.id ? {
        ...u,
        total_xp: updated.total_xp,
        current_level: updated.current_level,
        level_title: updated.level_title
      } : u));
      if (selectedUser?.id === xpModalUser.id) {
        setSelectedUser(updated);
      }
      setXpModalUser(null);
    } catch (err) {
      alert('Failed to adjust XP: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setXpSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#131b2e] p-6 rounded-2xl border border-cyan-500/20 shadow-xl">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
            <span>Developer Directory</span>
            <span className="text-xs font-mono font-normal text-emerald-400 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30">
              {users.length} Registered Accounts
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Student intelligence, progress tracking, role elevation, and manual XP adjustments.
          </p>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-[#131b2e] p-4 rounded-2xl border border-slate-800">
        <input
          type="text"
          placeholder="Search by username, email, display name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
        />

        <select
          value={isStaff}
          onChange={(e) => setIsStaff(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Roles</option>
          <option value="true">Staff & Admins</option>
          <option value="false">Students</option>
        </select>

        <select
          value={isActive}
          onChange={(e) => setIsActive(e.target.value)}
          className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
        >
          <option value="">All Account Statuses</option>
          <option value="true">Active Only</option>
          <option value="false">Suspended / Inactive</option>
        </select>
      </div>

      {/* Users Table */}
      <div className="bg-[#131b2e] border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        {loading && users.length === 0 ? (
          <div className="p-12 flex justify-center">
            <Spinner size="lg" />
          </div>
        ) : users.length === 0 ? (
          <div className="p-12 text-center text-slate-400 font-mono text-sm">
            No developers found matching the query.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/80 text-xs font-mono uppercase tracking-wider text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3.5">Developer</th>
                  <th className="px-4 py-3.5">Level & Title</th>
                  <th className="px-4 py-3.5">Total XP</th>
                  <th className="px-4 py-3.5">Problems Solved</th>
                  <th className="px-4 py-3.5">Role</th>
                  <th className="px-4 py-3.5">Status</th>
                  <th className="px-5 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-5 py-3.5">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white font-bold flex items-center justify-center text-sm flex-shrink-0">
                          {u.avatar_url ? (
                            <img src={u.avatar_url} alt="" className="w-full h-full rounded-xl object-cover" />
                          ) : (
                            u.username?.[0]?.toUpperCase() || 'U'
                          )}
                        </div>
                        <div>
                          <div className="font-bold text-white flex items-center gap-2">
                            <span>{u.display_name || u.username}</span>
                            {u.display_name && (
                              <span className="text-xs font-mono text-slate-400">@{u.username}</span>
                            )}
                          </div>
                          <div className="text-xs text-slate-400 font-mono">{u.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="font-mono text-xs font-bold text-cyan-300">
                        Level {u.current_level}
                      </div>
                      <div className="text-[11px] text-slate-400">{u.level_title}</div>
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-indigo-300 font-bold">
                      {u.total_xp?.toLocaleString()} XP
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-emerald-400">
                      {u.problems_solved_count} solved
                    </td>
                    <td className="px-4 py-3.5">
                      <button
                        onClick={() => handleToggleStaff(u)}
                        className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold transition-all ${u.is_staff
                            ? 'bg-red-500/20 text-red-400 border border-red-500/40 hover:bg-red-500/30'
                            : 'bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700'
                          }`}
                      >
                        {u.is_staff ? '★ Staff' : 'Student'}
                      </button>
                    </td>
                    <td className="px-4 py-3.5">
                      <button
                        onClick={() => handleToggleActive(u)}
                        className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold transition-all ${u.is_active
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : 'bg-red-500/20 text-red-400 border border-red-500/30'
                          }`}
                      >
                        {u.is_active ? 'Active' : 'Suspended'}
                      </button>
                    </td>
                    <td className="px-5 py-3.5 text-right space-x-2">
                      <button
                        onClick={() => handleInspectUser(u.id)}
                        className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-colors"
                      >
                        Intel
                      </button>
                      <button
                        onClick={() => handleOpenXpModal(u)}
                        className="px-2.5 py-1 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 text-xs font-semibold border border-indigo-500/30 transition-colors"
                      >
                        Adjust XP
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Student Intel Drawer */}
      {selectedUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-end bg-black/80 backdrop-blur-sm">
          <div className="bg-[#131b2e] border-l border-cyan-500/30 w-full max-w-xl h-full flex flex-col shadow-2xl overflow-y-auto p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-indigo-600 text-white font-bold flex items-center justify-center text-lg">
                  {selectedUser.avatar_url ? (
                    <img src={selectedUser.avatar_url} alt="" className="w-full h-full rounded-2xl object-cover" />
                  ) : (
                    selectedUser.username?.[0]?.toUpperCase() || 'U'
                  )}
                </div>
                <div>
                  <h2 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>{selectedUser.display_name || selectedUser.username}</span>
                    {selectedUser.is_staff && (
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/40">
                        Staff
                      </span>
                    )}
                  </h2>
                  <p className="text-xs text-slate-400 font-mono">@{selectedUser.username} • {selectedUser.email}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedUser(null)}
                className="text-slate-400 hover:text-white p-2 text-xl"
              >
                ✕
              </button>
            </div>

            {/* Profile Intel */}
            <div className="grid grid-cols-2 gap-3 font-mono text-xs">
              <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 text-[10px] uppercase">Rank & Level</span>
                <p className="font-bold text-cyan-300 text-sm mt-0.5">Level {selectedUser.current_level}</p>
                <p className="text-slate-400 text-[11px]">{selectedUser.level_title}</p>
              </div>
              <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                <span className="text-slate-400 text-[10px] uppercase">Total XP</span>
                <p className="font-bold text-indigo-400 text-sm mt-0.5">{selectedUser.total_xp?.toLocaleString()} XP</p>
                <p className="text-slate-400 text-[11px]">{selectedUser.streak_days} Day Streak</p>
              </div>
            </div>

            {/* Track Mastery Breakdown */}
            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Track Mastery</h3>
              <div className="grid grid-cols-3 gap-2 text-center font-mono">
                {Object.entries(selectedUser.track_breakdown || {}).map(([track, stats]) => (
                  <div key={track} className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                    <span className="text-xs font-bold text-white capitalize block mb-1">
                      {track === 'python' ? '🐍 Python' : track === 'javascript' ? '🟨 JS' : '⚡ C++'}
                    </span>
                    <span className="text-base font-black text-cyan-300 block">{stats.solved}</span>
                    <span className="text-[10px] text-slate-400 block">{stats.remaining} left</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Enrolled Projects */}
            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Engineering Projects</h3>
              {selectedUser.enrolled_projects?.length === 0 ? (
                <p className="text-xs text-slate-500 font-mono">No guided projects enrolled yet.</p>
              ) : (
                <div className="space-y-2">
                  {selectedUser.enrolled_projects?.map((proj) => (
                    <div key={proj.project_id} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs">
                      <div>
                        <p className="font-bold text-white">{proj.title}</p>
                        <p className="text-[11px] text-slate-400 font-mono">
                          {proj.completed_milestones_count} / {proj.total_milestones_count} milestones
                        </p>
                      </div>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${proj.status === 'COMPLETED' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-cyan-500/20 text-cyan-400'
                        }`}>
                        {proj.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Recent Submissions */}
            <div>
              <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2">Recent Submissions (Last 10)</h3>
              {selectedUser.recent_submissions?.length === 0 ? (
                <p className="text-xs text-slate-500 font-mono">No submissions logged.</p>
              ) : (
                <div className="space-y-1.5 font-mono text-xs">
                  {selectedUser.recent_submissions?.map((s) => (
                    <div key={s.id} className="p-2.5 rounded-lg bg-slate-900 border border-slate-800/80 flex items-center justify-between">
                      <div>
                        <span className="font-semibold text-white">{s.problem_title}</span>
                        <span className="text-slate-500 text-[10px] ml-2">({s.language})</span>
                      </div>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${s.status === 'ACCEPTED' ? 'text-emerald-400 bg-emerald-500/10' : 'text-red-400 bg-red-500/10'
                        }`}>
                        {s.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer Action */}
            <div className="pt-4 border-t border-slate-800">
              <button
                onClick={() => handleOpenXpModal(selectedUser)}
                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-indigo-500/20 transition-all"
              >
                + Adjust Developer XP
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Adjust XP Modal */}
      {xpModalUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
          <div className="bg-[#131b2e] border border-cyan-500/30 rounded-2xl w-full max-w-md p-6 shadow-2xl">
            <h2 className="text-lg font-bold text-white mb-1">
              Adjust Developer XP
            </h2>
            <p className="text-xs text-slate-400 mb-4">
              Updating XP for <span className="text-cyan-400 font-bold">{xpModalUser.username}</span>. Level will be recalculated automatically.
            </p>

            <form onSubmit={handleSaveXp} className="space-y-4">
              <div>
                <label className="block text-xs font-mono uppercase text-slate-400 mb-1">XP Delta (+ to add, - to deduct)</label>
                <input
                  type="number"
                  required
                  value={xpDelta}
                  onChange={(e) => setXpDelta(e.target.value)}
                  placeholder="e.g. 100 or -50"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white font-mono focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="block text-xs font-mono uppercase text-slate-400 mb-1">Audit Reason *</label>
                <input
                  type="text"
                  required
                  value={xpReason}
                  onChange={(e) => setXpReason(e.target.value)}
                  placeholder="e.g. Community challenge winner reward"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setXpModalUser(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={xpSaving}
                  className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:brightness-110 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 disabled:opacity-50"
                >
                  {xpSaving ? 'Applying...' : 'Apply XP Adjustment'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

