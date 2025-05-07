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
        self.is_playing = False
        self.last_play_time = None
    
    # Sửa lại định nghĩa hàm - đưa ra khỏi __init__
    def play_alert_sound(self, sound_name: str = "alert.mp3") -> None:
        """Phát âm thanh cảnh báo"""
        try:
            # Kiểm tra nếu đang phát âm thanh và chưa đủ thời gian
            current_time = datetime.now()
            if self.is_playing and self.last_play_time and (current_time - self.last_play_time).total_seconds() < 5:
                logger.info(f"Đang phát âm thanh, bỏ qua yêu cầu mới: {sound_name}")
                return

            # Map tên tư thế sang ID track
            track_id = self.map_posture_to_track(sound_name)
            
            # Ghi log trước khi gửi lệnh
            logger.info(f"Chuẩn bị gửi lệnh phát âm thanh: {sound_name} (Track {track_id})")
            
            # Đánh dấu đang phát âm thanh
            self.is_playing = True
            self.last_play_time = current_time
            
            # Gửi lệnh phát âm thanh đến ESP32 với track_id đã được ánh xạ
            self.send_audio_command_to_esp32(track_id)
            
            # Đặt hẹn giờ để đánh dấu kết thúc phát âm thanh sau 15 giây
            import threading
            threading.Timer(5, self._reset_playing_state).start()
            
            logger.info(f"Đã gửi lệnh phát âm thanh: {sound_name} (Track {track_id})")
        except Exception as e:
            logger.error(f"Lỗi khi phát âm thanh: {e}")
            self.is_playing = False
            # Thử phát âm thanh cục bộ nếu gửi lệnh đến ESP32 thất bại
            self._play_local_sound(f"{sound_name}")
    def _reset_playing_state(self):
        """Reset trạng thái phát âm thanh"""
        self.is_playing = False
        logger.info("Đã reset trạng thái phát âm thanh")
    
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
            
            "hunched_back": 7,
            "leaning_forward": 6,
            "leaning_backward": 8,
            "slouching": 1,
            "crossed_legs": 5,
            
            "vai_nho": 2,
            "vai_nho": 2,
            
            "nghieng_sang_trai": 3,
            "nghieng_sang_phai": 4,
            "nghieng_sang_trai": 3,
            "nghieng_sang_phai": 4,
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
