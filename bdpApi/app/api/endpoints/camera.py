from fastapi import APIRouter, Depends
from app.models.schemas import CameraRequest, ApiResponse
from app.core.camera import CameraState
import threading
import queue

router = APIRouter()

# Hàm để lấy camera_state từ dependency
def get_camera_state(message_queue=Depends(lambda: message_queue)):
    return camera_state

# Khởi tạo message_queue và camera_state
message_queue = queue.Queue()
camera_state = CameraState(message_queue)

# Hàm xử lý camera trong một luồng riêng biệt
def process_camera():
    try:
        while camera_state.is_running:
            if not camera_state.process_frame():
                # Ngủ một chút nếu không xử lý frame
                import time
                time.sleep(0.01)
    except Exception as e:
        from app.config import logger
        logger.error(f"Lỗi trong quá trình xử lý camera: {e}")
    finally:
        camera_state.stop()
        # Thông báo cho client rằng camera đã dừng
        status_message = {
            "type": "status",
            "data": {"running": False}
        }
        message_queue.put(status_message)

@router.post("/start_camera", response_model=ApiResponse)
async def start_camera(request: CameraRequest, camera_state=Depends(get_camera_state)):
    success = camera_state.start(request.camera_id)
    if success:
        # Khởi động luồng xử lý camera
        threading.Thread(target=process_camera, daemon=True).start()
        return ApiResponse(success=True, message="Camera đã được khởi động")
    else:
        return ApiResponse(success=False, message="Không thể khởi động camera")

@router.post("/stop_camera", response_model=ApiResponse)
async def stop_camera(camera_state=Depends(get_camera_state)):
    success = camera_state.stop()
    return ApiResponse(success=success, message="Camera đã được dừng" if success else "Không thể dừng camera")
