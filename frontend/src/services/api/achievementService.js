import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const achievementService = {
  /**
   * Retrieves all platform achievements with unlock status and progress for the current user.
   */
  async getAchievements() {
    return await axiosClient.get(ENDPOINTS.ACHIEVEMENTS);
  },
};

