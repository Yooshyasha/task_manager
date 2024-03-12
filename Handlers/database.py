import sqlite3

from Handlers.until import User
from loader import Singleton, Program


class Table:
    def __init__(self, name):
        self.name: str = name
        self._values: tuple = ()

    def set_values(self, values: tuple):
        self._values = values

    @property
    def get_values(self):
        return self._values

    def __str__(self):
        return f"{self.name} {self.get_values}"


class TableControl(Table):
    def set_values_plied(self, values: tuple):
        self.set_values(values)
        return self


class Database:
    def __init__(self):
        self.con = sqlite3.connect(Program().database_path)
        self.cur = self.con.cursor()
        self.tables: list = []

    def reconnect(self):
        pass

    def add_table(self, table: Table):
        self.tables.append(table)

    @property
    def get_tables(self):
        return self.tables


class DatabaseControl(Database):
    def start(self):
        table_tasks = TableControl("tasks").set_values_plied(("id", "owner", "name", "status", "child_tasks"))
        table_users = TableControl("users").set_values_plied(("id", "role"))
        # table_task_config = TableControl("task_config").set_values_plied(("owner", "role"))
        self.add_table_plied(table_tasks).add_table_plied(table_users)
        for table in self.tables:
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table}")
        self.con.commit()

    def add_table_plied(self, table: Table):
        self.add_table(table)
        return self

    def get_tasks(self, user: User):
        result = self.cur.execute("SELECT * FROM tasks WHERE owner = ?", (user.id,)).fetchall()
        return result

    def get_user(self, user: int | str):
        result = self.cur.execute("SELECT * FROM users WHERE id = ?", (user,)).fetchone()
        return result

    def write_user(self, user: int | str):
        _user = self.get_user(user)
        if _user is None or len(_user) == 0:
            self.cur.execute("INSERT INTO users VALUES (?, ?)", (user, "USER"))
            self.con.commit()
