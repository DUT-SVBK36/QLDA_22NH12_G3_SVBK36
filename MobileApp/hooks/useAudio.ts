import { useState, useEffect, useCallback, useRef } from 'react';
import { audioService, AudioOptions } from '@/services/audio';

/**
 * Type for the sound source (can be a require() result or a URI string)
 */
type AudioSource = number | string;

/**
 * Status of the sound playback
 */
interface PlaybackStatus {
  isLoaded: boolean;
  isPlaying: boolean;
  isBuffering: boolean;
  positionMillis: number;
  durationMillis: number;
  volume: number;
  didJustFinish: boolean;
  error?: string;
}

/**
 * Hook to use the audio service
 */
export const useAudio = (initialSource?: AudioSource) => {
  // Track if component is mounted
  const isMounted = useRef(true);
  
  // Track current source
  const [source, setSource] = useState<AudioSource | undefined>(initialSource);
  
  // Track playback status
  const [status, setStatus] = useState<PlaybackStatus>({
    isLoaded: false,
    isPlaying: false,
    isBuffering: false,
    positionMillis: 0,
    durationMillis: 0,
    volume: 1.0,
    didJustFinish: false
  });

  // Handle status updates from the audio service
  const handleStatusUpdate = useCallback((playbackStatus: any) => {
    if (!isMounted.current) return;
    
    if (playbackStatus.isLoaded) {
      setStatus({
        isLoaded: true,
        isPlaying: playbackStatus.isPlaying,
        isBuffering: playbackStatus.isBuffering || false,
        positionMillis: playbackStatus.positionMillis || 0,
        durationMillis: playbackStatus.durationMillis || 0,
        volume: playbackStatus.volume || 1.0,
        didJustFinish: playbackStatus.didJustFinish || false
      });
    } else {
      // Handle error state
      setStatus(prev => ({
        ...prev,
        isLoaded: false,
        error: playbackStatus.error
      }));
    }
  }, []);

  // Preload audio source
  const preload = useCallback(async (audioSource?: AudioSource) => {
    const sourceToPreload = audioSource || source;
    if (!sourceToPreload) return;
    
    try {
      await audioService.preload(sourceToPreload);
    } catch (error) {
      console.error('Error preloading audio:', error);
    }
  }, [source]);

  // Play sound
  const play = useCallback(async (audioSource?: AudioSource, options: AudioOptions = {}) => {
    const sourceToPlay = audioSource || source;
    if (!sourceToPlay) return;
    
    try {
      // Update source if a new one is provided
      if (audioSource && audioSource !== source) {
        setSource(audioSource);
      }
      
      await audioService.play(sourceToPlay, {
        ...options,
        onPlaybackStatusUpdate: handleStatusUpdate,
        onError: (error) => {
          console.error('Error playing audio:', error);
          if (isMounted.current) {
            setStatus(prev => ({ ...prev, error: error.message }));
          }
        }
      });
    } catch (error) {
      console.error('Error in play function:', error);
    }
  }, [source, handleStatusUpdate]);

  // Stop sound
  const stop = useCallback(async () => {
    try {
      await audioService.stop();
      if (isMounted.current) {
        setStatus(prev => ({ ...prev, isPlaying: false, positionMillis: 0 }));
      }
    } catch (error) {
      console.error('Error stopping audio:', error);
    }
  }, []);

  // Pause sound
  const pause = useCallback(async () => {
    try {
      await audioService.pause();
      if (isMounted.current) {
        setStatus(prev => ({ ...prev, isPlaying: false }));
      }
    } catch (error) {
      console.error('Error pausing audio:', error);
    }
  }, []);

  // Resume sound
  const resume = useCallback(async () => {
    try {
      await audioService.resume();
      if (isMounted.current) {
        setStatus(prev => ({ ...prev, isPlaying: true }));
      }
    } catch (error) {
      console.error('Error resuming audio:', error);
    }
  }, []);

  // Set volume
  const setVolume = useCallback(async (volume: number) => {
    try {
      await audioService.setVolume(volume);
      if (isMounted.current) {
        setStatus(prev => ({ ...prev, volume }));
      }
    } catch (error) {
      console.error('Error setting volume:', error);
    }
  }, []);

  // Preload initial source if provided
  useEffect(() => {
    if (initialSource) {
      preload(initialSource);
    }
    
    // Clean up on unmount
    return () => {
      isMounted.current = false;
    };
  }, [initialSource, preload]);

  return {
    status,
    preload,
    play,
    stop,
    pause,
    resume,
    setVolume,
    setSource
  };
};

export default useAudio;