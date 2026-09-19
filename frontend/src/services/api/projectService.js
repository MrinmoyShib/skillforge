import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const projectService = {
  getProjects: async (params = {}) => {
    return await axiosClient.get(ENDPOINTS.PROJECTS, { params });
  },

  getProjectBySlug: async (slug) => {
    return await axiosClient.get(`${ENDPOINTS.PROJECTS}${slug}/`);
  },

  startProject: async (slug) => {
    return await axiosClient.post(`${ENDPOINTS.PROJECTS}${slug}/start/`);
  },

  verifyMilestone: async (slug, milestoneId, sourceCode) => {
    return await axiosClient.post(
      `${ENDPOINTS.PROJECTS}${slug}/milestones/${milestoneId}/verify/`,
      { source_code: sourceCode }
    );
  },
};

