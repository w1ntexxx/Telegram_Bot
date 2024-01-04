import sqlite3 as sq


class DataBase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.con = None
        self.cursor = None
        self.connect()

    def __iter__(self):
        for x in self.cursor.fetchall():
            yield x

    def connect(self):
        try:
            self.con = sq.connect(self.db_path)
            self.cursor = self.con.cursor()
            self.con.commit()
        except sq.Error as e:
            print(f"Error connection: {e}")

    def disconnect(self):
        if self.con:
            self.con.close()
            self.con, self.cursor = None
            print(f"Database {self.db_path} disconnect")

    def insert(self, column: tuple, values: tuple):
        try:
            places = ",".join(["?" for _ in values])
            column_str = ", ".join(column)
            request = f"INSERT INTO {self.db_path} ({column_str}) VALUES ({places})"
            self.cursor.execute(request, values)
            self.con.commit()
            print("Inserted successfully")
        except sq.Error as e:
            print(f"Error insert: {e}")

    def get(self, table, columns="*", add_request=None):
        try:
            if columns != "*":
                columns = ", ".join(columns)

            requset = f"SELECT {columns} FROM {table}"

            if add_request:
                requset += " " + add_request

            self.cursor.execute(requset)
            return self
        except sq.Error as e:
            print(f"Error get: {e}")
            return None
