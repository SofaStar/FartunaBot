import os.path
import pandas as pd
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
def filter_table(table_name, good_name):
    df = pd.read_excel(f'./tables/{table_name}.ods',  engine='odf')
    print(table_name)
    filtered_goods = []
    for index, row in df.iterrows():

        if good_name in row["НАЗВАНИЕ ТОВАРА"]:
            good = dict(row)
            good['id'] = index

            filtered_goods.append(good)
    return filtered_goods


bot = Bot(token="5433136845:AAH6KqJ9kiDeDoNzDSLdHpnAyqHUINqKDaQ")
dp = Dispatcher(bot)

table_type = {}

@dp.message_handler(commands="start")
async def start(message: types.Message):

    kb = [
        [types.KeyboardButton(text="ВЕТРОВИКИ", )],
        [types.KeyboardButton(text="ОТБОЙНИКИ")],
        [types.KeyboardButton(text="РЕСНИЧКИ")],
        [types.KeyboardButton(text="НАКЛАДКИ НА БАМПЕР")],
        [types.KeyboardButton(text="СПОЙЛЕРЫ НА КРЫЖКУ БАГАЖНИКА")],
        [types.KeyboardButton(text="КОЗЫРЬКИ ЗАДНЕГО СТЕКЛА")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Что ищем?", reply_markup=keyboard)

@dp.message_handler(text="ВЕТРОВИКИ")
async def search_goods(message: types.Message):
    global table_type
    await message.answer('Введите название ветровика')

    print(message)

    table_type[str(message.chat.id)] = 'ветровики'


@dp.message_handler(text="ОТБОЙНИКИ")
async def search_goods(message: types.Message):
    global table_type
    await message.answer('Вы выбрали: Отбойники')
    table_type[str(message.chat.id)] = 'отбойники'


@dp.message_handler(text="РЕСНИЧКИ")
async def search_goods(message: types.Message):
    await message.answer('Вы выбрали: Реснички')

@dp.message_handler(text="НАКЛАДКИ НА БАМПЕР")
async def search_goods(message: types.Message):
    await message.answer('Вы выбрали Накладки на бампера')

@dp.message_handler(text="СПОЙЛЕРЫ НА КРЫЖКУ БАГАЖНИКА")
async def search_goods(message: types.Message):
    await message.answer('Вы выбрали спойлер на крышку багажника')

@dp.message_handler(text="КОЗЫРЬКИ ЗАДНЕГО СТЕКЛА")
async def search_goods(message: types.Message):
    await message.answer('Вы выбрали КОЗЫРЬКИ ЗАДНЕГО СТЕКЛА')


@dp.message_handler(content_types=['text'])
async def search_goods(message: types.Message):
    global table_type
    good_name = message.text
    print(table_type)
    table = table_type[str(message.chat.id)]
    print(table)
    if not bool(table_type):
        await message.reply('Вы не выбрали тип искомого товара')
        return
    answers = filter_table(table, good_name)
    for answer in answers:
        await message.answer(answer)

if __name__ == '__main__':
    executor.start_polling(dp)


