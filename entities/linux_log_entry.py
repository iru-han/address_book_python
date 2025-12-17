import datetime

class LinuxLogEntry:
    def __init__(self, id=None, timestamp=None, component=None, level=None, message=None, source_file=None):
        self.id = id
        self.timestamp = timestamp if timestamp else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.component = component  # 예: kernel, systemd, sshd, NetworkManager 등
        self.level = level          # 예: INFO, WARN, ERROR, DEBUG
        self.message = message      # 실제 로그 메시지
        self.source_file = source_file # 예: syslog, auth.log
        
    def __str__(self):
        return (f"[ID:{self.id}] [{self.timestamp}] [{self.level}] "
                f"({self.component}) - {self.message[:60]}...")