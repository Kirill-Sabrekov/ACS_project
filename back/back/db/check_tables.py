import asyncio
from sqlalchemy import text, inspect
from database import engine
import logging

logger = logging.getLogger(__name__)

async def check_tables():
    try:
        async with engine.begin() as conn:
            # Проверяем существование таблиц
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"Available tables: {tables}")
            
            if 'nodes' not in tables:
                logger.error("Table 'nodes' does not exist!")
                return
                
            if 'nodes_history' not in tables:
                logger.error("Table 'nodes_history' does not exist!")
                return
            
            # Проверяем структуру таблицы nodes
            nodes_columns = inspector.get_columns('nodes')
            logger.info("Nodes table columns:")
            for col in nodes_columns:
                logger.info(f"  {col['name']}: {col['type']}")
            
            # Проверяем структуру таблицы nodes_history
            history_columns = inspector.get_columns('nodes_history')
            logger.info("Nodes_history table columns:")
            for col in history_columns:
                logger.info(f"  {col['name']}: {col['type']}")
            
            # Проверяем данные в таблице nodes
            result = await conn.execute(text("SELECT COUNT(*) FROM nodes"))
            nodes_count = result.scalar()
            logger.info(f"Nodes table contains {nodes_count} records")
            
            if nodes_count > 0:
                result = await conn.execute(text("SELECT * FROM nodes LIMIT 5"))
                nodes = result.fetchall()
                logger.info("Sample nodes data:")
                for node in nodes:
                    logger.info(f"  {node}")
            
            # Проверяем данные в таблице nodes_history
            result = await conn.execute(text("SELECT COUNT(*) FROM nodes_history"))
            history_count = result.scalar()
            logger.info(f"Nodes_history table contains {history_count} records")
            
            if history_count > 0:
                result = await conn.execute(text("SELECT * FROM nodes_history LIMIT 5"))
                history = result.fetchall()
                logger.info("Sample history data:")
                for record in history:
                    logger.info(f"  {record}")
                
    except Exception as e:
        logger.error(f"Error checking tables: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(check_tables()) 