from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dependencies import get_db
from app.payment.service import PaymentService


def get_payment_service(
    session: AsyncSession = Depends(get_db),
) -> PaymentService:
    return PaymentService(session)


PaymentServiceDependency = Annotated[
    PaymentService,
    Depends(get_payment_service),
]
