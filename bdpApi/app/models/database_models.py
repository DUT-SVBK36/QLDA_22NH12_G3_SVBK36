from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

# Custom ObjectId field for Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator, _field_schema):
        return {"type": "string"}

# Pydantic models for MongoDB documents
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(..., unique=True, index=True)
    email: EmailStr = Field(..., unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDBModel(UserModel):
    hashed_password: str

class UserResponseModel(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    is_active: bool
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class LabelModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    label_id: str = Field(..., unique=True)
    name: str = Field(..., unique=True)
    description: str
    recommendation: str
    severity_level: int = Field(..., ge=0, le=5)  # 0-5 scale
    created_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class LabelResponseModel(BaseModel):
    id: str = Field(..., alias="_id")
    label_id: str
    name: str
    description: str
    recommendation: str
    severity_level: int
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }

class SessionModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    creation_date: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class SessionResponseModel(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    creation_date: datetime
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }

class SessionItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    session_id: PyObjectId
    timestamp: datetime = Field(default_factory=datetime.now)
    accuracy: float
    image: Optional[str] = None  # Base64 encoded image
    image_path: Optional[str] = None  # Path to local image file
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    label_name: str
    label_id: str
    label_recommendation: Optional[str] = None
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class SessionItemResponseModel(BaseModel):
    id: str = Field(..., alias="_id")
    session_id: str
    timestamp: datetime
    accuracy: float
    image: Optional[str] = None
    image_path: Optional[str] = None
    start_timestamp: datetime
    end_timestamp: Optional[datetime] = None
    label_name: str
    label_id: str
    label_recommendation: Optional[str] = None
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str}
    }

class SessionDetailModel(SessionResponseModel):
    items: List[SessionItemResponseModel] = [] 