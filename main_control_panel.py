from repositories.equipment_repository import EquipmentRepository
from entities.equipment import Equipment
from repositories.system_repository import SystemRepository

dbPath = "/mnt/c/Users/User/databases/equipment.db"

def main():
    person_repo = EquipmentRepository(dbPath)
    person_repo.createTable()

    system_repo = SystemRepository(dbPath)
    system_repo.createLogTable()
    system_repo.createStatusTable()

    while True:
        print("\n=== Equipment ===")
        print("1. 장비 추가")
        print("2. 전체 조회")
        print("3. 장비 수정")
        print("4. 장비 삭제")
        print("5. 전체 시스템 로그 조회")
        print("0. 종료")

        choice = input("선택: ").strip()

        match choice:
            case "1":
                name = input("이름: ").strip()
                pnumber = input("전화번호: ").strip()

                person = Equipment(name=name, pnumber=pnumber)
                person_repo.insert(person)

                print("저장 완료:", person)

            case "2":
                persons = person_repo.findAll()
                print("\n--- 전체 목록 ---")
                for p in persons:
                    print(p)
                    
            case "3":
                try:
                    target_id = int(input("수정할 장비의 ID: "))
                except ValueError:
                    print("ID는 숫자로 입력해주세요")
                    continue

                person_to_update = person_repo.findOne(target_id)
                print(f"person is {person_to_update}")

                if (person_to_update is None):
                    print(f"ID {target_id}에 해당하는 정보가 없습니다.")
                    continue

                print(f"현재 정보: {person_to_update}")
                new_name = input(f"새 이름 (현재: {person_to_update.name}): ").strip()
                new_pnumber = input(f"새 전화번호 (현재: {person_to_update.pnumber}): ").strip()

                new_person = Equipment(name=new_name, pnumber=new_pnumber)

                persons = person_repo.update(id=target_id, new_person=new_person)
                
                print("수정이 완료되었습니다.")
                    
            case "4":
                try:
                    target_id = int(input("수정할 장비의 ID: "))
                except ValueError:
                    print("ID는 숫자로 입력해주세요")
                    continue

                person_to_update = person_repo.findOne(target_id)
                print(f"person is {person_to_update}")

                if (person_to_update is None):
                    print(f"ID {target_id}에 해당하는 정보가 없습니다.")
                    continue
                
                person_repo.delete(id=target_id)
                
                print("삭제가 완료되었습니다")

            case "5":
                logs = system_repo.findAllLogs()
                print("\n-- 최신 시스템 로그 목록 --")
                for l in logs[:10]:
                    print(l)

            case "0":
                print("프로그램 종료")
                break

            case _:
                print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
