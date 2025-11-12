import sqlite3
class Database:
    def __enter__(self):
        print("Opening database")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print("Closing database")

    def create(self, db_path, sql):
        print(f"Creating database at {db_path}")
        self.connection = sqlite3.connect(db_path)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
