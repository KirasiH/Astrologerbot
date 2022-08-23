import sqlite3

class BotDB():

    def __init__(self):

        self.db = sqlite3.connect("database.db")
        self.cur = self.db.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS client(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            client_id TEXT,
            Zs TEXT
        )""")


    def add_client(self, chat_id, zs):

        data = self.cur.execute(f"SELECT client_id FROM client WHERE client_id = {chat_id}")

        if data.fetchall() == []:
            self.cur.execute("INSERT INTO client (client_id, Zs) VALUES (?, ?)", (chat_id, zs))
            self.db.commit()



    def get_client_chat_id(self):

        data = self.cur.execute("SELECT client_id, Zs FROM client").fetchall()

        return data

botdb = BotDB()
