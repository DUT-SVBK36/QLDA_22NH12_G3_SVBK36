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

  on('posture_update', (data: any) => {
    console.log('Posture update:', data);
  });

  on('statistics', (data: any) => {
    console.log('Statistics:', data);
  });

  on('frame', (data: any) => {
    console.log('Image:', data);
  });
}