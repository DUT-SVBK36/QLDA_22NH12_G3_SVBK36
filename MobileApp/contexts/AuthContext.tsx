import React, { createContext, useContext, useEffect, useState } from 'react';
import { AuthService } from '@/services/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authenticated = await AuthService.isAuthenticated();
        setIsAuthenticated(authenticated);
        
        if (authenticated) {
          const userData = await AuthService.getUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('Auth status check error:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (username: string, password: string) => {
    const success = await AuthService.login(username, password);
    if (success) {
      const userData = await AuthService.getUser();
      setUser(userData);
      setIsAuthenticated(true);
      console.log('User logged in:', userData);
    }
    return success;
  };

  const register = async (username: string, email: string, password: string) => {
    const success = await AuthService.register(username, email, password);
    if (success) {
      const userData = await AuthService.getUser();
      setUser(userData);
      setIsAuthenticated(true);
    }
    return success;
  };

  const logout = async () => {
    await AuthService.removeAuth();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
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