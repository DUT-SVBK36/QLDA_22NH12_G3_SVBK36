import React from 'react';
import { View, Text, Image } from 'react-native';
import { styles } from './style.css';

type Chat = 'user' | 'bot';

interface ChatBubbleProps {
    message: string;
    mode: Chat;
}

const ChatBubble = ({ message, mode }: ChatBubbleProps) => {
    const isSelf = mode === 'user';
    
    return (
        <View style={[
            styles.bubbleContainer, 
            isSelf ? styles.userBubbleContainer : styles.aiBubbleContainer
        ]}>
            {!isSelf && (
                <Image
                    source={require('../../../assets/images/ChatbotAvatar.png')} 
                    style={styles.avatar} 
                    resizeMode="cover"
                />
            )}
            <View style={[
                styles.bubble,
                isSelf ? styles.userBubble : styles.aiBubble
            ]}>
                <Text style={styles.bubbleText}>{message}</Text>
            </View>
            {isSelf && (
                <Image 
                    source={require('../../../assets/images/default.jpg')} 
                    style={styles.avatar}
                    resizeMode="cover"
                />
            )}
        </View>
    );
};

export default ChatBubble;