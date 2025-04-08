from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["detection_system"]

# Check if user already exists
existing_user = db.users.find_one({"username": "us1"})

if not existing_user:
    user = {
        "username": "us1",
        "email": "us1@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
        "created_at": datetime.now(),
        "user_id": 1
    }

    try:
        db.users.insert_one(user)
        print("User created successfully")
    except Exception as e:
        print(f"Error creating user: {str(e)}")
else:
    print("User already exists")