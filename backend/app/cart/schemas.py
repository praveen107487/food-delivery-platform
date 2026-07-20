from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AddToCartRequest(BaseModel):
    menu_item_id: UUID
    quantity: int = Field(..., ge=1)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., ge=1)


class ApplyCouponRequest(BaseModel):
    coupon_code: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )


class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cart_item_id: UUID
    menu_item_id: UUID
    menu_item_name: str
    quantity: int = Field(..., ge=1)
    unit_price: Decimal
    total_price: Decimal


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cart_id: UUID
    restaurant_id: UUID
    restaurant_name: str

    applied_coupon_code: str | None

    items: list[CartItemResponse]

    subtotal: Decimal
    discount: Decimal
    total: Decimal
