from collections.abc import Sequence

from app.payment.models.payment import Payment
from app.payment.schemas import PaymentHistoryResponse, PaymentResponse


def to_response(payment: Payment) -> PaymentResponse:
    return PaymentResponse.model_validate(payment)


def to_history_response(
    payments: Sequence[Payment],
) -> PaymentHistoryResponse:
    return PaymentHistoryResponse(
        payments=[PaymentResponse.model_validate(payment) for payment in payments]
    )
