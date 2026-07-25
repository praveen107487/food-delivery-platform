from uuid import UUID

from sqlalchemy import Result, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.order.models import Order, OrderStatusHistory
from app.shared.enums import OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _order_query(self) -> Select[tuple[Order]]:
        return select(Order).options(
            selectinload(Order.order_items),
            selectinload(Order.delivery_address_snapshot),
            selectinload(Order.applied_coupon_snapshot),
            selectinload(Order.status_history),
            selectinload(Order.payments),
        )

    async def create_order(
        self,
        order: Order,
    ) -> Order:
        self._session.add(order)
        await self._session.flush()
        await self._session.refresh(order)

        return order

    async def save(
        self,
        order: Order,
    ) -> Order:
        await self._session.flush()
        await self._session.refresh(order)

        return order

    async def get_order_by_id(
        self,
        order_id: UUID,
    ) -> Order | None:
        query = self._order_query().where(
            Order.order_id == order_id,
        )

        result: Result[tuple[Order]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_order(
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

    async def get_current_order(
        self,
        customer_id: UUID,
    ) -> Order | None:
        query = (
            self._order_query()
            .where(
                Order.customer_id == customer_id,
                Order.current_status.notin_(
                    (
                        OrderStatus.DELIVERED,
                        OrderStatus.CANCELLED,
                    )
                ),
            )
            .order_by(Order.created_at.desc())
            .limit(1)
        )

        result: Result[tuple[Order]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_order_timeline(
        self,
        customer_id: UUID,
        order_id: UUID,
    ) -> list[OrderStatusHistory]:
        order = await self.get_order(
            customer_id=customer_id,
            order_id=order_id,
        )

        if order is None:
            return []

        return sorted(
            order.status_history,
            key=lambda history: history.changed_at,
        )

    async def list_orders(
        self,
        customer_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[Order], int]:
        offset = (page - 1) * page_size

        query = (
            self._order_query()
            .where(
                Order.customer_id == customer_id,
            )
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        result: Result[tuple[Order]] = await self._session.execute(query)

        total_count = await self.count_customer_orders(customer_id)

        return list(result.scalars().all()), total_count

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
