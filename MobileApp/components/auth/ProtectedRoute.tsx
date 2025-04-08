// components/auth/ProtectedRoute.tsx
import { View } from 'react-native';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'expo-router';

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  if (loading) {
    return <View />;
  }

  if (!isAuthenticated) {
    router.push('/login');
    return <View />;
  }

  return <>{children}</>;
}