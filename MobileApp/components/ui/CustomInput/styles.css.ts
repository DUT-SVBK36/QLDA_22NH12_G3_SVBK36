import { Colors } from '@/constants/Colors';
import { StyleSheet, useColorScheme } from 'react-native';

const colorScheme = useColorScheme();
const styles = StyleSheet.create({
    container: {
        width: '100%',
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomWidth: 1,
        borderBottomColor: Colors[colorScheme ?? 'light'].text,
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
        color: Colors[colorScheme ?? 'light'].text,
    },
    input: {
        flex: 1,
        fontFamily: 'Lexend',
        fontSize: 14,
        color: Colors[colorScheme ?? 'light'].text,
        backgroundColor: "transparent",
    }
});

export default styles;