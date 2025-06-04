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
from app.config import MODELS_DIR, logger
from app.models.schemas import FrameData, PostureInfo

class ModelService:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self) -> None:
        """Load Neural Network model only"""
        try:
            # Đường dẫn đến mô hình Neural Network
            nn_path = os.path.join(MODELS_DIR, 'neural_network_model.keras')
            scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
            label_encoder_path = os.path.join(MODELS_DIR, 'label_encoder.pkl')
            
            # Tải Neural Network model
            if os.path.exists(nn_path):
                try:
                    self.models['nn'] = tf.keras.models.load_model(nn_path)
                    logger.info("✓ Đã tải Neural Network model")
                except Exception as e:
                    logger.error(f"✗ Lỗi khi tải Neural Network model: {e}")
                    raise
            else:
                logger.error(f"✗ Không tìm thấy Neural Network model tại: {nn_path}")
                raise FileNotFoundError(f"Neural Network model not found at {nn_path}")
                
            # Tải scaler
            if os.path.exists(scaler_path):
                try:
                    with open(scaler_path, 'rb') as f:
                        self.models['scaler'] = pickle.load(f)
                    logger.info("✓ Đã tải Scaler")
                except Exception as e:
                    logger.error(f"✗ Lỗi khi tải Scaler: {e}")
                    raise
            else:
                logger.error(f"✗ Không tìm thấy Scaler tại: {scaler_path}")
                raise FileNotFoundError(f"Scaler not found at {scaler_path}")
                    
            # Tải label encoder
            if os.path.exists(label_encoder_path):
                try:
                    with open(label_encoder_path, 'rb') as f:
                        self.models['label_encoder'] = pickle.load(f)
                    logger.info("✓ Đã tải Label Encoder")
                except Exception as e:
                    logger.error(f"✗ Lỗi khi tải Label Encoder: {e}")
                    raise
            else:
                logger.error(f"✗ Không tìm thấy Label Encoder tại: {label_encoder_path}")
                raise FileNotFoundError(f"Label Encoder not found at {label_encoder_path}")
                    
            logger.info("✓ Đã tải xong tất cả thành phần của Neural Network model")
            
        except Exception as e:
            logger.error(f"Lỗi khi tải mô hình Neural Network: {str(e)}")
            raise

    def predict_posture(self, features=None, results=None):
        """Dự đoán tư thế sử dụng Neural Network"""
        try:
            if not self.models:
                logger.error("Chưa tải mô hình. Không thể dự đoán.")
                return "unknown", 0.0
            
            # Kiểm tra các thành phần cần thiết
            required_components = ['nn', 'scaler', 'label_encoder']
            for component in required_components:
                if component not in self.models:
                    logger.error(f"Thiếu thành phần: {component}")
                    return "unknown", 0.0
            
            # Nếu có kết quả MediaPipe, trích xuất đặc trưng
            if results and hasattr(results, 'pose_landmarks') and results.pose_landmarks:
                features = extract_features_from_landmarks(results.pose_landmarks.landmark)
            
            if features is None:
                logger.warning("Không có đặc trưng để dự đoán")
                return "unknown", 0.0
            
            # Chuẩn hóa đặc trưng
            try:
                features_scaled = self.models['scaler'].transform([features])
            except Exception as e:
                logger.error(f"Lỗi khi chuẩn hóa đặc trưng: {e}")
                return "unknown", 0.0
            
            # Dự đoán với Neural Network
            try:
                prediction_proba = self.models['nn'].predict(features_scaled, verbose=0)
                predicted_class_idx = np.argmax(prediction_proba)
                confidence = prediction_proba[0][predicted_class_idx]
                
                # Chuyển đổi chỉ số lớp thành tên lớp
                predicted_class = self.models['label_encoder'].inverse_transform([predicted_class_idx])[0]
                
                return predicted_class, float(confidence)
                
            except Exception as e:
                logger.error(f"Lỗi khi dự đoán với Neural Network: {e}")
                return "unknown", 0.0
        
        except Exception as e:
            logger.error(f"Lỗi khi dự đoán tư thế: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "unknown", 0.0

    def get_model_info(self):
        """Lấy thông tin về mô hình Neural Network"""
        if 'nn' not in self.models:
            return None
        
        nn_model = self.models['nn']
        return {
            'model_type': 'Neural Network',
            'input_shape': nn_model.input_shape,
            'output_shape': nn_model.output_shape,
            'num_layers': len(nn_model.layers),
            'total_params': nn_model.count_params(),
            'classes': self.models['label_encoder'].classes_.tolist() if 'label_encoder' in self.models else []
        }


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
        
        # Smoothing variables
        self.recent_predictions = []
        self.max_predictions = 5  # Số lượng dự đoán gần đây để làm mịn
        
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
            logger.info(f"Starting Neural Network posture detection with camera ID: {self.camera_id}")
            self.running = True
            
            # Xử lý camera dựa trên loại camera
            if self.camera_id == 1 and not self.camera_url:
                # Camera WiFi mặc định nếu không cung cấp URL
                self.camera_url = 'http://192.168.8.3:81/stream'
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
        if hasattr(self, 'capture_thread') and self.capture_thread and self.capture_thread.is_alive():
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
        
        logger.info("Neural Network posture detection service stopped")
    
    def _smooth_prediction(self, posture_class):
        """Làm mịn dự đoán bằng cách lấy kết quả phổ biến nhất"""
        self.recent_predictions.append(posture_class)
        if len(self.recent_predictions) > self.max_predictions:
            self.recent_predictions.pop(0)
        
        # Lấy dự đoán phổ biến nhất
        from collections import Counter
        smoothed_class = Counter(self.recent_predictions).most_common(1)[0][0]
        return smoothed_class
    
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
        
        logger.info("Neural Network frame processing loop started")
        
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
                
                # Get posture prediction using Neural Network
                posture_class, confidence = self.model_service.predict_posture(results=results)
                
                # Smooth the prediction
                if posture_class != "unknown":
                    smoothed_posture = self._smooth_prediction(posture_class)
                else:
                    smoothed_posture = posture_class
                
                # Add model info to frame
               
                cv2.putText(annotated_frame, f"Posture: {smoothed_posture}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Confidence: {confidence:.3f}", 
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Convert frame to base64 for transmission
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                base64_image = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
                
                # Determine if this posture needs an alert
                is_good_posture = (
                    smoothed_posture.startswith("straight_") or 
                    "vai_thang" in smoothed_posture
                )
                needs_alert = not is_good_posture and smoothed_posture != "unknown"
                
                if needs_alert:
                    current_time = datetime.now()
                    if self.last_alert_time is None or (current_time - self.last_alert_time).total_seconds() > 20.0:
                        try:
                            logger.info(f"Neural Network phát hiện tư thế cần cảnh báo: {smoothed_posture}, confidence: {confidence:.3f}")
                            self.alert_service.play_alert_sound(smoothed_posture)
                            self.last_alert_time = current_time
                        except Exception as e:
                            logger.error(f"Lỗi khi phát âm thanh cảnh báo: {str(e)}")
                
                # Prepare the frame data
                posture_info = PostureInfo(
                    posture=smoothed_posture,
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
                logger.error(f"Error processing frame with Neural Network: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
            
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
            logger.warning("Timeout waiting for next frame from Neural Network")
            return None
        except Exception as e:
            logger.error(f"Error getting next frame from Neural Network: {str(e)}")
            return None

    def get_model_info(self):
        """Lấy thông tin về mô hình đang sử dụng"""
        return self.model_service.get_model_info()