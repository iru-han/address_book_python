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

# repositories/sensor_repository.py 내부

    def findLatest(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 가장 최근에 기록된 센서 데이터부터 조회
        cursor.execute("""
            SELECT id, timestamp, led_status, temperature, humidity, light_level 
            FROM sensor_data 
            ORDER BY timestamp DESC LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # SensorData 객체 리스트로 변환하여 반환
        return [SensorData(
            id=row['id'],
            timestamp=row['timestamp'],
            led_status=row['led_status'],
            temperature=row['temperature'],
            humidity=row['humidity'],
            light_level=row['light_level']
        ) for row in rows]