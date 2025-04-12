import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { router, usePathname } from 'expo-router';
import { BaseColors } from '@/constants/Colors';
import { AuthService } from '@/services/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const checkAuth = async () => {
      const authStatus = await AuthService.isAuthenticated();
      setIsAuthenticated(authStatus);

      const isAuthPath = pathname === '/login' || pathname === '/register';
      
      if (authStatus && isAuthPath) {
        router.replace('/(main)');
        return;
      }

      if (!authStatus && !isAuthPath && pathname !== '/') {
        router.replace('/login');
        return;
      }
    };

    checkAuth();
  }, [pathname]);

  if (isAuthenticated === null) {
    return (
      <View style={{ 
        flex: 1, 
        justifyContent: 'center', 
        alignItems: 'center', 
        backgroundColor: BaseColors.dark_pri 
      }}>
        <ActivityIndicator size="large" color={BaseColors.primary} />
      </View>
    );
  }

  return <>{children}</>;
}