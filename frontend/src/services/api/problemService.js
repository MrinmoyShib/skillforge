import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const problemService = {
  getProblems: async (params = {}) => {
    return await axiosClient.get(ENDPOINTS.PROBLEMS, { params });
  },

  getProblemBySlug: async (slug) => {
    return await axiosClient.get(`${ENDPOINTS.PROBLEMS}${slug}/`);
  },

  getCategories: async () => {
    return await axiosClient.get('/categories/');
  },

  getTags: async () => {
    return await axiosClient.get('/tags/');
  },
};

