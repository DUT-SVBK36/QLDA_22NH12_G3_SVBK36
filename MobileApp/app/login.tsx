import React, { useState } from 'react';
import { StyleSheet, TextInput, View, Text, TouchableOpacity, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Link } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      {/* Language selector button */}
      <View style={styles.languageContainer}>
        <Pressable style={styles.languageButton}>
          <Ionicons name="globe-outline" size={24} color="white" />
        </Pressable>
      </View>

      {/* Login form */}
      <View style={styles.formContainer}>
        <Text style={styles.title}>Login</Text>
        <Text style={styles.subtitle}>Please sign in to continue</Text>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Username:</Text>
          <TextInput
            style={styles.input}
            value={username}
            onChangeText={setUsername}
            placeholder="Placeholder"
            placeholderTextColor="rgba(255, 255, 255, 0.5)"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Password:</Text>
          <TextInput
            style={styles.input}
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            placeholder="Placeholder"
            placeholderTextColor="rgba(255, 255, 255, 0.5)"
          />
        </View>

        <TouchableOpacity style={styles.loginButton}>
          <Text style={styles.loginButtonText}>Login</Text>
        </TouchableOpacity>
      </View>

      {/* Register link */}
      <View style={styles.registerContainer}>
        <Text style={styles.registerText}>Don't have any account? </Text>
        <Link href="/(tabs)" asChild>
          <TouchableOpacity>
            <Text style={styles.registerLink}>Register</Text>
          </TouchableOpacity>
        </Link>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#282c4d', // Dark blue/purple color from the image
    padding: 16,
  },
  languageContainer: {
    position: 'absolute',
    top: 50,
    right: 20,
    zIndex: 1,
  },
  languageButton: {
    padding: 8,
  },
  formContainer: {
    flex: 1,
    justifyContent: 'center',
    width: '100%',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    marginBottom: 40,
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    color: 'white',
    marginBottom: 8,
  },
  input: {
    borderBottomWidth: 1,
    borderBottomColor: 'white',
    paddingVertical: 8,
    color: 'white',
    fontSize: 16,
  },
  loginButton: {
    backgroundColor: '#a5a6f6', // Light purple from the image
    borderRadius: 8,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 20,
  },
  loginButtonText: {
    color: '#282c4d', // Dark background color for contrast
    fontSize: 16,
    fontWeight: 'bold',
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 40,
  },
  registerText: {
    color: 'white',
  },
  registerLink: {
    color: '#a5a6f6', // Light purple from the image
    fontWeight: 'bold',
  },
});