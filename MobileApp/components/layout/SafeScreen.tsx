import React from 'react';
import { StyleSheet, StyleProp, ViewStyle, View, useColorScheme, ImageBackground } from 'react-native';
import { SafeAreaView, Edge } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Colors } from '@/constants/Colors';
import SharedAssets from '@/shared/SharedAssets';

interface SafeScreenProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  backgroundColor?: string;
  statusBarStyle?: 'auto' | 'inverted' | 'light' | 'dark';
  edges?: Edge[];
  hasBackground?: boolean;
}

export default function SafeScreen({
  children,
  style,
  backgroundColor,
  statusBarStyle = 'light',
  edges = ['top', 'right', 'bottom', 'left'],
  hasBackground = false,
}: SafeScreenProps) {
  const colorScheme = useColorScheme();
  
  // If no backgroundColor provided, use the theme's background color
  const bgColor = backgroundColor || Colors[colorScheme ?? 'light'].background;

  return (
    <View style={[styles.container, { backgroundColor: bgColor }, style]}>
      {hasBackground && (
         <ImageBackground
            source={SharedAssets.Bg}
            resizeMode="cover"
            style={{
                width: "100%",
                height: "100%",
                position: "absolute",
            }}
          />
      )}
      {/* SafeAreaView handles the safe area insets */}
      <StatusBar style={statusBarStyle} />
      <SafeAreaView style={styles.safeArea} edges={edges}>
        {children}
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    position: 'static',
  },
  safeArea: {
    flex: 1,
  },
});