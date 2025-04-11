import React, { useState } from 'react';
import { View, Text, TouchableOpacity, useColorScheme } from 'react-native';
import { router } from 'expo-router';
import CustomInput from '@/components/ui/CustomInput';
import styles from './styles.css';
import CustomButton from '@/components/ui/CustomButton';
import { Fonts } from '@/shared/SharedStyles';
import KeyboardAwareSafeScreen from '@/components/layout/KeyboardAwareSafeScreen';
import { Colors } from '@/constants/Colors';
import { AuthService } from '@/services/auth';

interface LoginFormData {
  username: string;
  password: string;
}

export default function LoginScreen() {
  const [formData, setFormData] = useState<LoginFormData>({
    username: '',
    password: ''
  });
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const colorScheme = useColorScheme();
  const textColor = Colors[colorScheme ?? "light"].text;
  const tintColor = Colors[colorScheme ?? "light"].tint;

  const validateForm = (): boolean => {
    if (!formData.username.trim()) {
      setError('Please enter your username');
      return false;
    }
    if (!formData.password.trim()) {
      setError('Please enter your password');
      return false;
    }
    setError('');
    return true;
  };

  const handleLogin = async (): Promise<void> => {
    if (!validateForm()) return;

    try {
      setLoading(true);
      const success = await AuthService.login(formData.username, formData.password);
      if (success) {
        router.replace('/(main)');
      } else {
        setError('Invalid username or password');
      }
    } catch (error) {
      setError('An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof LoginFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <KeyboardAwareSafeScreen 
      statusBarStyle="light"
      contentContainerStyle={styles.contentContainer}
    >
      <View style={styles.formContainer}>
        <Text style={[
          styles.title, 
          Fonts.h1,
          {color: textColor}
        ]}>
          Welcome Back
        </Text>
        <Text style={[
          styles.subtitle,
          Fonts.body,
          {color: textColor}
        ]}>
          Sign in to continue
        </Text>

        {error && (
          <Text style={{ 
            color: 'red', 
            marginBottom: 16,
            textAlign: 'center'
          }}>
            {error}
          </Text>
        )}

        <CustomInput
          value={formData.username}
          onChangeText={(text) => handleInputChange('username', text)}
          placeholder="Username"
          label="Username"
        />

        <CustomInput
        label="Password"
          value={formData.password}
          onChangeText={(text) => handleInputChange('password', text)}
          placeholder="Password"
          isPassword
        />

        <CustomButton
          label={loading ? 'Signing in...' : 'Sign In'}
          onPress={handleLogin}
          variant='default'
        />
      </View>
        <View style={styles.registerContainer}>
          <Text style={[styles.registerText, Fonts.caption, {color: textColor}]}>
            Don't have an account?{' '}
          </Text>
          <TouchableOpacity onPress={() => router.replace('/register')}>
            <Text style={[styles.registerLink, Fonts.caption , {color: tintColor}]}>
              Register
            </Text>
          </TouchableOpacity>
        </View>
    </KeyboardAwareSafeScreen>
  );
}