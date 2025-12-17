import os
import sys
import datetime

# 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.system_log import SystemLog
from repositories.system_repository import SystemRepository
from base.base_path import DB_PATH
# psutil 및 기타 필요한 모듈 import



def collect_and_record():
    """상태를 한 번 수집하고 DB에 기록하는 함수."""
    system_repo = SystemRepository(DB_PATH)
    
    try:
        status = system_repo.collect_system_status()
        system_repo.insertStatus(status)

        log_msg = f"Batch status recorded: CPU={status.cpu_usage}%"
        status_log = SystemLog(level="INFO", message=log_msg)
        system_repo.insertLog(status_log)

        # cron 작업이므로 print는 필요 없지만, 디버깅용으로 남겨둘 수 있습니다.
        # print(f"[CRON 수집] {status.timestamp}: 상태 기록 완료") 
        
    except Exception as e:
        # cron 작업에서는 오류를 로그 파일에 기록하는 것이 좋습니다.
        with open("cron_error.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] Error: {e}\n")

if __name__ == "__main__":
    collect_and_record()