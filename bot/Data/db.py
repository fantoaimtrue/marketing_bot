import os
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Data.models import Base, User, ChislaSoznaniya, Missions, Years

# Загружаем переменные окружения
load_dotenv()

# Получаем параметры подключения из переменных окружения
ip = os.getenv('IP')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
DATABASE = os.getenv('DATABASE')
DB_PORT = os.getenv('DB_PORT')

# Формируем строку подключения
DATABASE_URL = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{ip}:{DB_PORT}/{DATABASE}'

# Создаем движок базы данных
engine = create_async_engine(DATABASE_URL, echo=True)


# Создаем фабрику сессий
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        print("Создание таблиц...")
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы")
        
# Функция для удаления всех таблиц
async def drop_tables():
    async with engine.begin() as conn:
        print("Удаление таблиц...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Таблицы удалены")

# Функция для получения новой сессии
async def get_session() -> AsyncSession:
    session = async_session_factory()  # Создаем новую сессию
    return session  # Возвращаем сессию, чтобы её можно было использовать

# Функция для создания нового пользователя
async def create_user(user_id: int, username: str, first_name: str, last_name: str):
    async with async_session_factory() as session:
        async with session.begin():
            try:
                new_user = User(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
                session.add(new_user)
                print(f"Пользователь {username} успешно добавлен!")
            except Exception as e:
                await session.rollback()  # Откатить транзакцию в случае ошибки
                print(f"Ошибка при добавлении пользователя: {e}")
                
# Функция для добавления сообщений
async def create_conscience(description: str):
    async with async_session_factory() as session:
        async with session.begin():
            try:
                new_message = ChislaSoznaniya(description=description)
                session.add(new_message)
                print(f"Новое сообщение успешно загружено в БД")
            except Exception as e:
                await session.rollback()  # Откатить транзакцию в случае ошибки
                print(f"Ошибка при добавлении нового сообщения: {e}")
                
                
# Функция для добавления сообщений
async def create_mission(description: str):
    async with async_session_factory() as session:
        async with session.begin():
            try:
                new_message = Missions(description=description)
                session.add(new_message)
                print(f"Новое сообщение успешно загружено в БД")
            except Exception as e:
                await session.rollback()  # Откатить транзакцию в случае ошибки
                print(f"Ошибка при добавлении нового сообщения: {e}")
                
                
# Функция для добавления сообщений
async def create_years(description: str):
    async with async_session_factory() as session:
        async with session.begin():
            try:
                new_message = Years(description=description)
                session.add(new_message)
                print(f"Новое сообщение успешно загружено в БД")
            except Exception as e:
                await session.rollback()  # Откатить транзакцию в случае ошибки
                print(f"Ошибка при добавлении нового сообщения: {e}")


# Функция для получения одного сообщения по id
async def get_message_by_id(message_id: int):
    async with async_session_factory() as session:
        try:
            # Выполняем запрос для получения записи с заданным id
            result = await session.execute(select(ChislaSoznaniya).filter_by(id=message_id))
            message = result.scalars().first()  # Извлекаем первое совпадение
            
            return message  # Возвращаем сообщение или None, если не найдено
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            return None
        
        
# Функция для получения одного сообщения по id
async def get_mission_by_id(message_id: int):
    async with async_session_factory() as session:
        try:
            # Выполняем запрос для получения записи с заданным id
            result = await session.execute(select(Missions).filter_by(id=message_id))
            message = result.scalars().first()  # Извлекаем первое совпадение
            
            return message  # Возвращаем сообщение или None, если не найдено
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            return None
        
        
# Функция для получения одного сообщения по id
async def get_year_by_id(message_id: int):
    async with async_session_factory() as session:
        try:
            # Выполняем запрос для получения записи с заданным id
            result = await session.execute(select(Years).filter_by(id=message_id))
            message = result.scalars().first()  # Извлекаем первое совпадение
            
            return message  # Возвращаем сообщение или None, если не найдено
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            return None
        
        

async def get_all_users() -> list:
    async with async_session_factory() as session:
        async with session.begin():
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users

# Функция для завершения работы движка
async def close_engine():
    await engine.dispose()

