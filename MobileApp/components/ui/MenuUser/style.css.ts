import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
  container: {
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    borderRightWidth: 1,
    borderRightColor: "#FD87EA",
    marginBottom: 12,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
  },
  userInfo: {
    display: "flex",
    flexDirection: "column",
    flex: 1,
    marginLeft: 12,
  },
  username: {
    fontSize: 18,
    fontWeight: "bold",
  },
  badge: {
    alignSelf: "flex-start",
    backgroundColor: BaseColors.primary,
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 12,
    marginTop: 4,
    textAlign: "center",
  },
  badgetext: {
    color: BaseColors.dark_pri,
    fontSize: 14,
  },
  rightContainer: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
  },
  divider: {
    width: 1,
    height: 24,
    backgroundColor: "#E5E5E5",
    marginLeft: 12,
  },
});
