import RecentSession from "@/components/ui/_Detect/RecentSession";
import WrongPostureCard from "@/components/ui/_Detect/WrongPostureCard";
import CustomButton from "@/components/ui/CustomButton";
import CustomWindow from "@/components/ui/CustomWindow";
import { BaseColors } from "@/constants/Colors";
import { useSocket } from "@/contexts/DetectContext";
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
  const { socket, isConnected, connect, disconnect, emit } = useSocket();

  useEffect(() => {
    // Connect to socket when component mounts
    if(!socket) return;
    connect();

    // Listen for posture events
    socket.on('posture', (data: PostureData) => {
      console.log('Received posture data:', data);
      setWrongPostures(prev => [...prev, data]);
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
      socket.off('posture');
      socket.off('connect');
      socket.off('disconnect');
      disconnect();
    };
  }, [socket]);

  // Update the event handlers in detect.tsx
  const handleStartDetection = () => {
    if (socket && isConnected) {
      const detectMessage = {
        type: 'detect',
        client: 'mobile',
        timestamp: new Date().toISOString()
      };
      emit('message', detectMessage);
      console.log('Started detection');
      setIsStarted(true);
      setWrongPostures([]);
    }
  };
  
  const handleStopDetection = () => {
    if (socket && isConnected) {
      const stopMessage = {
        type: 'stopDetect',
        client: 'mobile',
        timestamp: new Date().toISOString()
      };
      emit('message', stopMessage);
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
    color: BaseColors.dark_blue,
    textAlign: "center",
    padding: 8
  },
  noPostures: {
    color: BaseColors.secondary,
    textAlign: "center",
    padding: 16
  }
});