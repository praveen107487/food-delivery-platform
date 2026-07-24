from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.order.exceptions import OrderNotFoundError
from app.order.models.order import Order
from app.order.models.order_status_history import OrderStatusHistory
from app.order.repository import OrderRepository
from app.payment.exceptions import (
    PaymentAccessDeniedException,
    PaymentAlreadySuccessfulException,
    PaymentNotEligibleException,
    PaymentNotFoundException,
    PaymentRetryNotAllowedException,
    PaymentVerificationFailedException,
)
from app.payment.mapper import (
    to_history_response,
    to_initiation_response,
    to_response,
    to_status_response,
    to_storage_payment_method,
)
from app.payment.models.payment import Payment
from app.payment.repository import PaymentRepository
from app.payment.schemas import (
    PaymentCreateRequest,
    PaymentHistoryResponse,
    PaymentInitiationResponse,
    PaymentResponse,
    PaymentRetryRequest,
    PaymentStatusResponse,
    PaymentVerificationRequest,
)
from app.shared.enums import OrderStatus, PaymentStatus


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
        customer_id: UUID,
        request: PaymentCreateRequest,
    ) -> PaymentInitiationResponse:
        order = await self._get_customer_order(
            customer_id=customer_id,
            order_id=request.order_id,
        )

        self._ensure_order_is_payable(order)

        successful_payment = await self._payment_repository.get_successful_payment(
            order.order_id
        )

        if successful_payment is not None:
            raise PaymentAlreadySuccessfulException(order.order_id)

        payment_method = to_storage_payment_method(request.payment_method)

        payment = Payment(
            order_id=order.order_id,
            payment_method=payment_method,
            payment_gateway=self._get_payment_gateway(payment_method),
            amount=order.grand_total,
            payment_status=PaymentStatus.INITIATED,
        )

        try:
            payment = await self._payment_repository.create(payment)

            await self._session.commit()
            await self._session.refresh(payment)

            return to_initiation_response(payment)

        except Exception:
            await self._session.rollback()
            raise

    async def verify_payment(
        self,
        customer_id: UUID,
        payment_id: UUID,
        request: PaymentVerificationRequest,
    ) -> PaymentStatusResponse:
        payment = await self._get_customer_payment(
            customer_id=customer_id,
            payment_id=payment_id,
        )

        if payment.payment_status == PaymentStatus.SUCCESS:
            raise PaymentAlreadySuccessfulException(payment.order_id)

        try:
            payment.payment_status = PaymentStatus.PROCESSING
            payment.gateway_transaction_id = request.gateway_transaction_id

            if self._is_gateway_transaction_verified(request.gateway_transaction_id):
                payment.payment_status = PaymentStatus.SUCCESS
                payment.paid_at = datetime.now(timezone.utc)
                payment.failure_reason = None
                payment.order.current_status = OrderStatus.CONFIRMED
                payment.order.confirmed_at = payment.paid_at
                payment.order.status_history.append(
                    OrderStatusHistory(
                        order_id=payment.order_id,
                        status=OrderStatus.CONFIRMED,
                    )
                )
            else:
                payment.payment_status = PaymentStatus.FAILED
                payment.failure_reason = "Verification Failed"

            await self._payment_repository.update(payment)
            await self._session.commit()
            await self._session.refresh(payment)

        except Exception:
            await self._session.rollback()
            raise

        if payment.payment_status == PaymentStatus.FAILED:
            raise PaymentVerificationFailedException(payment.payment_id)

        return to_status_response(payment)

    async def get_payment_status(
        self,
        customer_id: UUID,
        payment_id: UUID,
    ) -> PaymentStatusResponse:
        payment = await self._get_customer_payment(
            customer_id=customer_id,
            payment_id=payment_id,
        )

        return to_status_response(payment)

    async def get_payment_by_id(
        self,
        customer_id: UUID,
        payment_id: UUID,
    ) -> PaymentResponse:
        payment = await self._get_customer_payment(
            customer_id=customer_id,
            payment_id=payment_id,
        )

        return to_response(payment)

    async def list_order_payments(
        self,
        customer_id: UUID,
        order_id: UUID,
    ) -> PaymentHistoryResponse:
        await self._get_customer_order(
            customer_id=customer_id,
            order_id=order_id,
        )

        payments = await self._payment_repository.list_by_order(order_id)

        return to_history_response(payments)

    async def retry_payment(
        self,
        customer_id: UUID,
        payment_id: UUID,
        request: PaymentRetryRequest,
    ) -> PaymentInitiationResponse:
        payment = await self._get_customer_payment(
            customer_id=customer_id,
            payment_id=payment_id,
        )

        if payment.payment_status != PaymentStatus.FAILED:
            raise PaymentRetryNotAllowedException(payment.order_id)

        order = payment.order

        self._ensure_order_is_payable(order)

        payment_method = to_storage_payment_method(request.payment_method)

        new_payment = Payment(
            order_id=order.order_id,
            payment_method=payment_method,
            payment_gateway=self._get_payment_gateway(payment_method),
            amount=order.grand_total,
            payment_status=PaymentStatus.INITIATED,
        )

        try:
            new_payment = await self._payment_repository.create(new_payment)

            await self._session.commit()
            await self._session.refresh(new_payment)

            return to_initiation_response(new_payment)

        except Exception:
            await self._session.rollback()
            raise

    async def _get_customer_order(
        self,
        customer_id: UUID,
        order_id: UUID,
    ) -> Order:
        order = await self._order_repository.get_order_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(order_id)

        if order.customer_id != customer_id:
            raise PaymentAccessDeniedException(order_id)

        return order

    async def _get_customer_payment(
        self,
        customer_id: UUID,
        payment_id: UUID,
    ) -> Payment:
        payment = await self._payment_repository.get_by_id(payment_id)

        if payment is None:
            raise PaymentNotFoundException(payment_id)

        if payment.order.customer_id != customer_id:
            raise PaymentAccessDeniedException(payment_id)

        return payment

    def _ensure_order_is_payable(
        self,
        order: Order,
    ) -> None:
        if order.current_status != OrderStatus.PENDING_PAYMENT:
            raise PaymentNotEligibleException(order.order_id)

        if order.grand_total <= 0:
            raise PaymentNotEligibleException(order.order_id)

    def _get_payment_gateway(
        self,
        payment_method: str,
    ) -> str | None:
        if payment_method == "ONLINE":
            return "RAZORPAY"

        return None

    def _is_gateway_transaction_verified(
        self,
        gateway_transaction_id: str,
    ) -> bool:
        return gateway_transaction_id.strip() != ""
