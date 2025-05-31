import React, { useEffect, useState } from "react";
import UserCard from "@/components/ui/UserCard";
import { BaseColors } from "@/constants/Colors";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { Ionicons } from "@expo/vector-icons";
import { ImageBackground, ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { AuthService } from "@/services/auth";
import { useRouter } from "expo-router";
import IconBtn from "@/components/ui/IconBtn";

export default function HomeScreen() {
  const [username, setUsername] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();
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
    <>
    <ImageBackground 
        source={SharedAssets.Bg}
        resizeMode="cover"
        style={{
          width: "100%",
          height: "100%",
          position: "absolute",
        }}
      />
      <ScrollView style={[
        Container.base,
        
      ]}
        contentContainerStyle={[
          Container.baseContent
        ]}
      >
        {/* Screen label */}
        <Text
        style={[
          Container.title,
          Fonts.h1Large,
          styles.titleTint
        ]}
        >Home
        </Text>

        <Text style={[
          Fonts.medium,
          styles.tint,
          {
            textAlign: "left",
            alignSelf: "flex-start",
            marginBottom: 16,
          }
        ]}>
          Welcome back, {username}!
        </Text>
        <IconBtn 
          label="Detect"
          icon={"camera"}
          onPress={() => router.push('/detect')}
        />
        <IconBtn 
          label="History"
          icon={"time"}
          onPress={() => router.push('/(main)/menu/history')}
        />

        
        {/* Rest of the component remains unchanged */}
      </ScrollView>
    </>
  )
}

// Styles remain unchanged
const styles = StyleSheet.create({
  titleTint: {
    color: BaseColors.dark_pri,
  },
  tint: {
    color: BaseColors.dark_pri,
  },
  container: {
    width: "100%",
    display: "flex",
    flexDirection: "column",
    backgroundColor: BaseColors.white,
    opacity: 0.8,
    alignItems: "center",
    borderRadius: 5,
    padding: 16,
  }
});