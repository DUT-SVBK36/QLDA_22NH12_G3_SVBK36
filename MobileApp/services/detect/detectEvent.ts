import { on } from './detectSocket';

interface PostureDetectionData {
  client: string;
  image: string;  // Backend assets path to the image
  detectedPosture: string;
  accuracy: number;
  desc: string;
  timestamp: string;
}

export default function setupEventListeners(): void {
  on('connect', () => {
    console.log('WebSocket connected');
  });

  on('disconnect', () => {
    console.log('WebSocket disconnected');
  });

  on('error', (err: Error) => {
    console.log('Connection error:', err);
  });

  on('detect', (data: any) => {
    console.log('Detection started');
  });

  on('stopDetect', (data: any) => {
    console.log('Detection stopped');
  });

  on('message', (data: any) => {
    console.log('Received raw message:', data);
    
    try {
        // The data is already parsed by detectSocket.ts
        const messageData = data;
        
        // Extract the actual message payload
        const payload = messageData.payload || messageData;
        
        console.log('Received message:', {
            type: payload.type,
            client: payload.client,
            timestamp: payload.timestamp
        });
        
        // Handle different message types
        switch (payload.type) {
            case 'detect':
                console.log('Detection started for client:', payload.client);
                break;
            case 'stopDetect':
                console.log('Detection stopped for client:', payload.client);
                break;
            case 'posture':
                console.log('Posture detection:', {
                    posture: payload.detectedPosture,
                    accuracy: payload.accuracy,
                    description: payload.desc
                });
                break;
        }
    } catch (error) {
        console.error('Error processing message:', error);
        console.log('Raw message data:', data);
    }
  });
  on("posture", (data: any) => {
    try {
        // The data is already in the correct format
        console.log("Posture detection:", {
            posture: data.detectedPosture,
            accuracy: data.accuracy,
            description: data.desc,
            image: data.image,
            timestamp: data.timestamp
        });
    } catch (error) {
        console.error("Error processing posture detection data:", error);
        console.log("Raw posture data:", data);
    }
});
}