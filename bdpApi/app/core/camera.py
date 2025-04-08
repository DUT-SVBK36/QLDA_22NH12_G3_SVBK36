import cv2
import mediapipe as mp
import numpy as np
import base64
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from collections import Counter
import queue

from app.core.utils import extract_features_from_landmarks
from app.core.posture_monitor import PostureMonitor
from app.services.model_service import ModelService
from app.services.alert_service import AlertService
from app.config import POSTURE_NAMES_VI, CAMERA_FRAME_INTERVAL, IMAGE_SEND_INTERVAL, logger

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class CameraState:
    def __init__(self, message_queue: queue.Queue):
        self.is_running = False
        self.camera = None
        self.camera_id = 0
        self.pose = None
        self.model_service = ModelService()
        self.alert_service = AlertService()
        self.monitor = PostureMonitor()
        self.recent_predictions = []
        self.max_predictions = 10
        self.last_frame_time = time.time()
        self.frame_interval = CAMERA_FRAME_INTERVAL
        self.last_image_send_time = time.time()
        self.image_send_interval = IMAGE_SEND_INTERVAL
        self.message_queue = message_queue

    def start(self, camera_id: int = 0) -> bool:
        if self.is_running:
            return False
        
        try:
            self.camera_id = camera_id
            self.camera = cv2.VideoCapture(camera_id)
            if not self.camera.isOpened():
                logger.error(f"Không thể mở camera với ID: {camera_id}")
                return False
            
            self.pose = mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5)
            
            self.is_running = True
            self.monitor.reset()
            self.recent_predictions = []
            logger.info(f"Đã khởi động camera với ID: {camera_id}")
            return True
        
        except Exception as e:
            logger.error(f"Lỗi khi khởi động camera: {e}")
            return False
    
    def stop(self) -> bool:
        if not self.is_running:
            return False
        
        try:
            self.is_running = False
            if self.camera:
                self.camera.release()
            if self.pose:
                self.pose.close()
            
            logger.info("Đã dừng camera")
            return True
        
        except Exception as e:
            logger.error(f"Lỗi khi dừng camera: {e}")
            return False
    
    def process_frame(self) -> bool:
        """Xử lý một frame từ camera"""
        try:
            current_time = time.time()
            
            # Kiểm tra tần suất xử lý frame
            if current_time - self.last_frame_time < self.frame_interval:
                return False
            
            self.last_frame_time = current_time
            
            # Đọc frame từ camera
            ret, frame = self.camera.read()
            if not ret:
                logger.error("Không thể đọc frame từ camera")
                return False
            
            # Chuyển đổi hình ảnh sang RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Phát hiện tư thế
            results = self.pose.process(frame_rgb)
            
            # Tạo bản sao của frame để vẽ
            display_frame = frame.copy()
            
            # Biến để lưu thông tin tư thế
            posture_info = {
                "posture": "unknown",
                "confidence": 0.0,
                "posture_vi": "Không xác định",
                "angles": {},
                "need_alert": False
            }
            
            if results.pose_landmarks:
                # Vẽ landmark trên frame
                mp_drawing.draw_landmarks(
                    display_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                # Sử dụng phương pháp dự đoán mới (truyền trực tiếp kết quả MediaPipe)
                predicted_class, confidence = self.model_service.predict_posture(results=results)
                
                if predicted_class:
                    # Thêm dự đoán vào danh sách gần đây
                    self.recent_predictions.append(predicted_class)
                    if len(self.recent_predictions) > self.max_predictions:
                        self.recent_predictions.pop(0)
                    
                    # Lấy dự đoán phổ biến nhất trong các dự đoán gần đây
                    if self.recent_predictions:
                        smoothed_class = Counter(self.recent_predictions).most_common(1)[0][0]
                        
                        # Cập nhật thông tin tư thế
                        posture_info["posture"] = smoothed_class
                        posture_info["confidence"] = confidence
                        posture_info["posture_vi"] = POSTURE_NAMES_VI.get(smoothed_class, smoothed_class)
                        
                        # Lấy góc từ extract_features_from_landmarks (cho tương thích ngược)
                        try:
                            features = extract_features_from_landmarks(results.pose_landmarks.landmark)
                            back_angle = features[-5]  # Vị trí của góc lưng trong danh sách đặc trưng
                            neck_angle = features[-4]  # Vị trí của góc cổ trong danh sách đặc trưng
                            posture_info["angles"] = {
                                "back": float(back_angle),
                                "neck": float(neck_angle)
                            }
                        except:
                            pass
                        
                        # Kiểm tra xem có cần cảnh báo không
                        need_alert = self.monitor.update(smoothed_class, confidence)
                        posture_info["need_alert"] = need_alert
                        
                        # Hiển thị thông tin trên frame
                        
                        
                        # Nếu cần cảnh báo
                        if need_alert:
                            
                            
                            # Phát âm thanh cảnh báo
                            alert_sound_file = f"{smoothed_class}.mp3"
                            self.alert_service.play_alert_sound(alert_sound_file)
                            
                            # Lưu ảnh chụp
                            self.alert_service.save_screenshot(display_frame, smoothed_class)
            
            # Chỉ gửi ảnh mỗi 2 giây hoặc khi có cảnh báo
            should_send_image =  posture_info["need_alert"]
            
            if should_send_image:
                self.last_image_send_time = current_time
                
                # Giảm kích thước ảnh để tối ưu hóa băng thông
                scale_percent = 50  # Giảm kích thước xuống 50%
                width = int(display_frame.shape[1] * scale_percent / 100)
                height = int(display_frame.shape[0] * scale_percent / 100)
                dim = (width, height)
                resized_frame = cv2.resize(display_frame, dim, interpolation=cv2.INTER_AREA)
                
                # Chuyển đổi sang JPEG và sau đó thành base64
                _, buffer = cv2.imencode('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                
                # Tạo message để gửi qua WebSocket
                message = {
                    "type": "frame",
                    "data": {
                        "image": jpg_as_text,
                        "posture": posture_info,
                        "timestamp": datetime.now().isoformat()
                    }
                }
                
                # Thêm vào queue để gửi trong event loop chính
                self.message_queue.put(message)
            
            # Gửi thông tin tư thế mỗi khi xử lý frame (không cần gửi ảnh)
            posture_message = {
                "type": "posture_update",
                "data": {
                    "posture": posture_info,
                    "timestamp": datetime.now().isoformat()
                }
            }
            self.message_queue.put(posture_message)
            
            # Nếu cần thống kê, gửi thống kê mỗi 5 giây
            if int(current_time) % 5 == 0 and current_time - int(current_time) < 0.1:  # Mỗi 5 giây
                stats = self.monitor.get_statistics()
                stats_message = {
                    "type": "statistics",
                    "data": stats
                }
                self.message_queue.put(stats_message)
            
            return True
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình xử lý frame: {e}")
            return False

