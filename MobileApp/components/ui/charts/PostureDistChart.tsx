import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { PieChart } from 'react-native-gifted-charts';
import { PostureDist } from '@/models/analytics';
import { BaseColors } from '@/constants/Colors';

interface PostureDistChartProps {
  data: PostureDist;
  title?: string;
  titleStyle?: any;
  labelStyle?: any;
  valueStyle?: any;
}

const PostureDistChart: React.FC<PostureDistChartProps> = ({ 
  data, 
  title = 'Posture Distribution',
  titleStyle = {},
  labelStyle = {},
  valueStyle = {},
}) => {
  // Skip rendering if no data or distribution is available
  if (!data || !data.distribution) {
    return (
      <View style={styles.container}>
        <Text style={[styles.title, titleStyle]}>{title}</Text>
        <Text style={[styles.noDataText, labelStyle]}>No distribution data available</Text>
      </View>
    );
  }

  // Transform distribution data to pie chart format
  const pieData = Object.entries(data.distribution)
    .filter(([_, item]) => item && item.count && item.count > 0)
    .map(([key, item]) => {
      // Generate a color based on the posture type
      const colorMap: Record<string, string> = {
        good_sitting_side: '#4CAF50',
        too_lean_right_side: '#F44336',
        too_lean_left_side: '#FF9800',
        bad_sitting_backward_side: '#9C27B0',
        bad_sitting_forward_side: '#2196F3',
        neck_wrong_position: '#FFEB3B',
        leg_wrong_position: '#795548',
      };

      return {
        value: item?.count || 0,
        text: item?.name || key,
        color: colorMap[key] || '#607D8B',
        textColor: '#FFFFFF',
        textSize: 12,
      };
    });

  // Calculate total for percentage
  const total = pieData.reduce((sum, item) => sum + item.value, 0);

  // If no valid data points, show a message
  if (pieData.length === 0 || total === 0) {
    return (
      <View style={styles.container}>
        <Text style={[styles.title, titleStyle]}>{title}</Text>
        <Text style={[styles.noDataText, labelStyle]}>No distribution data available</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={[styles.title, titleStyle]}>{title}</Text>
      <View style={styles.chartContainer}>
        <PieChart
          data={pieData}
          donut
          radius={90}
          innerRadius={40}
          // showText
          textSize={12}
          textColor="#FFFFFF"
          centerLabelComponent={() => (
            <Text style={[styles.centerLabel, valueStyle]}>{total} items</Text>
          )}
        />
      </View>
      <View style={styles.legendContainer}>
        {pieData.map((item, index) => (
          <View key={index} style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: item.color }]} />
            <Text style={[styles.legendText, labelStyle]}>
              {item.text}: {Math.round((item.value / total) * 100)}%
            </Text>
          </View>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    padding: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 16,
    textAlign: 'center',
    color: BaseColors.dark_pri,
  },
  chartContainer: {
    alignItems: 'center',
    marginVertical: 16,
  },
  centerLabel: {
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
    color: BaseColors.dark_pri,
  },
  legendContainer: {
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  legendText: {
    fontSize: 14,
    color: BaseColors.dark_pri,
  },
  noDataText: {
    textAlign: 'center',
    color: BaseColors.grey,
    marginVertical: 24,
  },
});

export default PostureDistChart;