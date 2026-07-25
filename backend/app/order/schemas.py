from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.shared.enums import OrderStatus


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_item_id: UUID
    menu_item_id: UUID | None
    food_name: str
    unit_price: Decimal
    quantity: int
    total_price: Decimal


class DeliveryAddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recipient_name: str
    phone_number: str
    street: str
    city: str
    state: str
    postal_code: str
    delivery_instructions: str | None


class AppliedCouponResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    coupon_code: str
    coupon_type: str
    discount_type: str
    discount_value: Decimal
    actual_discount_applied: Decimal


class OrderTimelineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: OrderStatus
    changed_at: datetime


class OrderSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: UUID
    order_number: str
    restaurant_name: str

    grand_total: Decimal

    payment_method: str
    current_status: OrderStatus

    created_at: datetime


class OrderDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: UUID
    order_number: str

    customer_id: UUID
    restaurant_id: UUID
    restaurant_name: str

    subtotal: Decimal
    discount_amount: Decimal
    delivery_fee: Decimal
    tax_amount: Decimal
    grand_total: Decimal

    payment_method: str
    current_status: OrderStatus

    confirmed_at: datetime | None
    delivered_at: datetime | None
    cancelled_at: datetime | None

    created_at: datetime
    updated_at: datetime

    order_items: list[OrderItemResponse]

    delivery_address_snapshot: DeliveryAddressResponse

    applied_coupon_snapshot: AppliedCouponResponse | None


class CancelOrderRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    reason: str | None = Field(
        default=None,
        max_length=500,
    )


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    payment_method: str
    delivery_address_id: UUID
    customer_notes: str | None = Field(
        default=None,
        max_length=500,
    )
