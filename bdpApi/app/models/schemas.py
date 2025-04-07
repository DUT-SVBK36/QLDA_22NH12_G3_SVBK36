from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class CameraRequest(BaseModel):
    camera_id: int = 0

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class PostureInfo(BaseModel):
    posture: str
    posture_vi: Optional[str] = None
    confidence: float
    need_alert: bool
    angles: Optional[Dict[str, float]] = None

class FrameData(BaseModel):
    image: str
    posture: PostureInfo
    timestamp: str

class PostureUpdateData(BaseModel):
    posture: PostureInfo
    timestamp: str

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]

class WebSocketCommand(BaseModel):
    action: str
    camera_id: Optional[int] = 0
