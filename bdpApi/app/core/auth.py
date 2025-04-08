from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from app.models.database_models import UserModel, UserInDBModel
from app.database.database import get_users_collection

# Cấu hình JWT
SECRET_KEY = "posture_detection_super_secret_key_please_change_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 tuần

# Cấu hình mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def verify_password(plain_password, hashed_password):
    """Kiểm tra mật khẩu"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Tạo hash mật khẩu"""
    return pwd_context.hash(password)

async def get_user_by_username(username: str):
    """Lấy thông tin người dùng theo username"""
    users_collection = await get_users_collection()
    user = await users_collection.find_one({"username": username})
    if user:
        return UserInDBModel(**user)
    return None

async def get_user_by_email(email: str):
    """Lấy thông tin người dùng theo email"""
    users_collection = await get_users_collection()
    user = await users_collection.find_one({"email": email})
    if user:
        return UserInDBModel(**user)
    return None

async def get_user_by_id(user_id: str):
    """Lấy thông tin người dùng theo ID"""
    users_collection = await get_users_collection()
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserInDBModel(**user)
    return None

async def authenticate_user(username: str, password: str):
    """Xác thực người dùng"""
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Tạo JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Lấy người dùng hiện tại từ token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực thông tin đăng nhập",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    """Kiểm tra người dùng có đang hoạt động"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Tài khoản không hoạt động")
    return current_user 