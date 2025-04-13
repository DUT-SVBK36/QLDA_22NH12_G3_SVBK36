import numpy as np
import mediapipe as mp
from typing import List, Tuple, Dict, Any, Optional
import cv2

mp_pose = mp.solutions.pose

def calculate_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Tính góc giữa ba điểm"""
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    angle_deg = np.degrees(angle)
    return angle_deg

def extract_features_from_landmarks(landmarks: List) -> List[float]:
    """Trích xuất các đặc trưng từ landmarks"""
    # Cơ bản: tọa độ của tất cả các điểm
    features = []
    for landmark in landmarks:
        features.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
    
    # Tính các góc quan trọng
    try:
        # Vai
        left_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
        right_shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y])
        
        # Hông
        left_hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
        right_hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y])
        
        # Tai
        left_ear = np.array([landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y])
        right_ear = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y])
        
        # Đầu gối
        left_knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
        right_knee = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y])
        
        # Mắt cá chân
        left_ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
        right_ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y])
        
        # Tính điểm trung bình
        mid_shoulder = (left_shoulder + right_shoulder) / 2
        mid_hip = (left_hip + right_hip) / 2
        mid_ear = (left_ear + right_ear) / 2
        
        # Điểm tham chiếu trục y (thẳng đứng)
        vertical_ref = np.array([mid_shoulder[0], 0])
        
        # Góc lưng (giữa vai và hông)
        back_angle = calculate_angle(vertical_ref, mid_shoulder, mid_hip)
        
        # Góc cổ (giữa tai và vai)
        neck_angle = calculate_angle(mid_ear, mid_shoulder, vertical_ref)
        
        # Góc chân (giữa hông, đầu gối và mắt cá chân)
        left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
        
        # Khoảng cách giữa hai đầu gối (để phát hiện chân bắt chéo)
        knee_distance = np.linalg.norm(left_knee - right_knee)
        
        # Thêm các góc và khoảng cách vào đặc trưng
        additional_features = [back_angle, neck_angle, left_leg_angle, right_leg_angle, knee_distance]
        features.extend(additional_features)
    except:
        # Nếu không tính được góc, thêm giá trị mặc định
        features.extend([0, 0, 0, 0, 0])
    
    return features

# Functions from detect_posture.py for specialized keypoint extraction
def extract_keypoints(results) -> List[float]:
    """Extract keypoints from MediaPipe pose results for general purpose use"""
    keypoints = []
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            keypoints.extend([landmark.x, landmark.y, landmark.z])
    else:
        # If no landmarks detected, return zeros
        keypoints = [0] * (33 * 3)  # 33 landmarks * 3 coordinates
    
    return keypoints

def extract_leg_keypoints(results) -> List[float]:
    """Extract keypoints for leg model (10 keypoints * 3 coordinates = 30 features)"""
    leg_keypoints_idx = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32]  # Hip to feet
    leg_keypoints = []
    
    for idx in leg_keypoints_idx:
        if results.pose_landmarks:
            point = results.pose_landmarks.landmark[idx]
            leg_keypoints.extend([point.x, point.y, point.z])
        else:
            leg_keypoints.extend([0, 0, 0])
    
    return leg_keypoints

def extract_neck_keypoints(results) -> List[float]:
    """Extract keypoints for neck model (11 keypoints * 3 coordinates = 33 features)"""
    neck_keypoints_idx = list(range(0, 11))  # Head and face points (0-10)
    neck_keypoints = []
    
    for idx in neck_keypoints_idx:
        if results.pose_landmarks:
            point = results.pose_landmarks.landmark[idx]
            neck_keypoints.extend([point.x, point.y, point.z])
        else:
            neck_keypoints.extend([0, 0, 0])
    
    return neck_keypoints

def extract_posture_keypoints(results) -> List[float]:
    """Extract keypoints for posture model (12 keypoints * 3 coordinates = 36 features)"""
    posture_keypoints_idx = list(range(11, 23))  # Shoulders to hips (11-22)
    posture_keypoints = []
    
    for idx in posture_keypoints_idx:
        if results.pose_landmarks:
            point = results.pose_landmarks.landmark[idx]
            posture_keypoints.extend([point.x, point.y, point.z])
        else:
            posture_keypoints.extend([0, 0, 0])
    
    return posture_keypoints

def get_pose_results(image, pose_model):
    """Process an image and get MediaPipe pose results"""
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and get pose landmarks
    results = pose_model.process(image_rgb)
    
    return results
