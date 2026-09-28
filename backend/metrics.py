import psutil
import platform
import time

from functools import wraps


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"exception: {e}")
    return wrapper


class Metrics:
    BYTES_PER_GB = 1024 ** 3
    SECONDS_PER_HOURS = 3600

    @property
    @handle_exceptions
    def temperature(self) -> float:
        '''Get CPU temperature'''
        self._temperature = psutil.sensors_temperatures()['acpitz'][0].current
        return self._temperature

    @property
    @handle_exceptions
    def battery(self) -> float:
        '''Get machine battery charge percentage'''
        self._battery = psutil.sensors_battery()
        return round(self._battery.percent,2) if self._battery else None

    @property
    @handle_exceptions
    def memory_percentage(self) -> float:
        '''Get RAM usage percentage'''
        self._memory_percentage = psutil.virtual_memory().percent
        return self._memory_percentage

    @property
    @handle_exceptions
    def root_directory_used_percentage(self) -> float:
        '''Get disk usage percentage'''
        self.disk_usage_percentage = psutil.disk_usage("/").percent
        return self.disk_usage_percentage

    @property
    @handle_exceptions
    def root_directory_total_gigabyte(self) -> float:
        '''Get disk total gigabytes'''
        self.total_disk_gigabyte = psutil.disk_usage("/").total
        return round(self.total_disk_gigabyte / self.BYTES_PER_GB, 2)

    @property
    @handle_exceptions
    def root_directory_used_gigabyte(self) -> float:
        '''Get disk usage gigabytes'''
        self.disk_usage_gigabyte = psutil.disk_usage("/").used
        return round(self.disk_usage_gigabyte / self.BYTES_PER_GB, 2)

    @staticmethod
    @handle_exceptions
    def formatting_seconds(seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    @property
    @handle_exceptions
    def uptime(self) -> float:
        """Get the system uptime in format 00:00:00"""
        self.uptime_system = int(psutil.boot_time())
        self.start = int(time.time())
        return self.formatting_seconds(self.start - self.uptime_system)


if platform.system() != "Linux":
    raise RuntimeError("Metrics supported only on Linux systems")
else: metrics = Metrics()
