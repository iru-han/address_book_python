import sqlite3
import datetime

class AnalysisRepository:
    def __init__(self, db_path):
        self.db_path = db_path

# repositories/analysis_repository.py 내부

    def summarize_system_load(self, hours=1):
        """SystemStatus 테이블을 기반으로 최근 X시간 부하 요약 (메뉴 6번)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 분석 시작 시간 계산
        start_time = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")

        # 1. CPU 및 메모리 통계 계산
        # memory_free는 MB 단위라고 가정 (psutil 수집 시 설정에 따름)
        cursor.execute("""
            SELECT 
                MAX(cpu_usage) as max_cpu,
                AVG(cpu_usage) as avg_cpu,
                MIN(memory_free) as min_mem,
                COUNT(CASE WHEN cpu_usage > 80 THEN 1 END) as cpu_high_alerts,
                COUNT(CASE WHEN memory_free < 512 THEN 1 END) as mem_low_alerts
            FROM system_status 
            WHERE timestamp > ?
        """, (start_time,))
        
        row = cursor.fetchone()
        
        # 데이터가 없을 경우를 위한 기본값 처리
        if row and row['max_cpu'] is not None:
            summary = {
                "max_cpu": round(row['max_cpu'], 2),
                "avg_cpu": round(row['avg_cpu'], 2),
                "min_mem": round(row['min_mem'], 2),
                "cpu_alerts": row['cpu_high_alerts'],
                "mem_alerts": row['mem_low_alerts'],
                "data_found": True
            }
        else:
            summary = {"data_found": False}

        conn.close()
        return summary
        
    # Linux Log 분석 (메뉴 8번)
    def analyze_syslog_events(self, hours=6):
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 분석 대상 기간 설정
            now = datetime.datetime.now()
            start_time = (now - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
            
            # 1. 중요 이벤트 카운트 (보내주신 로그 특징 반영)
            # 시간 역전 현상 (Time Jump)
            cursor.execute("SELECT COUNT(*) FROM linux_log WHERE message LIKE '%Time jumped backwards%' AND timestamp > ?", (start_time,))
            time_jumps = cursor.fetchone()[0]
            
            # Windows Agent 연결 실패
            cursor.execute("SELECT COUNT(*) FROM linux_log WHERE message LIKE '%could not connect to Windows Agent%' AND timestamp > ?", (start_time,))
            conn_fails = cursor.fetchone()[0]
            
            # 서비스 재시작 관련 (Started/Restarted 키워드)
            cursor.execute("SELECT COUNT(*) FROM linux_log WHERE (message LIKE '%Started %' OR message LIKE '%restarted%') AND timestamp > ?", (start_time,))
            restarts = cursor.fetchone()[0]

            # 2. 상세 내역 (최근 5건의 중요 경고)
            cursor.execute("""
                SELECT timestamp, level, component, message 
                FROM linux_log 
                WHERE level IN ('WARN', 'ERROR') AND timestamp > ?
                ORDER BY timestamp DESC LIMIT 5
            """, (start_time,))
            details = cursor.fetchall()

            conn.close()
            
            return {
                "hours": hours,
                "time_jumps": time_jumps,
                "conn_fails": conn_fails,
                "restarts": restarts,
                "details": details
            }

    # Sensor Data 분석 (추가 분석 메뉴용)
# repositories/analysis_repository.py 내부

    def summarize_sensor_stats(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 최근 24시간 내 평균 온습도 및 조도 분석
        cursor.execute("""
            SELECT 
                AVG(temperature) as avg_temp,
                MAX(temperature) as max_temp,
                AVG(humidity) as avg_hum,
                COUNT(CASE WHEN temperature > 28 THEN 1 END) as heat_alerts
            FROM sensor_data 
            WHERE timestamp > datetime('now', '-1 day')
        """)
        
        stats = cursor.fetchone()
        conn.close()
        return stats