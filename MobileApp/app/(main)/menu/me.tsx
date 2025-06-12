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
import DropDownPicker from 'react-native-dropdown-picker';
import { Summary } from "@/models/charts/summary.model";
import SummaryCard from "@/components/ui/Analytics/SummaryCard";
export default function Me() {
  const [userData, setUserData] = useState<any>(null);
  const [analytics, setAnalytics] = useState<{
    summary: Summary | null;
    distribution: PostureDist | null;
    duration: PostureDuration | null;
    improvement: PostureImprovement | null;
  }>({
    summary:  null,
    distribution: null,
    duration: null,
    improvement: null,
  });
  const [filter, setFilter] = useState<string>("1"); // Default filter to "month"
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState([
        {label: 'Recent 24h', value: '1'},
        {label: 'Recent 7 days', value: '7'},
        {label: 'Recent 30 days', value: '30'},
    ]);

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
      let endDate = new Date();
      let startDate = new Date();
      startDate.setDate(endDate.getDate() - Number(filter)); // Default to last 30 days

      // Fetch analytics data in parallel
      const [summary, distribution, duration, improvement] = await Promise.all([
        AnalyticsService.getUserSummary(),
        AnalyticsService.getPostureDist(startDate, endDate),
        AnalyticsService.getPostureDuration(startDate, endDate),
        AnalyticsService.getPostureImprovement(filter), // Monthly improvement
      ]);

      setAnalytics({
        summary,
        distribution,
        duration,
        improvement,
      });
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Failed to load data. Please try again.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [filter]); // Empty dependency array means this function reference won't change

  useEffect(() => {
    console.log("useEffect: Fetching data with filter:", filter);
    fetchData();
    console.log("Fetching data...");
  }, [fetchData, filter]); // Add fetchData as a dependency

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    console.log("Refreshing...");
    fetchData();
  }, [fetchData, filter]); // Add fetchData as a dependency

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
        
          <SummaryCard 
            data={analytics.summary}
          />

          <DropDownPicker
              open={open}
              value={filter}
              items={items}
              setOpen={setOpen}
              setValue={setFilter}
              setItems={setItems}
              placeholder={'Choose a filter'}
          />
          

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

            {analytics.improvement && (
              <PostureImprovementChart 
                data={analytics.improvement} 
                titleStyle={Fonts.h3}
                labelStyle={Fonts.caption}
                valueStyle={Fonts.body}
              />
            )}


            {!analytics.distribution &&
              !analytics.duration &&
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