from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.coupon.models.platform_coupon import PlatformCoupon
from app.coupon.models.restaurant_coupon import RestaurantCoupon


class CouponRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_platform_coupon_by_code(
        self,
        coupon_code: str,
    ) -> PlatformCoupon | None:
        statement = select(PlatformCoupon).where(
            PlatformCoupon.coupon_code == coupon_code
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_restaurant_coupon_by_code(
        self,
        coupon_code: str,
    ) -> RestaurantCoupon | None:
        statement = select(RestaurantCoupon).where(
            RestaurantCoupon.coupon_code == coupon_code
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_coupon_by_code(
        self,
        coupon_code: str,
    ) -> PlatformCoupon | RestaurantCoupon | None:
        platform_coupon = await self.get_platform_coupon_by_code(coupon_code)

        if platform_coupon is not None:
            return platform_coupon

        return await self.get_restaurant_coupon_by_code(coupon_code)
