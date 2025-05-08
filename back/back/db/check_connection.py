import asyncio
from database import engine
import logging

logger = logging.getLogger(__name__)

async def check_connection():
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_connection()) 