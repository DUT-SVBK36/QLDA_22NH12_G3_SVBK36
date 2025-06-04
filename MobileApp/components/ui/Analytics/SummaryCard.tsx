import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Summary } from '@/models/charts/summary.model';

interface SummaryCardProps {
  data: Summary | null;
  titleStyle?: any;
  labelStyle?: any;
  valueStyle?: any;
}

// Plain color constants
const COLORS = {
  primary: '#2196F3',
  primaryLight: '#E3F2FD',
  green: '#4CAF50',
  greenLight: '#E8F5E8',
  orange: '#FF9800',
  orangeLight: '#FFF3E0',
  red: '#F44336',
  redLight: '#FFEBEE',
  grey: '#757575',
  lightGrey: '#F5F5F5',
  white: '#FFFFFF',
  dark: '#212121',
  background: '#F8F9FA',
};

const SummaryCard: React.FC<SummaryCardProps> = ({
  data,
  titleStyle = {},
  labelStyle = {},
  valueStyle = {},
}) => {
  if (!data) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Ionicons name="analytics-outline" size={20} color={COLORS.primary} />
          <Text style={[styles.title, titleStyle]}>Overview Summary</Text>
        </View>
        <Text style={[styles.noDataText, labelStyle]}>No summary data available</Text>
      </View>
    );
  }

  // Format duration from seconds to readable format
  const formatDuration = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  // Format date to readable format
  const formatDate = (dateString: string): string => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  // Calculate days between first and latest session
  const calculateUsageDays = (): number => {
    try {
      const firstDate = new Date(data.first_session_date);
      const latestDate = new Date(data.latest_session_date);
      const diffTime = Math.abs(latestDate.getTime() - firstDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays || 1;
    } catch {
      return 1;
    }
  };

  const usageDays = calculateUsageDays();

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="analytics-outline" size={20} color={COLORS.primary} />
        <Text style={[styles.title, titleStyle]}>Overview Summary</Text>
      </View>

      {/* Main Stats Grid */}
      <View style={styles.statsGrid}>
        <View style={[styles.statCard, styles.primaryCard]}>
          <Ionicons name="calendar-outline" size={18} color={COLORS.primary} />
          <Text style={[styles.statValue, valueStyle]}>{data.total_sessions}</Text>
          <Text style={[styles.statLabel, labelStyle]}>Sessions</Text>
        </View>

        <View style={[styles.statCard, styles.greenCard]}>
          <Ionicons name="time-outline" size={18} color={COLORS.green} />
          <Text style={[styles.statValue, valueStyle]}>{formatDuration(data.total_usage_time)}</Text>
          <Text style={[styles.statLabel, labelStyle]}>Usage Time</Text>
        </View>

        <View style={[styles.statCard, styles.orangeCard]}>
          <Ionicons name="trending-up-outline" size={18} color={COLORS.orange} />
          <Text style={[styles.statValue, valueStyle]}>{usageDays}</Text>
          <Text style={[styles.statLabel, labelStyle]}>Days Active</Text>
        </View>

        <View style={[styles.statCard, styles.successCard]}>
          <Ionicons name="checkmark-circle-outline" size={18} color={COLORS.green} />
          <Text style={[styles.statValue, valueStyle]}>{data.corrected_postures}</Text>
          <Text style={[styles.statLabel, labelStyle]}>Corrections</Text>
        </View>
      </View>

      {/* Posture Health Section */}
      <View style={styles.postureSection}>
        <Text style={[styles.sectionTitle, titleStyle]}>Posture Health</Text>
        <View style={styles.postureBar}>
          <View 
            style={[
              styles.postureGood, 
              { width: `${data.good_posture_percentage}%` }
            ]} 
          />
          <View 
            style={[
              styles.postureBad, 
              { width: `${data.bad_posture_percentage}%` }
            ]} 
          />
        </View>
        
        <View style={styles.postureStats}>
          <View style={styles.postureItem}>
            <View style={[styles.postureDot, { backgroundColor: COLORS.green }]} />
            <Text style={[styles.postureLabel, labelStyle]}>Good</Text>
            <Text style={[styles.postureValue, valueStyle]}>
              {data.good_posture_percentage.toFixed(1)}%
            </Text>
          </View>
          
          <View style={styles.postureItem}>
            <View style={[styles.postureDot, { backgroundColor: COLORS.red }]} />
            <Text style={[styles.postureLabel, labelStyle]}>Poor</Text>
            <Text style={[styles.postureValue, valueStyle]}>
              {data.bad_posture_percentage.toFixed(1)}%
            </Text>
          </View>
        </View>
      </View>

      {/* Duration Breakdown */}
      <View style={styles.durationSection}>
        <Text style={[styles.sectionTitle, titleStyle]}>Time Breakdown</Text>
        <View style={styles.durationRow}>
          <View style={styles.durationItem}>
            <Ionicons name="checkmark-circle" size={16} color={COLORS.green} />
            <View style={styles.durationText}>
              <Text style={[styles.durationValue, valueStyle]}>
                {formatDuration(data.good_posture_duration)}
              </Text>
              <Text style={[styles.durationLabel, labelStyle]}>Good Posture</Text>
            </View>
          </View>
          
          <View style={styles.durationItem}>
            <Ionicons name="alert-circle" size={16} color={COLORS.red} />
            <View style={styles.durationText}>
              <Text style={[styles.durationValue, valueStyle]}>
                {formatDuration(data.bad_posture_duration)}
              </Text>
              <Text style={[styles.durationLabel, labelStyle]}>Poor Posture</Text>
            </View>
          </View>
        </View>
      </View>

      {/* Usage Period */}
      <View style={styles.periodSection}>
        <Text style={[styles.periodText, labelStyle]}>
          📅 Using since {formatDate(data.first_session_date)}
        </Text>
        <Text style={[styles.lastSessionText, labelStyle]}>
          🕐 Last session: {formatDate(data.latest_session_date)}
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.white,
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 6,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.dark,
    marginLeft: 10,
  },
  
  // Stats Grid
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 24,
    gap: 12,
  },
  statCard: {
    width: '47%',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    minHeight: 90,
    justifyContent: 'center',
  },
  primaryCard: {
    backgroundColor: COLORS.primaryLight,
  },
  greenCard: {
    backgroundColor: COLORS.greenLight,
  },
  orangeCard: {
    backgroundColor: COLORS.orangeLight,
  },
  successCard: {
    backgroundColor: COLORS.greenLight,
  },
  statValue: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.dark,
    marginVertical: 6,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.grey,
    textAlign: 'center',
    fontWeight: '500',
  },
  
  // Posture Section
  postureSection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: COLORS.dark,
    marginBottom: 12,
  },
  postureBar: {
    flexDirection: 'row',
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.lightGrey,
    marginBottom: 12,
    overflow: 'hidden',
  },
  postureGood: {
    backgroundColor: COLORS.green,
    height: '100%',
  },
  postureBad: {
    backgroundColor: COLORS.red,
    height: '100%',
  },
  postureStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  postureItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  postureDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 8,
  },
  postureLabel: {
    fontSize: 13,
    color: COLORS.grey,
    marginRight: 6,
  },
  postureValue: {
    fontSize: 15,
    fontWeight: '600',
    color: COLORS.dark,
  },
  
  // Duration Section
  durationSection: {
    marginBottom: 20,
  },
  durationRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  durationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  durationText: {
    marginLeft: 8,
  },
  durationValue: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.dark,
  },
  durationLabel: {
    fontSize: 11,
    color: COLORS.grey,
  },
  
  // Period Section
  periodSection: {
    borderTopWidth: 1,
    borderTopColor: COLORS.lightGrey,
    paddingTop: 16,
    alignItems: 'center',
  },
  periodText: {
    fontSize: 12,
    color: COLORS.grey,
    textAlign: 'center',
    marginBottom: 4,
  },
  lastSessionText: {
    fontSize: 12,
    color: COLORS.grey,
    textAlign: 'center',
  },
  
  // No Data
  noDataText: {
    textAlign: 'center',
    color: COLORS.grey,
    marginVertical: 24,
    fontSize: 14,
    fontStyle: 'italic',
  },
});

export default SummaryCard;