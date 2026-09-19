import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const progressService = {
  /**
   * Retrieves overall progress, level, XP milestones, and daily streak.
   */
  async getUserProgress() {
    return await axiosClient.get(ENDPOINTS.PROGRESS);
  },

  /**
   * Retrieves array of problem IDs solved by the authenticated user.
   */
  async getSolvedProblemIds() {
    return await axiosClient.get(`${ENDPOINTS.PROGRESS}problems/`);
  },
};

