import React, { useEffect, useState } from "react";
import { Text, View, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { SessionService } from "@/services/sessions";
import { Session } from "@/models/session.model";
import { ImageBackground } from "react-native";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { useColorScheme } from "react-native";
import { BaseColors, Colors } from "@/constants/Colors";
import CustomWindow from "@/components/ui/CustomWindow";
import SessionItem from "@/components/ui/_Detect/SessionItem";
import { router } from "expo-router";

export default function History() {
    const [sessions, setSessions] = useState<Session[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState<number>(0);
    const [hasMore, setHasMore] = useState<boolean>(true);
    const colorScheme = useColorScheme();
    const check = colorScheme ?? "light";

    const fetchSessions = async () => {
        try {
            setLoading(true);
            const response = await SessionService.getAllSessions(page);
            
            if (page === 0) {
                setSessions(response);
            } else {
                // Filter out any duplicate sessions based on _id
                const existingIds = new Set(sessions.map(session => session._id));
                const newSessions = response.filter(session => !existingIds.has(session._id));
                
                setSessions(prevSessions => [...prevSessions, ...newSessions]);
            }
            
            // If we got fewer sessions than requested, there are no more
            setHasMore(response.length === 10);
            setError(null);
        } catch (err: any) {
            console.error('Error fetching sessions:', err);
            
            // Handle authentication errors
            if (err.message?.includes('Not authenticated') || 
                err.message?.includes('Authentication required')) {
                setError('Authentication needed. Please sign in again.');
                // Optional: Redirect to login
                router.replace("/login");
            } else {
                setError('Failed to load sessions. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    // Initial data fetching - only when component mounts
    useEffect(() => {
        fetchSessions();
    }, []);
    
    // Separate effect for pagination to avoid infinite loop
    useEffect(() => {
        if (page > 0) {
            fetchSessions();
        }
    }, [page]);

    // Handle load more
    const handleLoadMore = () => {
        if (!loading && hasMore) {
            setPage(prevPage => prevPage + 1);
        }
    };

    // Render footer with loading indicator
    const renderFooter = () => {
        if (loading) {
            return (
                <View style={styles.footer}>
                    <ActivityIndicator size="small" color={Colors[check].tint} />
                </View>
            );
        }
        return null;
    };
    
    // Generate unique keys for list items
    const keyExtractor = (item: Session, index: number) => {
        return item._id ? `session-${item._id}-${index}` : `session-index-${index}`;
    };

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
        <View style={[
            Container.base,
        ]}>
            <Text style={[
                Container.title,
                Fonts.h2,
                { color: BaseColors.dark_pri}
            ]}>
                Session History
            </Text>

            <CustomWindow title="Previous Sessions" scrollable={false}>
                {error ? (
                    <Text style={[Fonts.body, styles.errorText]}>{error}</Text>
                ) : sessions.length === 0 && !loading ? (
                    <Text style={[Fonts.body, styles.noSessionsText]}>No sessions found</Text>
                ) : (
                    //
                    <FlatList
                        data={sessions}
                        renderItem={({ item }) => (
                            <SessionItem data={item} />
                        )}
                        keyExtractor={keyExtractor}
                        contentContainerStyle={styles.listContainer}
                        onEndReached={handleLoadMore}
                        onEndReachedThreshold={0.5}
                        ListFooterComponent={renderFooter}
                    />
                    
                )}
            </CustomWindow>
        </View>
        </>
        
    );
}

const styles = StyleSheet.create({
    listContainer: {
        paddingVertical: 8,
        backgroundColor: BaseColors.white,
    },
    footer: {
        paddingVertical: 16,
        alignItems: 'center',
    },
    errorText: {
        color: '#f44336',
        textAlign: 'center',
        padding: 16,
    },
    noSessionsText: {
        color: '#ffffff',
        textAlign: 'center',
        padding: 16,
    },
});