from fastapi import APIRouter, Depends, HTTPException, Query, Path
from bson import ObjectId
from typing import List, Dict, Any
from datetime import datetime

from app.models.database_models import (
    SessionModel, SessionResponseModel, 
    SessionItemModel, SessionItemResponseModel,
    SessionDetailModel, UserModel
)
from app.database.database import (
    get_sessions_collection, get_session_items_collection
)
from app.core.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=SessionResponseModel)
async def create_session(current_user: UserModel = Depends(get_current_active_user)):
    """Tạo một phiên ghi nhận tư thế mới"""
    sessions_collection = await get_sessions_collection()
    
    new_session = SessionModel(
        user_id=current_user.id,
        creation_date=datetime.now()
    )
    
    result = await sessions_collection.insert_one(new_session.dict(by_alias=True))
    
    return SessionResponseModel(
        _id=str(result.inserted_id),
        user_id=str(current_user.id),
        creation_date=new_session.creation_date
    )

@router.get("/", response_model=List[SessionResponseModel])
async def get_user_sessions(
    current_user: UserModel = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Lấy danh sách phiên ghi nhận của người dùng hiện tại"""
    sessions_collection = await get_sessions_collection()
    
    cursor = sessions_collection.find(
        {"user_id": ObjectId(current_user.id)}
    ).sort("creation_date", -1).skip(skip).limit(limit)
    
    sessions = []
    async for session in cursor:
        sessions.append(SessionResponseModel(
            _id=str(session["_id"]),
            user_id=str(session["user_id"]),
            creation_date=session["creation_date"]
        ))
    
    return sessions

@router.get("/latest", response_model=SessionResponseModel)
async def get_latest_session(current_user: UserModel = Depends(get_current_active_user)):
    """Lấy phiên ghi nhận mới nhất của người dùng hiện tại"""
    sessions_collection = await get_sessions_collection()
    
    # Find the latest session by creation_date for the current user
    latest_session = await sessions_collection.find_one(
        {"user_id": ObjectId(current_user.id)},
        sort=[("creation_date", -1)]  # Sort by creation_date in descending order
    )
    
    if not latest_session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên ghi nhận nào")
    
    return SessionResponseModel(
        _id=str(latest_session["_id"]),
        user_id=str(latest_session["user_id"]),
        creation_date=latest_session["creation_date"]
    )

@router.get("/{session_id}", response_model=SessionDetailModel)
async def get_session_detail(
    session_id: str = Path(...),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Lấy chi tiết của một phiên ghi nhận"""
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="ID phiên không hợp lệ")
    
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    
    session = await sessions_collection.find_one({
        "_id": ObjectId(session_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên ghi nhận")
    
    # Lấy các mục trong phiên
    items_cursor = session_items_collection.find({"session_id": ObjectId(session_id)})
    
    session_items = []
    async for item in items_cursor:
        session_items.append(SessionItemResponseModel(
            _id=str(item["_id"]),
            session_id=str(item["session_id"]),
            timestamp=item["timestamp"],
            accuracy=item["accuracy"],
            image=item.get("image"),
            image_path=item.get("image_path"),
            start_timestamp=item["start_timestamp"],
            end_timestamp=item.get("end_timestamp"),
            label_name=item["label_name"],
            label_id=item["label_id"],
            label_recommendation=item.get("label_recommendation")
        ))
    
    return SessionDetailModel(
        _id=str(session["_id"]),
        user_id=str(session["user_id"]),
        creation_date=session["creation_date"],
        items=session_items
    )




@router.delete("/{session_id}", response_model=dict)
async def delete_session(
    session_id: str = Path(...),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Xóa một phiên ghi nhận"""
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="ID phiên không hợp lệ")
    
    sessions_collection = await get_sessions_collection()
    session_items_collection = await get_session_items_collection()
    
    session = await sessions_collection.find_one({
        "_id": ObjectId(session_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên ghi nhận")
    
    # Xóa tất cả các mục trong phiên
    await session_items_collection.delete_many({"session_id": ObjectId(session_id)})
    
    # Xóa phiên
    await sessions_collection.delete_one({"_id": ObjectId(session_id)})
    
    return {"message": "Đã xóa phiên ghi nhận thành công"} 