from pydantic import BaseModel


class MetricsSchema(BaseModel):
    temperature: float | None = None
    battery: float | None = None
    memory_percentage : float | None = None
    disk_usage_percentage: float | None = None
    total_disk_gigabyte: float | None = None
    disk_usage_gigabyte: float | None = None
    uptime_system: float | None = None