import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    width: "100%",
    paddingHorizontal: 12,
    paddingVertical: 12,
    backgroundColor: BaseColors.dark_pri,
    borderRadius: 8,
    marginBottom: 8,
  },
  sessionContent: {
    display: "flex",
    flexDirection: "column",
    gap: 4,
  },
  dateText: {
    color: BaseColors.white,
  },
  infoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 4,
  },
  infoText: {
    color: BaseColors.white,
  }
});

export default styles;