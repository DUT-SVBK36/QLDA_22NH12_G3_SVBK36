import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    width: "100%",
    paddingHorizontal: 12,
    paddingVertical: 12,
    backgroundColor: BaseColors.white,
    borderRadius: 8,
  },
  sessionContent: {
    display: "flex",
    flexDirection: "column",
    gap: 4,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5E5',
  },
  dateText: {
    color: BaseColors.black,
  },
  infoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 4,
  },
  infoText: {
    color: BaseColors.black,
  },
  arrow: {
    position: "absolute",
    right: 24,
    top: 24,
    color: BaseColors.primary,
  }
});

export default styles;