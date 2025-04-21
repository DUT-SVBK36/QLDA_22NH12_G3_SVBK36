import os
import logging
from pathlib import Path

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Đường dẫn cơ sở
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "posture_data"
MODELS_DIR = DATA_DIR / "models"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
AUDIO_ALERTS_DIR = DATA_DIR / "audio_alerts"

# Tạo thư mục nếu chưa tồn tại
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(AUDIO_ALERTS_DIR, exist_ok=True)

# Tên tư thế bằng tiếng Việt
POSTURE_NAMES_VI = {
    
    "straight_back": "Lưng thẳng",
    "hunched_back": "Gù lưng quá sau, cổ gập xuống",
    "leaning_forward": "Nghiêng trước",
    "leaning_backward": "Nghiêng sau",
    "slouching": "Lưng bị cong",
    "crossed_legs": "Bắt chéo chân",
    "vai_nho": "Vai bị lệch",
    "vai_thang": "Vai thẳng",
    "nghieng_sang_trai": "Nghiêng người sang trái",
    "nghieng_sang_phai": "Nghiêng người sang phải",
    
    
}

# Cấu hình camera
CAMERA_FRAME_INTERVAL = 0.1  # 10 FPS cho xử lý nội bộ
IMAGE_SEND_INTERVAL = 2.0    # 2 giây gửi một ảnh

# Cấu hình cảnh báo
BAD_POSTURE_THRESHOLD = 5    # Thời gian ngưỡng tính bằng giây
ALERT_COOLDOWN = 20.0          # Thời gian chờ giữa các cảnh báo (giây)
# Cấu hình ESP32 Audio Server
ESP32_AUDIO_SERVER = "http://192.168.248.180"
