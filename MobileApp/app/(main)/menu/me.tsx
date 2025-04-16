import React, { useEffect, useState, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  RefreshControl,
  SafeAreaView,
} from "react-native";
import { AuthService } from "@/services/auth";
import { AnalyticsService } from "@/services/analytics";
import {
  PostureDist,
  PostureDuration,
  PostureHistory,
  PostureImprovement,
} from "@/models/analytics";
import {
  PostureDistChart,
  PostureDurationChart,
  PostureHistoryChart,
  PostureImprovementChart,
} from "@/components/ui/charts";
import { BaseColors } from "@/constants/Colors";
import { Fonts } from "@/shared/SharedStyles";

export default function Me() {
  const [userData, setUserData] = useState<any>(null);
  const [analytics, setAnalytics] = useState<{
    distribution: PostureDist | null;
    duration: PostureDuration | null;
    history: PostureHistory | null;
    improvement: PostureImprovement | null;
  }>({
    distribution: null,
    duration: null,
    history: null,
    improvement: null,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Use useCallback to memoize the fetchData function
  const fetchData = useCallback(async () => {
    try {
      setError(null);
      // Fetch user data
      const user = await AuthService.me();
      if (user) {
        setUserData(user);
      }

      // Calculate date range for last 30 days
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);

      // Fetch analytics data in parallel
      const [distribution, duration, history, improvement] = await Promise.all([
        AnalyticsService.getPostureDist(startDate, endDate),
        AnalyticsService.getPostureDuration(startDate, endDate),
        AnalyticsService.getPostureHistory(30), // Last 30 records
        AnalyticsService.getPostureImprovement("month"), // Monthly improvement
      ]);

      setAnalytics({
        distribution,
        duration,
        history,
        improvement,
      });
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Failed to load data. Please try again.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []); // Empty dependency array means this function reference won't change

  useEffect(() => {
    fetchData();
    console.log("Fetching data...");
  }, [fetchData]); // Add fetchData as a dependency

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    console.log("Refreshing...");
    fetchData();
  }, [fetchData]); // Add fetchData as a dependency

  if (loading) {
    return (
      <SafeAreaView style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={BaseColors.primary} />
        <Text style={[Fonts.body, styles.loadingText]}>Loading your data...</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        <View style={styles.header}>
          <Text style={[Fonts.h1, styles.headerTitle]}>My Dashboard</Text>
          {userData && (
            <Text style={[Fonts.subtitle, styles.welcomeText]}>
              Welcome, {userData.username || "User"}
            </Text>
          )}
        </View>

        {error ? (
          <View style={styles.errorContainer}>
            <Text style={[Fonts.body, styles.errorText]}>{error}</Text>
          </View>
        ) : (
          <>
            {analytics.distribution && (
              <PostureDistChart 
                data={analytics.distribution} 
                titleStyle={Fonts.h3}
                labelStyle={Fonts.caption}
                valueStyle={Fonts.body}
              />
            )}

            {analytics.duration && (
              <PostureDurationChart 
                data={analytics.duration}
                titleStyle={Fonts.h3}
                labelStyle={Fonts.caption}
                valueStyle={Fonts.body}
              />
            )}

            {analytics.history && (
              <PostureHistoryChart 
                data={analytics.history}
                titleStyle={Fonts.h3}
                labelStyle={Fonts.caption}
                valueStyle={Fonts.body}
              />
            )}

            {!analytics.distribution &&
              !analytics.duration &&
              !analytics.history &&
              !analytics.improvement && (
                <View style={styles.noDataContainer}>
                  <Text style={[Fonts.body, styles.noDataText]}>
                    No analytics data available yet. Start using the posture
                    tracker to generate insights!
                  </Text>
                </View>
              )}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  // Keep your existing styles
  container: {
    flex: 1,
    backgroundColor: "#F5F7FA",
  },
  scrollContent: {
    padding: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5F7FA",
  },
  loadingText: {
    marginTop: 16,
    color: BaseColors.dark_pri,
  },
  header: {
    marginBottom: 24,
  },
  headerTitle: {
    color: BaseColors.dark_pri,
    marginBottom: 8,
  },
  welcomeText: {
    color: BaseColors.dark_pri,
  },
  errorContainer: {
    padding: 16,
    backgroundColor: "#FFEBEE",
    borderRadius: 8,
    marginBottom: 16,
  },
  errorText: {
    color: BaseColors.red,
    textAlign: "center",
  },
  noDataContainer: {
    padding: 24,
    backgroundColor: "#FFFFFF",
    borderRadius: 8,
    marginVertical: 16,
    alignItems: "center",
    justifyContent: "center",
  },
  noDataText: {
    color: BaseColors.grey,
    textAlign: "center",
  },
});