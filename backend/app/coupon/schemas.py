from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.shared.enums.coupon_status import CouponStatus
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
    status: CouponStatus
    created_at: datetime
    updated_at: datetime


class PlatformCouponDetails(CouponDetails):
    pass


class RestaurantCouponDetails(CouponDetails):
    restaurant_id: UUID
