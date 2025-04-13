import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator } from 'react-native';
import { useLocalSearchParams } from "expo-router";
import { Fonts } from '@/shared/SharedStyles';
import { BaseColors } from '@/constants/Colors';
import CustomWindow from '@/components/ui/CustomWindow';
import { SessionItem as SessionItemType, SessionService } from '@/services/sessions';

export default function SessionItem() {
    const { id } = useLocalSearchParams<{ id: string }>();
    const [item, setItem] = useState<SessionItemType | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSessionItem = async () => {
            try {
                console.log('Fetching item with ID:', id); // Debug log
                const data = await SessionService.getSessionItem(id);
                console.log('Received data:', data); // Debug log
                setItem(data);
            } catch (error) {
                console.error('Error fetching session item:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSessionItem();
    }, [id]);

    const formatTimespan = (timestamp: number) => {
        const date = new Date(timestamp * 1000);
        return date.toLocaleString();
    };

    if (loading) {
        return (
            <CustomWindow title="Loading...">
                <View style={styles.loadingContainer}>
                    <ActivityIndicator size="large" color={BaseColors.primary} />
                </View>
            </CustomWindow>
        );
    }

    if (!item) {
        return (
            <CustomWindow title="Error">
                <View style={styles.errorContainer}>
                    <Text style={[Fonts.body, styles.errorText]}>
                        Item not found
                    </Text>
                </View>
            </CustomWindow>
        );
    }

    return (
        <CustomWindow title="Posture Details">
            <View style={styles.container}>
                <View style={styles.imageContainer}>
                    <Image 
                        source={{ uri: item.image }} 
                        style={styles.image}
                        resizeMode="contain"
                    />
                </View>
                
                <View style={styles.infoContainer}>
                    <View style={styles.infoRow}>
                        <Text style={[Fonts.h1Large, styles.postureName]}>
                            {item.label_name}
                        </Text>
                        <View style={[
                            styles.accuracyBadge,
                            { backgroundColor: item.accuracy > 0.7 ? "red" : "yellow" }
                        ]}>
                            <Text style={styles.accuracyText}>
                                {Math.round(item.accuracy * 100)}%
                            </Text>
                        </View>
                    </View>

                    <Text style={[Fonts.bodySmall, styles.timestamp]}>
                        Recorded at: {formatTimespan(item.timestamp)}
                    </Text>

                    {item.label_recommendation && (
                        <View style={styles.recommendationContainer}>
                            <Text style={[Fonts.body, styles.recommendationTitle]}>
                                Recommendation:
                            </Text>
                            <Text style={[Fonts.bodySmall, styles.recommendationText]}>
                                {item.label_recommendation}
                            </Text>
                        </View>
                    )}
                </View>
            </View>
        </CustomWindow>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: BaseColors.white,
        borderRadius: 12,
        overflow: 'hidden',
    },
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    errorContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    errorText: {
        color: "red",
    },
    imageContainer: {
        width: '100%',
        height: 300,
        backgroundColor: BaseColors.black,
    },
    image: {
        width: '100%',
        height: '100%',
    },
    infoContainer: {
        padding: 16,
    },
    infoRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8,
    },
    postureName: {
        flex: 1,
        fontSize: 24,
        fontWeight: 'bold',
        color: BaseColors.black,
    },
    accuracyBadge: {
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 16,
        marginLeft: 8,
    },
    accuracyText: {
        color: BaseColors.white,
        fontWeight: 'bold',
        fontSize: 14,
    },
    timestamp: {
        color: BaseColors.black,
        marginBottom: 16,
    },
    recommendationContainer: {
        backgroundColor: BaseColors.black,
        padding: 16,
        borderRadius: 8,
        marginTop: 16,
    },
    recommendationTitle: {
        fontWeight: 'bold',
        marginBottom: 8,
        color: BaseColors.black,
    },
    recommendationText: {
        color: BaseColors.black,
        lineHeight: 20,
    },
});