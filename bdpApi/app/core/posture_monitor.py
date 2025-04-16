from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional
from collections import Counter

class PostureMonitor:
    def __init__(self, bad_posture_threshold=5):  # Thời gian ngưỡng tính bằng giây
        self.bad_posture_start = None
        self.bad_posture_threshold = bad_posture_threshold
        self.alert_active = False
        self.last_alert_time = None
        self.alert_cooldown = 20  # Thời gian chờ giữa các cảnh báo (giây)
        self.posture_history = []
        self.max_history = 100  # Số lượng mẫu tối đa trong lịch sử
    
    def update(self, posture: str, confidence: float) -> bool:
        current_time = datetime.now()
        
        # Thêm vào lịch sử
        self.posture_history.append((current_time, posture, confidence))
        if len(self.posture_history) > self.max_history:
            self.posture_history.pop(0)
        
        # Kiểm tra tư thế với hỗ trợ cho phân loại mới
        is_good_posture = (
            # Our simplified good postures
            "correct" in posture or
            posture == "posture" or  # Generic good posture
            posture.startswith("good_")  # Keep backward compatibility with good_ prefix
        )
        
        # Nếu tư thế không tốt
        if not is_good_posture:  
            # Bắt đầu tính thời gian tư thế xấu
            if self.bad_posture_start is None:
                self.bad_posture_start = current_time
            
            # Kiểm tra xem đã vượt quá ngưỡng chưa
            elapsed = (current_time - self.bad_posture_start).total_seconds()
            
            if elapsed >= self.bad_posture_threshold and not self.alert_active:
                # Kiểm tra thời gian chờ giữa các cảnh báo
                if self.last_alert_time is None or (current_time - self.last_alert_time).total_seconds() >= self.alert_cooldown:
                    self.alert_active = True
                    self.last_alert_time = current_time
                    return True  # Kích hoạt cảnh báo
        else:
            # Reset thời gian khi tư thế tốt
            self.bad_posture_start = None
            self.alert_active = False
        
        return False  # Không cần cảnh báo

    def get_statistics(self) -> Dict[str, Any]:
        """Tính toán thống kê tư thế"""
        if not self.posture_history:
            return {}
        
        # Tính tổng thời gian theo dõi
        start_time = self.posture_history[0][0]
        end_time = self.posture_history[-1][0]
        total_time = (end_time - start_time).total_seconds()
        
        # Đếm số lần xuất hiện của mỗi tư thế
        posture_counts = {}
        for _, posture, _ in self.posture_history:
            if posture not in posture_counts:
                posture_counts[posture] = 0
            posture_counts[posture] += 1
        
        # Tính phần trăm
        posture_percentages = {}
        for posture, count in posture_counts.items():
            posture_percentages[posture] = (count / len(self.posture_history)) * 100
        
        # Số lần chuyển đổi tư thế
        transitions = 0
        for i in range(1, len(self.posture_history)):
            if self.posture_history[i][1] != self.posture_history[i-1][1]:
                transitions += 1
        
        return {
            'total_time': total_time,
            'posture_counts': posture_counts,
            'posture_percentages': posture_percentages,
            'transitions': transitions
        }

    def reset(self) -> None:
        """Reset lịch sử tư thế"""
        self.posture_history = []
        self.bad_posture_start = None
        self.alert_active = False
        self.last_alert_time = None
