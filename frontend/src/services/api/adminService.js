import axiosClient from './axiosClient';

export const adminService = {
  // Telemetry & Analytics
  getAnalytics: async () => {
    return await axiosClient.get('/admin/analytics/');
  },

  // Problem Studio
  getProblems: async (params = {}) => {
    return await axiosClient.get('/admin/problems/', { params });
  },
  getProblem: async (id) => {
    return await axiosClient.get(`/admin/problems/${id}/`);
  },
  createProblem: async (data) => {
    return await axiosClient.post('/admin/problems/', data);
  },
  updateProblem: async (id, data) => {
    return await axiosClient.patch(`/admin/problems/${id}/`, data);
  },
  deleteProblem: async (id) => {
    return await axiosClient.delete(`/admin/problems/${id}/`);
  },
  verifyProblem: async (id, data) => {
    return await axiosClient.post(`/admin/problems/${id}/verify/`, data);
  },

  // Guided Projects
  getProjects: async () => {
    return await axiosClient.get('/admin/projects/');
  },
  getProject: async (id) => {
    return await axiosClient.get(`/admin/projects/${id}/`);
  },
  createProject: async (data) => {
    return await axiosClient.post('/admin/projects/', data);
  },
  updateProject: async (id, data) => {
    return await axiosClient.patch(`/admin/projects/${id}/`, data);
  },
  deleteProject: async (id) => {
    return await axiosClient.delete(`/admin/projects/${id}/`);
  },
  addMilestone: async (projectId, data) => {
    return await axiosClient.post(`/admin/projects/${projectId}/milestones/`, data);
  },
  updateMilestone: async (projectId, milestoneId, data) => {
    return await axiosClient.patch(`/admin/projects/${projectId}/milestones/${milestoneId}/`, data);
  },
  deleteMilestone: async (projectId, milestoneId) => {
    return await axiosClient.delete(`/admin/projects/${projectId}/milestones/${milestoneId}/`);
  },

  // User Management
  getUsers: async (params = {}) => {
    return await axiosClient.get('/admin/users/', { params });
  },
  getUser: async (id) => {
    return await axiosClient.get(`/admin/users/${id}/`);
  },
  updateUser: async (id, data) => {
    return await axiosClient.patch(`/admin/users/${id}/`, data);
  },
  adjustUserXP: async (id, data) => {
    return await axiosClient.post(`/admin/users/${id}/adjust-xp/`, data);
  },

  // Submissions Audit
  getSubmissions: async (params = {}) => {
    return await axiosClient.get('/admin/submissions/', { params });
  },
  getSubmission: async (id) => {
    return await axiosClient.get(`/admin/submissions/${id}/`);
  },
  rejudgeSubmission: async (id) => {
    return await axiosClient.post(`/admin/submissions/${id}/rejudge/`);
  },
};

export default adminService;

