import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { BarChart } from 'react-native-gifted-charts';
import { PostureDuration } from '@/models/analytics';
import { BaseColors } from '@/constants/Colors';

interface PostureDurationChartProps {
  data: PostureDuration;
  title?: string;
  titleStyle?: any;
  labelStyle?: any;
  valueStyle?: any;
}

const PostureDurationChart: React.FC<PostureDurationChartProps> = ({
  data,
  title = 'Posture Duration',
  titleStyle = {},
  labelStyle = {},
  valueStyle = {},
}) => {
  if (!data || !data.durations) {
    return (
      <View style={styles.container}>
        <Text style={[styles.title, titleStyle]}>{title}</Text>
        <Text style={[styles.noDataText, labelStyle]}>No duration data available</Text>
      </View>
    );
  }

  // Define posture name mapping
  const postureNames: Record<string, string> = {
    good_sitting_side: 'Good Posture',
    too_lean_right_side: 'Leaning Right',
    too_lean_left_side: 'Leaning Left',
    bad_sitting_backward_side: 'Leaning Backward',
    bad_sitting_forward_side: 'Leaning Forward',
    neck_wrong_position: 'Head Tilt',
    leg_wrong_position: 'Leg Position',
  };

  // Define color mapping
  const postureColors: Record<string, string> = {
    good_sitting_side: '#4CAF50',
    too_lean_right_side: '#FFEB3B',
    too_lean_left_side: '#2196F3',
    bad_sitting_backward_side: '#9C27B0',
    bad_sitting_forward_side: '#FF9800',
    neck_wrong_position: '#F44336',
    leg_wrong_position: '#795548',
  };

  // Transform duration data to bar chart format
  const barData = Object.entries(data.durations)
    .filter(([_, item]) => item && item.total_duration !== null)
    .map(([key, item]) => {
      const displayName = postureNames[key] || key;
      const color = postureColors[key] || '#607D8B';
      const durationMinutes = Math.round((item?.total_duration || 0) / 60);
      const percentage = item?.percentage || 0;

      return {
        value: durationMinutes,
        label: displayName,
        frontColor: color,
        sideColor: color,
        topColor: color,
        percentage: percentage,
        topLabelComponent: () => (
          <View style={styles.labelContainer}>
            <Text style={[styles.barLabel, valueStyle]}>
              {durationMinutes} min
            </Text>
            <Text style={[styles.percentageLabel, valueStyle]}>
              {Math.round(percentage)}%
            </Text>
          </View>
        ),
      };
    })
    .sort((a, b) => b.value - a.value); // Sort by duration descending

  if (barData.length === 0) {
    return (
      <View style={styles.container}>
        <Text style={[styles.title, titleStyle]}>{title}</Text>
        <Text style={[styles.noDataText, labelStyle]}>No duration data available</Text>
      </View>
    );
  }

  const totalDurationMinutes = Math.round((data.total_duration || 0) / 60);

  return (
    <View style={styles.container}>
      <Text style={[styles.title, titleStyle]}>{title}</Text>
      <Text style={[styles.subtitle, labelStyle]}>
        Total Duration: {totalDurationMinutes} minutes
      </Text>
      <View style={styles.chartContainer}>
        <BarChart
          data={barData}
          width={Dimensions.get('window').width - 64}
          height={220}
          barWidth={30}
          spacing={24}
          barBorderRadius={4}
          noOfSections={5}
          yAxisThickness={1}
          xAxisThickness={1}
          yAxisTextStyle={[styles.axisText, labelStyle]}
          xAxisLabelTextStyle={[styles.axisText, labelStyle]}
          backgroundColor={BaseColors.grey}
          showLine
          lineConfig={{
            color: BaseColors.dark_pri,
            thickness: 1,
            curved: true,
            dataPointsColor: BaseColors.dark_pri,
            dataPointsRadius: 3,
          }}
        />
      </View>

      {/* Legend with severity levels */}
      <View style={styles.legendContainer}>
        {barData.map((item, index) => (
          <View key={index} style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: item.frontColor }]} />
            <View style={styles.legendTextContainer}>
              <Text style={[styles.legendText, labelStyle]}>{item.label}</Text>
              <Text style={[styles.legendSubtext, labelStyle]}>
                {item.value} min ({Math.round(item.percentage)}%)
              </Text>
            </View>
          </View>
        ))}
      </View>

      <Text style={[styles.axisTitle, labelStyle]}>Minutes</Text>
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
    marginBottom: 8,
    textAlign: 'center',
    color: BaseColors.dark_pri,
  },
  subtitle: {
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 16,
    color: BaseColors.dark_pri,
  },
  chartContainer: {
    alignItems: 'center',
    marginVertical: 16,
  },
  barLabel: {
    color: BaseColors.dark_pri,
    fontSize: 12,
    marginTop: 4,
  },
  axisText: {
    color: BaseColors.dark_pri,
    fontSize: 10,
  },
  axisTitle: {
    textAlign: 'center',
    fontSize: 12,
    color: BaseColors.dark_pri,
    marginTop: 8,
  },
  noDataText: {
    textAlign: 'center',
    color: BaseColors.grey,
    marginVertical: 24,
  },
  labelContainer: {
    alignItems: 'center',
    paddingTop: 4,
  },
  percentageLabel: {
    color: BaseColors.dark_pri,
    fontSize: 10,
    marginTop: 2,
  },
  legendContainer: {
    marginTop: 16,
    paddingHorizontal: 8,
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
  legendTextContainer: {
    flex: 1,
  },
  legendText: {
    fontSize: 12,
    color: BaseColors.dark_pri,
    fontWeight: '500',
  },
  legendSubtext: {
    fontSize: 10,
    color: BaseColors.grey,
    marginTop: 2,
  },
});

export default PostureDurationChart;