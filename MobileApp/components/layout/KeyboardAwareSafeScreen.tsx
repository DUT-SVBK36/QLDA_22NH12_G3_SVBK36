import React from 'react';
import { StyleSheet, StyleProp, ViewStyle, KeyboardAvoidingView, Platform, ScrollView, ImageBackground } from 'react-native';
import { Edge } from 'react-native-safe-area-context';
import SafeScreen from './SafeScreen';
import SharedAssets from '@/shared/SharedAssets';

interface KeyboardAwareSafeScreenProps {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  contentContainerStyle?: StyleProp<ViewStyle>;
  backgroundColor?: string;
  statusBarStyle?: 'auto' | 'inverted' | 'light' | 'dark';
  edges?: Edge[];
  behavior?: 'padding' | 'height' | 'position';
  keyboardShouldPersistTaps?: 'always' | 'never' | 'handled';
}

export default function KeyboardAwareSafeScreen({
  children,
  style,
  contentContainerStyle,
  backgroundColor,
  statusBarStyle,
  edges,
  behavior = Platform.OS === 'ios' ? 'padding' : 'height',
  keyboardShouldPersistTaps = 'handled',
}: KeyboardAwareSafeScreenProps) {
  return (


    <>
    <SafeScreen
      style={style}
      backgroundColor={backgroundColor}
      statusBarStyle={statusBarStyle}
      edges={edges}
    >
      <KeyboardAvoidingView 
        style={styles.keyboardAvoid}
        behavior={behavior}
        enabled
      >
        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={[styles.contentContainer, contentContainerStyle]}
          keyboardShouldPersistTaps={keyboardShouldPersistTaps}
          showsVerticalScrollIndicator={false}
        >
          {children}
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeScreen>
    
    </>
  );
}

const styles = StyleSheet.create({
  keyboardAvoid: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    flexGrow: 1,
  },
});
