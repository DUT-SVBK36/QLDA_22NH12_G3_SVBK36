import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, FlatList, StatusBar, Text, useColorScheme, ScrollView } from 'react-native';
import { StyleSheet } from 'react-native';
import ChatBubble from '@/components/ui/ChatBubble';
import { BaseColors, Colors } from "@/constants/Colors";
import { Container, Fonts } from "@/shared/SharedStyles";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import SharedAssets from '@/shared/SharedAssets';
import SafeScreen from '@/components/layout/SafeScreen';

const INITIAL_MESSAGES = [
    { id: '1', message: 'Hi! I need some assistance.', mode: 'user' as const },
    { id: '2', message: 'Hello! How can I help you today?', mode: 'bot' as const },
    { id: '3', message: 'Lorem ipsum lorem Lorem ipsum  lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um', mode: 'user' as const },
    { id: '4', message: 'Lorem ipsum lorem Lorem ipsum  lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um', mode: 'bot' as const },
    { id: '5', message: 'Lorem ipsum lorem Lorem ipsum  lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um', mode: 'user' as const },
    { id: '6', message: 'Lorem ipsum lorem Lorem ipsum  lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um lorem ipsum um', mode: 'bot' as const },
    
];

export default function ChatBot() {
    const [messages] = useState(INITIAL_MESSAGES);

    return (
        <SafeScreen style={[Container.base, styles.container]} hasBackground>
            <Text style={[styles.header, { color: BaseColors.dark_pri}, Fonts.h1Large]}>
              AI Assistant
            </Text>

            {/* Chat Messages */}
            <ScrollView style={styles.chatContainer}>
                    {messages.map(item => (
                        <ChatBubble 
                            key={item.id}
                            message={item.message} 
                            mode={item.mode} 
                        />
                    ))}
            </ScrollView>

            <View style={styles.inputContainer}>
                <TextInput
                  style={[styles.input, ]}
                  placeholder="Ask something..."
                  placeholderTextColor={BaseColors.white}
                />
                <TouchableOpacity style={styles.sendButton}>
                    <FontAwesomeIcon 
                      icon={faArrowRight} 
                      size={15} 
                      color={BaseColors.white}
                    />
                </TouchableOpacity>
                
            </View>
        </SafeScreen>
    );
}

const styles = StyleSheet.create({
    container: {
        
    },
    header: {
        marginBottom: 24,
    },
    chatContainer: {
        flex: 1, // Add flex 1 to allow container to shrink
        maxHeight: '100%',
        backgroundColor: BaseColors.dark_blue,
        borderRadius: 5,
        margin: 10,
        padding: 15,
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 15,
        backgroundColor: BaseColors.dark_blue,
        borderRadius: 5,
        marginHorizontal: 10,
        marginBottom: 10, // Changed from margin to marginBottom
    },
    input: {
        flex: 1,
        paddingHorizontal: 15,
        color: BaseColors.white,
        maxHeight: 80,
    },
    sendButton: {
        padding: 10,
    },
});