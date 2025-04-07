import os
import pickle
import tensorflow as tf
import numpy as np
import logging
from typing import Dict, Tuple, Any, List, Optional

from app.config import MODELS_DIR, logger

class ModelService:
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self) -> None:
        """Tải các mô hình đã huấn luyện"""
        try:
            # Tải Random Forest
            rf_path = os.path.join(MODELS_DIR, 'random_forest_model.pkl')
            if os.path.exists(rf_path):
                with open(rf_path, 'rb') as f:
                    self.models['rf'] = pickle.load(f)
            
            # Tải Gradient Boosting
            gb_path = os.path.join(MODELS_DIR, 'gradient_boosting_model.pkl')
            if os.path.exists(gb_path):
                with open(gb_path, 'rb') as f:
                    self.models['gb'] = pickle.load(f)
            
            # Tải SVM
            svm_path = os.path.join(MODELS_DIR, 'svm_model.pkl')
            if os.path.exists(svm_path):
                with open(svm_path, 'rb') as f:
                    self.models['svm'] = pickle.load(f)
            
            # Tải Neural Network
            nn_path = os.path.join(MODELS_DIR, 'neural_network_model.keras')
            if os.path.exists(nn_path):
                self.models['nn'] = tf.keras.models.load_model(nn_path)
            
            # Tải thông tin về ensemble
            ensemble_path = os.path.join(MODELS_DIR, 'ensemble_meta.pkl')
            if os.path.exists(ensemble_path):
                with open(ensemble_path, 'rb') as f:
                    self.models['ensemble_meta'] = pickle.load(f)
            
            # Tải scaler
            scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.models['scaler'] = pickle.load(f)
            
            # Tải label encoder
            label_encoder_path = os.path.join(MODELS_DIR, 'label_encoder.pkl')
            if os.path.exists(label_encoder_path):
                with open(label_encoder_path, 'rb') as f:
                    self.models['label_encoder'] = pickle.load(f)
            
            logger.info(f"Đã tải thành công {len(self.models)} mô hình và thành phần")
        
        except Exception as e:
            logger.error(f"Lỗi khi tải mô hình: {e}")
    
    def predict_posture(self, features: List[float]) -> Tuple[Optional[str], float]:
        """Dự đoán tư thế sử dụng mô hình tổng hợp"""
        try:
            if not self.models or 'scaler' not in self.models or 'label_encoder' not in self.models:
                logger.error("Không thể tải các mô hình hoặc thiếu thành phần cần thiết.")
                return None, 0.0
                
            # Chuẩn hóa đặc trưng
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
            if len(predictions) > 0:
                # Tính trung bình có trọng số các dự đoán
                ensemble_pred = np.zeros_like(list(predictions.values())[0])
                
                # Nếu có thông tin về ensemble
                if 'ensemble_meta' in self.models:
                    weights = dict(zip(self.models['ensemble_meta']['models'], self.models['ensemble_meta']['weights']))
                    
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
                predicted_class = self.models['label_encoder'].inverse_transform([predicted_class_idx])[0]
                
                return predicted_class, float(confidence)
            
            return None, 0.0
        
        except Exception as e:
            logger.error(f"Lỗi khi dự đoán tư thế: {e}")
            return None, 0.0
