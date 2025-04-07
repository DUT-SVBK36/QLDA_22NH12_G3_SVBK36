import AsyncStorage from '@react-native-async-storage/async-storage';

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
        return null;
      }
      
      return jwt;
    } catch (error) {
      console.error('Error getting token:', error);
      return null;
    }
  }

  static async setAuth(token: string, user: any, expiresIn: number = 3600): Promise<void> {
    try {
      const expiration = Date.now() + (expiresIn * 1000);
      await AsyncStorage.setItem('auth_token', JSON.stringify({ token, user, expiration }));
    } catch (error) {
      console.error('Error setting token:', error);
    }
  }

  static async removeAuth(): Promise<void> {
    try {
      await AsyncStorage.removeItem('auth_token');
    } catch (error) {
      console.error('Error removing token:', error);
    }
  }

  static async getUser(): Promise<any | null> {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      if (!token) return null;
      
      const { user, expiration } = JSON.parse(token) as AuthToken;
      if (Date.now() >= expiration) {
        await AsyncStorage.removeItem('auth_token');
        return null;
      }
      
      return user;
    } catch (error) {
      console.error('Error getting user:', error);
      return null;
    }
  }
}