import { Tabs } from 'expo-router';
import React from 'react';
import { Platform } from 'react-native';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Ionicons } from '@expo/vector-icons';


export default function TabLayout() {
  const colorScheme = useColorScheme();
  const iconSize = 24;
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        tabBarInactiveTintColor: Colors[colorScheme ?? 'light'].tabIconDefault,
        headerShown: false,
        tabBarStyle: Platform.select({
          ios: {
            position: 'absolute',
            justifyContent: 'center',
          },
          default: {
            display: 'flex',
            backgroundColor: Colors[colorScheme ?? 'light'].background,
            borderTopWidth: 1,
            borderTopColor: Colors[colorScheme ?? 'light'].icon,
            justifyContent: 'center',
          },
        }),
        tabBarItemStyle: {
          paddingTop: 6,
          justifyContent: 'center',
          alignItems: 'center',
        },
        tabBarLabelStyle: {
          display: 'none',
        },
      }}>
      <Tabs.Screen
        name="index"
        options={{
          tabBarIcon: ({ color }) => <Ionicons size={iconSize} name="home" color={color} />,
        }}
      />
      <Tabs.Screen
        name="detect"
        options={{
          tabBarIcon: ({ color }) => <Ionicons size={iconSize} name="compass" color={color} />,
        }}
      />
      <Tabs.Screen
        name="notifications"
        options={{
          tabBarIcon: ({ color }) => <Ionicons size={iconSize} name="notifications" color={color} />,
        }}
      />
      <Tabs.Screen
        name="usermenu"
        options={{
          tabBarIcon: ({ color }) => <Ionicons size={iconSize} name="menu" color={color} />,
        }}
      />
    </Tabs>
  );
}
