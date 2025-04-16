import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, ActivityIndicator, FlatList, ImageBackground, SafeAreaView } from "react-native";
import { useLocalSearchParams } from "expo-router";
import { Session, SessionItem } from "@/models/session.model";
import { SessionService } from "@/services/sessions";
import { Container, Fonts } from "@/shared/SharedStyles";
import { BaseColors } from "@/constants/Colors";
import CustomWindow from "@/components/ui/CustomWindow";
import SharedAssets from "@/shared/SharedAssets";
import { usePopupStore } from "@/services/popup";
import PopUp from "@/components/ui/PopUp";
import SessionItemDetail from "@/components/ui/_Detect/SessionItemDetail";

export default function SessionDetailScreen() {
    const { id } = useLocalSearchParams<{ id: string }>();
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const { isVisible, currentItem, hidePopup } = usePopupStore();
    
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
    
    const renderSessionItem = ({ item }: { item: SessionItem }) => (
        <SessionItemDetail item={item} />
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
            <SafeAreaView style={styles.safeArea}>
                <View style={styles.scrollContainer}>
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

                    <CustomWindow 
                        title="Posture Items" 
                        scrollable={false}
                        maxHeight={400} // Set a max height for the scrollable area
                        contentContainerStyle={styles.postureItemsContainer}
                    >
                        {session.items && session.items.length > 0 ? (
                            <FlatList
                                data={session.items}
                                style={{ paddingHorizontal: 8 }}
                                renderItem={renderSessionItem}
                                keyExtractor={(item) => item._id}
                                contentContainerStyle={styles.listContainer}
                                // Ensure list is scrollable within the CustomWindow
                                nestedScrollEnabled={true}
                                // Add more bottom padding to prevent tab bar overlap
                                ListFooterComponent={<View style={styles.listFooter} />}
                            />
                        ) : (
                            <Text style={[Fonts.body, styles.noItemsText]}>
                                No items in this session
                            </Text>
                        )}
                    </CustomWindow>
                </View>
            </SafeAreaView>
            
            {currentItem && (
                <PopUp
                    visible={isVisible}
                    onClose={hidePopup}
                    image={currentItem.image}
                    label={currentItem.label_name || ''}
                    accuracy={currentItem.accuracy || 0}
                    timestamp={currentItem.timestamp as number || 0}
                    recommendation={currentItem.label_recommendation}
                />
            )}
        </>
    );
}

const styles = StyleSheet.create({
    safeArea: {
        flex: 1,
    },
    scrollContainer: {
        ...Container.base,
        // paddingBottom: 20, // Add extra padding at the bottom to account for tab bar
    },
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
    postureItemsContainer: {
        paddingBottom: 16,
    },
    listContainer: {
        paddingVertical: 8,
    },
    listFooter: {
        height: 80, // Add a footer spacer to ensure last items are visible
    },
    noItemsText: {
        color: BaseColors.black,
        textAlign: 'center',
        padding: 16,
    },
});