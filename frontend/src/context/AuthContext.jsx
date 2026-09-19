import { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import axiosClient from '../services/api/axiosClient';
import { ENDPOINTS } from '../services/api/endpoints';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const initAuth = useCallback(async () => {
    setIsLoading(true);
    try {
      await axiosClient.get(ENDPOINTS.AUTH.CSRF);
      const data = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  const login = useCallback(async (credentials) => {
    const res = await axiosClient.post(ENDPOINTS.AUTH.LOGIN, credentials);
    if (res?.user) {
      setUser(res.user);
    } else {
      const data = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(data);
    }
    return res;
  }, []);

  const logout = useCallback(async () => {
    try {
      await axiosClient.post(ENDPOINTS.AUTH.LOGOUT);
    } finally {
      setUser(null);
    }
  }, []);

  const register = useCallback(async (data) => {
    const res = await axiosClient.post(ENDPOINTS.AUTH.REGISTER, data);
    if (res?.user) {
      setUser(res.user);
    } else if (!res?.otp_required) {
      try {
        const meData = await axiosClient.get(ENDPOINTS.AUTH.ME);
        setUser(meData);
      } catch {
        // Unverified user or pending OTP
      }
    }
    return res;
  }, []);

  const verifyOTP = useCallback(async ({ email, otp }) => {
    const res = await axiosClient.post(ENDPOINTS.AUTH.VERIFY_OTP, { email, otp });
    if (res?.user) {
      setUser(res.user);
    } else {
      const meData = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(meData);
    }
    return res;
  }, []);

  const resendOTP = useCallback(async ({ email }) => {
    return await axiosClient.post(ENDPOINTS.AUTH.RESEND_OTP, { email });
  }, []);

  const refreshUser = useCallback(async () => {
    try {
      const data = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(data);
      return data;
    } catch {
      setUser(null);
      return null;
    }
  }, []);

  const contextValue = useMemo(() => ({
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
    register,
    verifyOTP,
    resendOTP,
    refreshUser
  }), [user, isLoading, login, logout, register, verifyOTP, resendOTP, refreshUser]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
