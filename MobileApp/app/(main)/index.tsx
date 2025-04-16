import React, { useEffect, useState } from "react";
import UserCard from "@/components/ui/UserCard";
import { BaseColors } from "@/constants/Colors";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { Ionicons } from "@expo/vector-icons";
import { ImageBackground, ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { AuthService } from "@/services/auth";
import { useRouter } from "expo-router";

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

        {/* User Card here */}
        <UserCard 
          username={username}
          onPress={() => router.push('/menu/me')}
        />
        
        {/* Rest of the component remains unchanged */}
        <View style={[
          styles.container,
          {
            padding: 16,
          }
        ]}>
          <Text style={[
            Fonts.h1Large,
            styles.tint
          ]}>
            50%
          </Text>
          <Text style={[
            Fonts.bodySmall,
            styles.tint
          ]}>
            Best right posture accuracy
          </Text>
        </View>
        <View style={
          {
            width: "100%",
            display: "flex",
            flexDirection: "row",
            gap: 16,
          }
        }>
          <TouchableOpacity 
            style={[
              styles.container,
              {
                backgroundColor: BaseColors.white,
                display: "flex",
                flex: 1,
                gap: 8,
              }
            ]}
          >
            <Ionicons name="trophy" size={48} color={BaseColors.dark_pri} />
            <Text style={[
            Fonts.bodySmall,
            styles.tint
            ]}>
            Leaderboard
          </Text>
          </TouchableOpacity>
          <View style={[
          styles.container,
          {
            alignItems: "flex-start",
            justifyContent: "center",
            flex: 2,
          }
          ]}>
            <Text style={[
              Fonts.h1Large,
              styles.tint
            ]}>
              256
            </Text>
            <Text style={[
              Fonts.bodySmall,
              styles.tint
            ]}>
              streak days
            </Text>
        </View>
        </View>
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