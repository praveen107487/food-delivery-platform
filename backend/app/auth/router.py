from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import (
    get_authentication_service,
    get_current_customer,
)
from app.auth.schemas import (
    AuthenticatedCustomerResponse,
    CustomerLoginRequest,
    CustomerRegistrationRequest,
    TokenResponse,
)
from app.auth.service import AuthenticationService
from app.customer.models.customer import Customer

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthenticatedCustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: CustomerRegistrationRequest,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
) -> AuthenticatedCustomerResponse:
    return await service.register(request)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: CustomerLoginRequest,
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
) -> TokenResponse:
    return await service.login(request)


@router.get(
    "/me",
    response_model=AuthenticatedCustomerResponse,
    status_code=status.HTTP_200_OK,
)
async def get_me(
    customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
) -> AuthenticatedCustomerResponse:
    return AuthenticatedCustomerResponse.model_validate(customer)
