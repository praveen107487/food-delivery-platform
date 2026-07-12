import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from app.infrastructure.database import Base, TimestampMixin
from app.shared.enums import PaymentStatus
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.order.models.order import Order


class Payment(TimestampMixin, Base):
    __tablename__ = "payments"

    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    payment_method: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    transaction_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        default=None,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.INITIATED,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "amount >= 0",
            name="ck_payments_amount_non_negative",
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="payments",
        lazy="selectin",
    )
