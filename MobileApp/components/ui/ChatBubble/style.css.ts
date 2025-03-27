import { BaseColors } from '@/constants/Colors';
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
    bubbleContainer: {
        marginVertical: 5,
        flexDirection: 'row',
        alignItems: 'center',
    },
    userBubbleContainer: {
        justifyContent: 'flex-end',
    },
    aiBubbleContainer: {
        justifyContent: 'flex-start',
    },
    bubble: {
        borderRadius: 10,
        padding: 10,
        marginHorizontal: 8,
        maxWidth: '80%',
    },
    userBubble: {
        backgroundColor: BaseColors.white,
    },
    aiBubble: {
        backgroundColor: BaseColors.tertiary,
    },
    bubbleText: {
        color: BaseColors.black,
        fontSize: 14,
    },
    avatar: {
        width: 40,
        height: 40,
        borderRadius: 20,
    },
});