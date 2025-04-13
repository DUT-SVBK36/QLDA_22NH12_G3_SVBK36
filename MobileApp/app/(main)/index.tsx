import UserCard from "@/components/ui/UserCard";
import { BaseColors } from "@/constants/Colors";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { Ionicons } from "@expo/vector-icons";
import { ImageBackground, ScrollView, StyleSheet, Text, TouchableOpacity, View } from "react-native";

export default function HomeScreen(){
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
      Container.base
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

      />
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
              backgroundColor: BaseColors.dark_pri,
              display: "flex",
              flex: 1,
              gap: 8,
            }
          ]}
        >
          <Ionicons name="trophy" size={48} color={BaseColors.white} />
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


const styles = StyleSheet.create({
  titleTint: {
    color: BaseColors.dark_pri,
  },
  tint: {
    color: BaseColors.white,
  },
  container: {
    width: "100%",
    display: "flex",
    flexDirection: "column",
    backgroundColor: BaseColors.dark_pri,
    alignItems: "center",
    borderRadius: 5,
    padding: 16,
  }
});