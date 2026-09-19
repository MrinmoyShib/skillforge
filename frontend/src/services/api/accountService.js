import axiosClient from './axiosClient';
import { ENDPOINTS } from './endpoints';

export const accountService = {
  updateProfile: async (data) => {
    return await axiosClient.patch(ENDPOINTS.AUTH.ME, data);
  },

  changePassword: async (data) => {
    return await axiosClient.post(ENDPOINTS.AUTH.CHANGE_PASSWORD, data);
  },

  verifyOTP: (data) => {
    return axiosClient.post(ENDPOINTS.AUTH.VERIFY_OTP, data);
  },

  resendOTP: (data) => {
    return axiosClient.post(ENDPOINTS.AUTH.RESEND_OTP, data);
  },

  requestEmailChange: (data) => {
    return axiosClient.post(ENDPOINTS.AUTH.REQUEST_EMAIL_CHANGE, data);
  },

  confirmEmailChange: (data) => {
    return axiosClient.post(ENDPOINTS.AUTH.CONFIRM_EMAIL_CHANGE, data);
  },
};

