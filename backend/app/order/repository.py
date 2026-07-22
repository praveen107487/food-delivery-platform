from uuid import UUID

from sqlalchemy import Result, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.order.models import Order


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _order_query(self) -> Select[tuple[Order]]:
        return select(Order).options(
            selectinload(Order.order_items),
            selectinload(Order.delivery_address_snapshot),
            selectinload(Order.applied_coupon_snapshot),
            selectinload(Order.status_history),
        )

    async def create_order(
        self,
        order: Order,
    ) -> Order:
        self._session.add(order)

        await self._session.flush()

        return order

    async def get_order_by_id(
        self,
        order_id: UUID,
    ) -> Order | None:
        query = self._order_query().where(Order.order_id == order_id)

        result: Result[tuple[Order]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_customer_order(
        self,
        customer_id: UUID,
        order_id: UUID,
    ) -> Order | None:
        query = self._order_query().where(
            Order.order_id == order_id,
            Order.customer_id == customer_id,
        )

        result: Result[tuple[Order]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def list_customer_orders(
        self,
        customer_id: UUID,
        offset: int,
        limit: int,
    ) -> list[Order]:
        query = (
            self._order_query()
            .where(
                Order.customer_id == customer_id,
            )
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result: Result[tuple[Order]] = await self._session.execute(query)

        return list(result.scalars().all())

    async def count_customer_orders(
        self,
        customer_id: UUID,
    ) -> int:
        query = (
            select(func.count())
            .select_from(Order)
            .where(
                Order.customer_id == customer_id,
            )
        )

        result: Result[tuple[int]] = await self._session.execute(query)

        return result.scalar_one()
