from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.database.engine import engine

async def check_database_connection() -> bool:
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False