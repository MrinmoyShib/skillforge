import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const adminService = {
  // Telemetry & Analytics
  getAnalytics: async () => {
    return await axiosClient.get(ENDPOINTS.ADMIN.ANALYTICS);
  },

  // Problem Studio
  getProblems: async (params = {}) => {
    return await axiosClient.get(ENDPOINTS.ADMIN.PROBLEMS, { params });
  },
  getProblem: async (id) => {
    return await axiosClient.get(`${ENDPOINTS.ADMIN.PROBLEMS}${id}/`);
  },
  createProblem: async (data) => {
    return await axiosClient.post(ENDPOINTS.ADMIN.PROBLEMS, data);
  },
  updateProblem: async (id, data) => {
    return await axiosClient.patch(`${ENDPOINTS.ADMIN.PROBLEMS}${id}/`, data);
  },
  deleteProblem: async (id) => {
    return await axiosClient.delete(`${ENDPOINTS.ADMIN.PROBLEMS}${id}/`);
  },
  verifyProblem: async (id, data) => {
    return await axiosClient.post(`${ENDPOINTS.ADMIN.PROBLEMS}${id}/verify/`, data);
  },

  // Guided Projects
  getProjects: async () => {
    return await axiosClient.get(ENDPOINTS.ADMIN.PROJECTS);
  },
  getProject: async (id) => {
    return await axiosClient.get(`${ENDPOINTS.ADMIN.PROJECTS}${id}/`);
  },
  createProject: async (data) => {
    return await axiosClient.post(ENDPOINTS.ADMIN.PROJECTS, data);
  },
  updateProject: async (id, data) => {
    return await axiosClient.patch(`${ENDPOINTS.ADMIN.PROJECTS}${id}/`, data);
  },
  deleteProject: async (id) => {
    return await axiosClient.delete(`${ENDPOINTS.ADMIN.PROJECTS}${id}/`);
  },
  addMilestone: async (projectId, data) => {
    return await axiosClient.post(`${ENDPOINTS.ADMIN.PROJECTS}${projectId}/milestones/`, data);
  },
  updateMilestone: async (projectId, milestoneId, data) => {
    return await axiosClient.patch(`${ENDPOINTS.ADMIN.PROJECTS}${projectId}/milestones/${milestoneId}/`, data);
  },
  deleteMilestone: async (projectId, milestoneId) => {
    return await axiosClient.delete(`${ENDPOINTS.ADMIN.PROJECTS}${projectId}/milestones/${milestoneId}/`);
  },

  // User Management
  getUsers: async (params = {}) => {
    return await axiosClient.get(ENDPOINTS.ADMIN.USERS, { params });
  },
  getUser: async (id) => {
    return await axiosClient.get(`${ENDPOINTS.ADMIN.USERS}${id}/`);
  },
  updateUser: async (id, data) => {
    return await axiosClient.patch(`${ENDPOINTS.ADMIN.USERS}${id}/`, data);
  },
  adjustUserXP: async (id, data) => {
    return await axiosClient.post(`${ENDPOINTS.ADMIN.USERS}${id}/adjust-xp/`, data);
  },

  // Submissions Audit
  getSubmissions: async (params = {}) => {
    return await axiosClient.get(ENDPOINTS.ADMIN.SUBMISSIONS, { params });
  },
  getSubmission: async (id) => {
    return await axiosClient.get(`${ENDPOINTS.ADMIN.SUBMISSIONS}${id}/`);
  },
  rejudgeSubmission: async (id) => {
    return await axiosClient.post(`${ENDPOINTS.ADMIN.SUBMISSIONS}${id}/rejudge/`);
  },
};

export default adminService;

