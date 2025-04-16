import { StyleSheet } from "react-native";
import { BaseColors } from "@/constants/Colors";

const styles = StyleSheet.create({
  itemContainer: {
    flexDirection: "row",
    padding: 12,
    backgroundColor: BaseColors.white,
    borderRadius: 8,
    marginBottom: 8,
  },
  itemImage: {
    width: 60,
    height: 60,
    borderRadius: 4,
    marginRight: 12,
  },
  itemContent: {
    flex: 1,
    justifyContent: "center",
  },
  itemTitle: {
    fontSize: 18, // Reduced from 24
    lineHeight: 20, // Reduced from 24
    color: BaseColors.black,
    // fontWeight: "bold",
    marginBottom: 4,
  },
  itemTime: {
    marginTop: 6, // Reduced from 8
    fontSize: 14, // Reduced from 16
    lineHeight: 16, // Reduced from 18
    color: "silver",
  },
  itemAccuracy: {
    marginTop: 6, // Reduced from 8
    fontSize: 14, // Reduced from 16
    lineHeight: 16, // Reduced from 18
    color: BaseColors.primary,
  },
  itemRecommendation: {
    color: BaseColors.black,
    marginTop: 4,
    fontSize: 12, // Reduced from default
    fontStyle: "italic",
  },
});

export default styles;
