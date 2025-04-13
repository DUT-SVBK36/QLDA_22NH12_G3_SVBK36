import React, { useCallback } from "react";
import { Text, TouchableOpacity, View } from "react-native";
import { router } from "expo-router";
import { Session } from "@/models/session.model";
import { Fonts } from "@/shared/SharedStyles";
import { BaseColors } from "@/constants/Colors";
import styles from "./style.css";
import { FontAwesomeIcon } from "@fortawesome/react-native-fontawesome";
import { faArrowRight } from "@fortawesome/free-solid-svg-icons";

interface SessionItemProps {
    data: Session;
}

export default function SessionItem({ data }: SessionItemProps) {
    // Navigate to session details
    const navToItem = useCallback(() => {
        router.push({
            pathname: "/(main)/menu/session",
            params: { id: data._id },
        });
    }, [data._id]);

    // Format date for better readability
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleString("en-US", { 
            weekday: 'short',
            year: 'numeric', 
            month: 'short', 
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric'
        });
    };

    // Calculate number of items in session

    return (
        <TouchableOpacity 
            style={[styles.container]}
            onPress={navToItem}
            activeOpacity={0.7}
        >
            <View style={styles.sessionContent}>
                <Text style={[Fonts.bodySmall, styles.dateText]}>
                    {formatDate(data.creation_date)}
                </Text>
                
                <View style={styles.infoRow}>
                    <Text style={[Fonts.bodySmall, styles.infoText]}>
                        Session ID: {data._id.slice(-6)}
                    </Text>
                </View>
            </View>
            <FontAwesomeIcon 
                icon={faArrowRight} 
                size={16}
                color={BaseColors.dark_pri}
                style={styles.arrow}
            />
        </TouchableOpacity>
    );
}