from fastapi import APIRouter, Depends, HTTPException, Path, Query
from bson import ObjectId
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.database_models import (
    LabelModel, LabelResponseModel, UserModel
)
from app.database.database import get_labels_collection
from app.core.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=LabelResponseModel)
async def create_label(
    label: LabelModel,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Tạo một nhãn tư thế mới"""
    labels_collection = await get_labels_collection()
    
    # Kiểm tra label_id đã tồn tại
    existing_label = await labels_collection.find_one({"label_id": label.label_id})
    if existing_label:
        raise HTTPException(status_code=400, detail="Mã nhãn đã tồn tại")
    
    # Kiểm tra tên đã tồn tại
    existing_name = await labels_collection.find_one({"name": label.name})
    if existing_name:
        raise HTTPException(status_code=400, detail="Tên nhãn đã tồn tại")
    
    # Lưu nhãn mới
    result = await labels_collection.insert_one(label.dict(by_alias=True))
    
    return LabelResponseModel(
        _id=str(result.inserted_id),
        label_id=label.label_id,
        name=label.name,
        description=label.description,
        recommendation=label.recommendation,
        severity_level=label.severity_level
    )

@router.get("/", response_model=List[LabelResponseModel])
async def get_labels(
    current_user: Optional[UserModel] = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Lấy danh sách nhãn tư thế"""
    labels_collection = await get_labels_collection()
    
    cursor = labels_collection.find().skip(skip).limit(limit)
    
    labels = []
    async for label in cursor:
        labels.append(LabelResponseModel(
            _id=str(label["_id"]),
            label_id=label["label_id"],
            name=label["name"],
            description=label["description"],
            recommendation=label["recommendation"],
            severity_level=label["severity_level"]
        ))
    
    return labels

@router.get("/{label_id}", response_model=LabelResponseModel)
async def get_label(
    label_id: str = Path(...),
    current_user: Optional[UserModel] = Depends(get_current_active_user)
):
    """Lấy thông tin chi tiết một nhãn tư thế"""
    labels_collection = await get_labels_collection()
    
    # Tìm theo label_id (không phải _id)
    label = await labels_collection.find_one({"label_id": label_id})
    
    if not label:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhãn tư thế")
    
    return LabelResponseModel(
        _id=str(label["_id"]),
        label_id=label["label_id"],
        name=label["name"],
        description=label["description"],
        recommendation=label["recommendation"],
        severity_level=label["severity_level"]
    )

@router.put("/{label_id}", response_model=LabelResponseModel)
async def update_label(
    label_update: LabelModel,
    label_id: str = Path(...),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Cập nhật thông tin một nhãn tư thế"""
    labels_collection = await get_labels_collection()
    
    # Tìm nhãn cần cập nhật
    existing_label = await labels_collection.find_one({"label_id": label_id})
    
    if not existing_label:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhãn tư thế")
    
    # Kiểm tra nếu đổi tên, tên mới đã tồn tại chưa
    if label_update.name != existing_label["name"]:
        name_exists = await labels_collection.find_one({"name": label_update.name, "_id": {"$ne": existing_label["_id"]}})
        if name_exists:
            raise HTTPException(status_code=400, detail="Tên nhãn đã tồn tại")
    
    # Cập nhật thông tin
    update_data = {
        "name": label_update.name,
        "description": label_update.description,
        "recommendation": label_update.recommendation,
        "severity_level": label_update.severity_level
    }
    
    await labels_collection.update_one(
        {"_id": existing_label["_id"]},
        {"$set": update_data}
    )
    
    # Trả về thông tin đã cập nhật
    updated_label = await labels_collection.find_one({"_id": existing_label["_id"]})
    
    return LabelResponseModel(
        _id=str(updated_label["_id"]),
        label_id=updated_label["label_id"],
        name=updated_label["name"],
        description=updated_label["description"],
        recommendation=updated_label["recommendation"],
        severity_level=updated_label["severity_level"]
    )

@router.delete("/{label_id}", response_model=dict)
async def delete_label(
    label_id: str = Path(...),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Xóa một nhãn tư thế"""
    labels_collection = await get_labels_collection()
    
    # Tìm nhãn cần xóa
    existing_label = await labels_collection.find_one({"label_id": label_id})
    
    if not existing_label:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhãn tư thế")
    
    # Xóa nhãn
    await labels_collection.delete_one({"_id": existing_label["_id"]})
    
    return {"message": "Đã xóa nhãn tư thế thành công"} 