import React, { useEffect, useState } from 'react';
import { Text, View, ActivityIndicator } from "react-native";
import CustomButton from "../../CustomButton";
import styles from "./styles.css";
import { Ionicons } from "@expo/vector-icons";
import { Fonts } from "@/shared/SharedStyles";
import { useRouter } from "expo-router";
import { SessionService } from "@/services/sessions";
import { Session } from '@/models/session.model';

export default function RecentSession() {
    const router = useRouter();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [session, setSession] = useState<Session | null>(null);

    useEffect(() => {
        async function fetchLatestSession() {
            try {
                setLoading(true);
                const latestSession = await SessionService.getLatestSession();
                setSession(latestSession);
            } catch (err) {
                console.error('Error fetching latest session:', err);
                setError('Could not load recent session');
            } finally {
                setLoading(false);
            }
        }

        fetchLatestSession();
    }, []);

    // Format date nicely
    const formatSessionDate = (dateString: string) => {
        try {
            const date = new Date(dateString);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            return dateString;
        }
    };

    // Navigate to session details
    const handleViewSession = () => {
        if (session?._id) {
            router.push(`/(main)/menu/session?id=${session._id}`);
        }
    };

    return (
        <View style={styles.container}>
            <View style={styles.content}>
                {loading ? (
                    <ActivityIndicator size="large" color="black" />
                ) : error ? (
                    <View style={styles.errorContainer}>
                        <Ionicons name="alert-circle-outline" size={48} color="black" />
                        <Text style={[Fonts.body, { color: "black" }]}>
                            {error}
                        </Text>
                    </View>
                ) : session ? (
                    <>
                        <Ionicons name="timer-outline" size={48} color="black" />
                        <View style={styles.textContent}>
                            <Text style={[Fonts.body, { color: "black" }]}>
                                Recent: {formatSessionDate(session.creation_date)}
                            </Text>
                            <Text style={[Fonts.caption, { color: "black", marginTop: 4 }]}>
                                {session.items?.length || 0} posture{session.items?.length !== 1 ? 's' : ''} recorded
                            </Text>
                        </View>
                    </>
                ) : (
                    <View style={styles.noSessionContainer}>
                        <Ionicons name="timer-outline" size={48} color="black" />
                        <Text style={[Fonts.body, { color: "black" }]}>
                            No recent sessions found
                        </Text>
                    </View>
                )}
            </View>

            {session ? (
                <View style={styles.buttonContainer}>
                    <CustomButton
                        label="View this session"
                        onPress={handleViewSession}
                        variant="blue"
                        // style={styles.button}
                    />
                    <CustomButton
                        label="View all history"
                        onPress={() => router.push("/(main)/menu/history")}
                        variant="blue"
                        // style={styles.button}
                    />
                </View>
            ) : (
                <CustomButton
                    label="View history"
                    onPress={() => router.push("/(main)/menu/history")}
                    variant="blue"
                />
            )}
        </View>
    );
}