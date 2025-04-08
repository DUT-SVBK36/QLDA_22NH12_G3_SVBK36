from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.router import router as api_router
from app.config import BASE_DIR, SCREENSHOTS_DIR, logger

# Khởi tạo FastAPI
app = FastAPI(title="Posture Detection API")

# Cấu hình CORS
cors_config = {
    "allow_origins": ["*"],  # Cho phép tất cả các origins
    "allow_credentials": True,
    "allow_methods": ["*"],  # Cho phép tất cả các HTTP methods
    "allow_headers": ["*"],  # Cho phép tất cả các headers
}
app.add_middleware(CORSMiddleware, **cors_config)

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
