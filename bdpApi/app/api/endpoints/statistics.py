from fastapi import APIRouter, Depends
from app.models.schemas import ApiResponse
from app.api.endpoints.camera import get_camera_state

router = APIRouter()

@router.get("/statistics", response_model=ApiResponse)
async def get_statistics(camera_state=Depends(get_camera_state)):
    stats = camera_state.monitor.get_statistics()
    return ApiResponse(success=True, message="Thống kê tư thế", data=stats)

@router.post("/reset_statistics", response_model=ApiResponse)
async def reset_statistics(camera_state=Depends(get_camera_state)):
    camera_state.monitor.reset()
    return ApiResponse(success=True, message="Đã reset thống kê")
