import os
import pickle
import tensorflow as tf
import numpy as np
import logging
import asyncio
import cv2
import base64
from typing import Dict, Tuple, Any, List, Optional
import mediapipe as mp
from datetime import datetime
from app.core.utils import extract_features_from_landmarks
from app.config import MODELS_DIR, logger, ESP32_AUDIO_SERVER
from app.models.schemas import FrameData, PostureInfo

class ModelService:
    def __init__(self):
        self.models = {}
        self.posture_classes = []
        self.leg_classes = []
        self.neck_classes = []
        self.load_models()
    
    # bdpApi/app/services/model_service.py
    def load_models(self) -> None:
        """Load trained posture detection models"""
        try:
            # Đường dẫn đến các mô hình
            rf_path = os.path.join(MODELS_DIR, 'random_forest_model.pkl')
            gb_path = os.path.join(MODELS_DIR, 'gradient_boosting_model.pkl')
            svm_path = os.path.join(MODELS_DIR, 'svm_model.pkl')
            nn_path = os.path.join(MODELS_DIR, 'neural_network_model.keras')
            scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
            label_encoder_path = os.path.join(MODELS_DIR, 'label_encoder.pkl')
            ensemble_path = os.path.join(MODELS_DIR, 'ensemble_meta.pkl')
            
            # Tải các mô hình
            if os.path.exists(rf_path):
                with open(rf_path, 'rb') as f:
                    self.models['rf'] = pickle.load(f)
                    
            if os.path.exists(gb_path):
                with open(gb_path, 'rb') as f:
                    self.models['gb'] = pickle.load(f)
                    
            if os.path.exists(svm_path):
                with open(svm_path, 'rb') as f:
                    self.models['svm'] = pickle.load(f)
                    
            if os.path.exists(nn_path):
                self.models['nn'] = tf.keras.models.load_model(nn_path)
                
            # Tải scaler và label encoder
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.models['scaler'] = pickle.load(f)
                    
            if os.path.exists(label_encoder_path):
                with open(label_encoder_path, 'rb') as f:
                    self.models['label_encoder'] = pickle.load(f)
                    
            # Tải thông tin ensemble nếu có
            if os.path.exists(ensemble_path):
                with open(ensemble_path, 'rb') as f:
                    self.models['ensemble_meta'] = pickle.load(f)
                    
            logger.info(f"Đã tải xong {len(self.models)} mô hình và thành phần")
            
        except Exception as e:
            logger.error(f"Lỗi khi tải mô hình: {str(e)}")

    
    def extract_and_preprocess_keypoints(self, results):
        """Extract and preprocess keypoints for all models as done in detect_posture.py"""
        # Extract keypoints for leg model (10 keypoints * 3 coordinates = 30 features)
        leg_keypoints_idx = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32]  # Hip to feet
        leg_keypoints = []
        for idx in leg_keypoints_idx:
            if results.pose_landmarks:
                point = results.pose_landmarks.landmark[idx]
                leg_keypoints.extend([point.x, point.y, point.z])
            else:
                leg_keypoints.extend([0, 0, 0])
        
        # Extract keypoints for neck model (11 keypoints * 3 coordinates = 33 features)
        neck_keypoints_idx = list(range(0, 11))  # Head and face points (0-10)
        neck_keypoints = []
        for idx in neck_keypoints_idx:
            if results.pose_landmarks:
                point = results.pose_landmarks.landmark[idx]
                neck_keypoints.extend([point.x, point.y, point.z])
            else:
                neck_keypoints.extend([0, 0, 0])
        
        # Extract keypoints for posture model (12 keypoints * 3 coordinates = 36 features)
        posture_keypoints_idx = list(range(11, 23))  # Shoulders to hips (11-22)
        posture_keypoints = []
        for idx in posture_keypoints_idx:
            if results.pose_landmarks:
                point = results.pose_landmarks.landmark[idx]
                posture_keypoints.extend([point.x, point.y, point.z])
            else:
                posture_keypoints.extend([0, 0, 0])
        
        # Reshape arrays to match model input shapes
        leg_keypoints = np.array(leg_keypoints).reshape(1, -1)  # Shape: (1, 30)
        neck_keypoints = np.array(neck_keypoints).reshape(1, -1)  # Shape: (1, 33)
        posture_keypoints = np.array(posture_keypoints).reshape(1, -1)  # Shape: (1, 36)
        
        return leg_keypoints, neck_keypoints, posture_keypoints
    
    def predict_posture(self, features=None, results=None):
        """Dự đoán tư thế sử dụng mô hình ensemble"""
        try:
            if not self.models:
                logger.error("Chưa tải mô hình. Không thể dự đoán.")
                return "unknown", 0.0
            
            # Nếu có kết quả MediaPipe, trích xuất đặc trưng
            if results and hasattr(results, 'pose_landmarks'):
                features = extract_features_from_landmarks(results.pose_landmarks.landmark)
            
            if features and 'scaler' in self.models:
                features_scaled = self.models['scaler'].transform([features])
                
                # Dự đoán với từng mô hình
                predictions = {}
                
                if 'rf' in self.models:
                    predictions['rf'] = self.models['rf'].predict_proba(features_scaled)
                
                if 'gb' in self.models:
                    predictions['gb'] = self.models['gb'].predict_proba(features_scaled)
                
                if 'svm' in self.models:
                    predictions['svm'] = self.models['svm'].predict_proba(features_scaled)
                
                if 'nn' in self.models:
                    predictions['nn'] = self.models['nn'].predict(features_scaled)
                
                # Kết hợp các dự đoán
                if predictions:
                    # Tính trung bình có trọng số các dự đoán
                    ensemble_pred = np.zeros_like(list(predictions.values())[0])
                    
                    # Nếu có thông tin về ensemble
                    if 'ensemble_meta' in self.models:
                        weights = dict(zip(self.models['ensemble_meta']['models'], 
                                        self.models['ensemble_meta']['weights']))
                        
                        for model_name, pred in predictions.items():
                            if model_name in weights:
                                ensemble_pred += pred * weights[model_name]
                    else:
                        # Nếu không có thông tin về ensemble, tính trung bình đơn giản
                        for pred in predictions.values():
                            ensemble_pred += pred
                        ensemble_pred /= len(predictions)
                    
                    # Lấy lớp có xác suất cao nhất
                    predicted_class_idx = np.argmax(ensemble_pred)
                    confidence = ensemble_pred[0][predicted_class_idx]
                    
                    # Chuyển đổi chỉ số lớp thành tên lớp
                    if 'label_encoder' in self.models:
                        predicted_class = self.models['label_encoder'].inverse_transform([predicted_class_idx])[0]
                        return predicted_class, float(confidence)
                    else:
                        return f"class_{predicted_class_idx}", float(confidence)
            
            return "unknown", 0.0
        
        except Exception as e:
            logger.error(f"Lỗi khi dự đoán tư thế: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "unknown", 0.0


class PostureDetectionService:
    def __init__(self, camera_id=0, camera_url=None):
        self.camera_id = camera_id
        self.camera_url = camera_url
        self.model_service = ModelService()
        self.running = False
        self.cap = None
        self.frame_queue = asyncio.Queue(maxsize=10)
        from app.services.alert_service import AlertService
        self.alert_service = AlertService()
        self.last_alert_time = None
        # MediaPipe setup
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Start the capture thread
        self.start()
    
    def is_camera_opened(self):
        """Kiểm tra xem camera có mở được không"""
        if self.cap is not None:
            return self.cap.isOpened()
        return False
    
    def start(self):
        """Start the detection service"""
        if not self.running:
            logger.info(f"Starting camera capture with camera ID: {self.camera_id}")
            self.running = True
            
            # Xử lý camera dựa trên loại camera
            if self.camera_id == 1 and not self.camera_url:
                # Camera WiFi mặc định nếu không cung cấp URL
                self.camera_url = 'http://192.168.248.93:81/stream'
                logger.info(f"Using WiFi camera at URL: {self.camera_url}")
                self.cap = cv2.VideoCapture(self.camera_url)
            elif self.camera_id == 1 and self.camera_url:
                # Sử dụng URL camera cụ thể nếu đã cung cấp
                logger.info(f"Using WiFi camera at custom URL: {self.camera_url}")
                self.cap = cv2.VideoCapture(self.camera_url)
            else:
                # Camera thông thường (webcam)
                logger.info(f"Using local camera with index: {self.camera_id}")
                self.cap = cv2.VideoCapture(self.camera_id)
            
            # Start the frame processing loop in a separate thread
            import threading
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.daemon = True
            self.capture_thread.start()
    
    def stop(self):
        """Stop the detection service"""
        self.running = False
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Fix the MediaPipe error by adding a check
        try:
            if self.pose and hasattr(self.pose, '_graph') and self.pose._graph is not None:
                self.pose.close()
        except Exception as e:
            logger.error(f"Error closing MediaPipe pose: {str(e)}")
        
        logger.info("Posture detection service stopped")
    
    def _capture_loop(self):
        """Background thread loop for capturing and processing frames"""
        if not self.cap or not self.cap.isOpened():
            logger.error(f"Failed to open camera with ID: {self.camera_id}")
            if self.camera_id == 1:
                logger.error(f"Check if the IP camera URL is correct: {self.camera_url}")
            return
        
        frame_count = 0
        reconnect_attempts = 0
        max_reconnect_attempts = 5
        
        while self.running:
            success, frame = self.cap.read()
            if not success:
                reconnect_attempts += 1
                logger.error(f"Failed to read frame from camera (attempt {reconnect_attempts}/{max_reconnect_attempts})")
                
                # Nếu là camera WiFi, thử kết nối lại
                if self.camera_id == 1 and reconnect_attempts < max_reconnect_attempts:
                    logger.info("Attempting to reconnect to WiFi camera...")
                    if self.cap:
                        self.cap.release()
                    
                    # Chờ 2 giây trước khi thử lại
                    import time
                    time.sleep(2)
                    
                    self.cap = cv2.VideoCapture(self.camera_url)
                    continue
                elif reconnect_attempts >= max_reconnect_attempts:
                    logger.error("Maximum reconnection attempts reached. Stopping camera capture.")
                    break
                else:
                    break
            
            # Reset reconnect counter on successful frame capture
            reconnect_attempts = 0
            
            # Skip frames to reduce CPU usage (process every 3rd frame)
            frame_count += 1
            if frame_count % 3 != 0:
                continue
            
            try:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process the frame with MediaPipe
                results = self.pose.process(rgb_frame)
                
                # Draw pose landmarks on the frame
                annotated_frame = frame.copy()
                if results.pose_landmarks:
                    self.mp_drawing.draw_landmarks(
                        annotated_frame, 
                        results.pose_landmarks, 
                        self.mp_pose.POSE_CONNECTIONS
                    )
                
                # Get posture prediction
                posture_class, confidence = self.model_service.predict_posture(results=results)
                
                # Convert frame to base64 for transmission
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                base64_image = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
                
                # Determine if this posture needs an alert (anything not 'good_')
                is_good_posture = (
                    posture_class.startswith("straight_") or 
                    
                    "vai_thang" in posture_class
                )
                needs_alert = not is_good_posture
                if needs_alert:
                    current_time = datetime.now()
                    if self.last_alert_time is None or (current_time - self.last_alert_time).total_seconds() > 20.0:
                        try:
                            logger.info(f"Phát hiện tư thế cần cảnh báo: {posture_class}, phát âm thanh")
                            self.alert_service.play_alert_sound(posture_class)
                            self.last_alert_time = current_time
                        except Exception as e:
                            logger.error(f"Lỗi khi phát âm thanh cảnh báo: {str(e)}")
                # Prepare the frame data
                posture_info = PostureInfo(
                    posture=posture_class,
                    confidence=float(confidence),
                    need_alert=needs_alert
                )
                
                frame_data = FrameData(
                    image=base64_image,
                    posture=posture_info,
                    timestamp=datetime.now().isoformat()
                )
                
                # Put the processed frame in the queue
                try:
                    # Use put_nowait to avoid blocking
                    self.frame_queue.put_nowait(frame_data)
                except asyncio.QueueFull:
                    # If queue is full, remove oldest item and add new one
                    try:
                        self.frame_queue.get_nowait()
                        self.frame_queue.put_nowait(frame_data)
                    except Exception:
                        pass
                
            except Exception as e:
                logger.error(f"Error processing frame: {str(e)}")
            
            # Sleep a bit to control the frame rate
            import time
            time.sleep(0.05)
    
    async def get_next_frame(self):
        """Get the next processed frame as a FrameData object"""
        if not self.running:
            return None
        
        try:
            # Wait for the next frame with a timeout
            frame_data = await asyncio.wait_for(self.frame_queue.get(), timeout=5.0)
            return frame_data
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for next frame")
            return None
        except Exception as e:
            logger.error(f"Error getting next frame: {str(e)}")
            return None 