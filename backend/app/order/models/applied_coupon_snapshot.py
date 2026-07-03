import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.order.models.order import Order


class AppliedCouponSnapshot(TimestampMixin, Base):
    __tablename__ = "applied_coupon_snapshots"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        primary_key=True,
        nullable=False,
    )

    coupon_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    coupon_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    discount_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    discount_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    actual_discount_applied: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "discount_value >= 0",
            name="ck_applied_coupon_snapshot_discount_value_non_negative",
        ),
        CheckConstraint(
            "actual_discount_applied >= 0",
            name="ck_applied_coupon_snapshot_actual_discount_non_negative",
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="applied_coupon_snapshot",
        lazy="selectin",
    )
