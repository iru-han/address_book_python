# collect_status_batch.py 파일 (SystemRepository와 같은 폴더에 있다고 가정)

from repositories.system_repository import SystemRepository
from entities.system_log import SystemLog
# psutil 및 기타 필요한 모듈 import

import datetime

dbPath = "/mnt/c/Users/User/databases/address_book.db"

def collect_and_record():
    """상태를 한 번 수집하고 DB에 기록하는 함수."""
    system_repo = SystemRepository(dbPath)
    
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