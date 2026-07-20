from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_customer
from app.cart.dependencies import get_cart_service
from app.cart.mapper import map_cart
from app.cart.schemas import (
    ApplyCouponRequest,
    CartResponse,
    UpdateCartItemRequest,
)
from app.cart.service import CartService
from app.customer.models import Customer

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get(
    "",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart(
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    cart = await service.get_cart(
        current_customer.customer_id,
    )

    return map_cart(cart)


@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_to_cart(
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
    menu_item_id: UUID,
    quantity: int = Query(gt=0),
) -> CartResponse:
    cart = await service.add_to_cart(
        customer_id=current_customer.customer_id,
        menu_item_id=menu_item_id,
        quantity=quantity,
    )

    return map_cart(cart)


@router.patch(
    "/items/{cart_item_id}",
    response_model=CartResponse,
)
async def update_cart_item(
    cart_item_id: UUID,
    request: UpdateCartItemRequest,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    cart = await service.update_cart_item(
        customer_id=current_customer.customer_id,
        cart_item_id=cart_item_id,
        quantity=request.quantity,
    )

    return map_cart(cart)


@router.delete(
    "/items/{cart_item_id}",
    response_model=CartResponse,
)
async def remove_cart_item(
    cart_item_id: UUID,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    cart = await service.remove_cart_item(
        customer_id=current_customer.customer_id,
        cart_item_id=cart_item_id,
    )

    return map_cart(cart)


@router.delete(
    "",
    response_model=CartResponse,
)
async def clear_cart(
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    cart = await service.clear_cart(
        current_customer.customer_id,
    )

    return map_cart(cart)


@router.post(
    "/coupon",
    response_model=CartResponse,
)
async def apply_coupon(
    request: ApplyCouponRequest,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    cart = await service.apply_coupon(
        customer_id=current_customer.customer_id,
        coupon_code=request.coupon_code,
    )

    return map_cart(cart)


@router.delete(
    "/coupon",
    response_model=CartResponse,
)
async def remove_coupon(
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    cart = await service.remove_coupon(
        customer_id=current_customer.customer_id,
    )

    return map_cart(cart)
