import asyncio
import sqlite3

import aiomysql


class BotDB:

    def __init__(self):

        self.db = sqlite3.connect("database.db")
        self.cur = self.db.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS client(
            id INTEGER PRIMARY KEY,
            Zs TEXT,
            status int
        )""")

    def add_client(self, id: int, zs: str):

        data = self.cur.execute(f"SELECT id FROM client WHERE id = {id}")

        if data.fetchall() == []:
            self.cur.execute("INSERT INTO client (id, Zs, status) VALUES (?, ?, ?)", (id, zs, 1))
            self.db.commit()

        else:
            self.cur.execute(f"UPDATE client SET Zs = '{zs}', status = {1} WHERE id = {id}")
            self.db.commit()

    def set_status(self, id: int, status: int):

        self.cur.execute(f"UPDATE client SET status = {status} WHERE id = {id}")
        self.db.commit()

    def get_client_chat_id(self):

        for client in self.cur.execute("SELECT id, Zs FROM client WHERE status = 1").fetchall():
            yield client

class BotDB:

    async def start(self):

        loop = asyncio.get_event_loop()

        self.conn = await aiomysql.connect(
            port=3306,
            host="127.0.0.1",
            user="root",
            password="123456789-zalik",
            db="astrolog",
            cursorclass=aiomysql.cursors.DictCursor,
            loop=loop
        )

        async with self.conn.cursor() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS client(
                id INT PRIMARY KEY AUTO_INCREMENT,
                Zs TEXT,
                status INT
            )""")

            await self.conn.commit()

    async def add_client(self, id: int, zs: str):

        async with self.conn.cursor() as cur:
            await cur.execute(f"SELECT id FROM client WHERE id = {id}")

            if await cur.fetchall() == []:
                await cur.execute("INSERT INTO client (id, Zs, status) VALUES (%s, %s, %s)", (id, zs, 1))

            else:
                await cur.execute(f"UPDATE client SET Zs = '{zs}', status = {1} WHERE id = {id}")

            await self.conn.commit()

    async def set_status(self, id: int, status: int):

        async with self.conn.cursor() as cur:
            await cur.execute(f"UPDATE client SET status = {status} WHERE id = {id}")
            await self.conn.commit()

    async def get_client_chat_id(self):

        async with self.conn.cursor() as cur:
            await cur.execute("SELECT id, Zs FROM client WHERE status = 1")
            for client in await cur.fetchall():
                yield client

botdb = BotDB()