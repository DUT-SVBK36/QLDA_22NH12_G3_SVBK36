import React from 'react';
import { View, Text, Modal, Image, TouchableOpacity, TouchableWithoutFeedback } from 'react-native';
import { Fonts } from '@/shared/SharedStyles';
import { BaseColors } from '@/constants/Colors';
import styles from './styles.css';
import { PostureMappedString } from '@/utils/postures-map';

interface PopUpProps {
  visible: boolean;
  onClose: () => void;
  image?: string;
  label: string;
  accuracy: number;
  timestamp: number;
  recommendation?: string;
}

const PopUp: React.FC<PopUpProps> = ({ 
  visible, 
  onClose, 
  image, 
  label, 
  accuracy, 
  timestamp,
  recommendation
}) => {
  const formatTimespan = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString();
  };

  return (
    <Modal
      transparent={true}
      visible={visible}
      animationType="fade"
      onRequestClose={onClose}
    >
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.modalOverlay}>
          <TouchableWithoutFeedback onPress={e => e.stopPropagation()}>
            <View style={styles.modalContent}>
              <Text style={[Fonts.h2, styles.title]}>{PostureMappedString[label]}</Text>
              
              {image && (
                <View style={styles.imageContainer}>
                  <Image 
                    source={{ uri: image }} 
                    style={styles.image} 
                    resizeMode="cover"
                  />
                </View>
              )}
              
              <View style={styles.infoContainer}>
                <Text style={[Fonts.bodySmall, styles.infoText]}>
                  Time: {typeof timestamp == "number" ? formatTimespan(timestamp) : new Date(timestamp).toLocaleString("vi-VN", { hour12: false })}
                </Text>
                {/* <Text style={[Fonts.bodySmall, styles.infoText]}>
                  Accuracy: {Math.round(accuracy * 100) + 50}%
                </Text> */}
                {recommendation && (
                  <Text style={[Fonts.bodySmall, styles.recommendation]}>
                    {recommendation}
                  </Text>
                )}
              </View>
              
              <TouchableOpacity 
                style={styles.button} 
                onPress={onClose}
                activeOpacity={0.8}
              >
                <Text style={styles.buttonText}>OK</Text>
              </TouchableOpacity>
            </View>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
};

export default PopUp;