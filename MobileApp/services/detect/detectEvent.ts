import { on } from './detectSocket';



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