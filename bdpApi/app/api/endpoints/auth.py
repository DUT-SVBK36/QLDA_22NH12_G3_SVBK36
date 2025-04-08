from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from typing import List, Dict
from pydantic import BaseModel

from app.core.auth import (
    authenticate_user, create_access_token, 
    get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user, get_user_by_id
)
from app.models.database_models import (
    UserModel, UserCreateModel, UserResponseModel
)
from app.database.database import get_users_collection

router = APIRouter()

class UserIDModel(BaseModel):
    user_id: str

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Đăng nhập và tạo token"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": str(user.id)
    }

@router.post("/user-token", response_model=dict)
async def get_token_by_user_id(user_data: UserIDModel):
    """Lấy token bằng user_id không cần password"""
    try:
        # Tìm user trong database
        user = await get_user_by_id(user_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy người dùng với ID này",
            )
        
        # Kiểm tra trạng thái hoạt động
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tài khoản không hoạt động",
            )
        
        # Tạo token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user_id": str(user.id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xử lý: {str(e)}",
        )

@router.post("/register", response_model=UserResponseModel)
async def register_user(user_data: UserCreateModel):
    """Đăng ký người dùng mới"""
    users_collection = await get_users_collection()
    
    # Kiểm tra username đã tồn tại
    existing_user = await users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại"
        )
    
    # Kiểm tra email đã tồn tại
    existing_email = await users_collection.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã được sử dụng"
        )
    
    # Tạo người dùng mới
    hashed_password = get_password_hash(user_data.password)
    user_model = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    # Lưu vào database
    result = await users_collection.insert_one(user_model.dict(by_alias=True))
    user_model.id = result.inserted_id
    
    # Trả về thông tin người dùng (không bao gồm mật khẩu)
    user_response = UserResponseModel(
        _id=str(user_model.id),
        username=user_model.username,
        email=user_model.email,
        is_active=user_model.is_active
    )
    
    return user_response

@router.get("/me", response_model=UserResponseModel)
async def get_user_profile(current_user: UserModel = Depends(get_current_active_user)):
    """Lấy thông tin người dùng hiện tại"""
    return UserResponseModel(
        _id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    ) 