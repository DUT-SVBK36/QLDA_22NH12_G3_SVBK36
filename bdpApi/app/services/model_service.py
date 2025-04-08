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
        self.posture_classes = []
        self.leg_classes = []
        self.neck_classes = []
        self.load_models()
    
    def load_models(self) -> None:
        """Load trained posture detection models using the approach from detect_posture.py"""
        try:
            # Load models
            posture_model_path = os.path.join(MODELS_DIR, 'pose_classifier.h5')
            leg_model_path = os.path.join(MODELS_DIR, 'leg_classifier.h5')
            neck_model_path = os.path.join(MODELS_DIR, 'neck_classifier.h5')

            # Load posture detection models
            if os.path.exists(posture_model_path):
                self.models['posture_model'] = tf.keras.models.load_model(posture_model_path)
            else:
                logger.error(f"Model not found: {posture_model_path}")
            
            if os.path.exists(leg_model_path):
                self.models['leg_model'] = tf.keras.models.load_model(leg_model_path)
            else:
                logger.error(f"Model not found: {leg_model_path}")
            
            if os.path.exists(neck_model_path):
                self.models['neck_model'] = tf.keras.models.load_model(neck_model_path)
            else:
                logger.error(f"Model not found: {neck_model_path}")
            
            # Load scalers
            scaler_posture_path = os.path.join(MODELS_DIR, 'scaler_posture.pkl')
            scaler_leg_path = os.path.join(MODELS_DIR, 'scaler_leg.pkl')
            scaler_neck_path = os.path.join(MODELS_DIR, 'scaler_neck.pkl')
            
            if os.path.exists(scaler_posture_path):
                with open(scaler_posture_path, 'rb') as f:
                    self.models['scaler_posture'] = pickle.load(f)
            else:
                logger.error(f"Scaler not found: {scaler_posture_path}")
            
            if os.path.exists(scaler_leg_path):
                with open(scaler_leg_path, 'rb') as f:
                    self.models['scaler_leg'] = pickle.load(f)
            else:
                logger.error(f"Scaler not found: {scaler_leg_path}")
            
            if os.path.exists(scaler_neck_path):
                with open(scaler_neck_path, 'rb') as f:
                    self.models['scaler_neck'] = pickle.load(f)
            else:
                logger.error(f"Scaler not found: {scaler_neck_path}")
            
            # Load metadata
            metadata_path = os.path.join(MODELS_DIR, 'model_metadata.json')
            if os.path.exists(metadata_path):
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                self.posture_classes = metadata.get('posture_classes', [])
                self.leg_classes = metadata.get('leg_classes', [])
                self.neck_classes = metadata.get('neck_classes', [])
            else:
                logger.error(f"Metadata not found: {metadata_path}")
                # Set default class names
                self.posture_classes = ["good_posture", "bad_posture"]
                self.leg_classes = ["correct_leg", "incorrect_leg"]
                self.neck_classes = ["correct_neck", "incorrect_neck"]
            
            logger.info(f"Successfully loaded {len(self.models)} models and components")
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
    
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
        """Predict posture using the models - can accept either features or MediaPipe results"""
        try:
            if not self.models:
                logger.error("Models not loaded. Cannot make predictions.")
                return "unknown", 0.0
            
            # If we have MediaPipe results, extract keypoints from them
            if results and hasattr(results, 'pose_landmarks'):
                leg_keypoints, neck_keypoints, posture_keypoints = self.extract_and_preprocess_keypoints(results)
                
                # Check if all necessary models and scalers are loaded
                required_components = ['posture_model', 'leg_model', 'neck_model', 
                                     'scaler_posture', 'scaler_leg', 'scaler_neck']
                if not all(comp in self.models for comp in required_components):
                    logger.error("Missing required model components")
                    return "unknown", 0.0
                
                # Normalize keypoints using appropriate scalers
                leg_keypoints_normalized = self.models['scaler_leg'].transform(leg_keypoints)
                neck_keypoints_normalized = self.models['scaler_neck'].transform(neck_keypoints)
                posture_keypoints_normalized = self.models['scaler_posture'].transform(posture_keypoints)
                
                # Make predictions
                leg_pred = self.models['leg_model'].predict(leg_keypoints_normalized, verbose=0)
                neck_pred = self.models['neck_model'].predict(neck_keypoints_normalized, verbose=0)
                posture_pred = self.models['posture_model'].predict(posture_keypoints_normalized, verbose=0)
                
                # Process results just like in detect_posture.py
                # First check leg position
                leg_prob = leg_pred[0][0]
                leg_correct = leg_prob <= 0.5  # Below 0.5 means correct leg position
                
                if leg_correct:
                    # Check posture
                    posture_probs = posture_pred[0]
                    max_posture_idx = np.argmax(posture_probs)
                    current_posture = self.posture_classes[max_posture_idx]
                    
                    # Check if this is a "good" posture
                    is_good_posture = current_posture.startswith("good_")
                    
                    if is_good_posture:
                        # Check neck position
                        neck_probs = neck_pred[0]
                        max_neck_idx = np.argmax(neck_probs)
                        
                        # Only if neck is correct, indicate fully correct posture
                        if max_neck_idx == 0:  # Correct neck position
                            return current_posture, float(posture_probs[max_posture_idx])
                        else:
                            # Neck is incorrect
                            return "neck_" + self.neck_classes[max_neck_idx], float(neck_probs[max_neck_idx])
                    else:
                        # Posture is incorrect
                        return current_posture, float(posture_probs[max_posture_idx])
                else:
                    # Leg position is incorrect
                    return "leg_" + self.leg_classes[1], float(leg_prob)
            
            # Legacy support for old feature-based prediction
            elif features:
                logger.warning("Using legacy feature-based prediction - consider updating to use MediaPipe results")
                if 'neural_network_model' in self.models and 'scaler' in self.models:
                    features_scaled = self.models['scaler'].transform([features])
                    posture_pred = self.models['neural_network_model'].predict(features_scaled, verbose=0)
                    predicted_class_idx = np.argmax(posture_pred)
                    confidence = posture_pred[0][predicted_class_idx]
                    
                    # Map to class name if label encoder is available
                    if 'label_encoder' in self.models:
                        predicted_class = self.models['label_encoder'].inverse_transform([predicted_class_idx])[0]
                        return predicted_class, float(confidence)
                    else:
                        return f"class_{predicted_class_idx}", float(confidence)
                else:
                    logger.error("Neural network model or scaler not loaded")
                    return "unknown", 0.0
            else:
                logger.error("No features or pose landmarks provided for prediction")
                return "unknown", 0.0
                
        except Exception as e:
            logger.error(f"Error predicting posture: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return "unknown", 0.0 