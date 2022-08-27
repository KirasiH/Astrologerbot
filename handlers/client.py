from aiogram import types, Router
from prognosclass import prognos
from database import botdb
from aiogram.dispatcher.fsm.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter, KICKED


form_router = Router()


Zs = {"1": "Овен",
      "2": "Телец",
      "3": "Близнецы",
      "4": "Рак",
      "5": "Лев",
      "6": "Дева",
      "7": "Весы",
      "8": "Скорпион",
      "9": "Стрелец",
      "10": "Козерог",
      "11": "Водолей",
      "12": "Рыбы"}


class FSM(StatesGroup):
    Zs = State()


async def prognos_day(message: types.Message, state: FSMContext):

    data = await state.update_data()

    await message.answer(
        f"Прогноз на сегодня:\n{prognos.get_prognos(Zs[data['zs']])}",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()


async def zodiak_sing(message: types.Message, state: FSMContext):

    await state.set_state(FSM.Zs)
    await state.update_data(zs=message.text)

    button = [[types.KeyboardButton(text="Прогноз")]]

    await message.answer(
        f"Хотите знать прогноз для - {Zs[message.text]}?",
        reply_markup=types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    )

    botdb.add_client(id=message.from_user.id, zs=Zs[message.text])


async def command_start(message: types.Message):
    await message.answer("Здравствуйте! Вас приветствует бот Астролог, я буду Вам предсказывать Ваш день, но для начала, какой Ваш Зз?")
    await message.answer("1 - Овен\n2 - Телец\n3 - Близнецы\n4 - Рак\n5 - Лев\n6 - Дева\n7 - Весы\n8 - Скорпион\n9 - Стрелец\n10 - Козерог\n11 - Водолей\n12 - Рыбы\n")


async def status_client_zero(event: types.ChatMemberUpdated):
    print("delete")
    botdb.set_status(event.from_user.id, 0)


async def echo(message):
    pass


def register_client():
    form_router.message.register(command_start, commands=["start"])
    form_router.message.register(zodiak_sing, text=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    form_router.message.register(prognos_day, text="Прогноз", state=FSM.Zs)
    form_router.my_chat_member.register(status_client_zero, ChatMemberUpdatedFilter(member_status_changed=KICKED))
    form_router.message.register(echo)

    return form_router
