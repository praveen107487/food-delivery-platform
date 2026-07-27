from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.notification.exceptions import (
    NotificationNotFoundException,
    NotificationOwnershipException,
)
from app.notification.mapper import NotificationMapper
from app.notification.models.notification import Notification
from app.notification.repository import NotificationRepository
from app.notification.schemas import (
    MarkAllNotificationsReadResponse,
    NotificationListResponse,
    NotificationResponse,
    UpdateNotificationRequest,
)
from app.shared.enums import NotificationType


class NotificationService:
    def __init__(
        self,
        repository: NotificationRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._mapper = NotificationMapper()
        self._session = session

    async def _get_owned_notification(
        self,
        customer_id: UUID,
        notification_id: UUID,
    ) -> Notification:
        notification = await self._repository.get_by_id(
            notification_id,
        )

        if notification is None:
            raise NotificationNotFoundException()

        if notification.customer_id != customer_id:
            raise NotificationOwnershipException()

        return notification

    async def list_notifications(
        self,
        customer_id: UUID,
        page: int = 1,
        page_size: int = 20,
        is_read: bool | None = None,
        notification_type: NotificationType | None = None,
    ) -> NotificationListResponse:
        notifications, total_count = await self._repository.list_notifications(
            customer_id,
            page=page,
            page_size=page_size,
            is_read=is_read,
            notification_type=notification_type,
        )

        return NotificationListResponse(
            notifications=[
                self._mapper.to_notification_response(notification)
                for notification in notifications
            ],
            total_count=total_count,
            page=page,
            page_size=page_size,
        )

    async def get_notification(
        self,
        customer_id: UUID,
        notification_id: UUID,
    ) -> NotificationResponse:
        notification = await self._get_owned_notification(
            customer_id,
            notification_id,
        )

        return self._mapper.to_notification_response(
            notification,
        )

    async def mark_as_read(
        self,
        customer_id: UUID,
        notification_id: UUID,
    ) -> NotificationResponse:
        notification = await self._get_owned_notification(
            customer_id,
            notification_id,
        )

        if notification.is_read:
            return self._mapper.to_notification_response(
                notification,
            )

        request = UpdateNotificationRequest(
            is_read=True,
        )

        self._mapper.apply_notification_update(
            notification,
            request,
        )

        await self._repository.update(
            notification,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                notification,
            )

            return self._mapper.to_notification_response(
                notification,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def mark_all_as_read(
        self,
        customer_id: UUID,
    ) -> MarkAllNotificationsReadResponse:
        await self._repository.mark_all_as_read(
            customer_id,
        )

        try:
            await self._session.commit()

            return MarkAllNotificationsReadResponse(
                message="All notifications marked as read.",
            )

        except Exception:
            await self._session.rollback()
            raise
