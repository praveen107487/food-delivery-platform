import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base, TimestampMixin
from app.shared.enums import CouponStatus, DiscountType


class PlatformCoupon(TimestampMixin, Base):
    __tablename__ = "platform_coupons"

    coupon_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    coupon_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    discount_type: Mapped[DiscountType] = mapped_column(
        Enum(
            DiscountType,
            name="discount_type",
        ),
        nullable=False,
    )

    discount_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    minimum_order_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    valid_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    valid_until: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[CouponStatus] = mapped_column(
        Enum(
            CouponStatus,
            name="coupon_status",
        ),
        nullable=False,
        default=CouponStatus.ACTIVE,
    )

    __table_args__ = (
        CheckConstraint(
            "discount_value >= 0",
            name="ck_platform_coupons_discount_value_non_negative",
        ),
        CheckConstraint(
            "minimum_order_amount >= 0",
            name="ck_platform_coupons_minimum_order_amount_non_negative",
        ),
        CheckConstraint(
            "valid_from < valid_until",
            name="ck_platform_coupons_valid_date_range",
        ),
    )