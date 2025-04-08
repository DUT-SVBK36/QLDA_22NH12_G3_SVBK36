import { View, StyleSheet, Image, ScrollView, Text } from "react-native";
import { useColorScheme } from "react-native";
import MenuOption from "@/components/ui/MenuOptions";
import MenuUser from "@/components/ui/MenuUser";
import SharedAssets from "@/shared/SharedAssets";
import { router } from 'expo-router';
import SafeScrollView from "@/components/layout/SafeScrollView";
import { Colors } from "@/constants/Colors";
import { Container, Fonts } from "@/shared/SharedStyles";

export default function UserMenu() {
  const colorScheme = useColorScheme();
  const check = colorScheme ?? "light";

  return (
    <ScrollView
        style={[
          Container.base,
          {
            backgroundColor: Colors[check].background,
            // paddingTop: 0,
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
        <MenuUser />
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
        <MenuOption icon="log-out" label="Log out" />
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