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
            "label_id": "straight_back",
            "name": "Lưng thẳng",
            "description": "Tư thế ngồi thẳng lưng, đầu thẳng",
            "recommendation": "Giữ tư thế này, rất tốt!",
            "severity_level": 0,
            "created_at": datetime.now()
        },
        {
            "label_id": "hunched_back",
            "name": "Gù lưng",
            "description": "Tư thế gù lưng, cổ gập xuống",
            "recommendation": "Hãy ngồi thẳng lưng, nâng đầu lên",
            "severity_level": 4,
            "created_at": datetime.now()
        },
         {
            "label_id": "leaning_forward",
            "name": "Nghiêng về phía trước",
            "description": "Tư thế nghiêng về phía trước, tạo áp lực lên cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để lưng thẳng",
            "severity_level": 2,
            "created_at": datetime.now()
            
        },
         {
            "label_id": "leaning_backward",
            "name": "Nghiêng về phía sau",
            "description": "Tư thế nghiêng về phía sau, không hỗ trợ đúng cách cho cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để lưng tiếp xúc với tựa lưng của ghế",
            "severity_level": 2,
            "created_at": datetime.now()
            
        },
         {
            "label_id": "slouching",
            "name": "Lưng bị cong",
            "description": "Tư thế lưng bị cong, không hỗ trợ đúng cách cho cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để lưng thẳng",
            "severity_level": 3,
            "created_at": datetime.now()
            
        },
         {
            "label_id": "crossed_legs",
            "name": "Bắt chéo chân",
            "description": "Tư thế bắt chéo chân, tạo áp lực không đều lên cột sống",
           
            "severity_level": 4,
            "created_at": datetime.now()
        },
         {
            "label_id": "vai_nho",
            "name": "Vai bị lệch",
            "description": "Tư thế vai bị lệch, tạo áp lực không đều lên cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để vai thẳng",
            "severity_level": 3,
           
            "created_at": datetime.now()
        },
         {
            "label_id": "vai_thang",
            "name": "Vai thẳng",
            "description": "Tư thế vai thẳng, tạo áp lực đều lên cột sống",
            "recommendation": "Giữ tư thế này, rất tốt!",
            "severity_level": 0,
           
            "created_at": datetime.now()
        },
         {
            "label_id": "nghieng_sang_trai",
            "name": "Nghiêng người sang trái",
            "description": "Tư thế nghiêng người sang trái, tạo áp lực không đều lên cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để trọng lượng phân bố đều trên cả hai bên hông",
            "severity_level": 2,
            "created_at": datetime.now()
           
        },
         {
            "label_id": "nghieng_sang_phai",
            "name": "Nghiêng người sang phải",
            "description": "Tư thế nghiêng người sang phải, tạo áp lực không đều lên cột sống",
            "recommendation": "Hãy điều chỉnh tư thế để trọng lượng phân bố đều trên cả hai bên hông",
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