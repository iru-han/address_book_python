import os
import random
import sys
import datetime

# 프로젝트 루트 디렉터리를 sys.path에 추가하여 내부 모듈 임포트 가능하게 함
# (WSL Cron 환경에서 독립 실행 시 필수)
# 현재 스크립트 위치: /home/robot/work/sql1/main_control_panel/batch/
# 프로젝트 루트 위치: /home/robot/work/sql1/main_control_panel/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.sensor_data import SensorData
from repositories.sensor_repository import SensorRepository

from base.base_path import DB_PATH

def generate_and_record_sensor_data():
    """
    랜덤한 센서 데이터를 생성하여 DB에 기록합니다.
    """
    try:
        # 1. 가상 데이터 생성
        temperature = round(random.uniform(20.0, 30.0), 2)  # 20.0 ~ 30.0 °C
        humidity = round(random.uniform(40.0, 70.0), 2)     # 40.0 ~ 70.0 %
        light_level = round(random.uniform(100, 1000), 2)   # 100 ~ 1000 Lux
        
        # LED 상태는 1/3 확률로 ON
        led_status = 1 if random.randint(1, 3) == 1 else 0

        # 2. SensorData 엔티티 생성
        sensor_data = SensorData(
            temperature=temperature,
            humidity=humidity,
            light_level=light_level,
            led_status=led_status
        )
        
        # 3. Repository를 통해 DB에 저장
        sensor_repo = SensorRepository(DB_PATH)
        # 테이블이 없을 경우 대비하여 생성 메서드 호출 (안전 장치)
        sensor_repo.createSensorTable() 
        sensor_repo.insert(sensor_data)

        # Cron 로그 파일에 기록될 메시지 (성공 확인용)
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sensor Data Recorded: Temp={temperature}, LED={sensor_data.led_status}")
        
    except Exception as e:
        # Cron 로그 파일에 에러를 기록
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR recording sensor data: {e}", file=sys.stderr)

if __name__ == "__main__":
    generate_and_record_sensor_data()