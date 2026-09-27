import psutil
import platform

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
        return round(self._battery.percent,2) if self.battery else None

    @property
    @handle_exceptions
    def memory_percentage(self) -> float:
        '''Get RAM usage percentage'''
        self._memory_percentage = psutil.virtual_memory().percent
        return self._memory_percentage

if platform.system() != "Linux":
    raise RuntimeError("Metrics supported only on Linux systems")
else: metrics = Metrics()