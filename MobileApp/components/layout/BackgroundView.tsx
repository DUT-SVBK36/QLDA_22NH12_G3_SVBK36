import React, { ReactNode } from 'react';
import { View, StyleSheet, StyleProp, ViewStyle, useColorScheme, ImageBackground } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Colors } from '@/constants/Colors';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface BackgroundViewProps {
  children: ReactNode;
  style?: StyleProp<ViewStyle>;
  useSafeArea?: boolean;
  statusBarStyle?: 'auto' | 'inverted' | 'light' | 'dark';
  customBackground?: any;
}

export default function BackgroundView({
  children,
  style,
  useSafeArea = true,
  statusBarStyle = 'light',
  customBackground,
}: BackgroundViewProps) {
  const colorScheme = useColorScheme();
  const insets = useSafeAreaInsets();
  
  // Get the background color from the theme or use the custom one if provided
  const backgroundColor = customBackground || Colors[colorScheme ?? 'light'].background;
  
  // Apply safe area padding if enabled
  const safeAreaStyle = useSafeArea ? {
    paddingTop: insets.top,
    paddingBottom: insets.bottom,
    paddingLeft: insets.left,
    paddingRight: insets.right,
  } : {};

  return (
    <View style={[ 
      safeAreaStyle,
      { 
        backgroundColor: customBackground ? 'transparent' : backgroundColor,
        paddingHorizontal: 20,
      },
      style
    ]}>
      
      <ImageBackground source={customBackground} 
      resizeMode='cover'
      style={{
        flex: 1,
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        position: 'absolute',
      }}/>
      <StatusBar style={statusBarStyle} />
      {children}
    </View>
  );
}