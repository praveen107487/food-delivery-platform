from __future__ import annotations

from uuid import UUID

from app.notification.models.notification import Notification
from app.notification.schemas import (
    CreateNotificationRequest,
    NotificationResponse,
    UpdateNotificationRequest,
)


class NotificationMapper:
    @staticmethod
    def to_notification(
        request: CreateNotificationRequest,
        customer_id: UUID,
    ) -> Notification:
        return Notification(
            customer_id=customer_id,
            **request.model_dump(),
        )

    @staticmethod
    def apply_notification_update(
        notification: Notification,
        request: UpdateNotificationRequest,
    ) -> Notification:
        updates = request.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(notification, field, value)

        return notification

    @staticmethod
    def to_notification_response(
        notification: Notification,
    ) -> NotificationResponse:
        return NotificationResponse.model_validate(notification)
