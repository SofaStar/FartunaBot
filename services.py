import pandas as pd
from aiogram import types

table_type = {}


def prepare_df(df):
    df['НАЗВАНИЕ ТОВАРА'] = [str(value).lower() for value in df['НАЗВАНИЕ ТОВАРА']]

    for column, data in df.items():
        for index, value in enumerate(data):
            if str(value) == 'nan':
                df[column][index] = 'не указано'
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


def create_answer_text(text_dict):
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

    return text


async def send_goods(message: types.Message, good_name):
    try:
        global table_type
        table = table_type[str(message.chat.id)]
        if not bool(table_type):
            await message.reply('Вы не выбрали тип искомого товара')
            return
        answers = filter_table(table, good_name)

        for answer in answers:
            await message.answer(create_answer_text(answer), parse_mode="HTML")

        return
    except:
        await message.answer('Произошла ошибка, убедитесь в правильности введённых данных.\nПерезапуск бота - /start')


def set_table_type(table, chat_id):
    global table_type
    table_type[str(chat_id)] = table



