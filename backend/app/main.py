from fastapi import FastAPI

from app.core.config import get_settings
from app.infrastructure.database.health import check_database_connection


def create_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    return app


app = create_application()


@app.get("/database-test")
async def check_connection():
    # We add 'async' to the def and 'await' the database check
    result = await check_database_connection()
    return result
