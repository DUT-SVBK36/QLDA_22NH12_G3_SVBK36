import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthService } from '@/services/auth';

interface AuthContextType {
  user: any | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string, user: any) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const user = await AuthService.getUser();
      const token = await AuthService.getToken();
      setUser(user);
      setToken(token);
    } catch (error) {
      console.error('Error checking auth:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (token: string, user: any) => {
    try {
      await AuthService.setAuth(token, user);
      setUser(user);
      setToken(token);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const logout = async () => {
    try {
      await AuthService.removeAuth();
      setUser(null);
      setToken(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const value = {
    user,
    token,
    isAuthenticated: !!token,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}