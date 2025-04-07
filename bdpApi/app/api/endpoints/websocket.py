import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from app.api.endpoints.camera import message_queue, get_camera_state,process_camera

router = APIRouter()

# Lưu trữ kết nối WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_json(self, websocket: WebSocket, message: Dict[str, Any]):
        await websocket.send_json(message)

    async def broadcast_json(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                from app.config import logger
                logger.error(f"Error broadcasting message: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

# Hàm xử lý các message từ queue trong event loop chính
async def process_messages():
    while True:
        try:
            # Kiểm tra message mới mỗi 0.01 giây
            await asyncio.sleep(0.01)
            
            # Lấy tất cả message có sẵn trong queue
            while not message_queue.empty():
                message = message_queue.get()
                await manager.broadcast_json(message)
                message_queue.task_done()
                
        except asyncio.CancelledError:
            break
        except Exception as e:
            from app.config import logger
            logger.error(f"Lỗi khi xử lý message từ queue: {e}")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Khởi động một task để xử lý các message từ queue
        process_task = asyncio.create_task(process_messages())
        
        while True:
            # Chờ tin nhắn từ client (có thể là lệnh dừng hoặc các tùy chọn khác)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            camera_state = get_camera_state()
            
            if message.get("action") == "stop":
                camera_state.stop()
                await manager.send_json(websocket, {"type": "status", "data": {"running": False}})
            
            elif message.get("action") == "start":
                camera_id = message.get("camera_id", 0)
                if camera_state.start(camera_id):
                    # Khởi động luồng xử lý camera
                    import threading
                    threading.Thread(target=process_camera, daemon=True).start()
                    await manager.send_json(websocket, {"type": "status", "data": {"running": True}})
                else:
                    await manager.send_json(websocket, {"type": "error", "data": {"message": "Không thể khởi động camera"}})
            
            elif message.get("action") == "reset_stats":
                camera_state.monitor.reset()
                await manager.send_json(websocket, {"type": "status", "data": {"stats_reset": True}})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        from app.config import logger
        logger.error(f"Lỗi WebSocket: {e}")
        manager.disconnect(websocket)
    finally:
        # Hủy task xử lý message
        if 'process_task' in locals():
            process_task.cancel()
