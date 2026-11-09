import sqlite3


class DatabaseRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)

    def get_by_id(self, comment_id: int):
        cursor = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE id = ?", (comment_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return {"id": row["id"], "name": row["name"], "message": row["message"]}

    def get_by_name(self, username: str):
        cursor = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE name = ?", (username,)
        )
        rows = cursor.fetchall()
        return [{"id": r["id"], "name": r["name"], "message": r["message"]} for r in rows]

    def get_all(self):
        cursor = self.conn.execute("SELECT id, name, message FROM comments")
        rows = cursor.fetchall()
        return [{"id": r["id"], "name": r["name"], "message": r["message"]} for r in rows]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        if not isinstance(comment_id, int) or not isinstance(username, str) or not isinstance(message, str):
            raise TypeError("Неверные типы: comment_id должен быть int, username и message — str")
        if len(username) > 256:
            raise ValueError("Длина имени не должна превышать 256 символов")
        if len(message) > 8096:
            raise ValueError("Длина сообщения не должна превышать 8096 символов")

        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                    (comment_id, username, message),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, comment_id: int, new_message: str) -> bool:
        if not isinstance(new_message, str):
            raise TypeError("new_message должен быть строкой")
        if len(new_message) > 8096:
            raise ValueError("Длина сообщения не должна превышать 8096 символов")

        with self.conn:
            cursor = self.conn.execute(
                "UPDATE comments SET message = ? WHERE id = ?", (new_message, comment_id)
            )
        return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть int")
        with self.conn:
            cursor = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        return cursor.rowcount > 0