import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const dashboardService = {
  /**
   * Retrieves aggregated dashboard payload including user stats,
   * category mastery breakdowns, recent submissions, and recommendations.
   */
  async getDashboardData() {
    return await axiosClient.get(ENDPOINTS.DASHBOARD);
  },
};

