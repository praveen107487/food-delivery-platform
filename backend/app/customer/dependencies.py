from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.customer.repository import CustomerRepository
from app.customer.service import CustomerService
from app.infrastructure.database.dependencies import get_db


def get_customer_service(
    session: AsyncSession = Depends(
        get_db,
    ),
) -> CustomerService:
    repository = CustomerRepository(
        session,
    )

    return CustomerService(
        repository=repository,
        session=session,
    )
