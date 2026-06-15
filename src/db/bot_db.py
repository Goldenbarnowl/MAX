import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

db_pool: asyncpg.Pool | None = None


async def create_db_pool() -> asyncpg.Pool:
    """
    Создание пула подключений к PostgreSQL.
    Пул используется для повторного использования соединений
    при обработке запросов от разных пользователей бота.
    """
    global db_pool

    db_pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        min_size=1,
        max_size=10
    )

    return db_pool


async def init_db(pool: asyncpg.Pool) -> None:
    """
    Создание таблиц базы данных при первом запуске проекта.
    Если таблицы уже существуют, повторно они не создаются.
    """
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        messenger_type VARCHAR(50) DEFAULT 'MAX',
        username VARCHAR(255),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        phone VARCHAR(20) UNIQUE,
        gender VARCHAR(10),
        birth_date DATE,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        user_id INTEGER NOT NULL,
        st_score INTEGER NOT NULL,
        lt_score INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_test_results_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """

    async with pool.acquire() as connection:
        await connection.execute(query)


async def close_db_pool() -> None:
    """
    Закрытие пула подключений при остановке приложения.
    """
    global db_pool

    if db_pool is not None:
        await db_pool.close()
        db_pool = None