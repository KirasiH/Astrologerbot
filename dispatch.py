from prognosclass import prognos
from database import botdb


async def mailing(bot):

    prognos.create_prognos()

    clients = botdb.get_client_chat_id()

    for client in clients:
        await bot.send_message(client[0], f"Прогноз на сегодня:\n {prognos.get_prognos(client[1])}")
