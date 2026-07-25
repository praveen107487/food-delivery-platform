from collections.abc import Sequence
from datetime import datetime, timedelta, timezone

from app.payment.models.payment import Payment
from app.payment.schemas import (
    PaymentHistoryResponse,
    PaymentInitiationResponse,
    PaymentMethod,
    PaymentResponse,
    PaymentStatusResponse,
    PaymentStatusView,
)
from app.shared.enums import PaymentStatus

PAYMENT_SESSION_TTL_MINUTES = 15


def to_api_payment_method(payment_method: str) -> PaymentMethod:
    if payment_method == "COD":
        return "COD"

    return "ONLINE"


def to_storage_payment_method(payment_method: PaymentMethod) -> str:
    if payment_method == "COD":
        return "COD"

    return payment_method


def to_api_payment_status(payment_status: PaymentStatus) -> PaymentStatusView:
    status_map: dict[PaymentStatus, PaymentStatusView] = {
        PaymentStatus.INITIATED: "PENDING",
        PaymentStatus.PROCESSING: "PROCESSING",
        PaymentStatus.SUCCESS: "COMPLETED",
        PaymentStatus.FAILED: "FAILED",
    }

    return status_map[payment_status]


def build_payment_url(payment: Payment) -> str | None:
    if payment.payment_method == "COD":
        return None

    return f"https://payment-gateway.example/session/{payment.payment_reference}"


def build_expires_at(payment: Payment) -> datetime | None:
    if payment.payment_method == "COD":
        return None

    created_at = payment.created_at

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    return created_at + timedelta(minutes=PAYMENT_SESSION_TTL_MINUTES)


def to_initiation_response(payment: Payment) -> PaymentInitiationResponse:
    return PaymentInitiationResponse(
        payment_id=payment.payment_id,
        order_id=payment.order_id,
        payment_method=to_api_payment_method(payment.payment_method),
        payment_status=to_api_payment_status(payment.payment_status),
        payment_url=build_payment_url(payment),
        expires_at=build_expires_at(payment),
    )


def to_status_response(payment: Payment) -> PaymentStatusResponse:
    return PaymentStatusResponse(
        payment_id=payment.payment_id,
        order_id=payment.order_id,
        payment_method=to_api_payment_method(payment.payment_method),
        payment_status=to_api_payment_status(payment.payment_status),
        paid_at=payment.paid_at,
    )


def to_response(payment: Payment) -> PaymentResponse:
    return PaymentResponse(
        payment_id=payment.payment_id,
        order_id=payment.order_id,
        payment_method=to_api_payment_method(payment.payment_method),
        payment_status=to_api_payment_status(payment.payment_status),
        paid_at=payment.paid_at,
        payment_reference=payment.payment_reference,
        payment_gateway=payment.payment_gateway,
        gateway_transaction_id=payment.gateway_transaction_id,
        amount=payment.amount,
        failure_reason=payment.failure_reason,
        created_at=payment.created_at,
    )


def to_history_response(
    payments: Sequence[Payment],
) -> PaymentHistoryResponse:
    return PaymentHistoryResponse(
        payments=[to_response(payment) for payment in payments],
    )
