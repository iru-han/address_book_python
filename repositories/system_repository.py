import sqlite3
import datetime
from entities.log import SystemLog, SystemStatus


# 필요한 라이브러리 (CPU/메모리 정보를 얻기 위해 psutil 사용을 가정)
# pip install psutil 로 설치 필요
import psutil 

dbPath = "/mnt/c/Users/User/databases/test7.db"


class SystemRepository:
    def __init__(self, dbPath: str):
        self.dbPath = dbPath

    def getConnection(self):
        return sqlite3.connect(self.dbPath)
        
    def createLogTable(self):
        """시스템 로그 테이블을 생성합니다."""
        conn = self.getConnection()
        cur = conn.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS SystemLog (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Timestamp TEXT NOT NULL,
            Level TEXT NOT NULL,
            Message TEXT NOT NULL
        );
        """
        cur.execute(sql)
        conn.commit()
        conn.close()

    def createStatusTable(self):
        """시스템 상태 정보 테이블을 생성합니다."""
        conn = self.getConnection()
        cur = conn.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS SystemStatus (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Timestamp TEXT NOT NULL,
            CpuUsage REAL NOT NULL,
            MemoryFree INTEGER NOT NULL
        );
        """
        cur.execute(sql)
        conn.commit()
        conn.close()

    def insertLog(self, log: SystemLog):
        """로그 데이터를 DB에 삽입합니다."""
        conn = self.getConnection()
        cur = conn.cursor()
        sql = "INSERT INTO SystemLog (Timestamp, Level, Message) VALUES (?, ?, ?);"
        cur.execute(sql, (log.timestamp, log.level, log.message))
        conn.commit()
        conn.close()
        
    def insertStatus(self, status: SystemStatus):
        """상태 데이터를 DB에 삽입합니다."""
        conn = self.getConnection()
        cur = conn.cursor()
        sql = "INSERT INTO SystemStatus (Timestamp, CpuUsage, MemoryFree) VALUES (?, ?, ?);"
        cur.execute(sql, (status.timestamp, status.cpu_usage, status.memory_free))
        conn.commit()
        conn.close()
        
    def findAllLogs(self):
        """모든 로그를 조회합니다."""
        conn = self.getConnection()
        cur = conn.cursor()
        sql = "SELECT ID, Level, Message, Timestamp FROM SystemLog ORDER BY ID DESC;"
        cur.execute(sql)
        
        logs = []
        for row in cur:
            logs.append(SystemLog(id=row[0], level=row[1], message=row[2], timestamp=row[3]))
            
        conn.close()
        return logs
    
    def collect_system_status() -> SystemStatus:
        """CPU 사용률과 사용 가능 메모리 정보를 수집하여 SystemStatus 객체로 반환합니다."""
        # psutil 라이브러리 사용을 가정
        
        # 1. CPU 사용률 (1초 간격으로 측정)
        cpu = psutil.cpu_percent(interval=1) 
        print(cpu)
        
        # 2. 메모리 정보
        memory = psutil.virtual_memory()
        print(memory)

        # 사용 가능 메모리를 메가바이트(MB) 단위로 변환
        memory_free_mb = int(memory.available / (1024 * 1024))
        print(memory_free_mb)
        
        return SystemStatus(cpu_usage=cpu, memory_free=memory_free_mb)