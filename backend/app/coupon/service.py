from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from app.coupon.exceptions import (
    CouponExpiredException,
    CouponInactiveException,
    CouponNotFoundException,
    CouponNotYetActiveException,
    MinimumOrderAmountNotMetException,
    RestaurantCouponMismatchException,
)
from app.coupon.models.platform_coupon import PlatformCoupon
from app.coupon.models.restaurant_coupon import RestaurantCoupon
from app.coupon.repository import CouponRepository
from app.shared.enums import CouponStatus, DiscountType

type Coupon = PlatformCoupon | RestaurantCoupon


class CouponService:
    def __init__(
        self,
        repository: CouponRepository,
    ) -> None:
        self._repository = repository

    async def validate_coupon(
        self,
        coupon_code: str,
        restaurant_id: UUID,
        subtotal: Decimal,
    ) -> Coupon:
        coupon = await self._repository.get_coupon_by_code(coupon_code)

        if coupon is None:
            raise CouponNotFoundException()

        if coupon.status != CouponStatus.ACTIVE:
            raise CouponInactiveException()

        now = datetime.now(timezone.utc)

        if now < coupon.valid_from:
            raise CouponNotYetActiveException()

        if now > coupon.valid_until:
            raise CouponExpiredException()

        if subtotal < coupon.minimum_order_amount:
            raise MinimumOrderAmountNotMetException()

        if (
            isinstance(coupon, RestaurantCoupon)
            and coupon.restaurant_id != restaurant_id
        ):
            raise RestaurantCouponMismatchException()

        return coupon

    def calculate_discount(
        self,
        coupon: Coupon,
        subtotal: Decimal,
    ) -> Decimal:
        if coupon.discount_type == DiscountType.PERCENTAGE:
            discount = (subtotal * coupon.discount_value) / Decimal("100")
        else:
            discount = coupon.discount_value

        discount = max(Decimal("0.00"), discount)
        discount = min(discount, subtotal)

        return discount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
