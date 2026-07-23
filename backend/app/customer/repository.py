from uuid import UUID

from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.customer.models.customer import Customer
from app.customer.models.saved_address import SavedAddress


class CustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:
        statement: Select[tuple[Customer]] = select(Customer).where(
            Customer.customer_id == customer_id,
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> Customer | None:
        statement: Select[tuple[Customer]] = select(Customer).where(
            Customer.email == email,
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def update(
        self,
        customer: Customer,
    ) -> Customer:
        await self._session.flush()

        return customer

    async def create_address(
        self,
        address: SavedAddress,
    ) -> SavedAddress:
        self._session.add(address)

        await self._session.flush()

        return address

    async def get_address_by_id(
        self,
        address_id: UUID,
    ) -> SavedAddress | None:
        statement: Select[tuple[SavedAddress]] = select(
            SavedAddress,
        ).where(
            SavedAddress.address_id == address_id,
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def list_addresses(
        self,
        customer_id: UUID,
    ) -> list[SavedAddress]:
        statement: Select[tuple[SavedAddress]] = (
            select(SavedAddress)
            .where(SavedAddress.customer_id == customer_id)
            .order_by(
                SavedAddress.is_default.desc(),
                SavedAddress.created_at.asc(),
            )
        )

        result = await self._session.execute(statement)

        return list(result.scalars().all())

    async def get_default_address(
        self,
        customer_id: UUID,
    ) -> SavedAddress | None:
        statement: Select[tuple[SavedAddress]] = select(
            SavedAddress,
        ).where(
            SavedAddress.customer_id == customer_id,
            SavedAddress.is_default.is_(True),
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def clear_default_address(
        self,
        customer_id: UUID,
    ) -> None:
        statement = (
            update(SavedAddress)
            .where(
                SavedAddress.customer_id == customer_id,
                SavedAddress.is_default.is_(True),
            )
            .values(is_default=False)
        )

        await self._session.execute(statement)

    async def update_address(
        self,
        address: SavedAddress,
    ) -> SavedAddress:
        await self._session.flush()

        return address

    async def delete_address(
        self,
        address: SavedAddress,
    ) -> None:
        await self._session.delete(address)

        await self._session.flush()
