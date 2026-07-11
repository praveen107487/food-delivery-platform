from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthenticationRepository
from app.auth.service import AuthenticationService
from app.customer.models.customer import Customer
from app.infrastructure.database.dependencies import get_db

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_authentication_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AuthenticationRepository:
    return AuthenticationRepository(session)


def get_authentication_service(
    repository: Annotated[
        AuthenticationRepository,
        Depends(get_authentication_repository),
    ],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AuthenticationService:

    return AuthenticationService(
        repository=repository,
        session=session,
    )


async def get_current_customer(
    token: Annotated[str, Depends(oauth2_schema)],
    service: Annotated[
        AuthenticationService,
        Depends(get_authentication_service),
    ],
) -> Customer:
    return await service.get_current_customer(token)
