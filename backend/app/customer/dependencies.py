from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.customer.repository import CustomerRepository
from app.customer.service import CustomerService
from app.infrastructure.database.dependencies import get_db


def get_customer_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> CustomerRepository:
    return CustomerRepository(session)


def get_customer_service(
    repository: Annotated[
        CustomerRepository,
        Depends(get_customer_repository),
    ],
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> CustomerService:
    return CustomerService(
        repository=repository,
        session=session,
    )
