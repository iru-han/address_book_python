import sqlite3
import datetime

class AnalysisRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    # PSUTIL 데이터 분석 (메뉴 6번)
    def summarize_system_load(self, hours=1):
        """SystemStatus 테이블을 기반으로 최근 X시간 부하 요약"""
        # ... (구현 예정: MAX/AVG CPU, 메모리 부족 횟수)
        pass
        
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
    def summarize_sensor_stats(self):
        # ... (구현 예정: 평균 온도, LED ON 시간 비율 등)
        pass