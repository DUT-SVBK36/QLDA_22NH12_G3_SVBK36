import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  contentContainer: {
    flexGrow: 1,
    paddingHorizontal: 16,
    paddingTop: 20,
    paddingBottom: 32,
  },
  backContainer: {
    marginBottom: 20, 
    marginTop: 20,
  },
  backButton: {
    padding: 8,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.1)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  formContainer: {
    justifyContent: 'center',
    width: '100%',
    marginBottom: 24,
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
    paddingVertical: 16,
  },
  registerText: {
    fontFamily: 'Lexend',
  },
  registerLink: {
    fontFamily: 'Lexend',
  },
});

export default styles;