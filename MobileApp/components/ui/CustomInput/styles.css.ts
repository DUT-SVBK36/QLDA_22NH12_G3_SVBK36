
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
    container: {
        width: '100%',
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomWidth: 1,
        paddingVertical: 8,
        paddingHorizontal: "auto",
        marginBottom: 16,
    },
    label: {
        fontFamily: 'Lexend',
        minWidth: 100,
        textAlign: 'left',
        paddingLeft: 4,
        fontSize: 14,
        fontWeight: 'semibold',
    },
    input: {
        flex: 1,
        fontFamily: 'Lexend',
        fontSize: 14,
        backgroundColor: "transparent",
    }
});

export default styles;