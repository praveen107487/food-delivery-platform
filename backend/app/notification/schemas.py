from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.shared.enums import NotificationType


class CreateNotificationRequest(BaseModel):
    type: NotificationType
    title: str = Field(
        min_length=1,
        max_length=255,
    )
    message: str = Field(
        min_length=1,
    )


class UpdateNotificationRequest(BaseModel):
    is_read: bool | None = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    notification_id: UUID
    customer_id: UUID
    type: NotificationType
    title: str
    message: str
    is_read: bool
    created_at: datetime


class NotificationListResponse(BaseModel):
    notifications: list[NotificationResponse]
    total_count: int
    page: int
    page_size: int


class MarkAllNotificationsReadResponse(BaseModel):
    message: str
