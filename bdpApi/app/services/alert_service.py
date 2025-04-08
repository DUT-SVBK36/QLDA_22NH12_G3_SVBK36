import os
import pygame
import logging
import cv2
from datetime import datetime
from typing import Optional

from app.config import AUDIO_ALERTS_DIR, SCREENSHOTS_DIR, logger

class AlertService:
    def __init__(self):
        # Khởi tạo pygame để phát âm thanh
        pygame.mixer.init()
    
    def play_alert_sound(self, sound_name: str = "alert.mp3") -> None:
        """Phát âm thanh cảnh báo"""
        try:
            # Map the model output posture names to our simplified alert names
            if "leg" in sound_name or sound_name.startswith("leg_"):
                if "right" in sound_name or "correct" in sound_name:
                    base_sound = "leg_right.mp3"
                else:
                    base_sound = "leg_wrong.mp3"
            elif "neck" in sound_name or sound_name.startswith("neck_"):
                if "right" in sound_name or "correct" in sound_name:
                    base_sound = "neck_right.mp3"
                else:
                    base_sound = "neck_wrong.mp3"
            elif "forward" in sound_name or "forward_head" in sound_name:
                base_sound = "bad_sitting_forward.mp3"
            elif "backward" in sound_name or "leaning_backward" in sound_name:
                base_sound = "bad_sitting_backward.mp3"
            elif "left" in sound_name or "nghieng_sang_trai" in sound_name:
                base_sound = "lean_left.mp3"
            elif "right" in sound_name or "nghieng_sang_phai" in sound_name:
                base_sound = "lean_right.mp3"
            else:
                # Default generic posture alert
                base_sound = "posture.mp3"
            
            alert_sound_path = os.path.join(AUDIO_ALERTS_DIR, base_sound)
            
            # Nếu không tìm thấy file âm thanh, sử dụng âm thanh mặc định
            if not os.path.exists(alert_sound_path):
                logger.warning(f"Không tìm thấy file âm thanh: {alert_sound_path}")
                alert_sound_path = os.path.join(AUDIO_ALERTS_DIR, "posture.mp3")
                
                if not os.path.exists(alert_sound_path):
                    logger.warning("Không tìm thấy file âm thanh mặc định")
                    return
            
            pygame.mixer.Sound(alert_sound_path).play()
            logger.info(f"Đang phát âm thanh: {alert_sound_path}")
        except Exception as e:
            logger.error(f"Lỗi khi phát âm thanh: {e}")
    
    def save_screenshot(self, frame, posture: str) -> Optional[str]:
        """Lưu ảnh chụp tư thế sai"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"bad_posture_{posture}_{timestamp}.jpg")
            cv2.imwrite(screenshot_path, frame)
            logger.info(f"Đã lưu ảnh chụp tư thế sai tại: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Lỗi khi lưu ảnh chụp: {e}")
            return None
