import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    width: "100%",
    marginBottom: 16,
  },
  titleBar: {
    paddingVertical: 8,
    backgroundColor: "#FFC0CB",
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  title: {
    color: "black",
    fontSize: 18,
    textAlign: "center",
  },
  content: {
    backgroundColor: BaseColors.white,
  },
  contentContainer: {
    borderBottomRightRadius: 5,
    borderBottomStartRadius: 5,
  },
});

export default styles;
