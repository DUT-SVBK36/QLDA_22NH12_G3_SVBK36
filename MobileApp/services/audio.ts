import { Audio } from 'expo-av';
import { Asset } from 'expo-asset';

export interface AudioOptions {
  volume?: number; // 0.0 to 1.0
  shouldPlay?: boolean; // Start playing immediately
  isLooping?: boolean; // Loop the sound
  onPlaybackStatusUpdate?: (status: any) => void; // Status updates
  onError?: (error: any) => void; // Error handling
}

// Sound cache to improve performance
type SoundInfo = {
  sound: Audio.Sound;
  isLoaded: boolean;
};

class AudioService {
  private soundCache: Map<string, SoundInfo> = new Map();
  private currentSound: Audio.Sound | null = null;
  private isInitialized: boolean = false;

  constructor() {
    this.initialize();
  }

  /**
   * Initialize the audio service
   */
  private async initialize(): Promise<void> {
    if (!this.isInitialized) {
      try {
        // Request audio permissions
        await Audio.setAudioModeAsync({
          playsInSilentModeIOS: true,
          staysActiveInBackground: false,
          shouldDuckAndroid: true,
        });
        this.isInitialized = true;
      } catch (error) {
        console.error('Failed to initialize audio service:', error);
      }
    }
  }

  /**
   * Get path for asset
   */
  private async getAssetPath(source: any): Promise<string> {
    // Handle require() style imports
    if (typeof source === 'number') {
      const asset = Asset.fromModule(source);
      await asset.downloadAsync();
      return asset.uri;
    }
    
    // If it's already a string (URL or path), return directly
    return source;
  }

  /**
   * Preload a sound file
   */
  async preload(source: any): Promise<void> {
    try {
      const sourceKey = typeof source === 'number' ? source.toString() : source;
      
      if (this.soundCache.has(sourceKey)) {
        return; // Already preloaded
      }

      const uri = await this.getAssetPath(source);
      const { sound } = await Audio.Sound.createAsync(
        { uri },
        { shouldPlay: false }
      );
      
      this.soundCache.set(sourceKey, {
        sound,
        isLoaded: true
      });
    } catch (error) {
      console.error('Error preloading audio:', error);
    }
  }

  /**
   * Play a sound
   */
  async play(source: any, options: AudioOptions = {}): Promise<void> {
    try {
      const sourceKey = typeof source === 'number' ? source.toString() : source;
      let sound: Audio.Sound;

      // Check if sound is in cache
      if (this.soundCache.has(sourceKey) && this.soundCache.get(sourceKey)!.isLoaded) {
        sound = this.soundCache.get(sourceKey)!.sound;
      } else {
        // Load the sound
        const uri = await this.getAssetPath(source);
        const soundObject = await Audio.Sound.createAsync(
          { uri },
          { 
            shouldPlay: options.shouldPlay !== false,
            isLooping: !!options.isLooping,
            volume: options.volume || 1.0,
          },
          options.onPlaybackStatusUpdate
        );
        
        sound = soundObject.sound;
        
        // Cache the sound for future use
        this.soundCache.set(sourceKey, {
          sound,
          isLoaded: true
        });
      }

      // Stop current sound if any
      if (this.currentSound) {
        await this.currentSound.stopAsync();
      }

      // Set as current sound
      this.currentSound = sound;

      // Configure sound based on options
      if (options.volume !== undefined) {
        await sound.setVolumeAsync(options.volume);
      }
      
      if (options.isLooping !== undefined) {
        await sound.setIsLoopingAsync(options.isLooping);
      }

      // Play the sound
      await sound.playAsync();
    } catch (error) {
      console.error('Error playing audio:', error);
      if (options.onError) options.onError(error);
    }
  }

  /**
   * Stop current sound
   */
  async stop(): Promise<void> {
    try {
      if (this.currentSound) {
        await this.currentSound.stopAsync();
        this.currentSound = null;
      }
    } catch (error) {
      console.error('Error stopping audio:', error);
    }
  }

  /**
   * Pause current sound
   */
  async pause(): Promise<void> {
    try {
      if (this.currentSound) {
        await this.currentSound.pauseAsync();
      }
    } catch (error) {
      console.error('Error pausing audio:', error);
    }
  }

  /**
   * Resume current sound
   */
  async resume(): Promise<void> {
    try {
      if (this.currentSound) {
        await this.currentSound.playAsync();
      }
    } catch (error) {
      console.error('Error resuming audio:', error);
    }
  }

  /**
   * Set volume
   */
  async setVolume(volume: number): Promise<void> {
    try {
      if (this.currentSound) {
        await this.currentSound.setVolumeAsync(Math.max(0, Math.min(1, volume)));
      }
    } catch (error) {
      console.error('Error setting volume:', error);
    }
  }

  /**
   * Clean up resources
   */
  async release(): Promise<void> {
    try {
      // Stop current sound
      if (this.currentSound) {
        await this.currentSound.stopAsync();
        this.currentSound = null;
      }

      // Unload all cached sounds
      for (const [key, { sound }] of this.soundCache.entries()) {
        await sound.unloadAsync();
        this.soundCache.delete(key);
      }
    } catch (error) {
      console.error('Error releasing audio resources:', error);
    }
  }
}

// Export a singleton instance
export const audioService = new AudioService();