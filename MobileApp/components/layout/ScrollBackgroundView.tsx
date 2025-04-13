import React, { ReactNode } from 'react';
import { ScrollView, StyleSheet, StyleProp, ViewStyle, ScrollViewProps, useColorScheme, ImageBackground } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Colors } from '@/constants/Colors';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface ScrollBackgroundViewProps extends ScrollViewProps {
  children: ReactNode;
  contentContainerStyle?: StyleProp<ViewStyle>;
  style?: StyleProp<ViewStyle>;
  useSafeArea?: boolean;
  statusBarStyle?: 'auto' | 'inverted' | 'light' | 'dark';
  customBackground?: any;
}

export default function ScrollBackgroundView({
  children,
  contentContainerStyle,
  style,
  useSafeArea = true,
  statusBarStyle = 'light',
  customBackground,
  ...scrollViewProps
}: ScrollBackgroundViewProps) {
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
    <>
      <StatusBar style={statusBarStyle} />
      <ScrollView
        style={[
          styles.container, 
          { backgroundColor },
          style
        ]}
        contentContainerStyle={[
          safeAreaStyle,
          contentContainerStyle
        ]}
        showsVerticalScrollIndicator={false}
        {...scrollViewProps}
      >
        <ImageBackground source={customBackground} 
              resizeMode='cover'
              style={{
                flex: 1,
                justifyContent: 'center',
                width: '100%',
                height: '100%',
                position: 'absolute',
                ...safeAreaStyle,
              }}/>
        {children}
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});