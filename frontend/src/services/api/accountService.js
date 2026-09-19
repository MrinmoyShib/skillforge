import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const accountService = {
  updateProfile: async (data) => {
    return await axiosClient.patch(ENDPOINTS.AUTH.ME, data);
  },

  changePassword: async (data) => {
    return await axiosClient.post('/auth/change-password/', data);
  },
};

