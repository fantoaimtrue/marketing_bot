from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_builder():
    builder = InlineKeyboardBuilder()
    for i in range(1, 17):
        builder.row(InlineKeyboardButton(text=str(i), callback_data=str(i)))
        builder.adjust(4, 3)
    return builder


def kb_report():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='/report', callback_data='kb_report')
        ],
    ])
    return ikb


def kb_check_error():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Верно', callback_data='check_yes'))
    builder.add(InlineKeyboardButton(text='Не верно', callback_data='check_no'))
    builder.adjust(1)
    return builder


def kb_mission():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Да', callback_data='kb_mission_yes'))
    builder.adjust(1)
    return builder


def check_subscribe():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Подписаться', url="https://t.me/testfantoaimtrue"))
    builder.add(InlineKeyboardButton(text='Проверить подписку', callback_data='check_sub'))
    builder.adjust(1)
    return builder


def buy_place():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Забронировать место', url="https://sblnk.ru/1167589460"))
    builder.adjust(1)
    return builder


def check_subscribe_return():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Проверить подписку еще раз', callback_data='check_sub'))
    builder.adjust(1)
    return builder


def check_valid_message():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Да', callback_data='check_valid_yes'))
    builder.add(InlineKeyboardButton(text='Нет', callback_data='check_valid_no'))
    builder.adjust(2)
    return builder


def years_inline():
    builder = InlineKeyboardBuilder()
    for date in range(2024, 2029):
        builder.add(InlineKeyboardButton(text=str(date), callback_data=f'years_{date}'))
    builder.add(InlineKeyboardButton(text='Назад 🔙', callback_data='back_years'))
    builder.adjust(4)
    return builder


all_month = {
    'Январь': '01',
    'Февраль': '02',
    'Март': '03',
    'Апрель': '04',
    'Май': '05',
    'Июнь': '06',
    'Июль': '07',
    'Август': '08',
    'Сентябрь': '09',
    'Октябрь': '10',
    'Ноябрь': '11',
    'Декабрь': '12',
}


def month_inline():
    builder = InlineKeyboardBuilder()
    for month, dt in all_month.items():
        builder.add(InlineKeyboardButton(text=month, callback_data=f'month_{dt}'))
    builder.add(InlineKeyboardButton(text='Назад 🔙', callback_data='back_years'))
    builder.adjust(4)
    return builder



