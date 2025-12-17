import sqlite3
from entities.equipment import Equipment

class EquipmentRepository:
    def __init__(self, DB_PATH: str):
        self.DB_PATH = DB_PATH

    def getConnection(self):
        return sqlite3.connect(self.DB_PATH)

    def createTable(self):
        conn = self.getConnection()
        cur = conn.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS Equipment (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Pnumber TEXT NOT NULL
        );
        """

        cur.execute(sql)
        conn.commit()
        conn.close()

    def insert(self, person: Equipment):
        conn = self.getConnection()
        cur = conn.cursor()

        sql = """
        INSERT INTO Equipment (Name, Pnumber)
        VALUES (?, ?);
        """

        cur.execute(sql, (person.name, person.pnumber))
        conn.commit()

        person.id = cur.lastrowid
        conn.close()

    def findOne(self, id: int) -> Equipment | None:
        conn = self.getConnection()
        cur = conn.cursor()

        sql = "SELECT ID, Name, Pnumber FROM Equipment WHERE id=?;"
        cur.execute(sql, (id,))

        print(f"cur : {cur}")

        row = cur.fetchone()
        conn.close()

        print(f"findOne Equipment : {row}")

        if row:
            return Equipment(row[0], row[1], row[2])
        else:
            return None

    def findAll(self) -> list[Equipment]:
        conn = self.getConnection()
        cur = conn.cursor()

        sql = "SELECT ID, Name, Pnumber FROM Equipment ORDER BY ID;"
        cur.execute(sql)

        persons = []
        for row in cur:  # (ID, Name, Pnumber)
            persons.append(Equipment(row[0], row[1], row[2]))

        conn.close()
        return persons
    
    def update(self, id: int, new_person: Equipment):
        conn = self.getConnection()
        cur = conn.cursor()

        sql = """
        UPDATE Equipment SET Name=?, Pnumber=?
        WHERE ID=?;
        """

        cur.execute(sql, (new_person.name, new_person.pnumber, id))
        conn.commit()

        new_person.id = cur.lastrowid
        print(f"cur.lastrowid : {cur.lastrowid}")
        conn.close()
    
    def delete(self, id: int):
        conn = self.getConnection()
        cur = conn.cursor()

        sql = """
        DELETE FROM Equipment
        WHERE ID=?;
        """

        cur.execute(sql, (id,))
        conn.commit()

        conn.close()
