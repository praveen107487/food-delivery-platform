from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_customer
from app.customer.models.customer import Customer
from app.notification.dependencies import get_notification_service
from app.notification.schemas import (
    MarkAllNotificationsReadResponse,
    NotificationListResponse,
    NotificationResponse,
)
from app.notification.service import NotificationService
from app.shared.enums import NotificationType

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_notifications(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    is_read: bool | None = Query(
        default=None,
    ),
    notification_type: NotificationType | None = Query(
        default=None,
        alias="type",
    ),
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: NotificationService = Depends(
        get_notification_service,
    ),
) -> NotificationListResponse:
    return await service.list_notifications(
        customer_id=current_customer.customer_id,
        page=page,
        page_size=page_size,
        is_read=is_read,
        notification_type=notification_type,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
async def get_notification(
    notification_id: UUID,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: NotificationService = Depends(
        get_notification_service,
    ),
) -> NotificationResponse:
    return await service.get_notification(
        customer_id=current_customer.customer_id,
        notification_id=notification_id,
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
async def mark_notification_as_read(
    notification_id: UUID,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: NotificationService = Depends(
        get_notification_service,
    ),
) -> NotificationResponse:
    return await service.mark_as_read(
        customer_id=current_customer.customer_id,
        notification_id=notification_id,
    )


@router.patch(
    "/read-all",
    response_model=MarkAllNotificationsReadResponse,
    status_code=status.HTTP_200_OK,
)
async def mark_all_notifications_as_read(
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: NotificationService = Depends(
        get_notification_service,
    ),
) -> MarkAllNotificationsReadResponse:
    return await service.mark_all_as_read(
        customer_id=current_customer.customer_id,
    )
