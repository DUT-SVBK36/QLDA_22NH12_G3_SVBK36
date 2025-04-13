import { audioService } from "@/services/audio";
import SharedAssets from "@/shared/SharedAssets";

type PostureType =
  | "good_posture"
  | "bad_sitting_backward"
  | "bad_sitting_forward"
  | "leaning_left_side"
  | "leaning_right_side"
  | "leg_right"
  | "leg_wrong"
  | "neck_wrong"
  | "neck_right"

/**
 * Play a posture warning sound
 * @param postureType Type of posture to warn about
 */
export function playPostureWarning(postureType: PostureType): void {
  try {
    // Handle the typo in the asset name for shoulders_up
    const assetKey = postureType;

    // Access the sound from SharedAssets
    const sound =
      SharedAssets.audio[assetKey as keyof typeof SharedAssets.audio];

    if (sound) {
      audioService.play(sound);
    } else {
      console.warn(`No sound found for posture type: ${postureType}`);
    }
  } catch (error) {
    console.error("Error playing posture warning sound:", error);
  }
}

/**
 * Preload all posture warning sounds for better performance
 */
export async function preloadPostureSounds(): Promise<void> {
  try {
    const soundsToPreload = Object.values(SharedAssets.audio);

    for (const sound of soundsToPreload) {
      await audioService.preload(sound);
    }

    console.log("All posture sounds preloaded successfully");
  } catch (error) {
    console.error("Error preloading posture sounds:", error);
  }
}
