import sqlite3
from entities.linux_log_entry import LinuxLogEntry

class LinuxLogRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def createLogTable(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linux_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                component TEXT,
                level TEXT,
                message TEXT,
                source_file TEXT
            )
        """)
        conn.commit()
        conn.close()

    def insert(self, log_entry: LinuxLogEntry):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO linux_log (timestamp, component, level, message, source_file)
            VALUES (?, ?, ?, ?, ?)
        """, (log_entry.timestamp, log_entry.component, log_entry.level, log_entry.message, log_entry.source_file))
        conn.commit()
        conn.close()
        
    def findAll(self, limit=100):
        # 최신 로그 100개 조회 기능 (타임라인에 사용)
        # ... (구현 예정)
        pass