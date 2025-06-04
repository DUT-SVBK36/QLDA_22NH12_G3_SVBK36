import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-gifted-charts';
import { PostureImprovement } from '@/models/analytics';
import { BaseColors } from '@/constants/Colors';
import { Fonts } from '@/shared/SharedStyles';
import { Ionicons } from '@expo/vector-icons';

interface PostureImprovementChartProps {
    data: PostureImprovement;
    title?: string;
    titleStyle?: any;
    labelStyle?: any;
    valueStyle?: any;
}

// Plain color constants
const COLORS = {
    primary: '#2196F3',        // Blue
    primaryLight: '#E3F2FD',   // Light blue
    red: '#F44336',            // Red  
    redLight: '#FFEBEE',       // Light red
    green: '#4CAF50',          // Green
    orange: '#FF9800',         // Orange
    grey: '#757575',           // Grey
    lightGrey: '#E0E0E0',      // Light grey
    white: '#FFFFFF',          // White
    dark: '#212121',           // Dark text
    background: '#F5F5F5',     // Background
};

const PostureImprovementChart: React.FC<PostureImprovementChartProps> = ({ 
    data, 
    title = 'Posture Improvement Trends By Time',
    titleStyle = {},
    labelStyle = {},
    valueStyle = {}
}) => {
    if (!data || !data.good_posture_trend || !data.bad_posture_trend) {
        return (
            <View style={styles.container}>
                <Text style={[styles.title, titleStyle]}>{title}</Text>
                <Text style={[styles.noDataText, labelStyle]}>No trend data available</Text>
            </View>
        );
    }

    // Filter and transform good posture trend data
    const goodTrendData = data.good_posture_trend
        .filter(item => item && item.value !== null && item.date !== null)
        .sort((a, b) => {
            if (!a.date || !b.date) return 0;
            return new Date(a.date).getTime() - new Date(b.date).getTime();
        })
        .map((item, index) => ({
            value: item.value || 0,
            label: formatDateLabel(item.date || ''),
            dataPointText: `${(item.value || 0).toFixed(1)}%`,
        }));

    // Filter and transform bad posture trend data
    const badTrendData = data.bad_posture_trend
        .filter(item => item && item.value !== null && item.date !== null)
        .sort((a, b) => {
            if (!a.date || !b.date) return 0;
            return new Date(a.date).getTime() - new Date(b.date).getTime();
        })
        .map((item, index) => ({
            value: item.value || 0,
            label: formatDateLabel(item.date || ''),
            dataPointText: `${(item.value || 0).toFixed(1)}%`,
        }));

    if (goodTrendData.length === 0 && badTrendData.length === 0) {
        return (
            <View style={styles.container}>
                <Text style={[styles.title, titleStyle]}>{title}</Text>
                <Text style={[styles.noDataText, labelStyle]}>No valid trend data available</Text>
            </View>
        );
    }

    // Generate summary based on overall improvement
    const getSummary = (overallImprovement: number | null) => {
        if (overallImprovement === null) {
            return {
                text: "No improvement data",
                icon: "help-circle-outline" as const,
                color: COLORS.grey
            };
        }

        if (overallImprovement <= 0) {
            return {
                text: "Need to improve more",
                icon: "trending-down-outline" as const,
                color: COLORS.red
            };
        } else if (overallImprovement > 50) {
            return {
                text: "You are doing it right!",
                icon: "trophy-outline" as const,
                color: COLORS.green
            };
        } else {
            return {
                text: "Keep it up!",
                icon: "trending-up-outline" as const,
                color: COLORS.orange
            };
        }
    };

    const summary = getSummary(data.overall_improvement);

    // Calculate chart dimensions
    const screenWidth = Dimensions.get('window').width;
    const chartWidth = screenWidth - 64;

    // Calculate spacing based on the longer dataset
    const maxDataPoints = Math.max(goodTrendData.length, badTrendData.length);
    const spacing = maxDataPoints > 1 ? chartWidth / (maxDataPoints - 1) : chartWidth;

    return (
        <View style={styles.container}>
            <Text style={[styles.title, titleStyle]}>{title}</Text>
            
            {/* Summary Section */}
            <View style={styles.summaryContainer}>
                <Text style={[styles.summaryText, valueStyle, { color: summary.color }]}>
                    {summary.text}
                </Text>
            </View>

            {/* Chart Container */}
            <View style={styles.chartContainer}>
                <LineChart
                    data={goodTrendData}
                    width={chartWidth}
                    height={220}
                    color1={COLORS.primary}
                    thickness1={3}
                    thickness2={3}
                    areaChart
                    areaChart1
                    areaChart2
                    startFillColor1={COLORS.primary}
                    endFillColor1={COLORS.primaryLight}
                    startOpacity={0.3}
                    endOpacity={0.1}
                    curved
                    showDataPointOnFocus
                    showVerticalLines
                    hideDataPoints1
                    yAxisColor={COLORS.grey}
                    xAxisColor={COLORS.grey}
                    yAxisThickness={1}
                    xAxisThickness={1}
                    yAxisTextStyle={[styles.axisText, labelStyle]}
                    xAxisLabelTextStyle={[styles.axisTextX, labelStyle]}
                    yAxisLabelSuffix="%"
                    noOfSections={5}
                    yAxisOffset={10}
                    maxValue={100}
                    rulesType="solid"
                    rulesColor={COLORS.lightGrey}
                    spacing={spacing}
                />
            </View>

            {/* Legend */}
            <View style={styles.legendContainer}>
                <View style={styles.legendItem}>
                    <View style={[styles.legendColor, { backgroundColor: COLORS.primary }]} />
                    <Text style={[styles.legendText, labelStyle]}>Good Posture Trend</Text>
                </View>
                {/* <View style={styles.legendItem}>
                    <View style={[styles.legendColor, { backgroundColor: COLORS.red }]} />
                    <Text style={[styles.legendText, labelStyle]}>Bad Posture Trend</Text>
                </View> */}
            </View>

            {/* Data Range Info */}
            <Text style={[styles.dataRangeText, labelStyle]}>
                Showing trends across {maxDataPoints} sessions
            </Text>
        </View>
    );
};

