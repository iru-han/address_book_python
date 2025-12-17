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
                print("\n" + "="*50)
                print(" 호스트 서버 자원 사용량 분석 (PSUTIL)")
                print("="*50)
                
                # 1시간 동안의 데이터 분석 호출
                summary = analysis_repo.summarize_system_load(hours=1)
                
                if not summary["data_found"]:
                    print("분석할 시스템 로그 데이터가 충분하지 않습니다.")
                    print("배치 작업(collect_status_batch.py)이 실행 중인지 확인하세요.")
                else:
                    print(f"분석 기간 : 최근 1시간")
                    print("-" * 30)
                    print(f"[CPU 분석]")
                    print(f"- 최대 사용률 : {summary['max_cpu']}%")
                    print(f"- 평균 사용률 : {summary['avg_cpu']}%")
                    print(f"- 임계치(80%) 초과 : {summary['cpu_alerts']}회")
                    
                    print(f"\n[메모리 분석]")
                    print(f"- 최소 여유 공간 : {summary['min_mem']} MB")
                    print(f"- 여유 부족(512MB 미만) : {summary['mem_alerts']}회")
                    
                    print("-" * 30)
                    print("[시스템 상태 진단]")
                    if summary['cpu_alerts'] > 0 or summary['mem_alerts'] > 0:
                        print("🚨 경고: 시스템 자원 부족 징후가 감지되었습니다. 프로세스를 점검하세요.")
                    elif summary['max_cpu'] < 50:
                        print("✅ 정상: 서버 자원이 매우 여유로운 상태입니다.")
                    else:
                        print("ℹ️ 알림: 시스템이 안정적으로 운영되고 있습니다.")

                print("="*50)
            case "7":
                print("\n" + "="*50)
                print(" 가상 센서 모니터링 및 실시간 데이터")
                print("="*50)
                
                # 1. 최신 데이터 조회
                latest_data = sensor_repo.findLatest(limit=5)
                
                print("[실시간 센서 피드 (최근 5건)]")
                if not latest_data:
                    print("수집된 데이터가 없습니다. 시뮬레이터를 확인하세요.")
                else:
                    for s in latest_data:
                        # s는 SensorData 객체이므로 __str__ 활용
                        print(f"[{s.timestamp[11:]}] {s}")

                # 2. 통계 데이터 분석 조회
                stats = analysis_repo.summarize_sensor_stats()
                if stats and stats['avg_temp']:
                    print("-" * 30)
                    print("[최근 24시간 통계 요약]")
                    print(f"- 평균 온도 : {stats['avg_temp']:.2f}°C (최대: {stats['max_temp']:.1f}°C)")
                    print(f"- 평균 습도 : {stats['avg_hum']:.2f}%")
                    print(f"- 고온 경보 : {stats['heat_alerts']}회 발생")
                    
                    # 간단한 상태 진단
                    if stats['heat_alerts'] > 0:
                        print("\n🚨 [경고] 설비 주변 온도가 임계치(28도)를 자주 초과하고 있습니다.")
                    else:
                        print("\n✅ [정상] 모든 센서 수치가 안정 범위 내에 있습니다.")
                
                print("="*50)
            case "8":
                print("\n" + "="*50)
                print(" 시스템 이상 징후 요약 (syslog 분석)")
                print("="*50)
                
                # 데이터 가져오기 (최근 6시간 분석)
                analysis = analysis_repo.analyze_syslog_events(hours=6)
                
                print(f"분석 대상  : /var/log/syslog")
                print(f"기간       : 최근 {analysis['hours']}시간")
                print("-" * 30)
                
                print("[중요 이벤트 요약]")
                print(f"- 시스템 시간 도약(Time Jump) : {analysis['time_jumps']}건")
                print(f"- Windows Agent 연결 실패     : {analysis['conn_fails']}건")
                print(f"- 서비스 시작/재시작 이벤트   : {analysis['restarts']}건")
                print("-" * 30)

                print("[최근 상세 타임라인 (경고/에러)]")
                if not analysis['details']:
                    print("특이 사항 없음")
                else:
                    for log in analysis['details']:
                        # 타임스탬프에서 시간만 추출 (HH:MM)
                        log_time = log['timestamp'][11:16]
                        print(f"{log_time} [{log['level']:5}] {log['component']:15} - {log['message'][:40]}...")

                print("="*50)
                
                # 간단한 추정 원인 제공 (로그 분석 결과 기반)
                if analysis['time_jumps'] > 0:
                    print("\n[추정 원인 분석]")
                    print("- 현상: 시스템 시간 역전 현상 반복 발생")
                    print("- 원인: WSL과 Windows 호스트 간의 시간 동기화 불안정 가능성 높음")

            case "0":
                print("프로그램 종료")
                break

            case _:
                print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
