import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axiosClient from '../services/api/axiosClient';
import { ENDPOINTS } from '../services/api/endpoints';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const initAuth = useCallback(async () => {
    try {
      await axiosClient.get(ENDPOINTS.AUTH.CSRF);
      const data = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(data);
    } catch {
      setUser(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  const login = async (credentials) => {
    const res = await axiosClient.post(ENDPOINTS.AUTH.LOGIN, credentials);
    if (res?.user) {
      setUser(res.user);
    } else {
      const data = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(data);
    }
    return res;
  };

  const logout = async () => {
    try {
      await axiosClient.post(ENDPOINTS.AUTH.LOGOUT);
    } finally {
      setUser(false);
    }
  };

  const register = async (data) => {
    const res = await axiosClient.post(ENDPOINTS.AUTH.REGISTER, data);
    if (res?.user) {
      setUser(res.user);
    } else {
      const meData = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(meData);
    }
    return res;
  };

  const refreshUser = async () => {
    try {
      const data = await axiosClient.get(ENDPOINTS.AUTH.ME);
      setUser(data);
      return data;
    } catch {
      setUser(false);
      return null;
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
