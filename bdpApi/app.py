from fastapi import FastAPI, HTTPException
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DFPlayer API", description="API để điều khiển DFPlayer Mini qua ESP32")

# Cấu hình CORS để cho phép truy cập từ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả nguồn gốc
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Địa chỉ IP của ESP32 - cần thay đổi theo địa chỉ IP thực tế của ESP32
# Bạn cần cập nhật địa chỉ IP này sau khi xem Serial Monitor của ESP32
ESP_IP = "http://192.168.1.27"  # Thay đổi địa chỉ IP cho phù hợp

@app.get("/")
async def root():
    return {"message": "DFPlayer Mini API is running"}

@app.get("/play/{track_number}")
async def play_track(track_number: int):
    """
    Phát một bài hát theo số thứ tự
    """
    if track_number <= 0:
        raise HTTPException(status_code=400, detail="Track number must be positive")
    
    try:
        response = requests.get(f"{ESP_IP}/play?track={track_number}", timeout=5)
        if response.status_code == 200:
            return {"status": "success", "message": f"Playing track {track_number}"}
        else:
            return {"status": "error", "message": f"Failed to play track: {response.text}"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@app.get("/volume/{volume_level}")
async def set_volume(volume_level: int):
    """
    Điều chỉnh âm lượng (0-30)
    """
    if volume_level < 0 or volume_level > 30:
        raise HTTPException(status_code=400, detail="Volume must be between 0 and 30")
    
    try:
        response = requests.get(f"{ESP_IP}/volume?volume={volume_level}", timeout=5)
        if response.status_code == 200:
            return {"status": "success", "message": f"Volume set to {volume_level}"}
        else:
            return {"status": "error", "message": f"Failed to set volume: {response.text}"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@app.get("/pause")
async def pause_playback():
    """
    Tạm dừng phát nhạc
    """
    try:
        response = requests.get(f"{ESP_IP}/pause", timeout=5)
        if response.status_code == 200:
            return {"status": "success", "message": "Music paused"}
        else:
            return {"status": "error", "message": f"Failed to pause: {response.text}"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@app.get("/resume")
async def resume_playback():
    """
    Tiếp tục phát nhạc
    """
    try:
        response = requests.get(f"{ESP_IP}/resume", timeout=5)
        if response.status_code == 200:
            return {"status": "success", "message": "Music resumed"}
        else:
            return {"status": "error", "message": f"Failed to resume: {response.text}"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@app.get("/status")
async def get_status():
    """
    Kiểm tra trạng thái của DFPlayer
    """
    try:
        response = requests.get(f"{ESP_IP}/status", timeout=5)
        if response.status_code == 200:
            return {"status": "success", "message": response.text}
        else:
            return {"status": "error", "message": f"Failed to get status: {response.text}"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

if __name__ == "__main__":
    print("Starting DFPlayer API server...")
    print(f"Make sure to update the ESP32 IP address in the code: {ESP_IP}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
