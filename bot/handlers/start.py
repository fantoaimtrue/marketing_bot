import asyncio
from email import message
from re import U
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup 
from aiogram.types import FSInputFile
from aiogram.types import Message, CallbackQuery
from aiogram.methods import SendPhoto
from aiogram.filters import Command
from sqlalchemy.future import select
from Data.db import get_message_by_id, get_session, get_mission_by_id, get_year_by_id
from Data.models import User
from keyboards.inline import buy_place, kb_check_error, kb_mission, check_subscribe, check_subscribe_return
from main import check_user_subscription


router = Router()

# Вспомогательная функция для получения или создания пользователя
async def get_or_create_user(db_session, message: Message):
    query = select(User).where(User.user_id == message.from_user.id)
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        db_session.add(user)
        await db_session.commit()
    return user


class Form(StatesGroup):
    change_date = State()
    date = State()
    check_date = State()
    get_mission = State()
    check_sub_chanel = State()



@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    async with await get_session() as db_session:
        await get_or_create_user(db_session, message)
        text_1 = ("Привет! 👋 Рад тебя видеть.\n\n"
            "Меня зовут Денис Сатаев. Я цифровой психолог и бизнес-коуч.\n\n"
            "Благодаря работе со мной люди:\n\n📍меняют и перепрошивают своё подсознание, мышление и состояние\n"
            "📍находят миссию и предназначение исходя из своей данности\n"
            "📍начинают глубже понимать себя и людей, которые их окружают\n\n"
            "Результат: ученики делают первые шаги к новой, желанной реальности и становятся богаче, успешнее и счастливее 🔥\n\n"
            "И у меня есть для тебя подарок 🎁\n\n"
            "<b><i>Прямо сейчас пройди экспресс диагностику по дате рождения, чтобы сделать первые шаги на пути к своему предназначению 👇</i></b>")
        photo = FSInputFile('photo/main.jpg')
        await state.set_state(Form.date)
        await message.answer_photo(photo=photo, caption=text_1, parse_mode="HTML")
        
        await asyncio.sleep(5)
        text_2 = (
            "Напиши свою дату рождения, я сделаю расчет и пришлю краткую характеристику\n\n"
            "📍 Дату рождения пишите в формате DD.MM.YYYY\n\n"
            "Пример: вы родились 09.08.1998. Значит нужно написать: 09.08.1998"
        )
        await message.answer(text=text_2)
        
        
