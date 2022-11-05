

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from services import filter_table, send_goods, set_table_type


bot = Bot(token="5433136845:AAH6KqJ9kiDeDoNzDSLdHpnAyqHUINqKDaQ")
dp = Dispatcher(bot)



@dp.message_handler(commands="start")
async def start(message: types.Message):

    kb = [
        [types.KeyboardButton(text="ВЕТРОВИКИ", )],
        [types.KeyboardButton(text="ОТБОЙНИКИ")],
        [types.KeyboardButton(text="РЕСНИЧКИ")],
        [types.KeyboardButton(text="НАКЛАДКИ НА БАМПЕР")],
        [types.KeyboardButton(text="СПОЙЛЕРЫ НА КРЫШКУ БАГАЖНИКА")],
        [types.KeyboardButton(text="КОЗЫРЬКИ ЗАДНЕГО СТЕКЛА")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Что ищем?", reply_markup=keyboard)

@dp.message_handler(text="ВЕТРОВИКИ")
async def search_goods(message: types.Message):
    await message.answer('Введите название ВЕТРОВИКА')

    set_table_type('ветровики', message.chat.id)


@dp.message_handler(text="ОТБОЙНИКИ")
async def search_goods(message: types.Message):
    await message.answer('Введите название ОТБОЙНИКА')
    set_table_type('отбойники', message.chat.id)


@dp.message_handler(text="РЕСНИЧКИ")
async def search_goods(message: types.Message):
    await message.answer('Введите название РЕСНИЧКИ')
    set_table_type('реснички', message.chat.id)


@dp.message_handler(text="НАКЛАДКИ НА БАМПЕР")
async def search_goods(message: types.Message):
    await message.answer('Введите название НАКЛАДКИ НА БАМПЕР')
    set_table_type('накладки_бампер', message.chat.id)


@dp.message_handler(text="СПОЙЛЕРЫ НА КРЫШКУ БАГАЖНИКА")
async def search_goods(message: types.Message):
    await message.answer('Введите название СПОЙЛЕРА НА КРЫШКУ БАГАЖНИКА')
    set_table_type('спойлеры_багажник', message.chat.id)


@dp.message_handler(text="КОЗЫРЬКИ ЗАДНЕГО СТЕКЛА")
async def search_goods(message: types.Message):
    await message.answer('Введите название КОЗЫРЬКА ЗАДНЕГО СТЕКЛА')
    set_table_type('козырьки_стекло', message.chat.id)


@dp.message_handler(content_types=['text'])
async def search_goods(message: types.Message):
    good_name = message.text

    await send_goods(message, good_name)

if __name__ == '__main__':
    executor.start_polling(dp)


