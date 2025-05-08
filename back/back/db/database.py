from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from core.config import settings
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# Настройки подключения к базе данных
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

try:
    # Создаем асинхронный движок
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,  # Включаем логирование SQL-запросов
        poolclass=NullPool  # Отключаем пул соединений для асинхронной работы
    )

    # Создаем фабрику сессий
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

async def get_db():
    """
    Dependency для получения сессии базы данных.
    Обрабатывает ошибки подключения и автоматически закрывает сессию.
    """
    async with AsyncSessionLocal() as session:
        try:
            # Проверяем подключение
            await session.execute("SELECT 1")
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error in database session: {e}")
            await session.rollback()
            raise
        finally:
            await session.close() 