import { StyleSheet } from "react-native";

export const Fonts = StyleSheet.create({
  // Text styles by size
  h1Large: {
    fontFamily: "Lexend-Bold",
    fontSize: 32,
    lineHeight: 40,
  },
  h1: {
    fontFamily: "Lexend-Bold",
    fontSize: 28,
    lineHeight: 36,
  },
  h2: {
    fontFamily: "Lexend-Bold",
    fontSize: 24,
    lineHeight: 32,
  },
  h3: {
    fontFamily: "Lexend-SemiBold",
    fontSize: 20,
    lineHeight: 28,
  },
  subtitle: {
    fontFamily: "Lexend-SemiBold",
    fontSize: 18,
    lineHeight: 24,
  },
  body: {
    fontFamily: "Lexend-Regular",
    fontSize: 16,
    lineHeight: 24,
  },
  bodySmall: {
    fontFamily: "Lexend-Regular",
    fontSize: 14,
    lineHeight: 20,
  },
  caption: {
    fontFamily: "Lexend-Medium",
    fontSize: 12,
    lineHeight: 16,
  },
  small: {
    fontFamily: "Lexend-Medium",
    fontSize: 10,
    lineHeight: 12,
  },

  // Just font families for custom use
  light: {
    fontFamily: "Lexend-Light",
  },
  regular: {
    fontFamily: "Lexend-Regular",
  },
  medium: {
    fontFamily: "Lexend-Medium",
  },
  semiBold: {
    fontFamily: "Lexend-SemiBold",
  },
  bold: {
    fontFamily: "Lexend-Bold",
  },
});

export const Container = StyleSheet.create({
  base: {
    flex: 1,
    display: "flex",
    paddingHorizontal: 16,
    paddingBottom: 32,
    paddingVertical: 54,
  },
  baseContent: {
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
  },
  title: {
    textAlign: "left",
    width: "100%",
    marginBottom: 12,
  },
});
