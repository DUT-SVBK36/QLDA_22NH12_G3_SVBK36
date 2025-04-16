import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { BarChart } from 'react-native-gifted-charts';
import { PostureImprovement } from '@/models/analytics';
import { BaseColors } from '@/constants/Colors';
import { Fonts } from '@/shared/SharedStyles';
import { AnalyticsService } from '@/services/analytics';

interface PostureImprovementChartProps {
    data: PostureImprovement;
    title?: string;
    titleStyle?: any;
    labelStyle?: any;
    valueStyle?: any;
}

const PostureImprovementChart: React.FC<PostureImprovementChartProps> = ({ 
    data, 
    title = 'Posture Improvement',
    titleStyle = {},
    labelStyle = {},
    valueStyle = {}
}) => {
    if (!data || !data.improvement_data || !Array.isArray(data.improvement_data)) {
        return (
            <View style={styles.container}>
                <Text style={[styles.title, titleStyle]}>{title}</Text>
                <Text style={[styles.noDataText, labelStyle]}>No improvement data available</Text>
            </View>
        );
    }

    // Sort data by date
    const sortedData = [...data.improvement_data]
        .filter(item => item && item.good_percentage !== null && item.date !== null)
        .sort((a, b) => {
            if (!a.date || !b.date) return 0;
            return new Date(a.date).getTime() - new Date(b.date).getTime();
        });

    if (sortedData.length < 2) {
        return (
            <View style={styles.container}>
                <Text style={[styles.title, titleStyle]}>{title}</Text>
                <Text style={[styles.noDataText, labelStyle]}>Insufficient data for comparison (need at least 2 sessions)</Text>
            </View>
        );
    }

    // Get the most recent two sessions for comparison
    const previousSession = sortedData[sortedData.length - 2];
    const currentSession = sortedData[sortedData.length - 1];

    // Transform improvement data to bar chart format for comparison
    const barData = [
        {
            value: previousSession.good_percentage || 0,
            label: 'Good',
            frontColor: BaseColors.grey,
            topLabelComponent: () => (
                <Text style={[styles.barLabel, labelStyle, { color: BaseColors.dark_pri }]}>
                    Previous
                </Text>
            ),
        },
        {
            value: currentSession.good_percentage || 0,
            label: ' ',
            frontColor: (currentSession.good_percentage || 0) > (previousSession.good_percentage || 0) ? 
                BaseColors.primary : BaseColors.red,
            topLabelComponent: () => (
                <Text style={[styles.barLabel, valueStyle, { 
                    color: (currentSession.good_percentage || 0) > (previousSession.good_percentage || 0) ? 
                        BaseColors.primary : BaseColors.red 
                }]}>
                    Current {(currentSession.good_percentage || 0) > (previousSession.good_percentage || 0) ? '▲' : '▼'}
                </Text>
            ),
        },
    ];

    // Calculate overall improvement
    const change = (currentSession.good_percentage || 0) - (previousSession.good_percentage || 0);
    const overallImproved = change > 0;

    return (
        <View style={styles.container}>
            <Text style={[styles.title, titleStyle]}>{title}</Text>
            <Text style={[styles.subtitle, valueStyle, { color: overallImproved ? BaseColors.primary : BaseColors.red }]}>
                Overall: {overallImproved ? 'Improved' : 'Declined'} by {Math.abs(change).toFixed(1)}%
            </Text>
            <View style={styles.chartContainer}>
                <BarChart
                    data={barData}
                    width={Dimensions.get('window').width - 64}
                    height={220}
                    barWidth={20}
                    spacing={8}
                    barBorderRadius={4}
                    yAxisThickness={1}
                    xAxisThickness={1}
                    yAxisTextStyle={[styles.axisText, labelStyle]}
                    xAxisLabelTextStyle={[styles.axisText, labelStyle]}
                    yAxisLabelSuffix="%"
                    noOfSections={5}
                    maxValue={100}
                />
            </View>
            <View style={styles.legendContainer}>
                <View style={styles.legendItem}>
                    <View style={[styles.legendColor, { backgroundColor: BaseColors.grey }]} />
                    <Text style={[styles.legendText, labelStyle]}>Previous Session ({previousSession.date})</Text>
                </View>
                <View style={styles.legendItem}>
                    <View style={[styles.legendColor, { backgroundColor: BaseColors.primary }]} />
                    <Text style={[styles.legendText, labelStyle]}>Current Session ({currentSession.date})</Text>
                </View>
            </View>
            <Text style={[styles.timeframeText, labelStyle]}>
                Comparing good posture percentages between sessions
            </Text>
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
        fontWeight: '600',
    },
    chartContainer: {
        alignItems: 'center',
        marginVertical: 16,
    },
    barLabel: {
        fontSize: 10,
        marginTop: 4,
    },
    axisText: {
        color: BaseColors.dark_pri,
        fontSize: 10,
    },
    legendContainer: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginTop: 16,
        flexWrap: 'wrap',
    },
    legendItem: {
        flexDirection: 'row',
        alignItems: 'center',
        marginRight: 16,
        marginBottom: 8,
    },
    legendColor: {
        width: 12,
        height: 12,
        borderRadius: 6,
        marginRight: 8,
    },
    legendText: {
        fontSize: 12,
        color: BaseColors.dark_pri,
    },
    timeframeText: {
        fontSize: 12,
        color: BaseColors.grey,
        textAlign: 'center',
        marginTop: 8,
    },
    noDataText: {
        textAlign: 'center',
        color: BaseColors.grey,
        marginVertical: 24,
    },
});

export default PostureImprovementChart;