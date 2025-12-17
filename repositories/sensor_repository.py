import sqlite3
from entities.sensor_data import SensorData

class SensorRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def createSensorTable(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                led_status INTEGER,
                temperature REAL,
                humidity REAL,
                light_level REAL
            )
        """)
        conn.commit()
        conn.close()
        
    def insert(self, data: SensorData):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_data (timestamp, led_status, temperature, humidity, light_level)
            VALUES (?, ?, ?, ?, ?)
        """, (data.timestamp, data.led_status, data.temperature, data.humidity, data.light_level))
        conn.commit()
        conn.close()

    def findLatest(self, limit=10):
        # 최신 센서 데이터 10개 조회 기능
        # ... (구현 예정)
        pass