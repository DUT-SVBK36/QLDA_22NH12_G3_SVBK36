import numpy as np
import mediapipe as mp
from typing import List, Tuple, Dict, Any, Optional

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
