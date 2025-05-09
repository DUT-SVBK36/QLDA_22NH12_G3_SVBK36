# bdpApi/app/services/alert_service.py
import os
import pygame
import logging
import cv2
import httpx
from datetime import datetime
from typing import Optional

from app.config import AUDIO_ALERTS_DIR, SCREENSHOTS_DIR, logger, ESP32_AUDIO_SERVER

class AlertService:
    def __init__(self):
        # Khởi tạo pygame để phát âm thanh (phương án dự phòng)
        pygame.mixer.init()
    
    # Sửa lại định nghĩa hàm - đưa ra khỏi __init__
    def play_alert_sound(self, sound_name: str = "alert.mp3") -> None:
        """Phát âm thanh cảnh báo"""
        try:
            # Map tên tư thế sang ID track
            track_id = self.map_posture_to_track(sound_name)
            
            # Ghi log trước khi gửi lệnh
            logger.info(f"Chuẩn bị gửi lệnh phát âm thanh: {sound_name} (Track {track_id})")
            
            # Gửi lệnh phát âm thanh đến ESP32 với track_id đã được ánh xạ
            self.send_audio_command_to_esp32(track_id)
            
            logger.info(f"Đã gửi lệnh phát âm thanh: {sound_name} (Track {track_id})")
        except Exception as e:
            logger.error(f"Lỗi khi phát âm thanh: {e}")
            # Thử phát âm thanh cục bộ nếu gửi lệnh đến ESP32 thất bại
            self._play_local_sound(f"track_{track_id}")
    
    def _play_local_sound(self, sound_name: str) -> None:
        """Phát âm thanh từ backend (phương án dự phòng)"""
        try:
            sound_path = os.path.join(AUDIO_ALERTS_DIR, f"{sound_name}.mp3")
            if os.path.exists(sound_path):
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                logger.info(f"Đã phát âm thanh cục bộ: {sound_path}")
            else:
                logger.warning(f"Không tìm thấy file âm thanh: {sound_path}")
        except Exception as e:
            logger.error(f"Lỗi khi phát âm thanh cục bộ: {e}")
        
    def map_posture_to_track(self, posture_name: str) -> int:
        """Ánh xạ tên tư thế sang ID track âm thanh"""
        # Map tên tư thế sang ID track tương ứng
        track_mapping = {
            "good_posture": 1,
            "bad_sitting_forward": 2,
            "bad_sitting_backward": 3,
            "leaning_left_side": 4,
            "leaning_right_side": 5,
            "neck_right": 6,
            "neck_wrong": 7,
            "leg_right": 8,
            "leg_wrong": 8
        }
        
        # Ánh xạ tên tư thế sang track ID
        for key, value in track_mapping.items():
            if key in posture_name:
                return value
        
        # Mặc định trả về track 2 (âm thanh cảnh báo chung) nếu không tìm thấy
        return 2
    
    def check_esp32_connection(self) -> bool:
        """Kiểm tra kết nối với ESP32"""
        try:
            url = f"{ESP32_AUDIO_SERVER}/status"
            response = httpx.get(url, timeout=1.0)
            return response.status_code == 200
        except Exception:
            return False

    def send_audio_command_to_esp32(self, track_id: int) -> None:
        """Gửi lệnh phát âm thanh đến ESP32"""
        try:
            # Kiểm tra kết nối trước
            if not self.check_esp32_connection():
                logger.warning("ESP32 không phản hồi, chuyển sang phát âm thanh từ backend")
                self._play_local_sound(f"track_{track_id}")
                return
                
            url = f"{ESP32_AUDIO_SERVER}/play?track={track_id}"
            
            # Sử dụng httpx.get đồng bộ với timeout ngắn
            response = httpx.get(url, timeout=2.0)
            
            if response.status_code == 200:
                logger.info(f"ESP32 đã nhận lệnh phát âm thanh track {track_id}")
            else:
                logger.warning(f"ESP32 phản hồi lỗi: {response.status_code} - {response.text}")
                # Phát âm thanh từ backend nếu ESP32 phản hồi lỗi
                self._play_local_sound(f"track_{track_id}")
                
        except Exception as e:
            logger.error(f"Không thể kết nối đến ESP32: {str(e)}")
            # Phát âm thanh từ backend nếu không kết nối được ESP32
            self._play_local_sound(f"track_{track_id}")
    
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
