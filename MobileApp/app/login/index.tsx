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

export default function LoginScreen() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const colorScheme = useColorScheme();
  const textColor = Colors[colorScheme ?? "light"].text;
  const tintColor = Colors[colorScheme ?? "light"].tint;

  return (
    <KeyboardAwareSafeScreen 
      statusBarStyle="light"
      contentContainerStyle={styles.contentContainer}
    >
      {/* Language selector button */}
      {/* <View style={styles.languageContainer}>
        <TouchableOpacity style={styles.languageButton}>
          <Ionicons name="globe-outline" size={24} color="white" />
        </TouchableOpacity>
      </View> */}

      {/* Login form */}
      <View style={styles.formContainer}>
        <Text style={[
          styles.title, 
          Fonts.h1,
          {color: textColor}
          ]}>Login</Text>
        <Text style={[styles.subtitle, Fonts.bodySmall, {color: textColor}]}>Please sign in to continue</Text>

        <CustomInput 
          label="Username"
          value={username}
          onChangeText={setUsername}
          placeholder="Enter your username"
        />
        <CustomInput 
          label="Password"
          value={password}
          onChangeText={setPassword}
          placeholder="Enter your password"
          isPassword
        />

        <CustomButton 
          label="Login"
          onPress={() => alert('Login')}
        />
      </View>

      {/* Register link */}
      <View style={styles.registerContainer}>
        <Text style={{

          ...styles.registerText,
          color: textColor

          }}>Don't have any account? </Text>
        <TouchableOpacity onPress={() => router.push('/register')}>
          <Text style={{...styles.registerLink, color: tintColor}}>Register</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAwareSafeScreen>
  );
}