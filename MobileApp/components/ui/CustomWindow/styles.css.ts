import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
    container:{
        width: '100%',
        borderRadius: 5,
        minHeight: 100,
        overflow: 'hidden',
    },
    titleBar: {
        // flex: 1,
        paddingVertical: 8,
        backgroundColor: BaseColors.dark_pri,
        paddingLeft: 12,
    },
    title: {
        color: '#fff'
    },
    content: {
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: BaseColors.dark_blue,
        maxHeight: 480,
        paddingBottom: 12,
    }
});

export default styles;