from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_customer
from app.customer.models import Customer
from app.order.exceptions import OrderNotFoundError
from app.payment.dependencies import PaymentServiceDependency
from app.payment.exceptions import (
    PaymentAccessDeniedException,
    PaymentAlreadySuccessfulException,
    PaymentNotEligibleException,
    PaymentNotFoundException,
    PaymentRetryNotAllowedException,
    PaymentVerificationFailedException,
)
from app.payment.schemas import (
    PaymentCreateRequest,
    PaymentInitiationResponse,
    PaymentResponse,
    PaymentRetryRequest,
    PaymentStatusResponse,
    PaymentVerificationRequest,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentInitiationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    request: PaymentCreateRequest,
    service: PaymentServiceDependency,
    current_customer: Annotated[Customer, Depends(get_current_customer)],
) -> PaymentInitiationResponse:
    try:
        return await service.create_payment(
            customer_id=current_customer.customer_id,
            request=request,
        )
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        ) from exc
    except PaymentAccessDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        ) from exc
    except PaymentNotEligibleException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment cannot be initiated for this order.",
        ) from exc
    except PaymentAlreadySuccessfulException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment has already been completed.",
        ) from exc


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_payment(
    payment_id: UUID,
    service: PaymentServiceDependency,
    current_customer: Annotated[Customer, Depends(get_current_customer)],
) -> PaymentResponse:
    try:
        return await service.get_payment_by_id(
            customer_id=current_customer.customer_id,
            payment_id=payment_id,
        )
    except PaymentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        ) from exc
    except PaymentAccessDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        ) from exc


@router.post(
    "/{payment_id}/verify",
    response_model=PaymentStatusResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_payment(
    payment_id: UUID,
    request: PaymentVerificationRequest,
    service: PaymentServiceDependency,
    current_customer: Annotated[Customer, Depends(get_current_customer)],
) -> PaymentStatusResponse:
    try:
        return await service.verify_payment(
            customer_id=current_customer.customer_id,
            payment_id=payment_id,
            request=request,
        )
    except PaymentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        ) from exc
    except PaymentAccessDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        ) from exc
    except PaymentAlreadySuccessfulException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment has already been completed.",
        ) from exc
    except PaymentVerificationFailedException as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payment verification unsuccessful.",
        ) from exc


@router.get(
    "/{payment_id}/status",
    response_model=PaymentStatusResponse,
    status_code=status.HTTP_200_OK,
)
async def get_payment_status(
    payment_id: UUID,
    service: PaymentServiceDependency,
    current_customer: Annotated[Customer, Depends(get_current_customer)],
) -> PaymentStatusResponse:
    try:
        return await service.get_payment_status(
            customer_id=current_customer.customer_id,
            payment_id=payment_id,
        )
    except PaymentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        ) from exc
    except PaymentAccessDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        ) from exc


@router.post(
    "/{payment_id}/retry",
    response_model=PaymentInitiationResponse,
    status_code=status.HTTP_200_OK,
)
async def retry_payment(
    payment_id: UUID,
    request: PaymentRetryRequest,
    service: PaymentServiceDependency,
    current_customer: Annotated[Customer, Depends(get_current_customer)],
) -> PaymentInitiationResponse:
    try:
        return await service.retry_payment(
            customer_id=current_customer.customer_id,
            payment_id=payment_id,
            request=request,
        )
    except PaymentNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        ) from exc
    except PaymentAccessDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        ) from exc
    except PaymentNotEligibleException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment cannot be initiated for this order.",
        ) from exc
    except PaymentRetryNotAllowedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment is not eligible for retry.",
        ) from exc
