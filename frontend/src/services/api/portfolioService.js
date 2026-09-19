import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const portfolioService = {
  getPortfolio: async (username) => {
    return await axiosClient.get(`${ENDPOINTS.PORTFOLIO}${username}/`);
  },
};

