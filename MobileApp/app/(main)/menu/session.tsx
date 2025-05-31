import React, { useEffect, useState } from "react";
import { 
  View, 
  Text, 
  StyleSheet, 
  ActivityIndicator, 
  FlatList, 
  ImageBackground, 
  SafeAreaView,
  ScrollView 
} from "react-native";
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
import { Ionicons } from "@expo/vector-icons";

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
            <View style={styles.centeredContainer}>
                <ImageBackground 
                    source={SharedAssets.Bg}
                    resizeMode="cover"
                    style={styles.backgroundImage}
                />
                <View style={styles.loadingOverlay}>
                    <ActivityIndicator size="large" color={BaseColors.primary} />
                    <Text style={[Fonts.body, styles.loadingText]}>Loading session...</Text>
                </View>
            </View>
        );
    }

    if (error || !session) {
        return (
            <View style={styles.centeredContainer}>
                <ImageBackground 
                    source={SharedAssets.Bg}
                    resizeMode="cover"
                    style={styles.backgroundImage}
                />
                <View style={styles.errorContainer}>
                    <Ionicons name="alert-circle-outline" size={64} color={BaseColors.red} />
                    <Text style={[Fonts.h2, styles.errorTitle]}>
                        Oops! Something went wrong
                    </Text>
                    <Text style={[Fonts.body, styles.errorText]}>
                        {error || "Session not found"}
                    </Text>
                </View>
            </View>
        );
    }

    const sessionDate = new Date(session.creation_date);
    const formattedDate = sessionDate.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    const formattedTime = sessionDate.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });

    return (
        <>
            <ImageBackground 
                source={SharedAssets.Bg}
                resizeMode="cover"
                style={styles.backgroundImage}
            />
            <SafeAreaView style={styles.safeArea}>
                <ScrollView 
                    style={styles.scrollView}
                    contentContainerStyle={styles.scrollContainer}
                    showsVerticalScrollIndicator={false}
                >
                    {/* Header Section */}
                    <View style={styles.headerSection}>
                        <Text style={[Fonts.h1, styles.title]}>Session Details</Text>
                        <Text style={[Fonts.caption, styles.subtitle]}>
                            View your posture monitoring session
                        </Text>
                    </View>
                    
                    {/* Session Information Card */}
                    <View style={styles.infoCard}>
                        <View style={styles.cardHeader}>
                            <Ionicons name="information-circle" size={24} color={BaseColors.dark_pri} />
                            <Text style={[Fonts.h3, styles.cardTitle]}>Session Information</Text>
                        </View>
                        
                        <View style={styles.infoGrid}>
                            <View style={styles.infoItem}>
                                <Ionicons name="calendar-outline" size={20} color={BaseColors.dark_pri} />
                                <View style={styles.infoTextContainer}>
                                    <Text style={[Fonts.caption, styles.infoLabel]}>Date</Text>
                                    <Text style={[Fonts.body, styles.infoValue]}>{formattedDate}</Text>
                                </View>
                            </View>
                            
                            <View style={styles.infoItem}>
                                <Ionicons name="time-outline" size={20} color={BaseColors.dark_pri} />
                                <View style={styles.infoTextContainer}>
                                    <Text style={[Fonts.caption, styles.infoLabel]}>Time</Text>
                                    <Text style={[Fonts.body, styles.infoValue]}>{formattedTime}</Text>
                                </View>
                            </View>
                            
                            <View style={styles.infoItem}>
                                <Ionicons name="analytics-outline" size={20} color={BaseColors.dark_pri} />
                                <View style={styles.infoTextContainer}>
                                    <Text style={[Fonts.caption, styles.infoLabel]}>Total Items</Text>
                                    <Text style={[Fonts.body, styles.infoValue]}>
                                        {session.items?.length || 0} recordings
                                    </Text>
                                </View>
                            </View>
                            
                            <View style={styles.infoItem}>
                                <Ionicons name="finger-print-outline" size={20} color={BaseColors.dark_pri} />
                                <View style={styles.infoTextContainer}>
                                    <Text style={[Fonts.caption, styles.infoLabel]}>Session ID</Text>
                                    <Text style={[Fonts.caption, styles.sessionId]} numberOfLines={1}>
                                        {session._id}
                                    </Text>
                                </View>
                            </View>
                        </View>
                    </View>

                    {/* Posture Items Section */}
                    <View style={styles.postureSection}>
                        <View style={styles.sectionHeader}>
                            <Ionicons name="body-outline" size={24} color={BaseColors.dark_pri} />
                            <Text style={[Fonts.h3, styles.sectionTitle]}>Posture Recordings</Text>
                            <View style={styles.itemCount}>
                                <Text style={[Fonts.caption, styles.itemCountText]}>
                                    {session.items?.length || 0}
                                </Text>
                            </View>
                        </View>
                        
                        <View style={styles.postureItemsContainer}>
                            {session.items && session.items.length > 0 ? (
                                <FlatList
                                    data={session.items}
                                    renderItem={renderSessionItem}
                                    keyExtractor={(item) => item._id}
                                    contentContainerStyle={styles.listContainer}
                                    nestedScrollEnabled={true}
                                    showsVerticalScrollIndicator={false}
                                    ItemSeparatorComponent={() => <View style={styles.itemSeparator} />}
                                    ListFooterComponent={<View style={styles.listFooter} />}
                                />
                            ) : (
                                <View style={styles.emptyState}>
                                    <Ionicons name="document-outline" size={48} color={BaseColors.inactive} />
                                    <Text style={[Fonts.body, styles.emptyStateText]}>
                                        No posture recordings found
                                    </Text>
                                    <Text style={[Fonts.caption, styles.emptyStateSubtext]}>
                                        This session doesn't contain any posture data
                                    </Text>
                                </View>
                            )}
                        </View>
                    </View>
                </ScrollView>
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
    centeredContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    backgroundImage: {
        width: "100%",
        height: "100%",
        position: "absolute",
    },
    safeArea: {
        flex: 1,
    },
    scrollView: {
        flex: 1,
    },
    scrollContainer: {
        paddingHorizontal: 20,
        paddingBottom: 100, // Extra space for tab bar
    },
    
    // Header Styles
    headerSection: {
        marginTop: 20,
        marginBottom: 24,
        alignItems: 'center',
    },
    title: {
        color: BaseColors.dark_pri,
        textAlign: 'center',
        marginBottom: 8,
        fontWeight: '700',
    },
    subtitle: {
        color: BaseColors.dark_pri,
        textAlign: 'center',
    },
    
    // Info Card Styles
    infoCard: {
        backgroundColor: BaseColors.white,
        borderRadius: 16,
        padding: 20,
        marginBottom: 24,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.12,
        shadowRadius: 8,
        elevation: 8,
    },
    cardHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 20,
    },
    cardTitle: {
        marginLeft: 12,
        color: BaseColors.dark_pri,
        fontWeight: '600',
    },
    infoGrid: {
        gap: 16,
    },
    infoItem: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 8,
    },
    infoTextContainer: {
        marginLeft: 16,
        flex: 1,
    },
    infoLabel: {
        color: BaseColors.black,
        marginBottom: 2,
    },
    infoValue: {
        color: BaseColors.dark_pri,
        fontWeight: '500',
    },
    sessionId: {
        color: BaseColors.black,
        fontFamily: 'monospace',
    },
    
    // Posture Section Styles
    postureSection: {
        flex: 1,
    },
    sectionHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 16,
        paddingHorizontal: 4,
    },
    sectionTitle: {
        marginLeft: 12,
        color: BaseColors.dark_pri,
        fontWeight: '600',
        flex: 1,
    },
    itemCount: {
        backgroundColor: BaseColors.dark_pri,
        borderRadius: 12,
        paddingHorizontal: 8,
        paddingVertical: 4,
        minWidth: 24,
        alignItems: 'center',
    },
    itemCountText: {
        color: BaseColors.white,
        fontWeight: '600',
    },
    
    // Posture Items Container
    postureItemsContainer: {
        backgroundColor: BaseColors.white,
        borderRadius: 16,
        overflow: 'hidden',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.12,
        shadowRadius: 8,
        elevation: 8,
        minHeight: 300,
    },
    listContainer: {
        padding: 16,
    },
    itemSeparator: {
        height: 12,
    },
    listFooter: {
        height: 20,
    },
    
    // Loading States
    loadingOverlay: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: 16,
        padding: 40,
        margin: 20,
    },
    loadingText: {
        marginTop: 16,
        color: BaseColors.dark_pri,
    },
    
    // Error States
    errorContainer: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderRadius: 16,
        padding: 40,
        margin: 20,
    },
    errorTitle: {
        color: BaseColors.dark_pri,
        textAlign: 'center',
        marginTop: 16,
        marginBottom: 8,
    },
    errorText: {
        color: BaseColors.red,
        textAlign: 'center',
    },
    
    // Empty State
    emptyState: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 60,
        paddingHorizontal: 20,
    },
    emptyStateText: {
        color: BaseColors.dark_pri,
        textAlign: 'center',
        marginTop: 16,
        marginBottom: 8,
    },
    emptyStateSubtext: {
        color: BaseColors.grey,
        textAlign: 'center',
        lineHeight: 20,
    },
});