from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class PostureDistributionItem(BaseModel):
    count: int
    name: str
    duration: float
    severity_level: int
    percentage: float
    duration_percentage: float

class PostureDistributionResponse(BaseModel):
    distribution: Dict[str, PostureDistributionItem]
    total_items: int
    total_duration: float

class PostureDurationItem(BaseModel):
    total_duration: float
    count: int
    avg_duration: float
    max_duration: float
    min_duration: float
    name: str
    severity_level: int
    percentage: float

class PostureDurationResponse(BaseModel):
    durations: Dict[str, PostureDurationItem]
    total_duration: float

class PostureHistoryItem(BaseModel):
    id: str
    session_id: str
    label_id: str
    label_name: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: float
    accuracy: float

class PostureHistoryResponse(BaseModel):
    history: List[PostureHistoryItem]
    total_items: int

class PostureImprovementItem(BaseModel):
    session_id: str
    date: datetime
    good_posture_count: int
    bad_posture_count: int
    total_count: int
    good_percentage: float
    bad_percentage: float

class PostureTrendItem(BaseModel):
    date: datetime
    value: float

class PostureImprovementResponse(BaseModel):
    improvement_data: List[PostureImprovementItem]
    overall_improvement: float
    good_posture_trend: List[PostureTrendItem]
    bad_posture_trend: List[PostureTrendItem]

class HourlyPostureData(BaseModel):
    hour: int
    item_count: int
    good_posture_duration: float
    bad_posture_duration: float
    total_duration: float

class DailyPostureSummaryResponse(BaseModel):
    date: datetime
    total_sessions: int
    total_duration: float
    posture_distribution: Dict[str, Any]
    hourly_data: List[HourlyPostureData]

class DailyData(BaseModel):
    date: datetime
    day_of_week: int
    session_count: int
    good_posture_duration: float
    bad_posture_duration: float
    total_duration: float

class WeeklyPostureSummaryResponse(BaseModel):
    start_date: datetime
    end_date: datetime
    total_sessions: int
    total_duration: float
    daily_data: List[DailyData]
    posture_distribution: Dict[str, Any]

class PeriodData(BaseModel):
    total_sessions: int
    total_duration: float
    posture_distribution: Dict[str, Any]
    good_posture_percentage: float
    bad_posture_percentage: float

class Period(BaseModel):
    start_date: datetime
    end_date: datetime
    data: PeriodData

class PostureChangeItem(BaseModel):
    name: str
    percentage_change: float
    duration_change: float
    count_change: int
    period1_percentage: float
    period2_percentage: float
    period1_duration: float
    period2_duration: float
    period1_count: int
    period2_count: int

class PostureComparisonResponse(BaseModel):
    period1: Period
    period2: Period
    good_posture_change: float
    bad_posture_change: float
    posture_changes: Dict[str, PostureChangeItem]
