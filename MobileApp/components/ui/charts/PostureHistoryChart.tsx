import React, { useMemo } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-gifted-charts';
import { PostureHistory } from '@/models/analytics';
import { BaseColors } from '@/constants/Colors';
import { Fonts } from '@/shared/SharedStyles';

interface PostureHistoryChartProps {
  data: PostureHistory;
  title?: string;
  titleStyle?: any;
  labelStyle?: any;
  valueStyle?: any;
}

// Function to generate a random color
const getRandomColor = (seed: string) => {
  // Using the seed string to generate a consistent color for the same posture type
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  // Convert to hex color
  let color = '#';
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xFF;
    color += ('00' + value.toString(16)).substr(-2);
  }
  
  return color;
};

const PostureHistoryChart: React.FC<PostureHistoryChartProps> = ({ 
  data, 
  title = 'Posture History',
  titleStyle = {},
  labelStyle = {},
  valueStyle = {}
}) => {
  if (!data || !data.history || !Array.isArray(data.history) || data.history.length === 0) {
    return (
      <View style={styles.container}>
        <Text style={[styles.title, titleStyle]}>{title}</Text>
        <Text style={[styles.noDataText, labelStyle]}>No history data available</Text>
      </View>
    );
  }

  // Group history data by label_name
  const groupedData: Record<string, Array<any>> = {};
  
  // First, collect all unique dates for proper alignment
  const allDates = new Set<string>();
  data.history
    .filter(item => item && typeof item.accuracy === 'number' && item.start_time)
    .forEach(item => {
      const date = new Date(item.start_time || Date.now());
      allDates.add(date.toLocaleDateString());
    });
  
  // Process each history item
  data.history
    .filter(item => item && typeof item.accuracy === 'number' && item.label_name)
    .forEach(item => {
      const labelName = item.label_name || 'Unknown';
      if (!groupedData[labelName]) {
        groupedData[labelName] = [];
      }
      
      const date = new Date(item.start_time || Date.now());
      groupedData[labelName].push({
        value: Math.round(item.accuracy * 100),
        date: date,
        label: date.toLocaleDateString(),
        dataPointText: `${Math.round(item.accuracy * 100)}%`,
      });
    });

  // Check if we have any grouped data
  if (Object.keys(groupedData).length === 0) {
    return (
      <View style={styles.container}>
        <Text style={[styles.title, titleStyle]}>{title}</Text>
        <Text style={[styles.noDataText, labelStyle]}>No classified posture data available</Text>
      </View>
    );
  }

  // Define colors for different posture types with predefined ones
  const basePostureColors: Record<string, string> = {
    'Good Posture': '#4CAF50',
    'Leaning Forward': '#FF9800',
    'Leaning Backward': '#9C27B0',
    'Leaning Left': '#2196F3',
    'Leaning Right': '#FFEB3B',
    'Head Tilt': '#F44336',
    'Neck Strain': '#795548',
    'Slouching': '#607D8B',
  };

  // Generate complete color map including random colors for undefined types
  const postureColors = useMemo(() => {
    const colorMap: Record<string, string> = {...basePostureColors};
    
    // Add random colors for any posture types not in the predefined list
    Object.keys(groupedData).forEach(label => {
      if (!colorMap[label]) {
        colorMap[label] = getRandomColor(label);
      }
    });
    
    return colorMap;
  }, [groupedData]);

  // Sort data points by date for each posture type
  Object.keys(groupedData).forEach(label => {
    groupedData[label].sort((a, b) => a.date.getTime() - b.date.getTime());
  });

  // Format data for multi-line chart
  // We need to create line data for each posture type
  const lineData = Object.entries(groupedData).map(([label, sessions]) => {
    const color = postureColors[label] || getRandomColor(label);
    
    return {
      label,
      color,
      dataPoints: sessions.map(session => ({
        value: session.value,
        label: session.label,
        date: session.date
      }))
    };
  });

  // Create a properly formatted dataset for react-native-gifted-charts
  // The library expects an array of objects with specific properties for multiple lines
  const chartData = lineData.flatMap(line => {
    return line.dataPoints.map((point, index) => ({
      value: point.value,
      date: point.date,
      label: point.label,
      dataPointText: `${point.value}%`,
      dataPointColor: line.color,
      color: line.color,
      showDataPoint: true,
      lineColor: line.color,
      // Adding this to differentiate lines
      lineDash: line.label === 'Good Posture' ? [] : [3, 3],
      // If this is the first point in this line, set it as the starting point of a line segment
      customDataPoint: index === 0 ? () => (
        <View style={[styles.lineStartPoint, { backgroundColor: line.color, borderColor: line.color }]} />
      ) : undefined
    }));
  }).sort((a, b) => a.date.getTime() - b.date.getTime());

  return (
    <View style={styles.container}>
      <Text style={[styles.title, titleStyle]}>{title}</Text>
      <Text style={[styles.subtitle, labelStyle]}>
        Tracking accuracy by posture type over time
      </Text>
      
      <View style={styles.chartContainer}>
        <LineChart
          data={chartData}
          width={Dimensions.get('window').width - 64}
          height={240}
          noOfSections={5}
          yAxisThickness={1}
          xAxisThickness={1}
          yAxisTextStyle={[styles.axisText, labelStyle]}
          xAxisLabelTextStyle={[styles.axisText, labelStyle]}
          showFractionalValues
          maxValue={100}
          initialSpacing={10}
          yAxisLabelSuffix="%"
          hideDataPoints={false}
          dataPointsRadius={3}
          dataPointsColor2={BaseColors.dark_pri}
          textShiftY={-2}
          textShiftX={-5}
          textFontSize={8}
          curved
          spacing={50}
          rulesType="solid"
          rulesColor={BaseColors.dark_pri}
          xAxisColor={BaseColors.dark_pri}
          yAxisColor={BaseColors.dark_pri}
          hideRules={false}
          pointerConfig={{
            pointerStripHeight: 160,
            pointerStripColor: BaseColors.dark_pri,
            pointerStripWidth: 1,
            pointerColor: BaseColors.primary,
            radius: 5,
            pointerLabelWidth: 120,
            pointerLabelHeight: 35,
            showPointerStrip: true,
            activatePointersOnLongPress: true,
            autoAdjustPointerLabelPosition: true,
            pointerLabelComponent: (item: any) => (
              <View style={[styles.tooltip, { backgroundColor: item.color || BaseColors.dark_pri }]}>
                <Text style={[styles.tooltipText, valueStyle]}>
                  {item.label}: {item.value}%
                </Text>
                <Text style={[styles.tooltipSubtext, valueStyle]}>
                  {lineData.find(line => line.color === item.color)?.label || ''}
                </Text>
              </View>
            ),
          }}
        />
      </View>
      
      {/* Legend */}
      <View style={styles.legendContainer}>
        {lineData.map((line, index) => (
          <View key={index} style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: line.color }]} />
            <Text style={[styles.legendText, labelStyle]}>{line.label}</Text>
          </View>
        ))}
      </View>
      
      {/* Summary */}
      <View style={styles.summaryContainer}>
        {Object.entries(groupedData).map(([label, sessions], index) => {
          const avgAccuracy = sessions.reduce((sum, session) => sum + session.value, 0) / sessions.length;
          return (
            <View key={index} style={styles.summaryItem}>
              <Text style={[styles.summaryLabel, labelStyle]}>
                {label}: 
              </Text>
              <Text style={[styles.summaryValue, valueStyle, { 
                color: avgAccuracy >= 70 ? BaseColors.primary : BaseColors.red 
              }]}>
                {Math.round(avgAccuracy)}% avg ({sessions.length} sessions)
              </Text>
            </View>
          );
        })}
      </View>
      
      <Text style={[styles.axisTitle, labelStyle]}>Date</Text>
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
  axisText: {
    color: BaseColors.dark_pri,
    fontSize: 8, // Reduced from 10
  },
  axisTitle: {
    textAlign: 'center',
    fontSize: 10, // Reduced from 12
    color: BaseColors.dark_pri,
    marginTop: 8,
  },
  noDataText: {
    textAlign: 'center',
    color: BaseColors.inactive,
    marginVertical: 24,
  },
  tooltip: {
    padding: 6, // Reduced from 8
    borderRadius: 4,
  },
  tooltipText: {
    color: '#FFFFFF',
    fontSize: 10, // Reduced from 12
    fontWeight: '600',
  },
  tooltipSubtext: {
    color: '#FFFFFF',
    fontSize: 8, // Reduced from 10
    marginTop: 2,
  },
  legendContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 12, // Reduced from 16
    marginBottom: 6, // Reduced from 8
  },
  legendColor: {
    width: 10, // Reduced from 12
    height: 10, // Reduced from 12
    borderRadius: 5,
    marginRight: 6, // Reduced from 8
  },
  legendText: {
    fontSize: 10, // Reduced from 12
    color: BaseColors.dark_pri,
  },
  lineStartPoint: {
    width: 8, // Reduced from 10
    height: 8, // Reduced from 10
    borderRadius: 4,
    borderWidth: 2,
  },
  summaryContainer: {
    marginTop: 12, // Reduced from 16
  },
  summaryItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 3, // Reduced from 4
  },
  summaryLabel: {
    fontSize: 10, // Reduced from 12
    color: BaseColors.dark_pri,
    fontWeight: '500',
  },
  summaryValue: {
    fontSize: 10, // Reduced from 12
    fontWeight: '500',
  }
});

export default PostureHistoryChart;