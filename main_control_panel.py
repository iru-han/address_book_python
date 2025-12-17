from repositories.equipment_repository import EquipmentRepository
from entities.equipment import Equipment
from repositories.system_repository import SystemRepository

from entities.linux_log_entry import LinuxLogEntry
from entities.sensor_data import SensorData

from repositories.linux_log_repository import LinuxLogRepository
from repositories.sensor_repository import SensorRepository
from repositories.analysis_repository import AnalysisRepository

from base.base_path import DB_PATH

def main():
    equipment_repo = EquipmentRepository(DB_PATH)
    equipment_repo.createTable()

    system_repo = SystemRepository(DB_PATH)
    system_repo.createLogTable()
    system_repo.createStatusTable()

    # Linux 로그 및 센서 Repository 초기화
    linux_log_repo = LinuxLogRepository(DB_PATH)
    linux_log_repo.createLogTable()

    sensor_repo = SensorRepository(DB_PATH)
    sensor_repo.createSensorTable() # sensor_data 테이블 생성

    # 3. [신규] 분석 전용 Repository 초기화
    analysis_repo = AnalysisRepository(DB_PATH) # 분석은 데이터만 사용하므로 테이블 생성 없음

    while True:
        print("\n=== System Control Panel ===")
        print("1. 장비 추가")
        print("2. 전체 조회")
        print("3. 장비 수정")
        print("4. 장비 삭제")
        print("--- 모니터링 및 분석 ---")
        print("5. (PSUTIL) 호스트 상태 로그 조회")
        print("6. 시스템 부하 분석 (CPU/Memory 요약)")
        print("7. 가상 센서 데이터 조회")
        print("8. Linux 이벤트 로그 요약 분석")
        print("0. 종료")

        choice = input("선택: ").strip()

        match choice:
            case "1":
                name = input("이름: ").strip()
                pnumber = input("전화번호: ").strip()

                person = Equipment(name=name, pnumber=pnumber)
                equipment_repo.insert(person)

                print("저장 완료:", person)

            case "2":
                equipments = equipment_repo.findAll()
                print("\n--- 전체 목록 ---")
                for p in equipments:
                    print(p)
                    
            case "3":
                try:
                    target_id = int(input("수정할 장비의 ID: "))
                except ValueError:
                    print("ID는 숫자로 입력해주세요")
                    continue

                person_to_update = equipment_repo.findOne(target_id)
                print(f"person is {person_to_update}")

                if (person_to_update is None):
                    print(f"ID {target_id}에 해당하는 정보가 없습니다.")
                    continue

                print(f"현재 정보: {person_to_update}")
                new_name = input(f"새 이름 (현재: {person_to_update.name}): ").strip()
                new_pnumber = input(f"새 전화번호 (현재: {person_to_update.pnumber}): ").strip()

                new_person = Equipment(name=new_name, pnumber=new_pnumber)

                equipments = equipment_repo.update(id=target_id, new_person=new_person)
                
                print("수정이 완료되었습니다.")
                    
            case "4":
                try:
                    target_id = int(input("수정할 장비의 ID: "))
                except ValueError:
                    print("ID는 숫자로 입력해주세요")
                    continue

                person_to_update = equipment_repo.findOne(target_id)
                print(f"person is {person_to_update}")

                if (person_to_update is None):
                    print(f"ID {target_id}에 해당하는 정보가 없습니다.")
                    continue
                
                equipment_repo.delete(id=target_id)
                
                print("삭제가 완료되었습니다")

            case "5":
                logs = system_repo.findAllLogs()
                print("\n-- 최신 PSUTIL 로그 목록 --")
                for l in logs[:10]:
                    print(l)
            case "6":
                # 신규: PSUTIL 데이터를 분석하는 AnalysisRepository 사용
                print("\n--- 호스트 서버 부하 분석 (최근 1시간) ---")
                summary = analysis_repo.summarize_system_load(hours=1)
                # 🚨 analysis_repo에 구현 예정인 메서드를 호출하고 결과 출력
                # print(f"최대 CPU: {summary['max_cpu']}%, 평균 메모리 부족 횟수: {summary['mem_warns']}")
                print("분석 기능 구현 예정") 

            case "7":
                # 신규: SensorRepository를 통해 가상 센서 데이터 조회
                print("\n--- 최신 가상 센서 데이터 ---")
                latest_sensors = sensor_repo.findLatest(limit=10)
                # 🚨 sensor_repo에 구현 예정인 메서드를 호출하고 결과 출력
                # for s in latest_sensors:
                #     print(s)
                print("가상 센서 조회 기능 구현 예정")

            case "8":
                # 신규: Linux Log 데이터를 분석하는 AnalysisRepository 사용
                print("\n--- Linux 이벤트 로그 요약 (syslog/auth) ---")
                log_summary = analysis_repo.analyze_syslog_events(hours=6)
                # 🚨 analysis_repo에 구현 예정인 메서드를 호출하고 결과 출력
                # print(f"서비스 재시작: {log_summary['restart_count']}건")
                print("Linux 로그 분석 기능 구현 예정")
                
            case "0":
                print("프로그램 종료")
                break

            case _:
                print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
