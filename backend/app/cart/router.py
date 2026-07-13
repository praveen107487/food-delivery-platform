from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_customer
from app.cart.dependencies import get_cart_service
from app.cart.exceptions import (
    CartItemNotFoundException,
    CartNotFoundException,
    CartRestaurantMismatchException,
    MenuItemUnavailableException,
)
from app.cart.mapper import map_cart
from app.cart.schemas import (
    AddToCartRequest,
    CartResponse,
    UpdateCartItemRequest,
)
from app.cart.service import CartService
from app.customer.models.customer import Customer

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.get(
    "",
    response_model=CartResponse,
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
    try:
        cart = await service.get_cart(
            current_customer.customer_id,
        )

        return map_cart(cart)

    except CartNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found.",
        ) from exc


@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_cart(
    request: AddToCartRequest,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        CartService,
        Depends(get_cart_service),
    ],
) -> CartResponse:
    try:
        cart = await service.add_to_cart(
            customer_id=current_customer.customer_id,
            menu_item_id=request.menu_item_id,
            quantity=request.quantity,
        )

        return map_cart(cart)

    except MenuItemUnavailableException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found or unavailable.",
        ) from exc

    except CartRestaurantMismatchException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Your cart already contains items from another restaurant. "
                "Clear your cart before adding items from a different restaurant."
            ),
        ) from exc


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
    try:
        cart = await service.update_cart_item(
            customer_id=current_customer.customer_id,
            cart_item_id=cart_item_id,
            quantity=request.quantity,
        )

        return map_cart(cart)

    except CartItemNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found.",
        ) from exc

    except CartNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found.",
        ) from exc


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
    try:
        cart = await service.remove_cart_item(
            customer_id=current_customer.customer_id,
            cart_item_id=cart_item_id,
        )

        return map_cart(cart)

    except CartItemNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found.",
        ) from exc

    except CartNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found.",
        ) from exc


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
    try:
        cart = await service.clear_cart(
            current_customer.customer_id,
        )

        return map_cart(cart)

    except CartNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found.",
        ) from exc
