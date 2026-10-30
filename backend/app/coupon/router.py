from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_customer
from app.coupon.dependencies import get_coupon_service
from app.coupon.exceptions import (
    CouponExpiredException,
    CouponInactiveException,
    CouponNotFoundException,
    CouponNotYetActiveException,
    MinimumOrderAmountNotMetException,
    RestaurantCouponMismatchException,
)
from app.coupon.schemas import (
    CouponDetails,
    PlatformCouponDetails,
    RestaurantCouponDetails,
)
from app.coupon.service import CouponService
from app.customer.models.customer import Customer

router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"],
)


@router.get(
    "/validate",
    response_model=CouponDetails,
    status_code=status.HTTP_200_OK,
    summary="Validate a coupon code",
)
async def validate_coupon(
    coupon_code: str,
    restaurant_id: UUID,
    subtotal: float,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CouponService,
        Depends(get_coupon_service),
    ],
) -> CouponDetails:
    try:
        from decimal import Decimal

        coupon = await service.validate_coupon(
            coupon_code=coupon_code,
            restaurant_id=restaurant_id,
            subtotal=Decimal(str(subtotal)),
        )

        if hasattr(coupon, "restaurant_id"):
            return RestaurantCouponDetails.model_validate(coupon)
        return PlatformCouponDetails.model_validate(coupon)

    except CouponNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found.",
        ) from exc
    except CouponInactiveException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon is inactive.",
        ) from exc
    except CouponExpiredException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon has expired.",
        ) from exc
    except CouponNotYetActiveException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon is not yet active.",
        ) from exc
    except MinimumOrderAmountNotMetException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum order amount not met for this coupon.",
        ) from exc
    except RestaurantCouponMismatchException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon is not valid for this restaurant.",
        ) from exc
