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
            alert_sound_path = os.path.join(AUDIO_ALERTS_DIR, sound_name)
            
            # Nếu không tìm thấy file âm thanh, sử dụng âm thanh mặc định
            if not os.path.exists(alert_sound_path):
                logger.warning(f"Không tìm thấy file âm thanh: {alert_sound_path}")
                alert_sound_path = os.path.join(AUDIO_ALERTS_DIR, "alert.mp3")
                
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
