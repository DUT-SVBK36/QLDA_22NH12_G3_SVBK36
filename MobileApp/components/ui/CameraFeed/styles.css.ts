import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
    cameraContainer: {
        width: "100%",
        height: 300,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: BaseColors.dark_pri,
        borderRadius: 5,
    },
    webview: {
        flex: 1,
    },
})

export default styles;