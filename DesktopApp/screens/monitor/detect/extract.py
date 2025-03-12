import cv2
import numpy as np
def extract_keypoints( results):
        """Extract keypoints from MediaPipe results directly"""
        if results.pose_landmarks:
            keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
            return keypoints
        return None

def extract_head_keypoints(results):
        """Extract head keypoints (nose, eyes, ears)"""
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            head_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # MediaPipe indices for head landmarks
            head_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in head_indices]).flatten()
            return head_points
        return None

def extract_body_keypoints(results):
        """Extract torso keypoints (shoulders, chest, hips)"""
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            body_indices = [11, 12, 23, 24]  # MediaPipe indices for body landmarks
            body_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in body_indices]).flatten()
            return body_points
        return None

def extract_arm_keypoints(results):
        """Extract arm keypoints (shoulders to wrists)"""
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            arm_indices = [11, 13, 15, 12, 14, 16]  # MediaPipe indices for arm landmarks
            arm_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in arm_indices]).flatten()
            return arm_points
        return None

def extract_leg_keypoints(results):
        """Extract leg keypoints (hips to ankles)"""
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            leg_indices = [23, 25, 27, 24, 26, 28]  # MediaPipe indices for leg landmarks
            leg_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in leg_indices]).flatten()
            return leg_points
        return None

def extract_foot_keypoints(results):
        """Extract foot keypoints (feet landmarks)"""
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            foot_indices = [29, 30, 31, 32]  # MediaPipe indices for foot landmarks
            foot_points = np.array([[landmarks[i].x, landmarks[i].y, landmarks[i].z] for i in foot_indices]).flatten()
            return foot_points
        return None

def get_multiple_predictions(label_encoder,prediction, threshold=0.5):
        """Get prediction labels above threshold"""
        predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])
        return predicted_label

def display_postures(frame, postures):
        """Display posture labels on the frame"""
        # Convert posture name to string if it's not already
        posture_text = str(postures[0]) if isinstance(postures, (list, np.ndarray)) else str(postures)
        
        # Add text to frame with proper font scale and positioning
        cv2.putText(
            frame,
            posture_text,
            (20, 40),  # Position at top-left with some margin
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Font scale
            (255, 0, 0),  # Blue color in RGB
            2,  # Line thickness
            cv2.LINE_AA  # Anti-aliased line type
        )