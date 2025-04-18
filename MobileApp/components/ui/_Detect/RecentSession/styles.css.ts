import { StyleSheet } from "react-native";
import { BaseColors } from "@/constants/Colors";

const styles = StyleSheet.create({
  container: {
    backgroundColor: BaseColors.white,
    borderRadius: 8,
    // marginVertical: 16,
    padding: 16,
    width: "100%",
    flex: 1,
  },
  content: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16,
  },
  textContent: {
    marginLeft: 16,
    flex: 1,
  },
  errorContainer: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    padding: 16,
  },
  noSessionContainer: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
    padding: 16,
  },
  buttonContainer: {
    flexDirection: "row",
    overflow: "hidden",
    justifyContent: "space-between",
  },
});

export default styles;
