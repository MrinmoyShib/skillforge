import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const leaderboardService = {
  /**
   * Retrieves global developer rankings with sort and pagination options.
   * @param {Object} params - { sort: 'xp'|'solved', limit: number, offset: number }
   */
  async getLeaderboard(params = {}) {
    return await axiosClient.get(ENDPOINTS.LEADERBOARD, { params });
  },
};

