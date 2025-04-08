import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-end',
        // alignItems: 'flex-start',
        backgroundColor: BaseColors.dark_pri,
        paddingHorizontal: 12,
        paddingVertical: 12,
        width: '100%',
        borderRadius: 5,
        gap: 8,
    },
    content: {
        display: 'flex',
        flexDirection: 'row',
        // alignItems: 'center',
        gap: 8,
        
        width: '100%',
    },
    textContent: {
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        justifyContent: 'center',
    }
})

export default styles;