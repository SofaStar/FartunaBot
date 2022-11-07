import pandas as pd
from aiogram import types

table_type = {}
processing_goods = {}


def validate_goods_text(text):
    validation_words = ['название товара: ', 'сектор: ', 'положение в секторе: ', 'количество: ', 'id: ', 'в таблице: ',
                        '\n']
    text_strings = text.strip().split('\n')

    is_goods_text = any([True for word in validation_words if (word in text)])
    try:
        table_name = text_strings[-1].split('в таблице: ')[-1]
        goods_id = int(text_strings[-2].split('id: ')[-1])
    except:
        table_name = ''
        goods_id = 0

    return is_goods_text, table_name, goods_id


async def process_goods_changing(message: types.Message, table_name, goods_id):
    set_processing_goods({'table': table_name, 'id': goods_id}, message.chat.id)

    kb = [
        [types.KeyboardButton(text="УМЕНЬШИТЬ КОЛИЧЕСТВО: -1")],
        [types.KeyboardButton(text="ПОПОЛНИТЬ: +1")],
        [types.KeyboardButton(text="ВЕРНУТЬСЯ К ПОИСКУ ТОВАРОВ")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.answer(f"Что вы хотите сделать с высланным товаром?", reply_markup=keyboard)


async def change_goods_count(message: types.Message, count):
    global processing_goods
    try:
        try:
            product_id = processing_goods[str(message.chat.id)]['id']
            table_name = processing_goods[str(message.chat.id)]['table']
        except:
            await message.answer("Вы не отправили боту сообщение с товаром, количество которого хотите изменить")
            return

        df = prepare_df(pd.read_excel(f'./tables/{table_name}.ods',  engine='odf'))

        try:
            result = int(df.loc[product_id, 'КОЛИЧЕСТВО']) + count
        except:
            await message.answer("Количество в данном товаре указано некорректно - бот не сможет его изменить! "
                                 "Для изменения количества вам необходимо отредактировать таблицу вручную.\n"
                                 "Перезапуск бота: /start")
            return

        if result < 0:
            processing_goods[str(message.chat.id)] = ''
            await message.answer("Этот товар весь РАСПРОДАН, его количество и так 0 шт.")
            await searching_keyboard(message)
        else:
            result_df = pd.read_excel(f'./tables/{table_name}.ods',  engine='odf')
            result_df.loc[product_id, 'КОЛИЧЕСТВО'] = result
            result_df.to_excel(f'./tables/{table_name}.ods', engine='odf', index=False)
            await message.answer(f"Количество товара успешно изменено!\n"
                                 f"<b>{df.loc[product_id, 'НАЗВАНИЕ ТОВАРА'].upper()}</b>:"
                                 f"\nНынешние количество: {result}", parse_mode="HTML")

            processing_goods[str(message.chat.id)] = ''

            await searching_keyboard(message)

    except:
        await message.answer("В процессе изменения количества товара произошла ошибка.\nПерезапуск бота: /start")


async def searching_keyboard(message: types.Message):
    kb = [
        [types.KeyboardButton(text="ВЕТРОВИКИ", )],
        [types.KeyboardButton(text="ОТБОЙНИКИ")],
        [types.KeyboardButton(text="РЕСНИЧКИ")],
        [types.KeyboardButton(text="НАКЛАДКИ НА БАМПЕР")],
        [types.KeyboardButton(text="СПОЙЛЕРЫ НА КРЫШКУ БАГАЖНИКА")],
        [types.KeyboardButton(text="КОЗЫРЬКИ ЗАДНЕГО СТЕКЛА")],

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Поиск: ", reply_markup=keyboard)


def prepare_df(df):
    df['НАЗВАНИЕ ТОВАРА'] = [str(value).lower() for value in df['НАЗВАНИЕ ТОВАРА']]

    for column, data in df.items():
        for index, value in enumerate(data):
            if str(value) == 'nan':
                df.loc[index, column] = 'не указано'
    return df


def compare_filtering_lists(target_name, filtering_name):
    target_name_list = target_name.lower().split(' ')
    filtering_name_list = filtering_name.split(' ')

    similarities = [any((word in filtering_word) for filtering_word in filtering_name_list)
                    for word in target_name_list]

    return not (False in similarities)


def filter_table(table_name, good_name):
    try:
        df = prepare_df(pd.read_excel(f'./tables/{table_name}.ods',  engine='odf'))
        filtered_goods = []
        for index, row in df.iterrows():

            if compare_filtering_lists(good_name, row["НАЗВАНИЕ ТОВАРА"]):
                good = dict(row)
                good['id'] = index

                filtered_goods.append(good)

        return filtered_goods
    except:
        return ['Ошибка в процессе поиска товаров проверьте:\nНАЖАЛИ ЛИ ВЫ НА КНОПКУ ТИПА ИСКОМОГО ТОВАРА,'
                '\nПРАВИЛЬНО ЛИ ВВЕЛИ НАЗВАНИЕ ТОВАРА,\nПопробуйте перезапустить бота - /start ']


def create_answer_text(text_dict, table):
    text = ''

    for key, value in text_dict.items():
        new_row = ''
        if key == 'КОЛИЧЕСТВО':
            if str(value) == '0':
                new_row = f'<i>{key.lower()}</i>: <b>ПРОДАНО</b>'
            else:
                new_row = f'<i>{key.lower()}</i>: <b>{value}</b>'
        elif key == 'НАЗВАНИЕ ТОВАРА':
            new_row = f'<i>{key.lower()}</i>: <b>{value.upper()}</b>'
        elif key == 'СЕКТОР' or key == 'ПОЛОЖЕНИЕ В СЕКТОРЕ':
            new_row = f'<i>{key.lower()}</i>: <b>{value}</b>'
        else:
            new_row = f'<i>{key.lower()}</i>: {value}'

        text += f'{new_row}\n'

    text += f'в таблице: {table}\n'

    return text


async def send_goods(message: types.Message, good_name):
    try:
        global table_type
        try:
            table = table_type[str(message.chat.id)]
        except:
            await message.reply('Вы не выбрали тип искомого товара')
            return

        answers = filter_table(table, good_name)

        for answer in answers:
            await message.answer(create_answer_text(answer, table), parse_mode="HTML")

        return
    except:
        await message.answer('Произошла ошибка, убедитесь в правильности введённых данных.\nПерезапуск бота - /start')


def set_table_type(table, chat_id):
    global table_type
    table_type[str(chat_id)] = table


def set_processing_goods(product, chat_id):
    global processing_goods
    processing_goods[str(chat_id)] = product



