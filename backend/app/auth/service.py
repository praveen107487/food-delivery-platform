from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.constants import JWT_SUBJECT_CLAIM
from app.auth.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.auth.repository import AuthenticationRepository
from app.auth.schemas import (
    AuthenticatedCustomerResponse,
    CustomerLoginRequest,
    CustomerRegistrationRequest,
    TokenResponse,
)
from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.customer.models.customer import Customer

settings = get_settings()


class AuthenticationService:
    def __init__(
        self,
        session: AsyncSession,
        repository: AuthenticationRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def register(
        self,
        request: CustomerRegistrationRequest,
    ) -> Customer:
        existing_customer = await self._repository.get_by_email(request.email)

        if existing_customer is not None:
            raise EmailAlreadyExistsError()

        customer = Customer(
            email=request.email,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
        )

        try:
            await self._repository.save(customer)
            await self._session.commit()
            await self._session.refresh(customer)

            return customer

        except Exception:
            await self._session.rollback()
            raise

    async def login(
        self,
        request: CustomerLoginRequest,
    ) -> TokenResponse:
        customer = await self._repository.get_by_email(
            request.email,
        )

        if customer is None:
            raise InvalidCredentialsError()

        if not verify_password(
            request.password,
            customer.password_hash,
        ):
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=str(customer.customer_id),
        )

        return TokenResponse(
            access_token=access_token,
            expires_in=settings.jwt_access_token_expire_minutes * 60,
            customer=AuthenticatedCustomerResponse.model_validate(customer),
        )

    async def get_current_customer(
        self,
        token: str,
    ) -> Customer:
        payload = decode_access_token(token)

        customer_id = payload.get(JWT_SUBJECT_CLAIM)

        if customer_id is None:
            raise InvalidTokenError()

        customer = await self._repository.get_by_id(
            UUID(customer_id),
        )

        if customer is None:
            raise InvalidTokenError()

        return customer
