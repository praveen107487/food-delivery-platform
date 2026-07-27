from uuid import UUID

from sqlalchemy import Select, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.notification.models.notification import Notification
from app.shared.enums import NotificationType


class NotificationRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_by_id(
        self,
        notification_id: UUID,
    ) -> Notification | None:
        statement: Select[tuple[Notification]] = select(
            Notification,
        ).where(
            Notification.notification_id == notification_id,
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_id_and_customer(
        self,
        notification_id: UUID,
        customer_id: UUID,
    ) -> Notification | None:
        statement: Select[tuple[Notification]] = select(
            Notification,
        ).where(
            Notification.notification_id == notification_id,
            Notification.customer_id == customer_id,
        )

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def list_notifications(
        self,
        customer_id: UUID,
        page: int = 1,
        page_size: int = 20,
        is_read: bool | None = None,
        notification_type: NotificationType | None = None,
    ) -> tuple[list[Notification], int]:
        offset = (page - 1) * page_size

        statement: Select[tuple[Notification]] = (
            select(Notification)
            .where(
                Notification.customer_id == customer_id,
            )
            .order_by(
                Notification.created_at.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        if is_read is not None:
            statement = statement.where(
                Notification.is_read == is_read,
            )

        if notification_type is not None:
            statement = statement.where(
                Notification.type == notification_type,
            )

        result = await self._session.execute(statement)

        count_statement = select(
            Notification.notification_id,
        ).where(
            Notification.customer_id == customer_id,
        )

        if is_read is not None:
            count_statement = count_statement.where(
                Notification.is_read == is_read,
            )

        if notification_type is not None:
            count_statement = count_statement.where(
                Notification.type == notification_type,
            )

        count_result = await self._session.execute(
            count_statement,
        )

        total_count = len(
            count_result.scalars().all(),
        )

        return list(result.scalars().all()), total_count

    async def create(
        self,
        notification: Notification,
    ) -> Notification:
        self._session.add(notification)

        await self._session.flush()

        return notification

    async def update(
        self,
        notification: Notification,
    ) -> Notification:
        await self._session.flush()

        return notification

    async def mark_all_as_read(
        self,
        customer_id: UUID,
    ) -> None:
        statement = (
            update(Notification)
            .where(
                Notification.customer_id == customer_id,
                Notification.is_read.is_(False),
            )
            .values(
                is_read=True,
            )
        )

        await self._session.execute(statement)

        await self._session.flush()
