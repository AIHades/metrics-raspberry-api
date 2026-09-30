import asyncio

from fastapi import WebSocketDisconnect, WebSocket, Request
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from metrics import metrics
from src.config import settings
from src.schemas.metrics import MetricsSchema


router = APIRouter(prefix="/metrics")
router.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
templates = Jinja2Templates(directory=settings.templates_dir)

def get_metrics() -> MetricsSchema:
    """Return current system metrics"""
    return MetricsSchema(
        cpu_temperature=metrics.temperature,
        battery=metrics.battery,
        memory_percentage=metrics.memory_percentage,
        disk_usage_percentage = metrics.root_directory_used_percentage,
        total_disk_gigabyte = metrics.root_directory_total_gigabyte,
        disk_usage_gigabyte = metrics.root_directory_used_gigabyte,
        uptime_system = metrics.uptime,
    )

@router.get("/")
async def get_main_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@router.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await asyncio.to_thread(get_metrics)
            data_dict = data.model_dump_json()
            await websocket.send_text(f"{data_dict}")
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        print("Closed")