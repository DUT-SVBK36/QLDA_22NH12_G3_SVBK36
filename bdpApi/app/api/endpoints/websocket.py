import json
import asyncio
import base64
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from app.api.endpoints.camera import message_queue, get_camera_state, process_camera
from app.config import logger, SCREENSHOTS_DIR
from queue import Empty
from bson import ObjectId
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.models.schemas import WebSocketMessage, WebSocketCommand
from app.services.model_service import PostureDetectionService
from app.models.database_models import (
    SessionModel, SessionItemModel, LabelModel
)
from app.database.database import (
    get_sessions_collection, get_session_items_collection, get_labels_collection, get_users_collection
)
from app.core.auth import get_current_user, SECRET_KEY, ALGORITHM

router = APIRouter()

# Quản lý kết nối WebSocket
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.detection_services: Dict[str, PostureDetectionService] = {}
        self.detection_tasks: Dict[str, asyncio.Task] = {}
        self.session_ids: Dict[str, ObjectId] = {}
        self.last_posture_check: Dict[str, datetime] = {}
        self.last_posture_label: Dict[str, str] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Kết nối client mới"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket client connected: {client_id}")
    
    def disconnect(self, client_id: str):
        """Ngắt kết nối client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.detection_services:
            self.detection_services[client_id].stop()
            del self.detection_services[client_id]
        if client_id in self.detection_tasks:
            self.detection_tasks[client_id].cancel()
            del self.detection_tasks[client_id]
        if client_id in self.last_posture_check:
            del self.last_posture_check[client_id]
        if client_id in self.last_posture_label:
            del self.last_posture_label[client_id]
        logger.info(f"WebSocket client disconnected: {client_id}")
    
    async def send_message(self, client_id: str, message: dict):
        """Gửi tin nhắn tới client"""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
    
    async def broadcast(self, message: dict):
        """Gửi tin nhắn tới tất cả client"""
        for client_id in self.active_connections:
            await self.send_message(client_id, message)
    
    async def start_detection(self, client_id: str, camera_id: int, user_id: str, camera_url: Optional[str] = None):
        """Bắt đầu phát hiện tư thế"""
        try:
            # Tạo phiên mới trong MongoDB
            if user_id:
                sessions_collection = await get_sessions_collection()
                new_session = SessionModel(
                    user_id=ObjectId(user_id),
                    creation_date=datetime.now()
                )
                result = await sessions_collection.insert_one(new_session.dict(by_alias=True))
                self.session_ids[client_id] = result.inserted_id
                logger.info(f"Created new session {result.inserted_id} for user {user_id}")
            else:
                await self.send_message(client_id, {
                    "type": "error",
                    "message": "User ID is required to start detection"
                })
                return
            
            # Khởi tạo dịch vụ phát hiện tư thế - hỗ trợ camera WiFi
            if camera_id == 1:
                logger.info(f"Initializing WiFi camera with URL: {camera_url}")
                service = PostureDetectionService(camera_id=camera_id, camera_url=camera_url)
            else:
                service = PostureDetectionService(camera_id=camera_id)
            
            self.detection_services[client_id] = service
            
            # Khởi tạo tracking variables
            self.last_posture_check[client_id] = datetime.now()
            self.last_posture_label[client_id] = None
            
            # Tạo task bất đồng bộ
            self.detection_tasks[client_id] = asyncio.create_task(
                self._detection_loop(client_id, service)
            )
            
            camera_info = f"local camera {camera_id}" if camera_id != 1 else f"WiFi camera at {camera_url}"
            await self.send_message(client_id, {
                "type": "status",
                "message": f"Detection started with {camera_info}"
            })
            
            logger.info(f"Started posture detection for client {client_id}, camera {camera_id}")
        except Exception as e:
            await self.send_message(client_id, {
                "type": "error",
                "message": f"Error starting detection: {str(e)}"
            })
            logger.error(f"Error starting detection for client {client_id}: {str(e)}")
    
    async def stop_detection(self, client_id: str):
        """Dừng phát hiện tư thế"""
        if client_id in self.detection_tasks:
            self.detection_tasks[client_id].cancel()
            del self.detection_tasks[client_id]
        
        if client_id in self.detection_services:
            self.detection_services[client_id].stop()
            del self.detection_services[client_id]
        
        await self.send_message(client_id, {
            "type": "status",
            "message": "Detection stopped"
        })
        
        logger.info(f"Stopped posture detection for client {client_id}")
    
    async def _detection_loop(self, client_id: str, service: PostureDetectionService):
        """Vòng lặp phát hiện tư thế"""
        session_items_collection = await get_session_items_collection() if client_id in self.session_ids else None
        labels_collection = await get_labels_collection() if client_id in self.session_ids else None
        
        # Tracking variables
        last_label_id = None
        current_start_time = None
        previous_session_item_id = None
        last_detection_time = datetime.now()
        current_posture_id = None
        last_sent_image = None  # Biến để theo dõi ảnh cuối cùng được gửi
        
        try:
            while True:
                frame_data = await service.get_next_frame()
                
                if frame_data:
                    current_time = datetime.now()
                    current_posture_id = frame_data.posture.posture
                    
                    # Chỉ xử lý thay đổi tư thế nếu đã qua 2 giây kể từ lần cuối kiểm tra
                    time_since_last_check = (current_time - last_detection_time).total_seconds()
                    
                    # Biến cờ để xác định có phải tư thế mới không
                    is_new_posture = False
                    should_save_image = False
                    image_path = None
                    
                    # Kiểm tra nếu thời gian trôi qua đủ 2 giây kể từ lần kiểm tra cuối
                    if time_since_last_check >= 2.0:
                        # Cập nhật thời gian kiểm tra cuối
                        last_detection_time = current_time
                        
                        # Kiểm tra có phải tư thế mới
                        if last_label_id is None or last_label_id != current_posture_id:
                            is_new_posture = True
                            should_save_image = True  # Lưu ảnh cho tư thế mới
                        else:
                            # Nếu tư thế vẫn giữ nguyên sau 2s, vẫn lưu ảnh mới
                            should_save_image = True
                    
                    # Chỉ lưu ảnh nếu cần thiết (tư thế mới hoặc interval 2s)
                    if should_save_image:
                        # Lưu ảnh xuống thư mục
                        timestamp = current_time.strftime("%Y%m%d_%H%M%S_%f")
                        image_filename = f"{timestamp}_{current_posture_id}.jpg"
                        image_path = os.path.join(SCREENSHOTS_DIR, image_filename)
                        
                        # Decode base64 image and save
                        try:
                            image_data = base64.b64decode(frame_data.image.split(',')[1] if ',' in frame_data.image else frame_data.image)
                            with open(image_path, "wb") as f:
                                f.write(image_data)
                            last_sent_image = frame_data.image  # Cập nhật ảnh đã gửi
                        except Exception as e:
                            logger.error(f"Error saving image: {str(e)}")
                    
                    # Gửi kết quả nhận dạng qua WebSocket
                    frame_data_dict = frame_data.dict()
                    
                    # Chỉ thêm ảnh vào response nếu đã lưu ảnh mới
                    if should_save_image and image_path:
                        frame_data_dict["image_path"] = image_path
                    else:
                        # Nếu không có ảnh mới, bỏ trường image để giảm dữ liệu gửi
                        frame_data_dict.pop("image", None)
                    
                    # Lưu tư thế vào MongoDB nếu là tư thế mới
                    if session_items_collection is not None and labels_collection is not None:
                        if is_new_posture:
                            # Đầu tiên, đóng session item cũ nếu có
                            if previous_session_item_id is not None:
                                await session_items_collection.update_one(
                                    {"_id": previous_session_item_id},
                                    {"$set": {"end_timestamp": current_time}}
                                )
                                
                                # Lấy thông tin session item đã hoàn tất
                                completed_item = await session_items_collection.find_one({"_id": previous_session_item_id})
                                if completed_item:
                                    duration = (completed_item["end_timestamp"] - completed_item["start_timestamp"]).total_seconds()
                                    # Gửi thông tin session item hoàn tất cho client
                                    await self.send_message(client_id, {
                                        "type": "session_item_completed",
                                        "data": {
                                            "session_item_id": str(completed_item["_id"]),
                                            "label_id": completed_item["label_id"],
                                            "start_time": completed_item["start_timestamp"].isoformat(),
                                            "end_time": completed_item["end_timestamp"].isoformat(),
                                            "duration_seconds": duration
                                        }
                                    })
                            
                            # Tạo session item mới cho tư thế mới
                            # Lấy thông tin khuyến nghị từ labels collection
                            label_info = await labels_collection.find_one({"label_id": current_posture_id})
                            recommendation = None
                            if label_info:
                                recommendation = label_info.get("recommendation")
                            
                            # Tạo đối tượng session item mới - chỉ lưu ảnh nếu đã lưu
                            session_item_dict = {
                                "session_id": self.session_ids[client_id],
                                "timestamp": current_time,
                                "accuracy": frame_data.posture.confidence,
                                "start_timestamp": current_time,
                                "end_timestamp": None,  # Sẽ cập nhật khi tư thế thay đổi
                                "label_name": current_posture_id,
                                "label_id": current_posture_id,
                                "label_recommendation": recommendation
                            }
                            
                            # Chỉ thêm ảnh và đường dẫn ảnh nếu đã lưu
                            if should_save_image and image_path:
                                session_item_dict["image"] = frame_data.image
                                session_item_dict["image_path"] = image_path
                            
                            session_item = SessionItemModel(**session_item_dict)
                            
                            # Lưu vào database
                            result = await session_items_collection.insert_one(session_item.dict(by_alias=True))
                            previous_session_item_id = result.inserted_id
                            
                            # Cập nhật trạng thái
                            last_label_id = current_posture_id
                            current_start_time = current_time
                            
                            # Cập nhật thông tin cho client
                            frame_data_dict["is_new_posture"] = True
                            frame_data_dict["duration"] = 0
                            frame_data_dict["recommendation"] = recommendation
                            frame_data_dict["session_item_id"] = str(previous_session_item_id)
                            
                            logger.info(f"New posture detected: {current_posture_id}")
                        else:
                            # Nếu không phải tư thế mới, chỉ cập nhật thời gian hiện tại
                            frame_data_dict["is_new_posture"] = False
                            
                            # Tính toán thời lượng của tư thế hiện tại
                            duration = 0
                            if current_start_time:
                                duration = (current_time - current_start_time).total_seconds()
                            
                            frame_data_dict["duration"] = duration
                            
                            if previous_session_item_id:
                                frame_data_dict["session_item_id"] = str(previous_session_item_id)
                    
                    # Gửi kết quả cho client - chỉ nếu là tư thế mới hoặc interval
                    if is_new_posture or should_save_image:
                        await self.send_message(client_id, {
                            "type": "detection_result",
                            "data": frame_data_dict
                        })
                    else:
                        # Gửi thông tin nhẹ hơn (không có ảnh) cho client mỗi 0.5s
                        if time_since_last_check % 0.5 < 0.1:
                            light_data = {
                                "posture": frame_data.posture.dict(),
                                "timestamp": frame_data.timestamp,
                                "duration": frame_data_dict.get("duration", 0)
                            }
                            await self.send_message(client_id, {
                                "type": "posture_update",
                                "data": light_data
                            })
                
                # Ngủ một khoảng thời gian trước khi xử lý khung hình tiếp theo
                await asyncio.sleep(0.1)
        
        except asyncio.CancelledError:
            # Cập nhật thời gian kết thúc của session item cuối cùng
            if session_items_collection is not None and previous_session_item_id is not None:
                try:
                    current_time = datetime.now()
                    await session_items_collection.update_one(
                        {"_id": previous_session_item_id},
                        {"$set": {"end_timestamp": current_time}}
                    )
                    
                    # Gửi thông báo về session item cuối cùng
                    completed_item = await session_items_collection.find_one({"_id": previous_session_item_id})
                    if completed_item:
                        duration = (completed_item["end_timestamp"] - completed_item["start_timestamp"]).total_seconds()
                        await self.send_message(client_id, {
                            "type": "session_item_completed",
                            "data": {
                                "session_item_id": str(completed_item["_id"]),
                                "label_id": completed_item["label_id"],
                                "start_time": completed_item["start_timestamp"].isoformat(),
                                "end_time": completed_item["end_timestamp"].isoformat(),
                                "duration_seconds": duration
                            }
                        })
                except Exception as e:
                    logger.error(f"Error updating final end timestamp: {str(e)}")
            
            # Đóng service
            try:
                service.stop()
            except Exception as e:
                logger.error(f"Error stopping service: {str(e)}")
            
            logger.info(f"Detection loop cancelled for client {client_id}")
        
        except Exception as e:
            await self.send_message(client_id, {
                "type": "error",
                "message": f"Detection error: {str(e)}"
            })
            logger.error(f"Error in detection loop for client {client_id}: {str(e)}")

# Khởi tạo WebSocket manager
ws_manager = WebSocketManager()

# Xác thực token JWT từ query parameter
async def verify_token(token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        # Lấy thông tin user từ database dựa vào username
        users_collection = await get_users_collection()
        user = await users_collection.find_one({"username": username})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        # Trả về MongoDB ObjectId của user
        return str(user["_id"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

# WebSocket endpoint
async def handle_websocket(websocket: WebSocket, client_id: str, token: str):
    await ws_manager.connect(websocket, client_id)
    
    try:
        # Xác thực token
        user_id = await verify_token(token)
        
        # Thông báo xác thực thành công
        await ws_manager.send_message(client_id, {
            "type": "auth_success",
            "user_id": user_id
        })
        
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                command = WebSocketCommand(**message)
                
                if command.action == "start":
                    # Sử dụng user_id đã xác thực và camera_url nếu có
                    camera_url = command.camera_url if hasattr(command, 'camera_url') else None
                    await ws_manager.start_detection(client_id, command.camera_id, user_id, camera_url)
                
                elif command.action == "stop":
                    await ws_manager.stop_detection(client_id)
                
                else:
                    await ws_manager.send_message(client_id, {
                        "type": "error",
                        "message": f"Unknown command: {command.action}"
                    })
            
            except json.JSONDecodeError:
                await ws_manager.send_message(client_id, {
                    "type": "error",
                    "message": "Invalid JSON format"
                })
            
            except Exception as e:
                await ws_manager.send_message(client_id, {
                    "type": "error",
                    "message": f"Error processing command: {str(e)}"
                })
    
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
    
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {str(e)}")
        await websocket.close()
        ws_manager.disconnect(client_id)

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    client_id: str = Query(...), 
    token: str = Query(...)
):
    await handle_websocket(websocket, client_id, token)
