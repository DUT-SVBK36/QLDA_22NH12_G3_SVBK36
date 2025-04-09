from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import Dict, Any, Optional, List
import requests
import asyncio
from datetime import datetime

from app.models.schemas import ApiResponse, ESPCommandRequest, ESPStatusResponse
from app.models.database_models import UserModel
from app.core.auth import get_current_active_user
from app.config import logger

router = APIRouter()

# Lưu trữ thông tin kết nối ESP
esp_devices = {}

@router.post("/register_esp", response_model=ApiResponse)
async def register_esp_device(
    request: ESPCommandRequest,
    current_user: Optional[UserModel] = Depends(get_current_active_user)
):
    """Đăng ký thiết bị ESP mới với hệ thống"""
    device_id = request.device_id
    ip_address = request.ip_address
    
    # Kiểm tra kết nối đến ESP
    try:
        # Gửi ping đến ESP để kiểm tra kết nối
        response = requests.get(f"http://{ip_address}/status", timeout=5)
        if response.status_code == 200:
            # Lưu thông tin thiết bị
            esp_devices[device_id] = {
                "ip_address": ip_address,
                "last_seen": datetime.now(),
                "user_id": str(current_user.id) if current_user else None,
                "status": "connected"
            }
            
            logger.info(f"ESP device registered: {device_id} at {ip_address}")
            return ApiResponse(
                success=True,
                message=f"Thiết bị ESP đã được đăng ký thành công: {device_id}",
                data={"device_id": device_id, "ip_address": ip_address}
            )
        else:
            raise HTTPException(status_code=400, detail=f"Không thể kết nối đến thiết bị ESP: {response.text}")
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Lỗi kết nối đến thiết bị ESP: {str(e)}")

@router.get("/esp_devices", response_model=List[ESPStatusResponse])
async def get_esp_devices(current_user: UserModel = Depends(get_current_active_user)):
    """Lấy danh sách thiết bị ESP đã đăng ký"""
    user_id = str(current_user.id)
    
    # Lọc thiết bị theo user_id
    user_devices = []
    for device_id, device_info in esp_devices.items():
        if device_info.get("user_id") == user_id:
            user_devices.append({
                "device_id": device_id,
                "ip_address": device_info["ip_address"],
                "last_seen": device_info["last_seen"].isoformat(),
                "status": device_info["status"]
            })
    
    return user_devices

@router.post("/play_audio", response_model=ApiResponse)
async def play_audio_on_esp(
    request: ESPCommandRequest,
    current_user: Optional[UserModel] = Depends(get_current_active_user)
):
    """Phát âm thanh trên thiết bị ESP"""
    device_id = request.device_id
    audio_file = request.audio_file
    
    # Kiểm tra thiết bị có tồn tại không
    if device_id not in esp_devices:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy thiết bị ESP: {device_id}")
    
    # Lấy thông tin thiết bị
    device_info = esp_devices[device_id]
    ip_address = device_info["ip_address"]
    
    # Kiểm tra quyền truy cập
    if current_user and device_info.get("user_id") != str(current_user.id):
        raise HTTPException(status_code=403, detail="Bạn không có quyền điều khiển thiết bị này")
    
    try:
        # Gửi lệnh phát âm thanh đến ESP
        payload = {"action": "play_audio", "file": audio_file}
        response = requests.post(f"http://{ip_address}/command", json=payload, timeout=5)
        
        if response.status_code == 200:
            # Cập nhật trạng thái thiết bị
            esp_devices[device_id]["last_seen"] = datetime.now()
            
            return ApiResponse(
                success=True,
                message=f"Đã gửi lệnh phát âm thanh đến thiết bị: {device_id}",
                data={"device_id": device_id, "audio_file": audio_file}
            )
        else:
            raise HTTPException(status_code=400, detail=f"Lỗi khi gửi lệnh đến ESP: {response.text}")
    
    except requests.RequestException as e:
        # Cập nhật trạng thái thiết bị
        esp_devices[device_id]["status"] = "disconnected"
        
        raise HTTPException(status_code=400, detail=f"Lỗi kết nối đến thiết bị ESP: {str(e)}")

@router.post("/send_posture_alert", response_model=ApiResponse)
async def send_posture_alert(
    posture_id: str = Query(..., description="ID của tư thế cần cảnh báo"),
    device_id: Optional[str] = Query(None, description="ID của thiết bị ESP cụ thể, nếu không có sẽ gửi đến tất cả thiết bị"),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Gửi cảnh báo tư thế đến thiết bị ESP"""
    user_id = str(current_user.id)
    
    # Map tư thế ID sang file âm thanh tương ứng
    posture_audio_map = {
        "bad_sitting_forward": "bad_sitting_forward.mp3",
        "bad_sitting_backward": "bad_sitting_backward.mp3",
        "leaning_left_side": "lean_left.mp3",
        "leaning_right_side": "lean_right.mp3",
        "neck_wrong": "neck_wrong.mp3",
        "leg_wrong": "leg_wrong.mp3"
    }
    
    # Lấy file âm thanh tương ứng
    audio_file = posture_audio_map.get(posture_id, "posture.mp3")
    
    # Danh sách thiết bị cần gửi cảnh báo
    target_devices = []
    
    if device_id:
        # Gửi đến thiết bị cụ thể
        if device_id in esp_devices and esp_devices[device_id].get("user_id") == user_id:
            target_devices.append((device_id, esp_devices[device_id]))
    else:
        # Gửi đến tất cả thiết bị của người dùng
        for dev_id, device_info in esp_devices.items():
            if device_info.get("user_id") == user_id:
                target_devices.append((dev_id, device_info))
    
    if not target_devices:
        raise HTTPException(status_code=404, detail="Không tìm thấy thiết bị ESP phù hợp")
    
    # Gửi lệnh đến các thiết bị
    results = []
    for dev_id, device_info in target_devices:
        ip_address = device_info["ip_address"]
        
        try:
            # Gửi lệnh phát âm thanh đến ESP
            payload = {"action": "play_audio", "file": audio_file}
            response = requests.post(f"http://{ip_address}/command", json=payload, timeout=5)
            
            if response.status_code == 200:
                # Cập nhật trạng thái thiết bị
                esp_devices[dev_id]["last_seen"] = datetime.now()
                
                results.append({
                    "device_id": dev_id,
                    "status": "success",
                    "message": "Đã gửi cảnh báo thành công"
                })
            else:
                results.append({
                    "device_id": dev_id,
                    "status": "error",
                    "message": f"Lỗi: {response.text}"
                })
        
        except requests.RequestException as e:
            # Cập nhật trạng thái thiết bị
            esp_devices[dev_id]["status"] = "disconnected"
            
            results.append({
                "device_id": dev_id,
                "status": "error",
                "message": f"Lỗi kết nối: {str(e)}"
            })
    
    return ApiResponse(
        success=True,
        message=f"Đã gửi cảnh báo tư thế {posture_id} đến {len(results)} thiết bị",
        data={"results": results}
    )
