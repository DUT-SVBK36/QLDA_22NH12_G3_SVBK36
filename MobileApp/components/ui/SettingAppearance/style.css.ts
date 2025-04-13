import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    section: {
        marginBottom: 8,
        width: '100%',
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: '600',        
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E5E5',
    },
    switchs: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        
    },
    label: {
        fontSize: 16,
        flex: 1,
    }
});