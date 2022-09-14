from prognosclass import prognos
from database import botdb


async def mailing(bot):

    prognos.create_prognos()

    async for row in botdb.get_client_chat_id():
        await bot.send_message(row['id'], f"Прогноз на сегодня:\n {prognos.get_prognos(row['Zs'])}")