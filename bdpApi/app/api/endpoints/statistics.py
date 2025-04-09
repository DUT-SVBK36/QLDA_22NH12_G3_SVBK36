from fastapi import APIRouter, Depends, HTTPException, Path, Query
from bson import ObjectId
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.models.schemas import ApiResponse, StatisticsResponse, UserStatisticsResponse
from app.models.database_models import UserModel
from app.database.database import get_sessions_collection, get_session_items_collection, get_labels_collection
from app.core.auth import get_current_active_user
from app.api.endpoints.camera import get_camera_state

router = APIRouter()

@router.get("/statistics", response_model=ApiResponse)
async def get_statistics(camera_state=Depends(get_camera_state)):
    """Lấy thống kê tư thế hiện tại từ camera"""
    stats = camera_state.monitor.get_statistics()
    return ApiResponse(success=True, message="Thống kê tư thế", data=stats)

@router.post("/reset_statistics", response_model=ApiResponse)
async def reset_statistics(camera_state=Depends(get_camera_state)):
    """Reset thống kê tư thế hiện tại"""
    camera_state.monitor.reset()
    return ApiResponse(success=True, message="Đã reset thống kê")

@router.get("/user_statistics", response_model=UserStatisticsResponse)
async def get_user_statistics(
    time_range: str = Query("week", description="Khoảng thời gian thống kê: day, week, month, year, all"),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Lấy thống kê chi tiết của người dùng theo khoảng thời gian"""
    # Xác định khoảng thời gian
    end_date = datetime.now()
    start_date = None
    
    if time_range == "day":
        start_date = end_date - timedelta(days=1)
    elif time_range == "week":
        start_date = end_date - timedelta(weeks=1)
    elif time_range == "month":
        start_date = end_date - timedelta(days=30)
    elif time_range == "year":
        start_date = end_date - timedelta(days=365)
    # Nếu là "all" thì không giới hạn thời gian
    
    # Lấy collections
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    labels_collection = await get_labels_collection()
    
    # Tìm tất cả các phiên của người dùng trong khoảng thời gian
    query = {"user_id": current_user.id}
    if start_date:
        query["creation_date"] = {"$gte": start_date}
    
    sessions_cursor = sessions_collection.find(query).sort("creation_date", -1)
    
    # Khởi tạo biến thống kê
    total_sessions = 0
    total_duration = 0
    posture_counts = {}
    posture_durations = {}
    daily_stats = {}
    severity_distribution = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    worst_postures = []
    
    # Lấy thông tin tất cả các nhãn để có thông tin mức độ nghiêm trọng
    labels = {}
    async for label in labels_collection.find():
        labels[label["label_id"]] = {
            "name": label["name"],
            "severity_level": label["severity_level"],
            "recommendation": label["recommendation"]
        }
    
    # Xử lý từng phiên
    async for session in sessions_cursor:
        total_sessions += 1
        session_id = session["_id"]
        session_date = session["creation_date"]
        
        # Lấy các mục trong phiên
        items_cursor = session_items_collection.find({"session_id": session_id})
        
        # Tạo key cho thống kê theo ngày
        day_key = session_date.strftime("%Y-%m-%d")
        if day_key not in daily_stats:
            daily_stats[day_key] = {
                "total_duration": 0,
                "posture_counts": {},
                "posture_durations": {}
            }
        
        # Xử lý từng mục trong phiên
        async for item in items_cursor:
            label_id = item["label_id"]
            
            # Tính thời lượng
            start_time = item["start_timestamp"]
            end_time = item.get("end_timestamp", datetime.now())
            duration = (end_time - start_time).total_seconds()
            
            # Cập nhật thống kê tổng
            total_duration += duration
            
            # Cập nhật số lần xuất hiện của tư thế
            if label_id not in posture_counts:
                posture_counts[label_id] = 0
            posture_counts[label_id] += 1
            
            # Cập nhật thời lượng của tư thế
            if label_id not in posture_durations:
                posture_durations[label_id] = 0
            posture_durations[label_id] += duration
            
            # Cập nhật thống kê theo ngày
            if label_id not in daily_stats[day_key]["posture_counts"]:
                daily_stats[day_key]["posture_counts"][label_id] = 0
            daily_stats[day_key]["posture_counts"][label_id] += 1
            
            if label_id not in daily_stats[day_key]["posture_durations"]:
                daily_stats[day_key]["posture_durations"][label_id] = 0
            daily_stats[day_key]["posture_durations"][label_id] += duration
            
            daily_stats[day_key]["total_duration"] += duration
            
            # Cập nhật phân phối mức độ nghiêm trọng
            if label_id in labels:
                severity = labels[label_id]["severity_level"]
                severity_distribution[severity] += 1
    
    # Tính tư thế xấu nhất (theo thời lượng và mức độ nghiêm trọng)
    posture_severity_scores = {}
    for label_id, duration in posture_durations.items():
        if label_id in labels:
            severity = labels[label_id]["severity_level"]
            if severity > 0:  # Chỉ tính các tư thế không tốt
                score = duration * severity
                posture_severity_scores[label_id] = score
    
    # Sắp xếp và lấy 5 tư thế xấu nhất
    sorted_postures = sorted(posture_severity_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    for label_id, score in sorted_postures:
        if label_id in labels:
            worst_postures.append({
                "label_id": label_id,
                "name": labels[label_id]["name"],
                "severity_level": labels[label_id]["severity_level"],
                "duration": posture_durations[label_id],
                "count": posture_counts[label_id],
                "recommendation": labels[label_id]["recommendation"]
            })
    
    # Chuyển đổi thống kê theo ngày thành danh sách
    daily_stats_list = []
    for day, stats in daily_stats.items():
        daily_stats_list.append({
            "date": day,
            "total_duration": stats["total_duration"],
            "posture_counts": stats["posture_counts"],
            "posture_durations": stats["posture_durations"]
        })
    
    # Sắp xếp theo ngày
    daily_stats_list.sort(key=lambda x: x["date"])
    
    # Tạo kết quả
    result = {
        "user_id": str(current_user.id),
        "username": current_user.username,
        "time_range": time_range,
        "total_sessions": total_sessions,
        "total_duration": total_duration,
        "posture_counts": posture_counts,
        "posture_durations": posture_durations,
        "daily_stats": daily_stats_list,
        "severity_distribution": severity_distribution,
        "worst_postures": worst_postures
    }
    
    return result

@router.get("/session_statistics/{session_id}", response_model=StatisticsResponse)
async def get_session_statistics(
    session_id: str = Path(...),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Lấy thống kê chi tiết của một phiên cụ thể"""
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="ID phiên không hợp lệ")
    
    # Lấy collections
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    labels_collection = await get_labels_collection()
    
    # Kiểm tra phiên có thuộc về người dùng không
    session = await sessions_collection.find_one({
        "_id": ObjectId(session_id),
        "user_id": current_user.id
    })
    
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên ghi nhận")
    
    # Lấy các mục trong phiên
    items_cursor = session_items_collection.find({"session_id": ObjectId(session_id)})
    
    # Khởi tạo biến thống kê
    total_duration = 0
    posture_counts = {}
    posture_durations = {}
    posture_transitions = []
    
    # Lấy thông tin tất cả các nhãn
    labels = {}
    async for label in labels_collection.find():
        labels[label["label_id"]] = {
            "name": label["name"],
            "severity_level": label["severity_level"],
            "recommendation": label["recommendation"]
        }
    
    # Xử lý từng mục trong phiên
    previous_item = None
    async for item in items_cursor:
        label_id = item["label_id"]
        
        # Tính thời lượng
        start_time = item["start_timestamp"]
        end_time = item.get("end_timestamp", datetime.now())
        duration = (end_time - start_time).total_seconds()
        
        # Cập nhật thống kê tổng
        total_duration += duration
        
        # Cập nhật số lần xuất hiện của tư thế
        if label_id not in posture_counts:
            posture_counts[label_id] = 0
        posture_counts[label_id] += 1
        
        # Cập nhật thời lượng của tư thế
        if label_id not in posture_durations:
            posture_durations[label_id] = 0
        posture_durations[label_id] += duration
        
        # Ghi lại chuyển đổi tư thế
        if previous_item:
            transition = {
                "from_label": previous_item["label_id"],
                "to_label": label_id,
                "from_name": labels.get(previous_item["label_id"], {}).get("name", "Unknown"),
                "to_name": labels.get(label_id, {}).get("name", "Unknown"),
                "timestamp": start_time.isoformat()
            }
            posture_transitions.append(transition)
        
        previous_item = item
    
    # Tính phần trăm thời lượng của từng tư thế
    posture_percentages = {}
    if total_duration > 0:
        for label_id, duration in posture_durations.items():
            posture_percentages[label_id] = (duration / total_duration) * 100
    
    # Tạo kết quả
    result = {
        "session_id": session_id,
        "start_time": session["creation_date"].isoformat(),
        "total_duration": total_duration,
        "posture_counts": posture_counts,
        "posture_durations": posture_durations,
        "posture_percentages": posture_percentages,
        "posture_transitions": posture_transitions,
        "posture_details": []
    }
    
    # Thêm chi tiết về từng tư thế
    for label_id in posture_counts.keys():
        if label_id in labels:
            posture_detail = {
                "label_id": label_id,
                "name": labels[label_id]["name"],
                "count": posture_counts[label_id],
                "duration": posture_durations[label_id],
                "percentage": posture_percentages.get(label_id, 0),
                "severity_level": labels[label_id]["severity_level"],
                "recommendation": labels[label_id]["recommendation"]
            }
            result["posture_details"].append(posture_detail)
    
    return result
