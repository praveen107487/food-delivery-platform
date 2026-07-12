from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dependencies import get_db
from app.restaurant.repository import RestaurantRepository
from app.restaurant.service import RestaurantService


def get_restaurant_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> RestaurantRepository:
    return RestaurantRepository(session)


def get_restaurant_service(
    repository: Annotated[
        RestaurantRepository,
        Depends(get_restaurant_repository),
    ],
) -> RestaurantService:
    return RestaurantService(repository)
