

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from services import filter_table, send_goods, set_table_type, searching_keyboard, validate_goods_text, \
    process_goods_changing, change_goods_count


bot = Bot(token="5402135297:AAHiKc64WL9GaQKT4JJh_zO17tfJKZ7nojg")
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await searching_keyboard(message)


@dp.message_handler(text="ВЕРНУТЬСЯ К ПОИСКУ ТОВАРОВ")
async def start(message: types.Message):
    await searching_keyboard(message)


@dp.message_handler(text="УМЕНЬШИТЬ КОЛИЧЕСТВО: -1")
async def change_goods(message: types.Message):
    await change_goods_count(message, -1)


@dp.message_handler(text="ПОПОЛНИТЬ: +1")
async def change_goods(message: types.Message):
    await change_goods_count(message, 1)


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
    is_goods_text, table_name, goods_id = validate_goods_text(message.text)

    if is_goods_text:
        await process_goods_changing(message, table_name, goods_id)
    else:
        good_name = message.text
        await send_goods(message, good_name)

if __name__ == '__main__':
    executor.start_polling(dp)


