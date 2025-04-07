import React, { useState } from "react";
import { StyleSheet, Text, TextInput, TouchableOpacity, View, useColorScheme } from "react-native";
import { Colors } from "@/constants/Colors";
import { Container, Fonts } from "@/shared/SharedStyles";
import KeyboardAwareSafeScreen from "@/components/layout/KeyboardAwareSafeScreen";
import SettingAppearance from "@/components/ui/SettingAppearance";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { useRouter } from "expo-router";

export default function SettingsScreen() {
    const colorScheme = useColorScheme();
    const check = colorScheme ?? "light";
    const router = useRouter();
    return (
        <KeyboardAwareSafeScreen style={[
            Container.base,
            { backgroundColor: Colors[check].background },
            { paddingTop: 0 },
            
            ]}>
            <Text style={[styles.sectionTitle,{ color: Colors[check].text }, Fonts.h2]}>Appearance</Text>
            <SettingAppearance />
            
            <View style={styles.section}>
                <Text style={[styles.sectionTitle, { color: Colors[check].text }, Fonts.h2]}>
                    Detection
                </Text>
                <Text style={[ { color: Colors[check].text }, Fonts.body]}>
                    Custom camera server
                </Text>
                <TextInput
                    style={[styles.input, { color: Colors[check].text }]}
                    placeholder="Enter your custom camera server"
                    placeholderTextColor={Colors[check].tabIconDefault}
                />
                <TouchableOpacity 
                    style={[styles.button, { backgroundColor: Colors[check].tint }]}
                    onPress={() => {
                        router.push("/login");
                    }}
                >
                    <Text style={[styles.buttonText, { color: Colors[check].background }, Fonts.medium]}>
                        Save
                    </Text>
                </TouchableOpacity>
            </View>
            
            <View style={styles.section}>
                <Text style={[styles.sectionTitle, { color: Colors[check].text }, Fonts.h2]}>
                    Account Settings
                </Text>
                <TouchableOpacity style={styles.row}>
                    <Text style={[ { color: Colors[check].text }, Fonts.light]}>
                        Change your password
                    </Text>
                    <FontAwesomeIcon 
                        icon={faArrowRight} 
                        size={15} 
                        color={Colors[check].text}
                    />
                </TouchableOpacity>
            </View>
        </KeyboardAwareSafeScreen>
    );
}

const styles = StyleSheet.create({
    header: {
        marginBottom: 24,
    },
    section: {
        marginBottom: 24,
        width: '100%',
    },
    sectionTitle: {
        marginBottom: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#E5E5E5',
        paddingVertical: 12,
    },
    row: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
    },
    input: {
        borderWidth: 1,
        borderColor: '#E5E5E5',
        borderRadius: 8,
        padding: 12,
        marginTop: 8,
    },
    button: {
        marginTop: 16,
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
    },
    buttonText: {
        fontSize: 16,
    },
});