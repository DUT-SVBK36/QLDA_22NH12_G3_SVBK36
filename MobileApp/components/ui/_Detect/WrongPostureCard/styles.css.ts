import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    display: "flex",
    flexDirection: "row",
    paddingVertical: 8,
    paddingHorizontal: 12,
    gap: 8,
    alignItems: "center",
  },
  img: {
    width: 56,
    height: 56,
    objectFit: "cover",
    borderRadius: 8,
  },
  titleTint: {
    color: BaseColors.secondary,
  },
  tint: {
    color: "gray",
  },
  content: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    // gap: 4,
    flex: 1,
  },
});

export default styles;
