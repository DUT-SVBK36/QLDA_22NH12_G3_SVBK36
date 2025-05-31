import { useCallback } from 'react';
import Toast from 'react-native-toast-message';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastOptions {
  type?: ToastType;
  text1?: string;
  text2?: string;
  position?: 'top' | 'bottom';
  visibilityTime?: number;
  autoHide?: boolean;
  topOffset?: number;
  bottomOffset?: number;
  onShow?: () => void;
  onHide?: () => void;
  onPress?: () => void;
}

export interface UseToastReturn {
  showToast: (message: string, options?: ToastOptions) => void;
  showSuccess: (message: string, subtitle?: string, options?: Omit<ToastOptions, 'type'>) => void;
  showError: (message: string, subtitle?: string, options?: Omit<ToastOptions, 'type'>) => void;
  showInfo: (message: string, subtitle?: string, options?: Omit<ToastOptions, 'type'>) => void;
  showWarning: (message: string, subtitle?: string, options?: Omit<ToastOptions, 'type'>) => void;
  hideToast: () => void;
}

/**
 * Custom hook for managing toast messages
 */
export const useToast = (): UseToastReturn => {
  // Generic toast function
  const showToast = useCallback((message: string, options: ToastOptions = {}) => {
    const {
      type = 'info',
      text2,
      position = 'top',
      visibilityTime = 4000,
      autoHide = true,
      topOffset = 60,
      bottomOffset = 40,
      onShow,
      onHide,
      onPress,
    } = options;

    Toast.show({
      type,
      text1: message,
      text2,
      position,
      visibilityTime,
      autoHide,
      topOffset,
      bottomOffset,
      onShow,
      onHide,
      onPress,
    });
  }, []);

  // Success toast
  const showSuccess = useCallback((
    message: string, 
    subtitle?: string, 
    options: Omit<ToastOptions, 'type'> = {}
  ) => {
    showToast(message, {
      ...options,
      type: 'success',
      text2: subtitle,
    });
  }, [showToast]);

  // Error toast
  const showError = useCallback((
    message: string, 
    subtitle?: string, 
    options: Omit<ToastOptions, 'type'> = {}
  ) => {
    showToast(message, {
      ...options,
      type: 'error',
      text2: subtitle,
      visibilityTime: 5000, // Error messages stay longer by default
    });
  }, [showToast]);

  // Info toast
  const showInfo = useCallback((
    message: string, 
    subtitle?: string, 
    options: Omit<ToastOptions, 'type'> = {}
  ) => {
    showToast(message, {
      ...options,
      type: 'info',
      text2: subtitle,
    });
  }, [showToast]);

  // Warning toast
  const showWarning = useCallback((
    message: string, 
    subtitle?: string, 
    options: Omit<ToastOptions, 'type'> = {}
  ) => {
    showToast(message, {
      ...options,
      type: 'warning',
      text2: subtitle,
    });
  }, [showToast]);

  // Hide toast
  const hideToast = useCallback(() => {
    Toast.hide();
  }, []);

  return {
    showToast,
    showSuccess,
    showError,
    showInfo,
    showWarning,
    hideToast,
  };
};

export default useToast;