from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.infrastructure.database.health import check_database_connection


def create_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.include_router(api_router)

    return app


app = create_application()


@app.get("/database-test")
async def check_connection():
    return await check_database_connection()
