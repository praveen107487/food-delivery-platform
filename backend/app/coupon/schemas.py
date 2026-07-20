from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.shared.enums.discount_type import DiscountType


class CouponDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    coupon_id: UUID
    coupon_code: str
    discount_type: DiscountType
    discount_value: Decimal
    minimum_order_amount: Decimal
    valid_from: datetime
    valid_until: datetime


class PlatformCouponDetails(CouponDetails):
    pass


class RestaurantCouponDetails(CouponDetails):
    restaurant_id: UUID
