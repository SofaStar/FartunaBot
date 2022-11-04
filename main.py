import os.path
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token="5433136845:AAH6KqJ9kiDeDoNzDSLdHpnAyqHUINqKDaQ")
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):

    kb = [
        [types.KeyboardButton(text="Ветровики", )],
        [types.KeyboardButton(text="Отбойники")],
        [types.KeyboardButton(text="Реснички")],
        [types.KeyboardButton(text="Накладки на бампер / спойлер на крышку багажника")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Что ищем?", reply_markup=keyboard)

@dp.message_handler(text="Ветровики")
async def getText(message: types.Message):
    await message.answer('Вы выбрали: Ветровики')

@dp.message_handler(text="Отбойники")
async def getText(message: types.Message):
    await message.answer('Вы выбрали: Отбойники')

@dp.message_handler(text="Реснички")
async def getText(message: types.Message):
    await message.answer('Вы выбрали: Реснички')

@dp.message_handler(text="Накладки на бампер / спойлер на крышку багажника")
async def getText(message: types.Message):
    await message.answer('Вы выбрали Накладки на бампер / спойлер на крышку багажника')






if __name__ == '__main__':
    executor.start_polling(dp)


