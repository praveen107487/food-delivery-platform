from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.order.exceptions import OrderNotFoundError
from app.order.repository import OrderRepository
from app.payment.exceptions import (
    PaymentAlreadySuccessfulException,
    PaymentNotFoundException,
    PaymentRetryNotAllowedException,
)
from app.payment.mapper import (
    to_history_response,
    to_response,
)
from app.payment.models.payment import Payment
from app.payment.repository import PaymentRepository
from app.payment.schemas import (
    PaymentCreateRequest,
    PaymentHistoryResponse,
    PaymentResponse,
    PaymentRetryRequest,
)
from app.shared.enums import PaymentStatus


class PaymentService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session
        self._payment_repository = PaymentRepository(session)
        self._order_repository = OrderRepository(session)

    async def create_payment(
        self,
        order_id: UUID,
        request: PaymentCreateRequest,
    ) -> PaymentResponse:
        """
        Create the initial payment attempt for an order.
        """

        order = await self._order_repository.get_order_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(order_id)

        successful_payment = await self._payment_repository.get_successful_payment(
            order_id
        )

        if successful_payment is not None:
            raise PaymentAlreadySuccessfulException(order_id)

        payment_gateway = "RAZORPAY" if request.payment_method == "ONLINE" else None

        payment = Payment(
            order_id=order.order_id,
            payment_method=request.payment_method,
            payment_gateway=payment_gateway,
            amount=order.grand_total,
            payment_status=PaymentStatus.INITIATED,
        )

        try:
            payment = await self._payment_repository.create(payment)

            await self._session.commit()

            return to_response(payment)

        except Exception:
            await self._session.rollback()
            raise

    async def get_payment_by_id(
        self,
        payment_id: UUID,
    ) -> PaymentResponse:

        payment = await self._payment_repository.get_by_id(payment_id)

        if payment is None:
            raise PaymentNotFoundException(payment_id)

        return to_response(payment)

    async def list_order_payments(
        self,
        order_id: UUID,
    ) -> PaymentHistoryResponse:

        order = await self._order_repository.get_order_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(order_id)

        payments = await self._payment_repository.list_by_order(order_id)

        return to_history_response(payments)

    async def retry_payment(
        self,
        payment_id: UUID,
        request: PaymentRetryRequest,
    ) -> PaymentResponse:

        payment = await self._payment_repository.get_by_id(payment_id)

        if payment is None:
            raise PaymentNotFoundException(payment_id)

        if payment.payment_status != PaymentStatus.FAILED:
            raise PaymentRetryNotAllowedException(payment.order_id)

        order = await self._order_repository.get_order_by_id(payment.order_id)

        if order is None:
            raise OrderNotFoundError(payment.order_id)

        payment_gateway = "RAZORPAY" if request.payment_method == "ONLINE" else None

        new_payment = Payment(
            order_id=order.order_id,
            payment_method=request.payment_method,
            payment_gateway=payment_gateway,
            amount=order.grand_total,
            payment_status=PaymentStatus.INITIATED,
        )

        try:
            new_payment = await self._payment_repository.create(new_payment)

            await self._session.commit()

            return to_response(new_payment)

        except Exception:
            await self._session.rollback()
            raise
