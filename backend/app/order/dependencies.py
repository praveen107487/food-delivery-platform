from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cart.dependencies import get_cart_repository
from app.cart.repository import CartRepository
from app.customer.dependencies import get_customer_repository
from app.customer.repository import CustomerRepository
from app.infrastructure.database.dependencies import get_db
from app.order.repository import OrderRepository
from app.order.service import OrderService


def get_order_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> OrderRepository:
    return OrderRepository(session)


def get_order_service(
    repository: Annotated[
        OrderRepository,
        Depends(get_order_repository),
    ],
    cart_repository: Annotated[
        CartRepository,
        Depends(get_cart_repository),
    ],
    customer_repository: Annotated[
        CustomerRepository,
        Depends(get_customer_repository),
    ],
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> OrderService:
    return OrderService(
        repository=repository,
        cart_repository=cart_repository,
        customer_repository=customer_repository,
        session=session,
    )
