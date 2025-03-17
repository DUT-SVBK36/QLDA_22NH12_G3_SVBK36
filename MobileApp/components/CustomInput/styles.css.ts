import { StyleSheet } from 'react-native';
const CustomInputCss = StyleSheet.create({
    container: {
        width: '100%',
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
        paddingVertical: 8,
        paddingHorizontal: "auto",
    },
    label: {
        minWidth: 100,
        textAlign: 'left',
        fontSize: 16,
        color: '#000',
    },
    input: {
        flex: 1,
        fontSize: 16,
        color: '#000',
    }
});

export default CustomInputCss;