import os
import sys
import re
import datetime
from datetime import datetime as dt

# 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.linux_log_entry import LinuxLogEntry
from repositories.linux_log_repository import LinuxLogRepository

DB_PATH = "/mnt/c/Users/User/databases/equipment.db"
LINUX_LOG_FILE = "/var/log/syslog"

# ISO 8601 타임스탬프와 색상 코드를 포함한 새로운 정규표현식
# 형식: 2025-12-16T11:23:42.775213+09:00 Tiger2 wsl-pro-service[197]: 메시지
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+[\+\-]\d{2}:\d{2})\s+"
    r"(?P<host>[\w\.\-]+)\s+(?P<component>[\w\-\/\[\]\.]+):\s+(?P<message>.*)$"
)

# ANSI 색상 코드 제거용 정규표현식 (예: #033[33m -> 제거)
ANSI_ESCAPE = re.compile(r'(\x1b|#033)\[[0-9;]*m')

def clean_message(msg):
    """메시지에서 색상 코드를 제거하고 레벨을 추출합니다."""
    clean_msg = ANSI_ESCAPE.sub('', msg)
    level = "INFO" # 기본값
    
    if "WARNING" in clean_msg: level = "WARN"
    elif "ERROR" in clean_msg or "Failed" in clean_msg: level = "ERROR"
    elif "DEBUG" in clean_msg: level = "DEBUG"
    elif "INFO" in clean_msg: level = "INFO"
    
    # 레벨 키워드가 메시지 시작 부분에 있으면 메시지 본문에서 제거 (선택 사항)
    clean_msg = re.sub(r'^(WARNING|INFO|DEBUG|ERROR)\s+', '', clean_msg)
    return level, clean_msg

def parse_and_record_logs():
    try:
        if not os.path.exists(LINUX_LOG_FILE):
             return

        print("LINUX_LOG_FILE is ", LINUX_LOG_FILE)
        with open(LINUX_LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        log_repo = LinuxLogRepository(DB_PATH)
        print("log_repo is ", log_repo)
        log_repo.createLogTable()
        
        recorded_count = 0
        for line in lines[-3:]: # 분석을 위해 최근 20줄로 확대
            print("line is ", line)
            match = LOG_PATTERN.match(line.strip())
            print("match is ", match)
            if match:
                data = match.groupdict()
                print("data is ", data)
                
                # ISO 타임스탬프 파싱 (2025-12-16T11:23:42... -> YYYY-MM-DD HH:MM:SS)
                try:
                    # 파이썬 3.7+ 에서 ISO 형식 지원
                    iso_dt = dt.fromisoformat(data['timestamp'])
                    formatted_ts = iso_dt.strftime("%Y-%m-%d %H:%M:%S")
                    print("iso_dt is ", iso_dt)
                    print("formatted_ts is ", formatted_ts)
                except:
                    formatted_ts = data['timestamp'][:19].replace('T', ' ')
                    print("except formatted_ts is ", formatted_ts)

                level, message = clean_message(data['message'])
                print("level, message is ", level, message)
                
                log_entry = LinuxLogEntry(
                    timestamp=formatted_ts,
                    component=data['component'].split('[')[0].strip(),
                    level=level,
                    message=message,
                    source_file="syslog"
                )
                print("log_entry is ", log_entry)
                log_repo.insert(log_entry)
                print("log_repo is ", log_repo)
                recorded_count += 1
        
        print(f"[{dt.now()}] Recorded {recorded_count} logs.")

    except Exception as e:
        print(f"[{dt.now()}] Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    parse_and_record_logs()