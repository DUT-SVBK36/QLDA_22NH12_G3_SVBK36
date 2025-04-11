import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator } from 'react-native';
import { router, usePathname } from 'expo-router';
import { useAuth } from '@/contexts/AuthContext';
import { BaseColors } from '@/constants/Colors';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAuth();
  const [shouldRender, setShouldRender] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    if (!loading) {
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        router.replace('/login');
      } else {
        // User is authenticated, show content
        setShouldRender(true);
        
        // If we're on login or register pages, redirect to main
        if (pathname.includes('/login') || pathname.includes('/register')) {
          router.replace('/(main)');
        }
      }
    }
  }, [isAuthenticated, loading, pathname]);

  if (loading) {
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

  if (!shouldRender) {
    return null;
  }

  return <>{children}</>;
}