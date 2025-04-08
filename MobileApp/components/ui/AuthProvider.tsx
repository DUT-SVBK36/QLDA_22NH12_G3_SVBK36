// components/ui/AuthProvider.tsx
import React from 'react';
import { AuthProvider as AuthContextProvider } from '@/contexts/AuthContext';

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <AuthContextProvider>
      {children}
    </AuthContextProvider>
  );
}