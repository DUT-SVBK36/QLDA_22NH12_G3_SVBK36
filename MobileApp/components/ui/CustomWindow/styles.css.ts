import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    width: "100%",
    marginBottom: 16,
    // Add flex properties to ensure proper containment
    flexDirection: "column",
  },
  titleBar: {
    paddingVertical: 8,
    backgroundColor: "#FFC0CB",
    borderTopLeftRadius: 5,
    borderTopRightRadius: 5,
  },
  title: {
    color: "black",
    fontSize: 16,
    textAlign: "center",
  },
  content: {
    backgroundColor: BaseColors.white,
    // Allow for flexible height
    flexGrow: 1,
    // Ensure scroll container can grow but also respects maxHeight
    minHeight: 10,
  },
  contentContainer: {
    borderBottomRightRadius: 5,
    borderBottomLeftRadius: 5,
    // Add padding at the bottom to ensure last items are visible
    paddingBottom: 16,
  },
});

export default styles;
