import { BaseColors } from "@/constants/Colors";
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({

    //container for the user card
    container: {
        backgroundColor: BaseColors.dark_pri,
        paddingVertical: 16,
        paddingHorizontal: 12,
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        borderRadius: 5,
        width: '100%',
    },
    //avatar image
    avatar: {
        width: 48,
        height: 48,
        borderRadius: 9999,
        borderWidth: 2,
        borderColor: BaseColors.primary,
    },
    //right side content holder
    contentHolder: {
        display: 'flex',
        flexDirection: 'column',
        gap: 6,
        flex: 1,
    },
    level: {
        paddingRight: 4,
        display: 'flex',
        flexDirection: 'column',
        overflowX: 'hidden',
        gap: 4,
    },
    progressBar:{
        // alignSelf: "stretch",
    }
})

export default styles;