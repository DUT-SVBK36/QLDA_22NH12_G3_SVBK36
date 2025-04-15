from fastapi import APIRouter, Depends, HTTPException, Query, Path
from bson import ObjectId
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.database_models import UserModel
from app.database.database import (
    get_sessions_collection, get_session_items_collection, get_labels_collection
)
from app.core.auth import get_current_active_user
from app.models.schemas import (
    PostureDistributionResponse, PostureDurationResponse, 
    PostureHistoryResponse, PostureImprovementResponse,
    DailyPostureSummaryResponse, WeeklyPostureSummaryResponse,
    PostureComparisonResponse
)

router = APIRouter()

@router.get("/distribution", response_model=PostureDistributionResponse)
async def get_posture_distribution(
    current_user: UserModel = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session_id: Optional[str] = None
):
    """Lấy phân bố các loại tư thế trong khoảng thời gian hoặc phiên cụ thể"""
    session_items_collection = await get_session_items_collection()
    labels_collection = await get_labels_collection()
    
    # Xây dựng query filter
    query = {}
    
    if session_id:
        # Nếu có session_id, chỉ lấy dữ liệu từ phiên đó
        if not ObjectId.is_valid(session_id):
            raise HTTPException(status_code=400, detail="ID phiên không hợp lệ")
        query["session_id"] = ObjectId(session_id)
    else:
        # Nếu không có session_id, lấy tất cả phiên của người dùng trong khoảng thời gian
        sessions_collection = await get_sessions_collection()
        
        # Lọc theo thời gian nếu có
        session_query = {"user_id": ObjectId(current_user.id)}
        if start_date:
            session_query["creation_date"] = {"$gte": start_date}
        if end_date:
            if "creation_date" not in session_query:
                session_query["creation_date"] = {}
            session_query["creation_date"]["$lte"] = end_date
        
        # Lấy danh sách ID phiên
        session_ids = []
        async for session in sessions_collection.find(session_query):
            session_ids.append(session["_id"])
        
        if not session_ids:
            return {"distribution": {}, "total_items": 0}
        
        query["session_id"] = {"$in": session_ids}
    
    # Thực hiện aggregation để đếm số lượng mỗi loại tư thế
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": "$label_id",
            "count": {"$sum": 1},
            "total_duration": {
                "$sum": {
                    "$cond": [
                        {"$ne": ["$end_timestamp", None]},
                        {"$divide": [
                            {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                            1000  # Chuyển từ milliseconds sang seconds
                        ]},
                        0
                    ]
                }
            }
        }},
        {"$sort": {"count": -1}}
    ]
    
    distribution_data = {}
    total_items = 0
    total_duration = 0
    
    async for item in session_items_collection.aggregate(pipeline):
        label_id = item["_id"]
        count = item["count"]
        duration = item["total_duration"]
        
        # Lấy thông tin nhãn
        label_info = await labels_collection.find_one({"label_id": label_id})
        label_name = label_info["name"] if label_info else label_id
        
        distribution_data[label_id] = {
            "count": count,
            "name": label_name,
            "duration": duration,
            "severity_level": label_info.get("severity_level", 0) if label_info else 0
        }
        
        total_items += count
        total_duration += duration
    
    # Tính phần trăm cho mỗi loại tư thế
    for label_id in distribution_data:
        distribution_data[label_id]["percentage"] = (distribution_data[label_id]["count"] / total_items * 100) if total_items > 0 else 0
        distribution_data[label_id]["duration_percentage"] = (distribution_data[label_id]["duration"] / total_duration * 100) if total_duration > 0 else 0
    
    return {
        "distribution": distribution_data,
        "total_items": total_items,
        "total_duration": total_duration
    }

