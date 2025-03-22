import { Colors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  contentContainer: {
    flexGrow: 1,
    paddingHorizontal: 16,
    paddingTop: 56,
    paddingBottom: 32,

  },
  languageContainer: {
    position: 'absolute',
    top: 16,
    right: 16,
    zIndex: 1,
  },
  languageButton: {
    padding: 8,
  },
  formContainer: {
    justifyContent: 'center',
    width: '100%',
    marginBottom: 40,
  },
  title: {
    fontSize: 32,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 40,
  },
  registerContainer: {
    marginTop: 'auto',
    flexDirection: 'row',
    justifyContent: 'center',
    width: '100%',
  },
  registerText: {
    fontFamily: 'Lexend',
  },
  registerLink: {
    fontFamily: 'Lexend',
  },
});

export default styles;