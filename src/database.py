import sqlite3


class Database:
    def __init__(self, db_name=":memory:"):
        self.connection = sqlite3.connect(db_name)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                confirm TEXT NOT NULL,
                result INTEGER NOT NULL,
                error_message TEXT,
                PRIMARY KEY (login, password, confirm)
            )
        """)
        self.connection.commit()

    def add(self, login, password, confirm, result, error_message=""):
        self.connection.execute(
            "INSERT OR REPLACE INTO registrations VALUES (?, ?, ?, ?, ?)",
            (login, password, confirm, int(result), error_message)
        )
        self.connection.commit()

    def get(self, login, password, confirm):
        cursor = self.connection.execute(
            "SELECT result, error_message FROM registrations "
            "WHERE login = ? AND password = ? AND confirm = ?",
            (login, password, confirm)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return bool(row[0]), row[1]

    def delete(self, login, password, confirm):
        self.connection.execute(
            "DELETE FROM registrations "
            "WHERE login = ? AND password = ? AND confirm = ?",
            (login, password, confirm)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()