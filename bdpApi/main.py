from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime

from app.api.router import router as api_router
from app.config import BASE_DIR, SCREENSHOTS_DIR, logger

# Khởi tạo FastAPI
app = FastAPI(title="Posture Detection API",docs_url="/docs")

# Cấu hình CORS
cors_config = {
    "allow_origins": ["*"],  # Cho phép tất cả các origins
    "allow_credentials": True,
    "allow_methods": ["*"],  # Cho phép tất cả các HTTP methods
    "allow_headers": ["*"],  # Cho phép tất cả các headers
}
app.add_middleware(CORSMiddleware, **cors_config)

# Kiểm tra MongoDB và các thư viện cần thiết
@app.on_event("startup")
async def startup_db_client():
    try:
        from app.database.database import client
        await client.admin.command('ping')
        logger.info("MongoDB connection established successfully")
        
        # Khởi tạo dữ liệu mặc định nếu cần
        await initialize_default_data()
    except ImportError:
        logger.error("MongoDB related packages not installed. Run 'pip install motor pymongo bson'")
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")

# Khởi tạo dữ liệu mặc định
async def initialize_default_data():
    try:
        from app.database.database import get_labels_collection
        
        # Khởi tạo các nhãn tư thế mặc định
        labels_collection = await get_labels_collection()
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
        
        # Chỉ thêm nhãn nếu chưa tồn tại
        for label in default_labels:
            try:
                # Insert if not exists
                await labels_collection.update_one(
                    {"label_id": label["label_id"]},
                    {"$setOnInsert": label},
                    upsert=True
                )
                logger.info(f"Created or verified label: {label['label_id']}")
            except Exception as e:
                logger.error(f"Error inserting label {label['label_id']}: {str(e)}")
        
        logger.info("Default data initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing default data: {str(e)}")

# Thêm API router
app.include_router(api_router, prefix="/api")

# Mount thư mục static
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Mount thư mục screenshots
app.mount("/screenshots", StaticFiles(directory=SCREENSHOTS_DIR), name="screenshots")

# Cấu hình templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Xử lý lỗi 404
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    return templates.TemplateResponse(
        "404.html", 
        {"request": request}, 
        status_code=404
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


