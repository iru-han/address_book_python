import datetime

class SensorData:
    def __init__(self, id=None, timestamp=None, led_status=None, temperature=None, humidity=None, light_level=None):
        self.id = id
        self.timestamp = timestamp if timestamp else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.led_status = led_status  # 0: OFF, 1: ON
        self.temperature = temperature
        self.humidity = humidity
        self.light_level = light_level # 조도 (Lux)
        
    def __str__(self):
        return (f"[ID:{self.id}] {self.timestamp}: "
                f"Temp={self.temperature}°C, Humid={self.humidity}%, "
                f"Light={self.light_level} Lux, LED={'ON' if self.led_status else 'OFF'}")