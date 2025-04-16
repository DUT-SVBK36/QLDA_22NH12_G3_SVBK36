import api from "@/constants/api";
import { fetchWithAuth } from "@/utils/fetch-with-auth";
import {
  PostureDist,
  PostureDuration,
  PostureHistory,
  PostureImprovement,
  PostureDailySum,
} from "@/models/analytics";

/**
 * Service for fetching and processing analytics data
 */
export class AnalyticsService {
  /**
   * Get posture distribution data
   * @param startDate Optional start date for filtering
   * @param endDate Optional end date for filtering
   * @returns Posture distribution data
   */
  static async getPostureDist(
    startDate?: string | Date,
    endDate?: string | Date
  ): Promise<PostureDist> {
    try {
      const params: Record<string, string> = {};
      if (startDate) params.start_date = new Date(startDate).toISOString();
      if (endDate) params.end_date = new Date(endDate).toISOString();

      return await fetchWithAuth<PostureDist>(
        api.analytics.getPostureDist,
        params
      );
    } catch (error) {
      console.error("Error fetching posture distribution:", error);
      throw error;
    }
  }

  /**
   * Get posture duration data
   * @param startDate Optional start date for filtering
   * @param endDate Optional end date for filtering
   * @returns Posture duration data
   */
  static async getPostureDuration(
    startDate?: string | Date,
    endDate?: string | Date
  ): Promise<PostureDuration> {
    try {
      const params: Record<string, string> = {};
      if (startDate) params.start_date = new Date(startDate).toISOString();
      if (endDate) params.end_date = new Date(endDate).toISOString();

      return await fetchWithAuth<PostureDuration>(
        api.analytics.getPostureDuration,
        params
      );
    } catch (error) {
      console.error("Error fetching posture duration:", error);
      throw error;
    }
  }

  /**
   * Get posture history data
   * @param limit Optional limit for the number of records to retrieve
   * @param offset Optional offset for pagination
   * @returns Posture history data
   */
  static async getPostureHistory(
    limit?: number,
    offset?: number
  ): Promise<PostureHistory> {
    try {
      const params: Record<string, string> = {};
      if (limit !== undefined) params.limit = limit.toString();
      if (offset !== undefined) params.offset = offset.toString();

      return await fetchWithAuth<PostureHistory>(
        api.analytics.getPostureHistory,
        params
      );
    } catch (error) {
      console.error("Error fetching posture history:", error);
      throw error;
    }
  }

  /**
   * Get posture improvement data
   * @param timeFrame Optional time frame for analysis (e.g., 'week', 'month')
   * @returns Posture improvement data
   */
  static async getPostureImprovement(
    timeFrame?: string
  ): Promise<PostureImprovement> {
    try {
      const params: Record<string, string> = {};
      if (timeFrame) params.time_frame = timeFrame;

      return await fetchWithAuth<PostureImprovement>(
        api.analytics.getPostureImprovement,
        params
      );
    } catch (error) {
      console.error("Error fetching posture improvement:", error);
      throw error;
    }
  }

  /**
   * Get daily summary of posture data
   * @param date Optional specific date for the summary
   * @returns Posture daily summary data
   */
  static async getPostureDailySum(
    date?: string | Date
  ): Promise<PostureDailySum> {
    try {
      const params: Record<string, string> = {};
      if (date) params.date = new Date(date).toISOString().split("T")[0];

      return await fetchWithAuth<PostureDailySum>(
        api.analytics.getPostureDailySum,
        params
      );
    } catch (error) {
      console.error("Error fetching posture daily summary:", error);
      throw error;
    }
  }

  /**
   * Get comprehensive analytics data (all endpoints in one call)
   * @param startDate Optional start date for filtering
   * @param endDate Optional end date for filtering
   * @returns Combined analytics data from all endpoints
   */
  static async getComprehensiveAnalytics(
    startDate?: string | Date,
    endDate?: string | Date
  ): Promise<{
    distribution: PostureDist;
    duration: PostureDuration;
    history: PostureHistory;
    improvement: PostureImprovement;
    dailySummary: PostureDailySum;
  }> {
    try {
      // Use Promise.all to fetch data from all endpoints concurrently
      const [distribution, duration, history, improvement, dailySummary] =
        await Promise.all([
          this.getPostureDist(startDate, endDate),
          this.getPostureDuration(startDate, endDate),
          this.getPostureHistory(),
          this.getPostureImprovement(),
          this.getPostureDailySum(),
        ]);

      return {
        distribution,
        duration,
        history,
        improvement,
        dailySummary,
      };
    } catch (error) {
      console.error("Error fetching comprehensive analytics:", error);
      throw error;
    }
  }

  /**
   * Format duration from seconds to a readable string
   * @param seconds Duration in seconds
   * @returns Formatted duration string (e.g., "1h 30m")
   */
  static formatDuration(seconds?: number | null): string {
    if (!seconds) return "0m";

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  }

  /**
   * Format percentage to a string with precision
   * @param percentage Percentage value
   * @param precision Number of decimal places
   * @returns Formatted percentage string
   */
  static formatPercentage(
    percentage?: number | null,
    precision: number = 1
  ): string {
    if (percentage === null || percentage === undefined) return "0%";
    return `${percentage.toFixed(precision)}%`;
  }
}
