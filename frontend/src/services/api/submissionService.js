import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const submissionService = {
  createSubmission: async ({ problem_id, source_code, language = 'cpp', is_sample_run = false }) => {
    return await axiosClient.post(ENDPOINTS.SUBMISSIONS, {
      problem_id,
      source_code,
      language,
      is_sample_run,
    });
  },

  getSubmission: async (id) => {
    return await axiosClient.get(`${ENDPOINTS.SUBMISSIONS}${id}/`);
  },

  getSubmissionsForProblem: async (problem_id) => {
    return await axiosClient.get(ENDPOINTS.SUBMISSIONS, {
      params: { problem_id },
    });
  },
};

