import RecentSession from "@/components/ui/_Detect/RecentSession";
import WrongPostureCard from "@/components/ui/_Detect/WrongPostureCard";
import CustomButton from "@/components/ui/CustomButton";
import CustomWindow from "@/components/ui/CustomWindow";
import { BaseColors } from "@/constants/Colors";
import { useSocket } from "@/contexts/DetectContext";
import { Frame, PostureUpdate, Statistics } from "@/models/posture.model";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { useEffect, useState } from "react";
import { ImageBackground, ScrollView, StyleSheet, Text, View} from "react-native";

interface PostureData {
  id: string;
  image: string;
  posture: string;
  accuracy: number;
  timestamp: string;
}

export default function DetectScreen() {
  const [isStarted, setIsStarted] = useState(false);
  const [wrongPostures, setWrongPostures] = useState<PostureData[]>([]);
  const [livePostureData, setLivePostureData] = useState<PostureUpdate | null>(null);
  const { socket, isConnected, connect, disconnect, emit } = useSocket();

  useEffect(() => {
    // Connect to socket when component mounts
    if(!socket) return;
    connect();

    // Listen for posture events
    socket.on('posture_update', (data: PostureUpdate) => {
      console.log('Raw posture update data:', data); // Log the raw data first
      setLivePostureData(data);
    });
    socket.on('statistics', (data: Statistics) => {
      console.log('Statistics:', data);
    });
    socket.on('frame', (data: Frame) => {
      console.log('Image:', data);
      setWrongPostures(prev => [...prev, {
        id: new Date().toISOString(),
        image: data.image,
        posture: data.posture.posture_vi,
        accuracy: data.posture.confidence,
        timestamp: data.timestamp
      }]);
    });
    // Add connection status listener
    socket.on('connect', () => {
      console.log('Connected to detection server');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from detection server');
    });

    // Clean up event listeners
    return () => {
      socket.off('posture_update');
      socket.off('statistics');
      socket.off('frame')
      socket.off('connect');
      socket.off('disconnect');
      disconnect();
    };
  }, [socket]);

  // Update the event handlers in detect.tsx
  const handleStartDetection = () => {
    if (socket && isConnected) {
      const message = {
        action: "start"
      }
      emit('action', message);
      console.log('Started detection');
      setIsStarted(true);
      setWrongPostures([]);
    }
  };
  
  const handleStopDetection = () => {
    if (socket && isConnected) {
      const message = {
        action: "stop"
      }
      emit('action', message);
      console.log('Stopped detection');
      setIsStarted(false);
    }
  };

  return (
    <>
      <ImageBackground 
        source={SharedAssets.Bg}
        resizeMode="cover"
        style={{
          width: "100%",
          height: "100%",
          position: "absolute",
        }}
      />
      <ScrollView style={[
          Container.base
      ]}
        contentContainerStyle={[
          Container.baseContent,
        ]}
      >
        <Text
          style={[
            Fonts.h1Large,
            styles.title
          ]}
        >
          Detect
        </Text>
        {/* camera feed  */}
        {isStarted 
          ? 
          <CustomWindow
            title="Status"
          >
            <Text style={styles.statusText}>
              {isConnected ? 'Detection is active' : 'Connecting...'}
            </Text>
            {livePostureData && (
              <Text style={styles.statusText}>
                Current posture: {livePostureData.posture.posture_vi} 
                Accuracy: {(livePostureData.posture.confidence * 100).toFixed(2)}%
              </Text>
            )}
          </CustomWindow>
          : 
          <RecentSession />
        }
        
        <CustomButton 
          label={isStarted ? "Stop Detection" : "Start Detection"}
          onPress={isStarted ? handleStopDetection : handleStartDetection}
          variant="red"
        />

        
          <CustomWindow
            title="Wrong Postures"
          >
            {wrongPostures.length === 0 ? (
              <Text style={styles.noPostures}>No wrong postures detected yet</Text>
            ) : (
              wrongPostures.map((posture, index) => (
                <WrongPostureCard
                  key={posture.id || index}
                  image={posture.image}
                  detectedPosture={posture.posture}
                  accuracy={posture.accuracy}
                  timestamp={posture.timestamp}
                />
              ))
            )}
          </CustomWindow>
        
      </ScrollView>
    </>
  )
}

const styles = StyleSheet.create({
  title: {
    color: BaseColors.dark_pri,
    textAlign: "left",
    width: "100%",
    marginBottom: 12
  },
  statusText: {
    color: "white",
    fontFamily: "Lexend",
    marginLeft: 8
  },
  noPostures: {
    color: BaseColors.secondary,
    textAlign: "center",
    padding: 16
  }
});