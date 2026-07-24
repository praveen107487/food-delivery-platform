from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.shared.enums import PaymentStatus


class PaymentCreateRequest(BaseModel):
    payment_method: str = Field(
        ...,
        examples=["ONLINE"],
    )


class PaymentRetryRequest(BaseModel):
    payment_method: str = Field(
        ...,
        examples=["ONLINE"],
    )


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_id: UUID
    payment_reference: str
    order_id: UUID

    payment_method: str
    payment_gateway: str | None
    gateway_transaction_id: str | None

    amount: Decimal

    payment_status: PaymentStatus

    paid_at: datetime | None

    failure_reason: str | None

    created_at: datetime


class PaymentHistoryResponse(BaseModel):
    payments: list[PaymentResponse]
