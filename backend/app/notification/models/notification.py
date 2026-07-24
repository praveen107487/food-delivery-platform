import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from app.infrastructure.database import Base
from app.shared.enums import NotificationType
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.customer.models.customer import Customer


class Notification(Base):
    __tablename__ = "notifications"

    __table_args__ = (
        Index(
            "ix_notifications_customer_id",
            "customer_id",
        ),
        Index(
            "ix_notifications_is_read",
            "is_read",
        ),
        Index(
            "ix_notifications_created_at",
            "created_at",
        ),
        Index(
            "ix_notifications_customer_is_read",
            "customer_id",
            "is_read",
        ),
    )

    notification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    type: Mapped[NotificationType] = mapped_column(
        Enum(
            NotificationType,
            name="notification_type",
        ),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="notifications",
        lazy="selectin",
    )
