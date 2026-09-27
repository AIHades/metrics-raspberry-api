import psutil
import time
import platform


def check_platform() -> str:
    if platform.system() == "Windows":
        return "check temperature is not supported"
    elif platform.system() == "Linux":
        return platform.system() + " system"
    else: return None


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"exception: {e}")
    return wrapper


@handle_exceptions
def get_temperature() -> int:
    '''Get CPU temperature'''
    temperature = psutil.sensors_temperatures()['acpitz'][0].current
    return temperature

@handle_exceptions
def get_battery() -> float:
    '''Get machine battery charge percentage'''
    battery = psutil.sensors_battery()[0]
    return round(battery,2) if battery else None

@handle_exceptions
def get_memory_percentage() -> float:
    '''Get RAM usage percentage'''
    memory_percentage = psutil.virtual_memory()[2]
    return memory_percentage

if __name__ == "__main__":
    if check_platform() == "Linux system":
        try:
            while True:
                print(f"temperature: {get_temperature()}")

                if get_battery() is not None:
                    print(f"battery_charge = {get_battery()}%")

                print(f"memory = {get_memory_percentage()}% \n")
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopped")
    else: print("Your system is not supported")