@router.get("/duration", response_model=PostureDurationResponse)
async def get_posture_duration(
    current_user: UserModel = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session_id: Optional[str] = None
):
    """Lấy thời lượng của mỗi loại tư thế"""
    session_items_collection = await get_session_items_collection()
    
    # Xây dựng query tương tự như ở trên
    query = {}
    
    if session_id:
        if not ObjectId.is_valid(session_id):
            raise HTTPException(status_code=400, detail="ID phiên không hợp lệ")
        query["session_id"] = ObjectId(session_id)
    else:
        sessions_collection = await get_sessions_collection()
        session_query = {"user_id": ObjectId(current_user.id)}
        
        if start_date:
            session_query["creation_date"] = {"$gte": start_date}
        if end_date:
            if "creation_date" not in session_query:
                session_query["creation_date"] = {}
            session_query["creation_date"]["$lte"] = end_date
        
        session_ids = []
        async for session in sessions_collection.find(session_query):
            session_ids.append(session["_id"])
        
        if not session_ids:
            return {"durations": {}, "total_duration": 0}
        
        query["session_id"] = {"$in": session_ids}
    
    # Chỉ xem xét các mục có end_timestamp (đã hoàn thành)
    query["end_timestamp"] = {"$ne": None}
    
    # Thực hiện aggregation để tính tổng thời lượng
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": "$label_id",
            "total_duration": {
                "$sum": {
                    "$divide": [
                        {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                        1000  # Chuyển từ milliseconds sang seconds
                    ]
                }
            },
            "count": {"$sum": 1},
            "avg_duration": {
                "$avg": {
                    "$divide": [
                        {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                        1000
                    ]
                }
            },
            "max_duration": {
                "$max": {
                    "$divide": [
                        {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                        1000
                    ]
                }
            },
            "min_duration": {
                "$min": {
                    "$divide": [
                        {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                        1000
                    ]
                }
            }
        }},
        {"$sort": {"total_duration": -1}}
    ]
    
    duration_data = {}
    total_duration = 0
    
    async for item in session_items_collection.aggregate(pipeline):
        label_id = item["_id"]
        duration_data[label_id] = {
            "total_duration": item["total_duration"],
            "count": item["count"],
            "avg_duration": item["avg_duration"],
            "max_duration": item["max_duration"],
            "min_duration": item["min_duration"]
        }
        total_duration += item["total_duration"]
    
    # Lấy thông tin tên nhãn
    labels_collection = await get_labels_collection()
    for label_id in duration_data:
        label_info = await labels_collection.find_one({"label_id": label_id})
        if label_info:
            duration_data[label_id]["name"] = label_info["name"]
            duration_data[label_id]["severity_level"] = label_info.get("severity_level", 0)
        else:
            duration_data[label_id]["name"] = label_id
            duration_data[label_id]["severity_level"] = 0
    
    # Tính phần trăm thời lượng
    for label_id in duration_data:
        duration_data[label_id]["percentage"] = (duration_data[label_id]["total_duration"] / total_duration * 100) if total_duration > 0 else 0
    
    return {
        "durations": duration_data,
        "total_duration": total_duration
    }

@router.get("/history", response_model=PostureHistoryResponse)
async def get_posture_history(
    current_user: UserModel = Depends(get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000)
):
    """Lấy lịch sử tư thế theo thời gian"""
    session_items_collection = await get_session_items_collection()
    sessions_collection = await get_sessions_collection()
    
    # Lấy danh sách phiên của người dùng
    session_query = {"user_id": ObjectId(current_user.id)}
    if start_date:
        session_query["creation_date"] = {"$gte": start_date}
    if end_date:
        if "creation_date" not in session_query:
            session_query["creation_date"] = {}
        session_query["creation_date"]["$lte"] = end_date
    
    session_ids = []
    async for session in sessions_collection.find(session_query):
        session_ids.append(session["_id"])
    
    if not session_ids:
        return {"history": [], "total_items": 0}
    
    # Lấy các mục tư thế đã hoàn thành
    query = {
        "session_id": {"$in": session_ids},
        "end_timestamp": {"$ne": None}
    }
    
    # Sắp xếp theo thời gian bắt đầu
    cursor = session_items_collection.find(query).sort("start_timestamp", 1).limit(limit)
    
    history_items = []
    async for item in cursor:
        duration = (item["end_timestamp"] - item["start_timestamp"]).total_seconds() if item.get("end_timestamp") else 0
        
        history_items.append({
            "id": str(item["_id"]),
            "session_id": str(item["session_id"]),
            "label_id": item["label_id"],
            "label_name": item["label_name"],
            "start_time": item["start_timestamp"],
            "end_time": item["end_timestamp"],
            "duration": duration,
            "accuracy": item["accuracy"]
        })
    
    return {
        "history": history_items,
        "total_items": len(history_items)
    }

@router.get("/improvement", response_model=PostureImprovementResponse)
async def get_posture_improvement(
    current_user: UserModel = Depends(get_current_active_user),
    days: int = Query(30, ge=1, le=365)
):
    """Phân tích sự cải thiện tư thế theo thời gian"""
    session_items_collection = await get_session_items_collection()
    sessions_collection = await get_sessions_collection()
    labels_collection = await get_labels_collection()
    
    # Tính ngày bắt đầu dựa trên số ngày yêu cầu
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Lấy danh sách phiên của người dùng trong khoảng thời gian
    session_query = {
        "user_id": ObjectId(current_user.id),
        "creation_date": {"$gte": start_date, "$lte": end_date}
    }
    
    # Lấy tất cả các phiên
    session_ids = []
    session_dates = {}
    
    async for session in sessions_collection.find(session_query).sort("creation_date", 1):
        session_ids.append(session["_id"])
        session_dates[str(session["_id"])] = session["creation_date"]
    
    if not session_ids:
        return {
            "improvement_data": [],
            "overall_improvement": 0,
            "good_posture_trend": [],
            "bad_posture_trend": []
        }
    
    # Lấy thông tin về các nhãn tư thế tốt/xấu
    good_posture_ids = []
    bad_posture_ids = []
    
    async for label in labels_collection.find():
        if label.get("severity_level", 0) <= 1:  # Tư thế tốt có mức độ nghiêm trọng thấp
            good_posture_ids.append(label["label_id"])
        else:
            bad_posture_ids.append(label["label_id"])
    
    # Tính toán thống kê cho mỗi phiên
    improvement_data = []
    good_posture_percentages = []
    bad_posture_percentages = []
    
    for session_id in session_ids:
        # Đếm số lượng tư thế tốt/xấu trong phiên
        good_count = await session_items_collection.count_documents({
            "session_id": session_id,
            "label_id": {"$in": good_posture_ids}
        })
        
        bad_count = await session_items_collection.count_documents({
            "session_id": session_id,
            "label_id": {"$in": bad_posture_ids}
        })
        
        total_count = good_count + bad_count
        
        if total_count > 0:
            good_percentage = (good_count / total_count) * 100
            bad_percentage = (bad_count / total_count) * 100
        else:
            good_percentage = 0
            bad_percentage = 0
        
        session_date = session_dates[str(session_id)]
        
        improvement_data.append({
            "session_id": str(session_id),
            "date": session_date,
            "good_posture_count": good_count,
            "bad_posture_count": bad_count,
            "total_count": total_count,
            "good_percentage": good_percentage,
            "bad_percentage": bad_percentage
        })
        
        good_posture_percentages.append(good_percentage)
        bad_posture_percentages.append(bad_percentage)
    
    # Tính toán sự cải thiện tổng thể
    overall_improvement = 0
    if len(good_posture_percentages) >= 2:
        # So sánh phần trăm tư thế tốt giữa phiên đầu tiên và phiên cuối cùng
        initial_good = good_posture_percentages[0]
        final_good = good_posture_percentages[-1]
        overall_improvement = final_good - initial_good
    
    # Tạo dữ liệu xu hướng
    good_posture_trend = []
    bad_posture_trend = []
    
    for item in improvement_data:
        good_posture_trend.append({
            "date": item["date"],
            "value": item["good_percentage"]
        })
        
        bad_posture_trend.append({
            "date": item["date"],
            "value": item["bad_percentage"]
        })
    
    return {
        "improvement_data": improvement_data,
        "overall_improvement": overall_improvement,
        "good_posture_trend": good_posture_trend,
        "bad_posture_trend": bad_posture_trend
    }

@router.get("/daily-summary", response_model=DailyPostureSummaryResponse)
async def get_daily_posture_summary(
    current_user: UserModel = Depends(get_current_active_user),
    date: Optional[datetime] = None
):
    """Lấy tóm tắt tư thế theo ngày"""
    if not date:
        date = datetime.now()
    
    # Tính ngày bắt đầu và kết thúc
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
    end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
    
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    labels_collection = await get_labels_collection()
    
    # Lấy các phiên trong ngày
    session_query = {
        "user_id": ObjectId(current_user.id),
        "creation_date": {"$gte": start_of_day, "$lte": end_of_day}
    }
    
    session_ids = []
    async for session in sessions_collection.find(session_query):
        session_ids.append(session["_id"])
    
    if not session_ids:
        return {
            "date": date,
            "total_sessions": 0,
            "total_duration": 0,
            "posture_distribution": {},
            "hourly_data": []
        }
    
    # Lấy thông tin tư thế trong các phiên
    query = {
        "session_id": {"$in": session_ids},
        "end_timestamp": {"$ne": None}
    }
    
    # Tính tổng thời lượng và phân bố tư thế
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": "$label_id",
            "count": {"$sum": 1},
            "total_duration": {
                "$sum": {
                    "$divide": [
                        {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                        1000
                    ]
                }
            }
        }}
    ]
    
    posture_distribution = {}
    total_duration = 0
    
    async for item in session_items_collection.aggregate(pipeline):
        label_id = item["_id"]
        count = item["count"]
        duration = item["total_duration"]
        
        # Lấy thông tin nhãn
        label_info = await labels_collection.find_one({"label_id": label_id})
        label_name = label_info["name"] if label_info else label_id
        
        posture_distribution[label_id] = {
            "count": count,
            "name": label_name,
            "duration": duration,
            "severity_level": label_info.get("severity_level", 0) if label_info else 0
        }
        
        total_duration += duration
    
    # Tính phần trăm cho mỗi loại tư thế
    for label_id in posture_distribution:
        posture_distribution[label_id]["percentage"] = (posture_distribution[label_id]["duration"] / total_duration * 100) if total_duration > 0 else 0
    
    # Tính dữ liệu theo giờ
    hourly_data = []
    
    for hour in range(24):
        hour_start = datetime(date.year, date.month, date.day, hour, 0, 0)
        hour_end = datetime(date.year, date.month, date.day, hour, 59, 59)
        
        # Đếm số lượng tư thế trong giờ này
        hour_query = {
            "session_id": {"$in": session_ids},
            "start_timestamp": {"$gte": hour_start, "$lte": hour_end}
        }
        
        hour_count = await session_items_collection.count_documents(hour_query)
        
        # Tính thời lượng tư thế tốt/xấu trong giờ này
        good_posture_duration = 0
        bad_posture_duration = 0
        
        hour_items = session_items_collection.find(hour_query)
        async for item in hour_items:
            if not item.get("end_timestamp"):
                continue
            
            duration = (item["end_timestamp"] - item["start_timestamp"]).total_seconds()
            
            # Kiểm tra nhãn tư thế
            label_info = await labels_collection.find_one({"label_id": item["label_id"]})
            
            if label_info and label_info.get("severity_level", 0) <= 1:
                good_posture_duration += duration
            else:
                bad_posture_duration += duration
        
        hourly_data.append({
            "hour": hour,
            "item_count": hour_count,
            "good_posture_duration": good_posture_duration,
            "bad_posture_duration": bad_posture_duration,
            "total_duration": good_posture_duration + bad_posture_duration
        })
    
    return {
        "date": date,
        "total_sessions": len(session_ids),
        "total_duration": total_duration,
        "posture_distribution": posture_distribution,
        "hourly_data": hourly_data
    }

