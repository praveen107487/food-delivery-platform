import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.cart.models.cart_item import CartItem
    from app.order.models.order_item import OrderItem
    from app.restaurant.models.restaurant import Restaurant


class MenuItem(TimestampMixin, Base):
    __tablename__ = "menu_items"

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="ck_menu_items_price_non_negative",
        ),
        CheckConstraint(
            "preparation_time > 0",
            name="ck_menu_items_preparation_time_positive",
        ),
        CheckConstraint(
            "name <> ''",
            name="ck_menu_items_name_not_empty",
        ),
        CheckConstraint(
            "category <> ''",
            name="ck_menu_items_category_not_empty",
        ),
        Index(
            "ix_menu_items_restaurant_id",
            "restaurant_id",
        ),
        Index(
            "ix_menu_items_category",
            "category",
        ),
        Index(
            "ix_menu_items_is_available",
            "is_available",
        ),
        Index(
            "ix_menu_items_name",
            "name",
        ),
    )

    menu_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.restaurant_id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    preparation_time: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="menu_items",
        lazy="selectin",
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="menu_item",
        lazy="selectin",
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="menu_item",
        lazy="selectin",
    )
