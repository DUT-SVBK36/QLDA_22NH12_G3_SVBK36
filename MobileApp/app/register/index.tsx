import React, { useState } from 'react';
import { View, Text, TouchableOpacity, useColorScheme, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import CustomInput from '@/components/ui/CustomInput';
import styles from './styles.css';
import CustomButton from '@/components/ui/CustomButton';
import { Fonts } from '@/shared/SharedStyles';
import KeyboardAwareSafeScreen from '@/components/layout/KeyboardAwareSafeScreen';
import { Colors } from '@/constants/Colors';
import { AuthService } from '@/services/auth';

interface RegisterregisterForm {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export default function Register() {
  const [registerForm, setRegisterForm] = useState<RegisterregisterForm>({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const colorScheme = useColorScheme();
  const textColor = Colors[colorScheme ?? "light"].text;
  const tintColor = Colors[colorScheme ?? "light"].tint;

  const validateForm = (): boolean => {
    if (!registerForm.username.trim()) {
      setError('Please enter a username');
      return false;
    }

    if (!registerForm.email.trim() || !registerForm.email.includes('@')) {
      setError('Please enter a valid email');
      return false;
    }

    if (!registerForm.password.trim() || registerForm.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return false;
    }

    if (registerForm.password !== registerForm.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    setError('');
    return true;
  };

  const handleInputChange = (field: keyof RegisterregisterForm, value: string) => {
    setRegisterForm(prev => ({ ...prev, [field]: value }));
  };

  const handleRegister = async (): Promise<void> => {
    if (!validateForm()) return;

    try {
      setLoading(true);
      const success = await AuthService.register(
        registerForm.username,
        registerForm.email,
        registerForm.password
      );

      if (success) {
        Alert.alert('Success', 'Registration successful');
        router.replace('/login');
      } else {
        setError('Registration failed. Please try again.');
      }
    } catch (error) {
      setError('An error occurred during registration');
    } finally {
      setLoading(false);
    }
  };
  return (
    <KeyboardAwareSafeScreen
      statusBarStyle="light"
      contentContainerStyle={styles.contentContainer}
    >
      {/* Back button */}
      <View style={styles.backContainer}>
        <TouchableOpacity 
          style={styles.backButton} 
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color="white" />
        </TouchableOpacity>
      </View>
        
      {/* Register form */}
      <View style={styles.formContainer}>
        <Text style={[
            styles.title, 
            Fonts.h1,
            {color: textColor}
            ]}>Register</Text>
        <Text style={[styles.subtitle, Fonts.bodySmall, {color: textColor}]}>Start your session after a few steps</Text>

        <CustomInput 
          label="Username"
          value={registerForm.username}
          onChangeText={e => setRegisterForm({...registerForm, username: e})}
          placeholder="Enter your username"
        />
        <CustomInput 
          label="Email"
          value={registerForm.email}
          onChangeText={e => setRegisterForm({...registerForm, email: e})}
          placeholder="Enter your email"
        />
        <CustomInput 
          label="Password"
          value={registerForm.password}
          onChangeText={e => setRegisterForm({...registerForm, password: e})}
          placeholder="Enter your password"
          isPassword
        />
        <CustomInput 
          label="Confirm"
          value={registerForm.confirmPassword}
          onChangeText={e => setRegisterForm({...registerForm, confirmPassword: e})}
          placeholder="Confirm your password"
          isPassword
        />

        <CustomButton
          label={loading ? 'Registering...' : 'Register'}
          onPress={handleRegister}
          variant='default'
        />
      </View>

      {/* Login link */}
      <View style={styles.registerContainer}>
        <Text style={{
            ...styles.registerText
            , color: textColor
            }}>Already owned an account? </Text>
        <TouchableOpacity onPress={() => router.push('/login')}>
          <Text style={
            {
                ...styles.registerLink, 
                color: tintColor
            }
            }>Sign in</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAwareSafeScreen>
  );
}