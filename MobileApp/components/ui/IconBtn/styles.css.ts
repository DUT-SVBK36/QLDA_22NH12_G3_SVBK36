import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    minHeight: 48,
    backgroundColor: BaseColors.dark_pri,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    paddingLeft: 12,
    borderRadius: 5,
    gap: 8,
    width: "100%",
  },
});

export default styles;
