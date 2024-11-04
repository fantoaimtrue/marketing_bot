import asyncio
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message
import pandas as pd

from Data.db import (
    create_conscience,
    create_mission,
    create_years,
    get_all_users,
    get_session,
)
from keyboards.inline import check_valid_message
from decouple import config


ALLOWED_USER_IDS = list(map(int, config("ALLOWED_USER_IDS").split(",")))

router = Router()


class AddConscience(StatesGroup):
    add_mes = State()
    save_mes = State()


class AddMission(StatesGroup):
    add_mes = State()
    save_mes = State()


class AddYear(StatesGroup):
    add_mes = State()
    save_mes = State()


@router.message(Command(commands=["add_conscience"]))
async def cmd_add_conscience(message: Message, state: FSMContext):
    if message.from_user.id not in ALLOWED_USER_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Напишите текст который нужно добавить в базу данных")
    await state.set_state(AddConscience.add_mes)


@router.message(AddConscience.add_mes)
async def print_message(message: Message, state: FSMContext):
    description = message.text  # Получаем текст сообщения от пользователя
    if description:
        await message.answer(
            "Вы уверены что хотите добавить это сообщение в базу данных?",
            reply_markup=check_valid_message().as_markup(),
        )
        await state.update_data(description=description)
        await state.set_state(AddConscience.save_mes)
        # await create_message(description)


@router.callback_query(AddConscience.save_mes, F.data == "check_valid_yes")
async def check_valid_message_yes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    description = data["description"]
    await create_conscience(description=description)
    await callback.answer("Сообщение успешно добавлено в базу")
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.callback_query(AddConscience.save_mes, F.data == "check_valid_no")
async def check_valid_message_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите текст который нужно добавить в базу данных")
    await state.set_state(AddConscience.add_mes)


@router.message(Command(commands=["add_mission"]))
async def cmd_add_mission(message: Message, state: FSMContext):
    if message.from_user.id not in ALLOWED_USER_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Напишите текст который нужно добавить в базу данных")
    await state.set_state(AddMission.add_mes)


@router.message(AddMission.add_mes)
async def print_message(message: Message, state: FSMContext):
    description = message.text  # Получаем текст сообщения от пользователя
    if description:
        await message.answer(
            "Вы уверены что хотите добавить это сообщение в базу данных?",
            reply_markup=check_valid_message().as_markup(),
        )
        await state.update_data(description=description)
        await state.set_state(AddMission.save_mes)
        # await create_message(description)


@router.callback_query(AddMission.save_mes, F.data == "check_valid_yes")
async def check_valid_message_yes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    description = data["description"]
    await create_mission(description=description)
    await callback.answer("Сообщение успешно добавлено в базу")
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.callback_query(AddMission.save_mes, F.data == "check_valid_no")
async def check_valid_message_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите текст который нужно добавить в базу данных")
    await state.set_state(AddMission.add_mes)


@router.message(Command(commands=["add_year"]))
async def cmd_add_year(message: Message, state: FSMContext):
    if message.from_user.id not in ALLOWED_USER_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Напишите текст который нужно добавить в базу данных")
    await state.set_state(AddYear.add_mes)


@router.message(AddYear.add_mes)
async def print_message_year(message: Message, state: FSMContext):
    description = message.text  # Получаем текст сообщения от пользователя
    if description:
        await message.answer(
            "Вы уверены что хотите добавить это сообщение в базу данных?",
            reply_markup=check_valid_message().as_markup(),
        )
        await state.update_data(description=description)
        await state.set_state(AddYear.save_mes)
        # await create_message(description)


@router.callback_query(AddYear.save_mes, F.data == "check_valid_yes")
async def check_valid_message_yes_year(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    description = data["description"]
    await create_years(description=description)
    await callback.answer("Сообщение успешно добавлено в базу")
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.callback_query(AddYear.save_mes, F.data == "check_valid_no")
async def check_valid_message_no_year(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите текст который нужно добавить в базу данных")
    await state.set_state(AddYear.add_mes)


async def export_users_to_excel():
    users = await get_all_users()  # Получаем всех пользователей
    if not users:
        print("Нет пользователей для выгрузки.")
        return

    # Создаем DataFrame из списка пользователей
    data = {
        "User ID": [user.user_id for user in users],
        "Username": [user.username for user in users],
        "First Name": [user.first_name for user in users],
        "Last Name": [user.last_name for user in users],
    }
    df = pd.DataFrame(data)

    # Сохраняем DataFrame в Excel файл
    file_name = "users_list.xlsx"
    df.to_excel(file_name, index=False)

    print(f"Список пользователей успешно выгружен в {file_name}.")


@router.message(Command(commands=["export_users"]))
async def cmd_export_users(message: Message):
    if message.from_user.id not in ALLOWED_USER_IDS:  # Проверка на админские права
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    # Экспортируем пользователей в Excel
    await export_users_to_excel()
    
    # Отправляем файл пользователю
    file_name = "users_list.xlsx"
    document = FSInputFile(file_name)
    await message.answer_document(document=document)
    await message.answer("Список пользователей был выгружен и отправлен в Excel.")
