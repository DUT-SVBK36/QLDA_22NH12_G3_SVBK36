import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ActivityIndicator, FlatList, Image, ImageBackground } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { Session, SessionItem } from "@/models/session.model";
import { SessionService } from "@/services/sessions";
import { Container, Fonts } from "@/shared/SharedStyles";
import { BaseColors } from "@/constants/Colors";
import CustomWindow from "@/components/ui/CustomWindow";
import SharedAssets from "@/shared/SharedAssets";

export default function SessionDetailScreen() {
    const { id } = useLocalSearchParams<{ id: string }>();
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSessionDetail = async () => {
            if (!id) return;
            
            try {
                setLoading(true);
                const sessionData = await SessionService.getSessionById(id);
                setSession(sessionData);
            } catch (err) {
                console.error(`Error fetching session ${id}:`, err);
                setError('Failed to load session details');
            } finally {
                setLoading(false);
            }
        };

        fetchSessionDetail();
    }, [id]);

    const formatTimespan = (timestamp: number) => {
        const date = new Date(timestamp * 1000);
        return date.toLocaleTimeString();
    };
    
    const renderSessionItem = ({ item }: { item: SessionItem }) => (
        <View style={styles.itemContainer}>
            {item.image && (
                <Image 
                    source={{ uri: item.image }} 
                    style={styles.itemImage} 
                    resizeMode="cover"
                />
            )}
            <View style={styles.itemContent}>
                <Text style={[Fonts.bodySmall, styles.itemTitle]}>
                    {item.label_name}
                </Text>
                <Text style={[Fonts.small, styles.itemTime]}>
                    Time: {formatTimespan(item.timestamp)}
                </Text>
                <Text style={[Fonts.small, styles.itemAccuracy]}>
                    Accuracy: {Math.round(item.accuracy * 100)}%
                </Text>
                {item.label_recommendation && (
                    <Text style={[Fonts.small, styles.itemRecommendation]}>
                        {item.label_recommendation}
                    </Text>
                )}
            </View>
        </View>
    );

    if (loading) {
        return (
            <View style={[Container.base, styles.loadingContainer]}>
                <ActivityIndicator size="large" color={BaseColors.primary} />
            </View>
        );
    }

    if (error || !session) {
        return (
            <View style={Container.base}>
                <Text style={[Fonts.h2, styles.errorText]}>
                    {error || "Session not found"}
                </Text>
            </View>
        );
    }

    const sessionDate = new Date(session.creation_date).toLocaleString();

    return (
        <>
        <ImageBackground 
                source={SharedAssets.Bg}
                resizeMode="cover"
                style={{
                    width: "100%",
                    height: "100%",
                    position: "absolute",
                }}
            />
        <View style={Container.base}>
            <Text style={[Container.title, Fonts.h1]}>Session Detail</Text>
            
            <CustomWindow title="Session Information" scrollable={false}>
                <Text style={[Fonts.bodySmall, styles.sessionInfo]}>
                    Date: {sessionDate}
                </Text>
                <Text style={[Fonts.bodySmall, styles.sessionInfo]}>
                    ID: {session._id}
                </Text>
                <Text style={[Fonts.bodySmall, styles.sessionInfo]}>
                    Items: {session.items?.length || 0}
                </Text>
            </CustomWindow>

            <CustomWindow title="Posture Items" scrollable={false}>
                {session.items && session.items.length > 0 ? (
                    <FlatList
                        data={session.items}
                        renderItem={renderSessionItem}
                        keyExtractor={(item) => item._id}
                        contentContainerStyle={styles.listContainer}
                    />
                ) : (
                    <Text style={[Fonts.body, styles.noItemsText]}>
                        No items in this session
                    </Text>
                )}
            </CustomWindow>
        </View>
        </>
        
    );
}

const styles = StyleSheet.create({
    loadingContainer: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    errorText: {
        color: "red",
        textAlign: 'center',
    },
    sessionInfo: {
        paddingLeft: 12,
        color: BaseColors.black,
        marginBottom: 8,
        fontSize: 16,
        marginTop: 8,
    },
    listContainer: {
        paddingVertical: 8,
    },
    itemContainer: {
        flexDirection: 'row',
        padding: 12,
        backgroundColor: BaseColors.white,
        borderRadius: 8,
        marginBottom: 8,
    },
    itemImage: {
        width: 120,
        height: 120,
        borderRadius: 4,
        marginRight: 12,
    },
    itemContent: {
        flex: 1,
        justifyContent: 'center',

    },
    itemTitle: {
        fontSize: 24,
        lineHeight: 24,
        color: BaseColors.black,
        fontWeight: 'bold',
        marginBottom: 4,
    },
    itemTime: {
        marginTop: 8,
        fontSize: 16,
        lineHeight: 18,
        color: "silver",
    },
    itemAccuracy: {
        marginTop: 8,
        fontSize: 16,
        lineHeight: 18,
        color: BaseColors.primary,
    },
    itemRecommendation: {
        color: BaseColors.black,
        marginTop: 4,
        fontStyle: 'italic',
    },
    noItemsText: {
        color: BaseColors.black,
        textAlign: 'center',
        padding: 16,
    },
});