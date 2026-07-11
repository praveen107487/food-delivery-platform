from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.customer.models.customer import Customer


class AuthenticationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> Customer | None:
        statement = select(Customer).where(Customer.email == email)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        statement = select(Customer).where(Customer.customer_id == customer_id)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def save(self, customer: Customer) -> Customer:
        self._session.add(customer)
        await self._session.flush()

        return customer
