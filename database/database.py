import aiomysql
import asyncio


class BotDB:

    async def start(self):

        loop = asyncio.get_event_loop()

        self.conn = await aiomysql.connect(
            port=3306,
            host="127.0.0.1",
            user="root",
            db="astrolog",
            password="123456789-zalik",
            cursorclass=aiomysql.cursors.DictCursor,
            loop=loop
        )


        async with self.conn.cursor() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS client(
                id INTEGER PRIMARY KEY,
                Zs TEXT,
                status int
            )""")

            await self.conn.commit()

    async def add_client(self, id, zs):

        async with self.conn.cursor() as cur:
            await cur.execute(f"SELECT id FROM client WHERE id = {id}")

            if await cur.fetchall() == ():
                await cur.execute("INSERT INTO client (id, Zs, status) VALUES (%s, %s, %s)", (str(id), str(zs), int(1)))
                await self.conn.commit()

            else:
                await cur.execute(f"UPDATE client SET Zs = '{zs}', status = {1} WHERE id = {id}")
                await self.conn.commit()

            await cur.close()


    async def set_status(self, id, status):

        async with self.conn.cursor() as cur:
            await cur.execute(f"UPDATE client SET status = {status} WHERE id = {id}")
            await self.conn.commit()
            await cur.close()

    async def get_client_chat_id(self):

        async with self.conn.cursor() as cur:
            await cur.execute("SELECT id, Zs FROM client WHERE status = 1")
            data = await cur.fetchall()
            await cur.close()
            return data


botdb = BotDB()

