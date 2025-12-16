from repositories.person_repository import PersonRepository
from entities.person import Person

dbPath = "/mnt/c/Users/User/databases/address_book.db"

def main():
    repo = PersonRepository(dbPath)
    repo.createTable()

    while True:
        print("\n=== Person Address Book ===")
        print("1. 사람 추가")
        print("2. 전체 조회")
        print("3. 사람 수정")
        print("4. 사람 삭제")
        print("0. 종료")

        choice = input("선택: ").strip()

        match choice:
            case "1":
                name = input("이름: ").strip()
                pnumber = input("전화번호: ").strip()

                person = Person(name=name, pnumber=pnumber)
                repo.insert(person)

                print("저장 완료:", person)

            case "2":
                persons = repo.findAll()
                print("\n--- 전체 목록 ---")
                for p in persons:
                    print(p)
                    
            case "3":
                try:
                    target_id = int(input("수정할 사람의 ID: "))
                except ValueError:
                    print("ID는 숫자로 입력해주세요")
                    continue

                person_to_update = repo.findOne(target_id)
                print(f"person is {person_to_update}")

                if (person_to_update is None):
                    print(f"ID {target_id}에 해당하는 정보가 없습니다.")
                    continue

                print(f"현재 정보: {person_to_update}")
                new_name = input(f"새 이름 (현재: {person_to_update.name}): ").strip()
                new_pnumber = input(f"새 전화번호 (현재: {person_to_update.pnumber}): ").strip()

                new_person = Person(name=new_name, pnumber=new_pnumber)

                persons = repo.update(id=target_id, new_person=new_person)
                
                print("수정이 완료되었습니다.")
                    
            case "4":
                try:
                    target_id = int(input("수정할 사람의 ID: "))
                except ValueError:
                    print("ID는 숫자로 입력해주세요")
                    continue

                person_to_update = repo.findOne(target_id)
                print(f"person is {person}")

                if (person_to_update is None):
                    print(f"ID {target_id}에 해당하는 정보가 없습니다.")
                    continue
                
                repo.delete(id=target_id)
                
                print("삭제가 완료되었습니다")

            case "0":
                print("프로그램 종료")
                break

            case _:
                print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
