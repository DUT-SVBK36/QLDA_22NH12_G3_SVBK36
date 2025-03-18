import { ScrollView, StyleSheet, Text } from "react-native";

export default function HomeScreen(){
  return (
    <ScrollView style={styles.container}
      contentContainerStyle={styles.content}
    >
      <Text>Home Screen</Text>
    </ScrollView>
  )
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#282c4d',
  },
  content: {
    alignItems: 'center', 
    justifyContent: 'center'
  }
});