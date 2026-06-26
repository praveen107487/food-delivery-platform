from fastapi import FastAPI

from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    return app


app = create_application()