@router.message(Form.date, F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$"))
async def process_date(message: Message, state: FSMContext):
    async with await get_session() as db_session:
        await state.update_data(date=message.text)
        data = await state.get_data()
        await state.set_state(Form.check_date)
        text_3 = (
            "Проверь данные, все верно? 🤔\n\n"
        )
        await message.answer(f'{text_3}{data.get("date")}', parse_mode="HTML", reply_markup=kb_check_error().as_markup())
    



@router.callback_query(Form.check_date, F.data == 'check_yes')
async def check_date(callback: CallbackQuery, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    date = data.get('date')
    
    if not date:
        await callback.message.answer("Ошибка: дата не найдена.")
        return

    # Функция для сокращения до однозначного числа
    def reduce_to_single_digit(date_str):
        day, _, _ = date_str.split(".")  # Извлекаем только день
        total = sum(int(digit) for digit in day)  # Складываем цифры дня
        
        while total >= 10:
            total = sum(int(digit) for digit in str(total))  # Сокращаем до однозначного числа
        
        return total

    # Получаем сокращенное число
    reduce = reduce_to_single_digit(date)

    try:
        # Загружаем фото с именем файла, соответствующим числу
        photo = FSInputFile(f'photo/conscience/{str(reduce)}.jpg')
        await callback.message.answer_photo(photo=photo)

        # Получаем сообщение по идентификатору и отправляем пользователю
        message = await get_message_by_id(message_id=reduce)
        await callback.message.answer(message.description)

        # Переходим к следующему состоянию
        await state.set_state(Form.get_mission)
        await callback.message.answer(
            'Ты хочешь узнать свою миссию исходя из даты рождения? 🔥',
            parse_mode="HTML",
            reply_markup=kb_mission().as_markup()
        )
    except Exception as ex:
        await callback.message.answer(f'Ошибка: {ex}')



@router.callback_query(Form.get_mission, F.data=='kb_mission_yes')
async def get_mission(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data['date']
    
    # Применяем функцию для расчета однозначного числа
    def calculate_single_digit(date_str):
        total = sum(int(char) for char in date_str if char.isdigit())
        while total > 9:
            total = sum(int(digit) for digit in str(total))
        return total
    
    single_digit = calculate_single_digit(date)
    message = await get_mission_by_id(message_id=single_digit)
    text_3 = (
        "В подарок я хочу дать тебе личный расчет на 2024 год! В нем ты узнаешь свой секрет квантового скачка во всех сферах жизни.\n\n"
        "Для получения «РАСЧЕТА», пожалуйста, вступи в канал 👇🏼"
        "https://t.me/testfantoaimtrue"
    )
    
    photo = FSInputFile(f'photo/mission/{str(single_digit)}.jpg')
    await callback.message.answer_photo(photo=photo)
    await callback.message.answer(message.description)
    
    question = "Узнаете себя?"
    options = ["Да", "Нет", "Немного"]
    await callback.message.answer_poll(question=question, options=options, is_anonymous=True, allows_multiple_answers=False)
    await callback.message.answer(text_3, parse_mode="HTML", reply_markup=check_subscribe().as_markup())
    await state.set_state(Form.check_sub_chanel)
    
    
    
@router.callback_query(Form.check_sub_chanel, F.data == 'check_sub')
async def check_channel_sub(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    is_subscribed = await check_user_subscription(user_id)
    text_4 = (
        f"{callback.from_user.username}, представь себе жизнь, в которой нет места упущенным возможностям. \n\n"
        "Тебе больше незнакомы сожаления о том, что очередной шанс “проплывает мимо”, и ты буквально 'притягиваешь' к себе новые возможности. Все твои желания уже исполнились, и с каждым днем жизнь становится всё лучше и лучше!✨\n\n"
        "Именно такую реальность ты создашь себе после подробного текстового разбора.\n\n"
        "Только для тебя, следующие 24 часа стоимость такого разбора составляет 1491 рубль / 17$, вместо 6000 рублей / 68$\n\n"
        "Вы получите:\n1. Разбор Числа Сознания - число реализации Души (направление вектора эго, наслаждение, причины разрушения, задача, понимание..)\n"
        "2. Разбор «Матрицы» - Сильные стороны Сознания и стороны которые Душа пришла наработать.\n"
        "3. Разбор числа Миссии (предназначение)\n"
        "4. Обозначаются и прорабатываются инструменты для наработки Матрицы\n"
        "5. Просматриваем текущий год, его характеристики и влияние\n"
        "6. Определяем сферу реализации человека\n"
        "7. Разбор значения имени\n\n"
        "+ БОНУС экспресс-консультация от цифрового психолога\n\n"
        "Для оплаты перейдите по ссылке: https://sblnk.ru/1167589460"
    )
    data = await state.get_data()
    date = data['date']
    
    def reduce_to_single_digit(date_str):
        day, month, _ = date_str.split(".")  # Извлекаем день и месяц
        # Суммируем цифры дня и месяца
        total = sum(int(digit) for digit in day) + sum(int(digit) for digit in month) + 8  # 2 + 2 + 4 = 8
        
        # Сокращаем до однозначного числа
        while total >= 10:
            total = sum(int(digit) for digit in str(total))
        
        return total
    
    single_digit = reduce_to_single_digit(date)
    message = await get_year_by_id(message_id=single_digit)
    if is_subscribed:
        photo = FSInputFile(f'photo/years/{str(single_digit)}.jpg')
        await callback.message.answer_photo(photo=photo)
        await callback.message.answer(text=message.description)
        await callback.message.answer(text=text_4, reply_markup=buy_place().as_markup())
    else:
        await callback.message.answer(
            "❌ Вы не подписаны на канал. Пожалуйста, подпишитесь и нажмите «Проверить подписку» ещё раз.", reply_markup=check_subscribe_return().as_markup()
        )
    




