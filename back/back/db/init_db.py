import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from core.config import settings
import logging
from models import Base

logger = logging.getLogger(__name__)

async def init_db():
    try:
        # Создаем движок
        engine = create_async_engine(settings.DATABASE_URL)
        
        # Проверяем подключение
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            
            # Создаем таблицы, если они не существуют
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created successfully")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db()) 