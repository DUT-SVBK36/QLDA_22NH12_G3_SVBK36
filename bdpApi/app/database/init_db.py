import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB connection settings
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "detection_system"

async def init_mongodb():
    """Initialize MongoDB with necessary collections and indexes"""
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Create collections if they don't exist
    # (MongoDB creates collections automatically when you insert data)
    
    # Create indexes on users collection
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True)
    
    # Create indexes on sessions collection
    await db.sessions.create_index("user_id")
    await db.sessions.create_index("creation_date")
    
    # Create indexes on session_items collection
    await db.session_items.create_index("session_id")
    await db.session_items.create_index("datetime")
    await db.session_items.create_index("label_name")
    await db.session_items.create_index("label_id")
    
    # Create indexes on labels collection
    await db.labels.create_index("label_id", unique=True)
    await db.labels.create_index("name", unique=True)
    
    # Insert default labels if they don't exist
    default_labels = [
        {
            "label_id": "good_posture",
            "name": "Tư thế đúng",
            "description": "Tư thế ngồi thẳng lưng, đầu thẳng",
            "recommendation": "Giữ tư thế này, rất tốt!",
            "severity_level": 0,
            "created_at": datetime.now()
        },
        {
            "label_id": "bad_sitting_forward",
            "name": "Ngồi cong lưng về phía trước",
            "description": "Tư thế cong lưng về phía trước, tăng áp lực lên cột sống",
            "recommendation": "Hãy ngồi thẳng lưng, dựa vào lưng ghế và điều chỉnh màn hình ngang tầm mắt",
            "severity_level": 3,
            "created_at": datetime.now()
        },
        {
            "label_id": "bad_sitting_backward",
            "name": "Ngồi ngả quá xa về phía sau",
            "description": "Tư thế ngồi ngả quá xa về phía sau, không hỗ trợ đúng cách cho cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để lưng tiếp xúc với tựa lưng của ghế ở góc khoảng 100-110 độ",
            "severity_level": 2,
            "created_at": datetime.now()
        },
        {
            "label_id": "leaning_left_side",
            "name": "Nghiêng về bên trái",
            "description": "Tư thế nghiêng về bên trái, tạo áp lực không đều lên cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để trọng lượng phân bố đều trên cả hai bên hông",
            "severity_level": 2,
            "created_at": datetime.now()
        },
        {
            "label_id": "leaning_right_side",
            "name": "Nghiêng về bên phải",
            "description": "Tư thế nghiêng về bên phải, tạo áp lực không đều lên cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để trọng lượng phân bố đều trên cả hai bên hông",
            "severity_level": 2,
            "created_at": datetime.now()
        },
        {
            "label_id": "neck_right",
            "name": "Tư thế cổ đúng",
            "description": "Cổ thẳng, đầu ngang tầm màn hình",
            "recommendation": "Tiếp tục giữ tư thế cổ như vậy, rất tốt!",
            "severity_level": 0,
            "created_at": datetime.now()
        },
        {
            "label_id": "neck_wrong",
            "name": "Tư thế cổ sai",
            "description": "Cổ và đầu nghiêng về phía trước hoặc các bên, gây căng cơ cổ",
            "recommendation": "Nâng màn hình lên ngang tầm mắt, giữ cổ thẳng và thả lỏng vai",
            "severity_level": 4,
            "created_at": datetime.now()
        },
        {
            "label_id": "leg_right",
            "name": "Tư thế chân đúng",
            "description": "Chân đặt trên sàn hoặc giá đỡ, tạo góc 90 độ tại đầu gối",
            "recommendation": "Tiếp tục giữ tư thế chân như vậy, rất tốt!",
            "severity_level": 0,
            "created_at": datetime.now()
        },
        {
            "label_id": "leg_wrong",
            "name": "Tư thế chân sai",
            "description": "Chân không đặt đúng vị trí, gây áp lực lên đầu gối và hông",
            "recommendation": "Điều chỉnh độ cao ghế để chân tiếp xúc với sàn hoặc sử dụng giá đỡ chân",
            "severity_level": 2,
            "created_at": datetime.now()
        }
    ]
    
    for label in default_labels:
        try:
            # Insert if not exists
            await db.labels.update_one(
                {"label_id": label["label_id"]},
                {"$setOnInsert": label},
                upsert=True
            )
        except Exception as e:
            print(f"Error inserting label {label['label_id']}: {str(e)}")
    
    print("MongoDB collections and indexes initialized successfully.")

if __name__ == "__main__":
    # Run the async function
    asyncio.run(init_mongodb()) 