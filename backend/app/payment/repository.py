from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.payment.models.payment import Payment
from app.shared.enums.payment_status import PaymentStatus


class PaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        payment: Payment,
    ) -> Payment:
        self._session.add(payment)

        await self._session.flush()

        return payment

    async def get_by_id(
        self,
        payment_id: UUID,
    ) -> Payment | None:
        statement = select(Payment).where(Payment.payment_id == payment_id)

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_reference(
        self,
        payment_reference: str,
    ) -> Payment | None:
        statement = select(Payment).where(
            Payment.payment_reference == payment_reference
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def list_by_order(
        self,
        order_id: UUID,
    ) -> Sequence[Payment]:

        statement = (
            select(Payment)
            .where(Payment.order_id == order_id)
            .order_by(Payment.created_at.desc())
        )

        result = await self._session.execute(statement)

        return result.scalars().all()

    async def get_successful_payment(
        self,
        order_id: UUID,
    ) -> Payment | None:
        statement = select(Payment).where(
            Payment.order_id == order_id,
            Payment.payment_status == PaymentStatus.SUCCESS,
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def update(
        self,
        payment: Payment,
    ) -> Payment:

        await self._session.flush()

        await self._session.refresh(payment)

        return payment
