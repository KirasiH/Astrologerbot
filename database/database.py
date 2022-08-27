import sqlite3

class BotDB:

    def __init__(self):

        self.db = sqlite3.connect("database.db")
        self.cur = self.db.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS client(
            id INTEGER PRIMARY KEY,
            Zs TEXT,
            status int
        )""")

    def add_client(self, id, zs):

        data = self.cur.execute(f"SELECT id FROM client WHERE id = {id}")

        if data.fetchall() == []:
            self.cur.execute("INSERT INTO client (id, Zs, status) VALUES (?, ?, ?)", (id, zs, 1))
            self.db.commit()

        else:
            self.cur.execute(f"UPDATE client SET Zs = '{zs}', status = {1} WHERE id = {id}")
            self.db.commit()

    def set_status(self, id, status):

        self.cur.execute(f"UPDATE client SET status = {status} WHERE id = {id}")
        self.db.commit()

    def get_client_chat_id(self):

        for client in self.cur.execute("SELECT id, Zs FROM client WHERE status = 1").fetchall():
            yield client

botdb = BotDB()
