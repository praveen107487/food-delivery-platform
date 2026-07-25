from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.dependencies import get_current_customer
from app.customer.models import Customer
from app.order.dependencies import get_order_service
from app.order.exceptions import (
    ActiveCartNotFoundError,
    ActiveOrderNotFoundError,
    CheckoutValidationError,
    EmptyCartError,
    OrderNotFoundError,
)
from app.order.schemas import (
    CheckoutRequest,
    OrderDetailsResponse,
    OrderSummaryResponse,
)
from app.order.service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderDetailsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def place_order(
    request: CheckoutRequest,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
) -> OrderDetailsResponse:
    try:
        order = await service.checkout(
            customer_id=current_customer.customer_id,
            request=request,
        )
        return order
    except ActiveCartNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cart found.",
        ) from exc
    except EmptyCartError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot place an order with an empty cart.",
        ) from exc
    except CheckoutValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/current",
    response_model=OrderSummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_current_order(
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
) -> OrderSummaryResponse:
    try:
        order = await service.get_current_order(
            customer_id=current_customer.customer_id,
        )
        return order
    except ActiveOrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active order found.",
        ) from exc


@router.get(
    "/{order_id}",
    response_model=OrderDetailsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order(
    order_id: UUID,
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
) -> OrderDetailsResponse:
    try:
        order = await service.get_order(
            customer_id=current_customer.customer_id,
            order_id=order_id,
        )
        return order
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        ) from exc


@router.get(
    "/history",
    response_model=list[OrderSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_order_history(
    current_customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
    service: Annotated[
        OrderService,
        Depends(get_order_service),
    ],
    page: int = Query(ge=1, default=1),
    page_size: int = Query(ge=1, le=100, default=20),
) -> list[OrderSummaryResponse]:
    orders = await service.list_orders(
        customer_id=current_customer.customer_id,
        page=page,
        page_size=page_size,
    )
    return list(orders)
