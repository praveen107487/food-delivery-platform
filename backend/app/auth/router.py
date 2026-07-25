from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import (
    get_authentication_service,
    get_current_customer,
)
from app.auth.exceptions import EmailAlreadyExistsError, InvalidCredentialsError
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
    try:
        customer = await service.register(request)

        return AuthenticatedCustomerResponse.model_validate(customer)

    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        ) from exc


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
    try:
        return await service.login(request)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc


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


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    customer: Annotated[
        Customer,
        Depends(get_current_customer),
    ],
) -> None:
    # Stateless JWT authentication - logout is client-side
    # Client should discard the JWT token
    return None
