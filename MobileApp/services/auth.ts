import api from '@/constants/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { jwtDecode } from 'jwt-decode';

interface AuthToken {
  token: string;
  user: any;
  expiration: number;
}

export class AuthService {
  static async getToken(): Promise<string | null> {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      if (!token) return null;
      
      const { token: jwt, expiration } = JSON.parse(token) as AuthToken;
      if (Date.now() >= expiration) {
        await AsyncStorage.removeItem('auth_token');
        await AsyncStorage.removeItem('user');
        return null;
      }
      
      return jwt;
    } catch (error) {
      console.error('Error getting token:', error);
      return null;
    }
  }

  static async getUser(): Promise<any | null> {
    try {
      const user = await AsyncStorage.getItem('user');
      return user ? JSON.parse(user) : null;
    } catch (error) {
      console.error('Error getting user:', error);
      return null;
    }
  }

  static async setAuth(token: string): Promise<void> {
    try {
      // Decode JWT to get user data and expiration
      const decoded = jwtDecode(token) as {
        sub: string;
        exp: number;
      };
  
      // Store token with expiration
      await AsyncStorage.setItem('auth_token', JSON.stringify({ 
        token,
        expiration: decoded.exp * 1000 // Convert to milliseconds
      }));
      
      // Store user data with proper structure
      await AsyncStorage.setItem('user', JSON.stringify({
        id: decoded.sub,
        username: decoded.sub,
        exp: decoded.exp
      }));
    } catch (error) {
      console.error('Error setting auth:', error);
      throw error; // Re-throw error to be handled by caller
    }
  }

  static async removeAuth(): Promise<void> {
    try {
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user');
    } catch (error) {
      console.error('Error removing auth:', error);
    }
  }

  static async login(username: string, password: string): Promise<boolean> {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(api.auth.login, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString()
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Login failed');
      }

      const { access_token: token, user_id } = await response.json();
      await this.setAuth(token);
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }

  static async register(username: string, email: string, password: string): Promise<boolean> {
    try {
      const response = await fetch(api.auth.register, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Registration failed');
      }

      const { is_active } = await response.json();
      if (!is_active) {
        throw new Error('Account is not active');
      }

      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  }

  static async isAuthenticated(): Promise<boolean> {
    return !!await this.getToken();
  }
}