@router.get("/weekly-summary", response_model=WeeklyPostureSummaryResponse)
async def get_weekly_posture_summary(
    current_user: UserModel = Depends(get_current_active_user),
    start_date: Optional[datetime] = None
):
    """Lấy tóm tắt tư thế theo tuần"""
    if not start_date:
        # Tính ngày đầu tuần (thứ 2)
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday())
        start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    
    # Tính ngày kết thúc tuần (chủ nhật)
    end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    
    # Lấy các phiên trong tuần
    session_query = {
        "user_id": ObjectId(current_user.id),
        "creation_date": {"$gte": start_date, "$lte": end_date}
    }
    
    session_ids = []
    async for session in sessions_collection.find(session_query):
        session_ids.append(session["_id"])
    
    if not session_ids:
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_sessions": 0,
            "total_duration": 0,
            "daily_data": [],
            "posture_distribution": {}
        }
    
    # Lấy thông tin tư thế trong các phiên
    query = {
        "session_id": {"$in": session_ids},
        "end_timestamp": {"$ne": None}
    }
    
    # Tính tổng thời lượng và phân bố tư thế
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": "$label_id",
            "count": {"$sum": 1},
            "total_duration": {
                "$sum": {
                    "$divide": [
                        {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                        1000
                    ]
                }
            }
        }}
    ]
    
    posture_distribution = {}
    total_duration = 0
    
    labels_collection = await get_labels_collection()
    
    async for item in session_items_collection.aggregate(pipeline):
        label_id = item["_id"]
        count = item["count"]
        duration = item["total_duration"]
        
        # Lấy thông tin nhãn
        label_info = await labels_collection.find_one({"label_id": label_id})
        label_name = label_info["name"] if label_info else label_id
        
        posture_distribution[label_id] = {
            "count": count,
            "name": label_name,
            "duration": duration,
            "severity_level": label_info.get("severity_level", 0) if label_info else 0
        }
        
        total_duration += duration
    
    # Tính phần trăm cho mỗi loại tư thế
    for label_id in posture_distribution:
        posture_distribution[label_id]["percentage"] = (posture_distribution[label_id]["duration"] / total_duration * 100) if total_duration > 0 else 0
    
    # Tính dữ liệu theo ngày
    daily_data = []
    
    for day_offset in range(7):
        day_date = start_date + timedelta(days=day_offset)
        day_start = datetime(day_date.year, day_date.month, day_date.day, 0, 0, 0)
        day_end = datetime(day_date.year, day_date.month, day_date.day, 23, 59, 59)
        
        # Lấy các phiên trong ngày
        day_session_query = {
            "user_id": ObjectId(current_user.id),
            "creation_date": {"$gte": day_start, "$lte": day_end}
        }
        
        day_session_ids = []
        async for session in sessions_collection.find(day_session_query):
            day_session_ids.append(session["_id"])
        
        # Tính thời lượng tư thế tốt/xấu trong ngày
        good_posture_duration = 0
        bad_posture_duration = 0
        
        if day_session_ids:
            day_query = {
                "session_id": {"$in": day_session_ids},
                "end_timestamp": {"$ne": None}
            }
            
            day_items = session_items_collection.find(day_query)
            async for item in day_items:
                duration = (item["end_timestamp"] - item["start_timestamp"]).total_seconds()
                
                # Kiểm tra nhãn tư thế
                label_info = await labels_collection.find_one({"label_id": item["label_id"]})
                
                if label_info and label_info.get("severity_level", 0) <= 1:
                    good_posture_duration += duration
                else:
                    bad_posture_duration += duration
        
        daily_data.append({
            "date": day_date,
            "day_of_week": day_date.weekday(),
            "session_count": len(day_session_ids),
            "good_posture_duration": good_posture_duration,
            "bad_posture_duration": bad_posture_duration,
            "total_duration": good_posture_duration + bad_posture_duration
        })
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_sessions": len(session_ids),
        "total_duration": total_duration,
        "daily_data": daily_data,
        "posture_distribution": posture_distribution
    }

