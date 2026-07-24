import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from app.infrastructure.database import Base
from app.shared.enums import PaymentStatus
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.order.models.order import Order


def generate_payment_reference() -> str:
    return f"PAY-{uuid.uuid4().hex[:12].upper()}"


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    payment_reference: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default=generate_payment_reference,
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

    payment_gateway: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None,
    )

    gateway_transaction_id: Mapped[str | None] = mapped_column(
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

    failure_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_payments_amount_positive",
        ),
        CheckConstraint(
            "payment_method IN ('ONLINE', 'COD')",
            name="ck_payments_payment_method",
        ),
        UniqueConstraint(
            "payment_reference",
            name="uq_payments_payment_reference",
        ),
        UniqueConstraint(
            "gateway_transaction_id",
            name="uq_payments_gateway_transaction_id",
        ),
        Index(
            "ix_payments_order_id",
            "order_id",
        ),
        Index(
            "ix_payments_payment_status",
            "payment_status",
        ),
        Index(
            "ix_payments_created_at",
            "created_at",
        ),
        Index(
            "uq_payments_order_success",
            "order_id",
            unique=True,
            postgresql_where=text("payment_status = 'SUCCESS'"),
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="payments",
        lazy="selectin",
    )
