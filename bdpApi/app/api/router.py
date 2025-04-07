from fastapi import APIRouter
from app.api.endpoints import camera, statistics, websocket

router = APIRouter()

router.include_router(camera.router, tags=["camera"])
router.include_router(statistics.router, tags=["statistics"])
router.include_router(websocket.router, tags=["websocket"])