@router.get("/compare-periods", response_model=PostureComparisonResponse)
async def compare_periods(
    current_user: UserModel = Depends(get_current_active_user),
    period1_start: datetime = Query(...),
    period1_end: datetime = Query(...),
    period2_start: datetime = Query(...),
    period2_end: datetime = Query(...)
):
    """So sánh tư thế giữa hai khoảng thời gian"""
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    labels_collection = await get_labels_collection()
    
    # Hàm helper để lấy dữ liệu cho một khoảng thời gian
    async def get_period_data(start_date, end_date):
        # Lấy các phiên trong khoảng thời gian
        period_session_query = {
            "user_id": ObjectId(current_user.id),
            "creation_date": {"$gte": start_date, "$lte": end_date}
        }
        
        period_session_ids = []
        async for session in sessions_collection.find(period_session_query):
            period_session_ids.append(session["_id"])
        
        if not period_session_ids:
            return {
                "total_sessions": 0,
                "total_duration": 0,
                "posture_distribution": {},
                "good_posture_percentage": 0,
                "bad_posture_percentage": 0
            }
        
        # Lấy thông tin tư thế
        period_query = {
            "session_id": {"$in": period_session_ids},
            "end_timestamp": {"$ne": None}
        }
        
        # Tính tổng thời lượng và phân bố tư thế
        pipeline = [
            {"$match": period_query},
            {"$group": {
                "_id": "$label_id",
                "count": {"$sum": 1},
                "total_duration": {
                    "$sum": {
                        "$divide": [
                            {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                            1000
                        ]
                    }
                }
            }}
        ]
        
        posture_distribution = {}
        total_duration = 0
        good_posture_duration = 0
        bad_posture_duration = 0
        
        async for item in session_items_collection.aggregate(pipeline):
            label_id = item["_id"]
            count = item["count"]
            duration = item["total_duration"]
            
            # Lấy thông tin nhãn
            label_info = await labels_collection.find_one({"label_id": label_id})
            label_name = label_info["name"] if label_info else label_id
            severity = label_info.get("severity_level", 0) if label_info else 0
            
            posture_distribution[label_id] = {
                "count": count,
                "name": label_name,
                "duration": duration,
                "severity_level": severity
            }
            
            total_duration += duration
            
            # Phân loại tư thế tốt/xấu
            if severity <= 1:
                good_posture_duration += duration
            else:
                bad_posture_duration += duration
        
        # Tính phần trăm
        good_posture_percentage = (good_posture_duration / total_duration * 100) if total_duration > 0 else 0
        bad_posture_percentage = (bad_posture_duration / total_duration * 100) if total_duration > 0 else 0
        
        # Tính phần trăm cho mỗi loại tư thế
        for label_id in posture_distribution:
            posture_distribution[label_id]["percentage"] = (posture_distribution[label_id]["duration"] / total_duration * 100) if total_duration > 0 else 0
        
        return {
            "total_sessions": len(period_session_ids),
            "total_duration": total_duration,
            "posture_distribution": posture_distribution,
            "good_posture_percentage": good_posture_percentage,
            "bad_posture_percentage": bad_posture_percentage
        }
    
    # Lấy dữ liệu cho hai khoảng thời gian
    period1_data = await get_period_data(period1_start, period1_end)
    period2_data = await get_period_data(period2_start, period2_end)
    
    # Tính sự thay đổi
    good_posture_change = period2_data["good_posture_percentage"] - period1_data["good_posture_percentage"]
    bad_posture_change = period2_data["bad_posture_percentage"] - period1_data["bad_posture_percentage"]
    
    # So sánh phân bố tư thế
    posture_changes = {}
    all_posture_ids = set(list(period1_data["posture_distribution"].keys()) + list(period2_data["posture_distribution"].keys()))
    
    for posture_id in all_posture_ids:
        p1_data = period1_data["posture_distribution"].get(posture_id, {"percentage": 0, "duration": 0, "count": 0})
        p2_data = period2_data["posture_distribution"].get(posture_id, {"percentage": 0, "duration": 0, "count": 0})
        
        percentage_change = p2_data["percentage"] - p1_data["percentage"]
        duration_change = p2_data["duration"] - p1_data["duration"]
        count_change = p2_data["count"] - p1_data["count"]
        
        posture_changes[posture_id] = {
            "name": p2_data.get("name", p1_data.get("name", posture_id)),
            "percentage_change": percentage_change,
            "duration_change": duration_change,
            "count_change": count_change,
            "period1_percentage": p1_data["percentage"],
            "period2_percentage": p2_data["percentage"],
            "period1_duration": p1_data["duration"],
            "period2_duration": p2_data["duration"],
            "period1_count": p1_data["count"],
            "period2_count": p2_data["count"]
        }
    
    return {
        "period1": {
            "start_date": period1_start,
            "end_date": period1_end,
            "data": period1_data
        },
        "period2": {
            "start_date": period2_start,
            "end_date": period2_end,
            "data": period2_data
        },
        "good_posture_change": good_posture_change,
        "bad_posture_change": bad_posture_change,
        "posture_changes": posture_changes
    }

@router.get("/user-stats", response_model=Dict[str, Any])
async def get_user_statistics(
    current_user: UserModel = Depends(get_current_active_user)
):
    """Lấy thống kê tổng hợp của người dùng"""
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    
    # Tổng số phiên
    total_sessions = await sessions_collection.count_documents({"user_id": ObjectId(current_user.id)})
    
    # Thời gian phiên đầu tiên và mới nhất
    first_session = await sessions_collection.find_one(
        {"user_id": ObjectId(current_user.id)},
        sort=[("creation_date", 1)]
    )
    
    latest_session = await sessions_collection.find_one(
        {"user_id": ObjectId(current_user.id)},
        sort=[("creation_date", -1)]
    )
    
    first_session_date = first_session["creation_date"] if first_session else None
    latest_session_date = latest_session["creation_date"] if latest_session else None
    
    # Tổng thời gian sử dụng
    total_usage_time = 0
    
    if first_session:
        # Lấy tất cả phiên
        session_ids = []
        async for session in sessions_collection.find({"user_id": ObjectId(current_user.id)}):
            session_ids.append(session["_id"])
        
        if session_ids:
            # Tính tổng thời lượng
            pipeline = [
                {"$match": {
                    "session_id": {"$in": session_ids},
                    "end_timestamp": {"$ne": None}
                }},
                {"$group": {
                    "_id": None,
                    "total_duration": {
                        "$sum": {
                            "$divide": [
                                {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                                1000
                            ]
                        }
                    }
                }}
            ]
            
            result = await session_items_collection.aggregate(pipeline).to_list(length=1)
            if result:
                total_usage_time = result[0]["total_duration"]
    
    # Tính phần trăm tư thế tốt/xấu
    labels_collection = await get_labels_collection()
    
    # Lấy danh sách nhãn tư thế tốt/xấu
    good_posture_ids = []
    bad_posture_ids = []
    
    async for label in labels_collection.find():
        if label.get("severity_level", 0) <= 1:
            good_posture_ids.append(label["label_id"])
        else:
            bad_posture_ids.append(label["label_id"])
    
    # Tính thời lượng tư thế tốt/xấu
    good_posture_duration = 0
    bad_posture_duration = 0
    
    if first_session:
        session_ids = []
        async for session in sessions_collection.find({"user_id": ObjectId(current_user.id)}):
            session_ids.append(session["_id"])
        
        if session_ids:
            # Tính thời lượng tư thế tốt
            good_pipeline = [
                {"$match": {
                    "session_id": {"$in": session_ids},
                    "label_id": {"$in": good_posture_ids},
                    "end_timestamp": {"$ne": None}
                }},
                {"$group": {
                    "_id": None,
                    "duration": {
                        "$sum": {
                            "$divide": [
                                {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                                1000
                            ]
                        }
                    }
                }}
            ]
            
            good_result = await session_items_collection.aggregate(good_pipeline).to_list(length=1)
            if good_result:
                good_posture_duration = good_result[0]["duration"]
            
            # Tính thời lượng tư thế xấu
            bad_pipeline = [
                {"$match": {
                    "session_id": {"$in": session_ids},
                    "label_id": {"$in": bad_posture_ids},
                    "end_timestamp": {"$ne": None}
                }},
                {"$group": {
                    "_id": None,
                    "duration": {
                        "$sum": {
                            "$divide": [
                                {"$subtract": ["$end_timestamp", "$start_timestamp"]},
                                1000
                            ]
                        }
                    }
                }}
            ]
            
            bad_result = await session_items_collection.aggregate(bad_pipeline).to_list(length=1)
            if bad_result:
                bad_posture_duration = bad_result[0]["duration"]
    
    # Tính phần trăm
    total_posture_duration = good_posture_duration + bad_posture_duration
    good_posture_percentage = (good_posture_duration / total_posture_duration * 100) if total_posture_duration > 0 else 0
    bad_posture_percentage = (bad_posture_duration / total_posture_duration * 100) if total_posture_duration > 0 else 0
    
    # Tính số lượng tư thế xấu được sửa
    corrected_postures = 0
    
    if first_session:
        session_ids = []
        async for session in sessions_collection.find({"user_id": ObjectId(current_user.id)}):
            session_ids.append(session["_id"])
        
        if session_ids:
            # Lấy tất cả các mục tư thế theo thời gian
            items = []
            cursor = session_items_collection.find({"session_id": {"$in": session_ids}}).sort("start_timestamp", 1)
            
            async for item in cursor:
                items.append(item)
            
            # Đếm số lần chuyển từ tư thế xấu sang tư thế tốt
            for i in range(1, len(items)):
                prev_item = items[i-1]
                curr_item = items[i]
                
                # Kiểm tra nếu mục trước là tư thế xấu và mục hiện tại là tư thế tốt
                prev_is_bad = prev_item["label_id"] in bad_posture_ids
                curr_is_good = curr_item["label_id"] in good_posture_ids
                
                if prev_is_bad and curr_is_good:
                    corrected_postures += 1
    
    return {
        "total_sessions": total_sessions,
        "first_session_date": first_session_date,
        "latest_session_date": latest_session_date,
        "total_usage_time": total_usage_time,
        "good_posture_duration": good_posture_duration,
        "bad_posture_duration": bad_posture_duration,
        "good_posture_percentage": good_posture_percentage,
        "bad_posture_percentage": bad_posture_percentage,
        "corrected_postures": corrected_postures
    }
