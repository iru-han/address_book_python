import datetime

# --- 1. 로그 데이터 모델 (Log) ---
class SystemLog:
    def __init__(self, level: str, message: str, timestamp: str = None, id: int = None):
        self.id = id
        self.level = level  # 예: INFO, WARNING, ERROR
        self.message = message
        # 타임스탬프가 없으면 현재 시간으로 설정
        self.timestamp = timestamp if timestamp else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Log(ID={self.id}, Level={self.level}, Time={self.timestamp}, Msg='{self.message}')"

# --- 2. 상태 데이터 모델 (Status) ---
class SystemStatus:
    def __init__(self, cpu_usage: float, memory_free: int, timestamp: str = None, id: int = None):
        self.id = id
        self.cpu_usage = cpu_usage  # CPU 사용률 (%)
        self.memory_free = memory_free  # 사용 가능 메모리 (MB)
        self.timestamp = timestamp if timestamp else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Status(ID={self.id}, Time={self.timestamp}, CPU={self.cpu_usage}%, MemFree={self.memory_free}MB)"