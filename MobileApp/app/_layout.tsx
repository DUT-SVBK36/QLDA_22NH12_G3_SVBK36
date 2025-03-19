import React, { useEffect } from 'react';
import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/useColorScheme';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
    'Lexend-Light': require('../assets/fonts/Lexend/Lexend-Light.ttf'),
    'Lexend-Regular': require('../assets/fonts/Lexend/Lexend-Regular.ttf'),
    'Lexend-Medium': require('../assets/fonts/Lexend/Lexend-Medium.ttf'),
    'Lexend-SemiBold': require('../assets/fonts/Lexend/Lexend-SemiBold.ttf'),
    'Lexend-Bold': require('../assets/fonts/Lexend/Lexend-Bold.ttf'),
    // You can also keep the original for backward compatibility
    Lexend: require('../assets/fonts/Lexend/Lexend-Regular.ttf'),
  });

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded) {
    return null;
  }

  return (
      <SafeAreaProvider>
          <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
            <Stack>
              <Stack.Screen name="loading" options={{ headerShown: false }} />
              <Stack.Screen name="(main)" options={{ headerShown: false }} />
              <Stack.Screen name='login/index' options={{ headerShown: false }} />
              <Stack.Screen name='register/index' options={{ headerShown: false }} />
              <Stack.Screen name="+not-found" />
              <Stack.Screen name="test" options={{ headerShown: false }} />
              <Stack.Screen name="language/index" options={{ headerShown: false }} />
            </Stack>
            <StatusBar style="auto" />
          </ThemeProvider>
      </SafeAreaProvider>
  );
}
