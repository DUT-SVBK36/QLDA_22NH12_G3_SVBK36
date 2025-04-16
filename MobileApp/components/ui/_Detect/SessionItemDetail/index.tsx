import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';
import { Fonts } from '@/shared/SharedStyles';
import { SessionItem } from '@/models/session.model';
import { usePopupStore } from '@/services/popup';
import styles from './styles.css';
import { PostureMappedString } from '@/utils/postures-map';

interface SessionItemDetailProps {
  item: SessionItem;
}

const SessionItemDetail: React.FC<SessionItemDetailProps> = ({ item }) => {
  const { showPopup } = usePopupStore();
  
  return (
    <TouchableOpacity 
      style={styles.itemContainer}
      onPress={() => showPopup(item)}
      activeOpacity={0.7}
    >
      {item.image && (
        <Image 
          source={{ uri: item.image }} 
          style={styles.itemImage} 
          resizeMode="cover"
        />
      )}
      <View style={styles.itemContent}>
        <Text style={[Fonts.bodySmall, styles.itemTitle]}>
          {PostureMappedString[item.label_name]}
        </Text>
        <Text style={[Fonts.small, styles.itemTime]}>
          Time: {new Date(item.timestamp).toTimeString()}
        </Text>
        <Text style={[Fonts.small, styles.itemAccuracy]}>
          Accuracy: {Math.round(item.accuracy * 100)}%
        </Text>
        {item.label_recommendation && (
          <Text style={[Fonts.small, styles.itemRecommendation]}>
            {item.label_recommendation}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );
};

export default SessionItemDetail;