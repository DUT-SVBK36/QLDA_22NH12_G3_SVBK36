import React, { useState } from 'react';
import { View, Text, TouchableOpacity, useColorScheme } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import CustomInput from '@/components/ui/CustomInput';
import styles from './styles.css';
import CustomButton from '@/components/ui/CustomButton';
import { Fonts } from '@/shared/SharedStyles';
import KeyboardAwareSafeScreen from '@/components/layout/KeyboardAwareSafeScreen';
import { Colors } from '@/constants/Colors';


export default function Register() {
  const [registerForm, setRegisterForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const colorScheme = useColorScheme();
  const textColor = Colors[colorScheme ?? "light"].text;
  const tintColor = Colors[colorScheme ?? "light"].tint;
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
          label="Register"
          onPress={() => alert('register')}
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