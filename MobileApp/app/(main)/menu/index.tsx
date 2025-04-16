import React, { useEffect, useState } from "react";
import { View, StyleSheet, Image, ScrollView, Text } from "react-native";
import { useColorScheme } from "react-native";
import MenuOption from "@/components/ui/MenuOptions";
import MenuUser from "@/components/ui/MenuUser";
import SharedAssets from "@/shared/SharedAssets";
import { router, useRouter } from 'expo-router';
import { Colors } from "@/constants/Colors";
import { Container, Fonts } from "@/shared/SharedStyles";
import { useAuth } from "@/contexts/AuthContext";
import { AuthService } from "@/services/auth";

export default function UserMenu() {
  const colorScheme = useColorScheme();
  const check = colorScheme ?? "light";
  const { logout } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);
        const userData = await AuthService.me();
        if (userData) {
          setUsername(userData.username || "");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  return (
    <ScrollView
        style={[
          Container.base,
          {
            backgroundColor: Colors[check].background,
          }
        ]}
      >
        <Text
            style={[
              Container.title,
              Fonts.h1Large,
              {color: Colors[check].text}
            ]}
        >
            Menu
        </Text>
        <MenuUser username={username} onPress={
          () => router.push('/menu/me')}
        />
        <MenuOption icon="globe" label="Language: English" />
        <MenuOption icon="test" label="Test" 
          onPress={() => router.push('/test/socket')}
        />
        <View style={styles.divider} />
        <MenuOption icon="check-circle" label="Goals" />
        <MenuOption icon="history" label="History" 
          onPress={() => router.push('/menu/history')}
        />
        <MenuOption 
          icon="settings" 
          label="Settings" 
          onPress={() => router.push('/menu/setting')} 
        />
        <View style={styles.divider} />
        <MenuOption icon="info" label="About us" />
        <MenuOption icon="log-out" label="Log out" 
          onPress={async () => {
            await logout();
            // router.replace('/login');
          }}
        />
        <View style={styles.footer}>
          <Image 
            source={SharedAssets.Logo}
            style={styles.logo}
            resizeMode="contain"
            />
        </View>
      </ScrollView>
  );
}

// Styles remain unchanged
const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 16,
  },
  content: {
    padding: 16,
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E5E5',
    marginVertical: 8,
  },
  footer: {
    alignItems: 'flex-start',
    marginTop: 'auto',
    paddingVertical: 16,
  },
  logo: {
    width: 120,
    height: 50,
  }
});