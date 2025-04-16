/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */

/**
 * BaseColors colors
 */
export const BaseColors = {
  primary: "#b7b1f2",
  secondary: "#fdb7ea",
  tertiary: "#ffdccc",
  quaternary: "#fbf3b9",
  dark_pri: "#2b2e4a",
  dark_blue: "#2a2b38",
  white: "#fff",
  black: "#000",
  inactive: "#9b9b9b",
  grey: "#f0f0f0",
  light_grey: "#d9d9d9",
  light: "#f1f1f1",
  red: "#ff0000",
  pink: "#FFC0CB",
};

const tintColorDark = BaseColors.primary;
const tintColorLight = BaseColors.dark_pri;

export const Colors = {
  light: {
    text: BaseColors.black,
    background: BaseColors.white,
    tint: tintColorLight,
    icon: BaseColors.dark_pri,
    tabIconDefault: "#687076",
    tabIconSelected: tintColorLight,

    button: {
      bg: BaseColors.dark_pri,
      tint: BaseColors.primary,
    },
  },
  dark: {
    text: BaseColors.white,
    background: BaseColors.dark_pri,
    tint: tintColorDark,
    icon: BaseColors.primary,
    tabIconDefault: BaseColors.inactive,
    tabIconSelected: tintColorDark,
    button: {
      bg: BaseColors.primary,
      tint: BaseColors.dark_pri,
    },
  },
};
