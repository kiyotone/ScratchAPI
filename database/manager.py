import sqlite3
from typing import List, Any, Optional


class DatabaseManager:
    def __init__(self, db_file: str = "app.db"):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    # ---------- Table Management ----------
    def create_table(self, table_name: str, fields: dict) -> None:
        fields_sql = []
        for field, field_type in fields.items():
            if field == "id":
                fields_sql.append(f"{field} INTEGER PRIMARY KEY AUTOINCREMENT")
                continue

            # map Python types to SQLite types
            if field_type == int:
                sql_type = "INTEGER"
            elif field_type == float:
                sql_type = "REAL"
            else:
                sql_type = "TEXT"

            fields_sql.append(f"{field} {sql_type}")

        fields_clause = ", ".join(fields_sql)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_clause})")
        self.conn.commit()

    # ---------- CRUD ----------
    def insert(self, table_name: str, data: dict) -> int:
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        sql = f"INSERT INTO {table_name} ({keys}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all(self, table_name: str) -> List[dict]:
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_by_id(self, table_name: str, record_id: int) -> Optional[dict]:
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE id=?", (record_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def update(self, table_name: str, record_id: int, data: dict) -> int:
        if not data:
            return 0
        set_clause = ", ".join([f"{k}=?" for k in data.keys()])
        values = tuple(data.values()) + (record_id,)
        sql = f"UPDATE {table_name} SET {set_clause} WHERE id=?"
        self.cursor.execute(sql, values)
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self, table_name: str, record_id: int) -> int:
        self.cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (record_id,))
        self.conn.commit()
        return self.cursor.rowcount

    def execute_raw(self, query: str, params: tuple = ()) -> List[Any]:
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def __del__(self):
        self.conn.close()
