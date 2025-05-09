import RecentSession from "@/components/ui/_Detect/RecentSession";
import WrongPostureCard from "@/components/ui/_Detect/WrongPostureCard";
import CustomButton from "@/components/ui/CustomButton";
import CustomWindow from "@/components/ui/CustomWindow";
import { BaseColors } from "@/constants/Colors";
import { useSocket } from "@/contexts/DetectContext";
import { PostureUpdate } from "@/models/posture.model";
import { AuthService } from "@/services/auth";
import SharedAssets from "@/shared/SharedAssets";
import { Container, Fonts } from "@/shared/SharedStyles";
import { playPostureWarning, preloadPostureSounds } from "@/utils/play-audio";
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
    if(!socket) return;
    const prepareApp = async () => {
      // Preload sounds alongside other app initialization
      await preloadPostureSounds();
      // Other initialization...
    };
    const client_id = AuthService.getUser() || '';
    const token = AuthService.getToken();
    Promise.all([client_id, token, prepareApp]).then(res => {
      
      const [client_id, token] = res;
      connect(client_id.id, token as string);
    })


    // Listen for posture events
    socket.on('posture_update', (data: PostureUpdate) => {
      console.log('Raw posture update data:', data); // Log the raw data first
      /**
       * "data": {
          "posture": {
            "posture": "good_posture",
            "confidence": 0.95,
            "need_alert": false
          },
          "timestamp": "2023-04-28T15:30:45.123456",
          "duration": 10.5
        }
       * 
       */

      setLivePostureData(data);
    });
    socket.on('detection_result', (data: any) => {
      console.log('res:', data);
      /**
       * "data": {
          "image": "base64_encoded_image",
          "posture": {
            "posture": "good_posture",
            "confidence": 0.95,
            "need_alert": false
          },
          "timestamp": "2023-04-28T15:30:45.123456",
          "image_path": "/path/to/image.jpg",
          "is_new_posture": true,
          "duration": 0
        }
       * 
       */
      
      if(data.is_new_posture && data.posture.confidence > 0.9) {
        setInterval(() => setWrongPostures(prev => [...prev, {
          id: new Date().toISOString(),
          image: data.image,
          posture: data.posture.posture,
          accuracy: data.posture.confidence,
          timestamp: data.timestamp
        }]), 2000);

        console.log('New posture detected:', data.posture.posture);
        // Play sound based on the detected posture
        if (data.posture.posture === "good_posture") return;
        playPostureWarning("bad_sitting_backward");
      }
    });
    socket.on('session_item_completed', (data: any) => {
      console.log('session_item_completed:', data);
      /*
        "data": {
          "session_item_id": "mongodb_id",
          "label_id": "good_posture",
          "start_time": "2023-04-28T15:30:45.123456",
          "end_time": "2023-04-28T15:31:45.123456",
          "duration_seconds": 60.0
        }
      */ 
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
        action: "start",
        camera_id: "0",
      }
      emit(message);
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
      emit(message);
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
              <>
                <Text style={styles.statusText}>
                  Current posture: {livePostureData.posture.posture} 
                </Text>
                <Text style={styles.statusText}>
                  Accuracy: {(livePostureData.posture.confidence * 100).toFixed(2)}%
                </Text>
              </>
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
          maxHeight={400} // Set a reasonable max height
          contentContainerStyle={{
            flexDirection: "column-reverse", // This will correctly apply the column-reverse
          }}
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
    marginLeft: 8,
    marginTop: 12,
  },
  noPostures: {
    color: BaseColors.secondary,
    textAlign: "center",
    padding: 16
  }
});