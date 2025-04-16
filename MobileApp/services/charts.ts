import { SessionItem } from "@/models/session.model";
import {
  LineChartDataPoint,
  BarChartDataPoint,
  StackedBarDataPoint,
  MultipleBarDataPoint,
  PieChartDataPoint,
  HeatMapDataPoint,
  ComparisonDataPoint,
} from "@/models/charts";

// Chart service functions for data transformation
export class ChartService {
  /**
   * Transform posture session data for a line chart showing accuracy over time
   */
  static prepareAccuracyLineChartData(
    items: SessionItem[]
  ): LineChartDataPoint[] {
    if (!items || items.length === 0) return [];

    return items.map((item, index) => ({
      value: Math.round(item.accuracy * 100),
      date: item.timestamp,
      dateLabel: new Date(item.timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      showDataPoint: true,
      label: `${index + 1}`,
      dataPointText: `${Math.round(item.accuracy * 100)}%`,
    }));
  }

  /**
   * Transform session data for a bar chart showing posture distribution
   */
  static preparePostureDistributionBarData(
    items: SessionItem[]
  ): BarChartDataPoint[] {
    if (!items || items.length === 0) return [];

    // Group by posture label and count occurrences
    const postureCounts = items.reduce((acc, item) => {
      const label = item.label_name;
      acc[label] = (acc[label] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    // Convert to chart data format
    return Object.entries(postureCounts).map(([label, count]) => ({
      value: count,
      label,
      frontColor: this.getColorForPosture(label),
      dataPointText: count.toString(),
    }));
  }

  /**
   * Transform session data for a stacked bar chart showing posture distribution by time period
   */
  static prepareStackedBarData(
    items: SessionItem[],
    timeIntervals: number = 5
  ): StackedBarDataPoint[] {
    if (!items || items.length === 0) return [];

    // Sort items by timestamp
    const sortedItems = [...items].sort(
      (a, b) =>
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );

    // Get time range
    const firstTime = new Date(sortedItems[0].timestamp).getTime();
    const lastTime = new Date(
      sortedItems[sortedItems.length - 1].timestamp
    ).getTime();
    const timeRange = lastTime - firstTime;
    const intervalSize = timeRange / timeIntervals;

    // Create interval buckets
    const intervals: StackedBarDataPoint[] = Array(timeIntervals)
      .fill(null)
      .map((_, i) => {
        const startTime = firstTime + i * intervalSize;
        const endTime = startTime + intervalSize;

        // Create label for this time interval
        const startDate = new Date(startTime);
        const endDate = new Date(endTime);
        const label = `${startDate.getHours()}:${startDate.getMinutes()}-${endDate.getHours()}:${endDate.getMinutes()}`;

        return {
          label,
          stacks: [],
        };
      });

    // Group postures by type for each interval
    const postureGroups: Record<string, number>[] = intervals.map(() => ({}));

    sortedItems.forEach((item) => {
      const itemTime = new Date(item.timestamp).getTime();
      const intervalIndex = Math.min(
        timeIntervals - 1,
        Math.floor((itemTime - firstTime) / intervalSize)
      );

      const posture = item.label_name;
      postureGroups[intervalIndex][posture] =
        (postureGroups[intervalIndex][posture] || 0) + 1;
    });

    // Convert to stacked bar format
    postureGroups.forEach((group, i) => {
      intervals[i].stacks = Object.entries(group).map(([posture, count]) => ({
        value: count,
        color: this.getColorForPosture(posture),
        label: posture,
      }));
    });

    return intervals;
  }

  /**
   * Transform posture data for a pie chart showing percentage distribution
   */
  static preparePosturePieChartData(items: SessionItem[]): PieChartDataPoint[] {
    if (!items || items.length === 0) return [];

    // Group by posture label and count occurrences
    const postureCounts = items.reduce((acc, item) => {
      const label = item.label_name;
      acc[label] = (acc[label] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    // Convert to pie chart format
    return Object.entries(postureCounts).map(([label, count]) => ({
      value: count,
      text: label,
      color: this.getColorForPosture(label),
      textColor: "#fff",
      textSize: 12,
    }));
  }

  /**
   * Transform session data for a heat map showing posture intensity
   */
  static prepareHeatMapData(items: SessionItem[]): HeatMapDataPoint[][] {
    if (!items || items.length === 0) return [];

    // Get unique dates and posture types
    const dates = [
      ...new Set(
        items.map((item) => new Date(item.timestamp).toLocaleDateString())
      ),
    ].sort();

    const postureTypes = [...new Set(items.map((item) => item.label_name))];

    // Create heat map matrix
    return dates.map((date) => {
      const dateItems = items.filter(
        (item) => new Date(item.timestamp).toLocaleDateString() === date
      );

      return postureTypes.map((posture) => {
        const count = dateItems.filter(
          (item) => item.label_name === posture
        ).length;
        return {
          label: posture,
          value: count,
        };
      });
    });
  }

  /**
   * Transform session data for a comparison chart showing actual vs target values
   */
  static prepareComparisonChartData(
    items: SessionItem[],
    targetAccuracy: number = 0.8
  ): ComparisonDataPoint[] {
    if (!items || items.length === 0) return [];

    // Group by posture type and calculate average accuracy
    const postureAccuracy = items.reduce((acc, item) => {
      const label = item.label_name;
      if (!acc[label]) {
        acc[label] = { total: 0, count: 0 };
      }
      acc[label].total += item.accuracy;
      acc[label].count += 1;
      return acc;
    }, {} as Record<string, { total: number; count: number }>);

    // Convert to comparison chart format
    return Object.entries(postureAccuracy).map(([label, { total, count }]) => {
      const avgAccuracy = total / count;
      return {
        label,
        value: Math.round(avgAccuracy * 100),
        color: this.getColorForPosture(label),
        targetValue: Math.round(targetAccuracy * 100),
        targetColor: "#FF5722",
      };
    });
  }

  /**
   * Get a consistent color for a particular posture type
   */
  private static getColorForPosture(posture: string): string {
    // Map posture types to colors - extend as needed
    const colorMap: Record<string, string> = {
      normal_sitting: "#4CAF50",
      head_forward: "#F44336",
      lean_forward: "#FF9800",
      lean_backward: "#9C27B0",
      lean_left: "#2196F3",
      lean_right: "#FFEB3B",
      slouching: "#795548",
      default: "#607D8B",
    };

    return colorMap[posture] || colorMap.default;
  }

  /**
   * Prepare data for multiple bars chart comparing different metrics
   */
  static prepareMultipleBarData(
    sessions: SessionItem[][],
    sessionLabels: string[]
  ): MultipleBarDataPoint[] {
    if (!sessions || sessions.length === 0) return [];

    // Create comparison chart for each posture across sessions
    const postureTypes = [
      ...new Set(sessions.flat().map((item) => item.label_name)),
    ];

    return postureTypes.map((posture) => {
      const bars = sessions.map((sessionItems, index) => {
        const postureItems = sessionItems.filter(
          (item) => item.label_name === posture
        );
        const count = postureItems.length;

        return {
          value: count,
          color: this.getSessionColor(index),
          label: sessionLabels[index] || `Session ${index + 1}`,
        };
      });

      return {
        label: posture,
        bars,
      };
    });
  }

  /**
   * Get a consistent color for a specific session index
   */
  private static getSessionColor(index: number): string {
    const colors = [
      "#3366CC",
      "#DC3912",
      "#FF9900",
      "#109618",
      "#990099",
      "#3B3EAC",
      "#0099C6",
      "#DD4477",
      "#66AA00",
      "#B82E2E",
    ];

    return colors[index % colors.length];
  }
}
