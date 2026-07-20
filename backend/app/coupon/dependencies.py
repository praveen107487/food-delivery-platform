from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.coupon.repository import CouponRepository
from app.coupon.service import CouponService
from app.infrastructure.database.dependencies import get_db


def get_coupon_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> CouponRepository:
    return CouponRepository(session)


def get_coupon_service(
    repository: Annotated[
        CouponRepository,
        Depends(get_coupon_repository),
    ],
) -> CouponService:
    return CouponService(repository)
