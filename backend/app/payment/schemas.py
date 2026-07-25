from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

PaymentMethod = Literal["ONLINE", "COD"]
PaymentStatusView = Literal[
    "PENDING",
    "PROCESSING",
    "COMPLETED",
    "FAILED",
    "REFUND_PENDING",
    "REFUNDED",
]


class PaymentCreateRequest(BaseModel):
    order_id: UUID = Field(alias="orderId")
    payment_method: PaymentMethod = Field(alias="paymentMethod")

    model_config = ConfigDict(populate_by_name=True)


class PaymentVerificationRequest(BaseModel):
    gateway_transaction_id: str = Field(
        alias="gatewayTransactionId",
        min_length=1,
        max_length=255,
    )

    model_config = ConfigDict(populate_by_name=True)


class PaymentRetryRequest(BaseModel):
    payment_method: PaymentMethod = Field(
        default="ONLINE",
        alias="paymentMethod",
    )

    model_config = ConfigDict(populate_by_name=True)


class PaymentInitiationResponse(BaseModel):
    payment_id: UUID = Field(alias="paymentId")
    order_id: UUID = Field(alias="orderId")
    payment_method: PaymentMethod = Field(alias="paymentMethod")
    payment_status: PaymentStatusView = Field(alias="paymentStatus")
    payment_url: str | None = Field(alias="paymentUrl")
    expires_at: datetime | None = Field(alias="expiresAt")

    model_config = ConfigDict(populate_by_name=True)


class PaymentStatusResponse(BaseModel):
    payment_id: UUID = Field(alias="paymentId")
    order_id: UUID = Field(alias="orderId")
    payment_method: PaymentMethod = Field(alias="paymentMethod")
    payment_status: PaymentStatusView = Field(alias="paymentStatus")
    paid_at: datetime | None = Field(alias="paidAt")

    model_config = ConfigDict(populate_by_name=True)


class PaymentResponse(PaymentStatusResponse):
    payment_reference: str = Field(alias="paymentReference")
    payment_gateway: str | None = Field(alias="paymentGateway")
    gateway_transaction_id: str | None = Field(alias="gatewayTransactionId")
    amount: Decimal
    failure_reason: str | None = Field(alias="failureReason")
    created_at: datetime = Field(alias="createdAt")


class PaymentHistoryResponse(BaseModel):
    payments: list[PaymentResponse]

    model_config = ConfigDict(populate_by_name=True)
