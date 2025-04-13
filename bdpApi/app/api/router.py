from fastapi import APIRouter
from app.api.endpoints import camera, statistics, websocket, auth, sessions, labels

router = APIRouter()

router.include_router(camera.router, tags=["camera"])
router.include_router(statistics.router, tags=["statistics"])
router.include_router(websocket.router, tags=["websocket"])
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
router.include_router(labels.router, prefix="/labels", tags=["labels"])

