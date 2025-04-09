from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class CameraRequest(BaseModel):
    camera_id: int = 0
    camera_url: Optional[str] = None

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
    camera_url: Optional[str] = None

class PostureDetail(BaseModel):
    label_id: str
    name: str
    count: int
    duration: float
    percentage: float
    severity_level: int
    recommendation: Optional[str] = None

class PostureTransition(BaseModel):
    from_label: str
    to_label: str
    from_name: str
    to_name: str
    timestamp: str

class StatisticsResponse(BaseModel):
    session_id: str
    start_time: str
    total_duration: float
    posture_counts: Dict[str, int]
    posture_durations: Dict[str, float]
    posture_percentages: Dict[str, float]
    posture_transitions: List[PostureTransition]
    posture_details: List[PostureDetail]

class DailyStats(BaseModel):
    date: str
    total_duration: float
    posture_counts: Dict[str, int]
    posture_durations: Dict[str, float]

class WorstPosture(BaseModel):
    label_id: str
    name: str
    severity_level: int
    duration: float
    count: int
    recommendation: Optional[str] = None

class UserStatisticsResponse(BaseModel):
    user_id: str
    username: str
    time_range: str
    total_sessions: int
    total_duration: float
    posture_counts: Dict[str, int]
    posture_durations: Dict[str, float]
    daily_stats: List[DailyStats]
    severity_distribution: Dict[int, int]
    worst_postures: List[WorstPosture]

class ESPCommandRequest(BaseModel):
    device_id: str
    ip_address: Optional[str] = None
    audio_file: Optional[str] = None

class ESPStatusResponse(BaseModel):
    device_id: str
    ip_address: str
    last_seen: str
    status: str
