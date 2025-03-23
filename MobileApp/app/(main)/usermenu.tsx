import { ScrollView, View, Text, StyleSheet, Image } from "react-native";
import { useColorScheme } from "react-native";
import MenuOption from "@/components/ui/MenuOptions";
import MenuUser from "@/components/ui/MenuUser";
import SafeScreen from "@/components/layout/SafeScreen";
import SharedAssets from "@/shared/SharedAssets";
import { Container } from "@/shared/SharedStyles";

export default function UserMenu() {
  const colorScheme = useColorScheme();
  const check = colorScheme ?? "light";

  return (
    <SafeScreen style={Container.base}
    >
      <MenuUser />

      <View>
        <MenuOption icon="globe" label="Language: English" />
        <View style={styles.divider} />
        <MenuOption icon="check-circle" label="Goals" />
        <MenuOption icon="history" label="History" />
        <MenuOption icon="settings" label="Settings" />
        <View style={styles.divider} />
        <MenuOption icon="info" label="About us" />
        <MenuOption icon="log-out" label="Log out" />
      </View>

      <View style={styles.footer}>
        <Image 
          source={SharedAssets.Logo}
          style={styles.logo}
          resizeMode="contain"
        />
      </View>
    </SafeScreen>
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