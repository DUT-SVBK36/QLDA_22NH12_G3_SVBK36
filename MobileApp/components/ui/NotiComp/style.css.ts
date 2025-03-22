
import { StyleSheet } from "react-native";

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flexDirection: 'row',
        gap: 16,
        paddingVertical: 8,
        alignItems: 'center',
        width: '100%',
    },
    contentHolder: {
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        alignItems: 'flex-start',
        justifyContent: 'center',
    },
    timeStampsTint: {
        color: '#A5A5A5',
    },
    
})

export default styles;