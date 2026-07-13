from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cart.repository import CartRepository
from app.cart.service import CartService
from app.infrastructure.database.dependencies import get_db
from app.restaurant.dependencies import (
    get_restaurant_repository,
)
from app.restaurant.repository import RestaurantRepository


def get_cart_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> CartRepository:
    return CartRepository(session)


def get_cart_service(
    repository: Annotated[
        CartRepository,
        Depends(get_cart_repository),
    ],
    restaurant_repository: Annotated[
        RestaurantRepository,
        Depends(get_restaurant_repository),
    ],
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> CartService:
    return CartService(
        repository=repository,
        restaurant_repository=restaurant_repository,
        session=session,
    )