// Helper function to format date labels from ISO format: 2025-06-04T08:43:50.872000
const formatDateLabel = (dateString: string): string => {
    try {
        // Parse the ISO date string
        const date = new Date(dateString);
        
        // Check if the date is valid
        if (isNaN(date.getTime())) {
            // If invalid, try to extract just the date part
            const datePart = dateString.split('T')[0];
            const fallbackDate = new Date(datePart);
            if (!isNaN(fallbackDate.getTime())) {
                return fallbackDate.toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric' 
                });
            }
            return dateString.substring(5, 10); // MM-DD fallback
        }
        
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        });
    } catch (error) {
        // Fallback: extract MM-DD from the string
        try {
            const datePart = dateString.split('T')[0]; // Get "2025-06-04"
            const [year, month, day] = datePart.split('-');
            const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
            return date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
            });
        } catch {
            return dateString.substring(5, 10); // Return MM-DD as last resort
        }
    }
};

const styles = StyleSheet.create({
    container: {
        backgroundColor: COLORS.white,
        borderRadius: 12,
        padding: 16,
        marginVertical: 8,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 3 },
        shadowOpacity: 0.12,
        shadowRadius: 6,
        elevation: 5,
    },
    title: {
        fontSize: 18,
        fontWeight: '600',
        marginBottom: 12,
        textAlign: 'center',
        color: COLORS.dark,
    },
    summaryContainer: {
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: COLORS.background,
        borderRadius: 8,
        padding: 12,
        marginBottom: 16,
    },
    summaryText: {
        fontSize: 12,
        fontWeight: '600',
        marginLeft: 8,
    },
    improvementValue: {
        fontSize: 12,
        color: COLORS.grey,
        marginLeft: 4,
    },
    chartContainer: {
        alignItems: 'center',
        marginVertical: 16,
        overflow: 'hidden',
    },
    axisText: {
        color: COLORS.dark,
        fontSize: 8,
        fontWeight: '500',
        
    }, 
    axisTextX: {
        color: COLORS.dark,
        fontSize: 8,
        fontWeight: '500',
        display: 'none', // Hide X-axis labels
    },
    legendContainer: {
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 16,
        gap: 20,
    },
    legendItem: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    legendColor: {
        width: 12,
        height: 12,
        borderRadius: 6,
        marginRight: 6,
    },
    legendText: {
        fontSize: 12,
        color: COLORS.dark,
        fontWeight: '500',
    },
    dataRangeText: {
        fontSize: 11,
        color: COLORS.grey,
        textAlign: 'center',
        marginTop: 8,
        fontStyle: 'italic',
    },
    noDataText: {
        textAlign: 'center',
        color: COLORS.grey,
        marginVertical: 24,
        fontSize: 14,
    },
});

export default PostureImprovementChart;