import uuid
from datetime import time
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Numeric, String, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.cart.models.cart import Cart
    from app.coupon.models.restaurant_coupon import RestaurantCoupon
    from app.order.models.order import Order
    from app.restaurant.models.menu_item import MenuItem


class Restaurant(TimestampMixin, Base):
    __tablename__ = "restaurants"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    restaurant_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    street: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    cuisine_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    opening_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    closing_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    average_rating: Mapped[Decimal | None] = mapped_column(
        Numeric(2, 1),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    menu_items: Mapped[list["MenuItem"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    carts: Mapped[list["Cart"]] = relationship(
        back_populates="restaurant",
        lazy="selectin",
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="restaurant",
        lazy="selectin",
    )

    restaurant_coupons: Mapped[list["RestaurantCoupon"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
