import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    width: "100%",
    marginBottom: 16,
  },
  titleBar: {
    paddingVertical: 8,
    backgroundColor: BaseColors.dark_pri,
    paddingLeft: 12,
    borderTopRightRadius: 5,
    borderTopStartRadius: 5,
  },
  title: {
    color: "#fff",
  },
  content: {
    backgroundColor: BaseColors.dark_blue,
  },
  contentContainer: {
    borderBottomRightRadius: 5,
    borderBottomStartRadius: 5,
  },
});

export default styles;
