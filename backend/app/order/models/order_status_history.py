import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.database import Base
from app.shared.enums import OrderStatus

if TYPE_CHECKING:
    from app.order.models.order import Order


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    __table_args__ = (
        Index(
            "ix_order_status_history_order_id",
            "order_id",
        ),
        Index(
            "ix_order_status_history_changed_at",
            "changed_at",
        ),
    )

    status_history_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"),
        nullable=False,
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    order: Mapped["Order"] = relationship(
        back_populates="status_history",
        lazy="selectin",
    )
