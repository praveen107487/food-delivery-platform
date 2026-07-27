from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dependencies import get_db
from app.notification.repository import NotificationRepository
from app.notification.service import NotificationService


def get_notification_repository(
    session: AsyncSession = Depends(get_db),
) -> NotificationRepository:
    return NotificationRepository(
        session=session,
    )


def get_notification_service(
    repository: NotificationRepository = Depends(
        get_notification_repository,
    ),
    session: AsyncSession = Depends(get_db),
) -> NotificationService:
    return NotificationService(
        repository=repository,
        session=session,
    )
