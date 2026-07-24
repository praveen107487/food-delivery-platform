import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.order.models.order import Order
    from app.restaurant.models.menu_item import MenuItem
    from app.review.models.food_item_review import FoodItemReview


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    menu_item_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.menu_item_id"),
        nullable=True,
        default=None,
    )

    food_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_order_items_unit_price_non_negative",
        ),
        CheckConstraint(
            "total_price >= 0",
            name="ck_order_items_total_price_non_negative",
        ),
        Index(
            "ix_order_items_order_id",
            "order_id",
        ),
        Index(
            "ix_order_items_menu_item_id",
            "menu_item_id",
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="order_items",
        lazy="selectin",
    )

    menu_item: Mapped["MenuItem"] = relationship(
        back_populates="order_items",
        lazy="selectin",
    )

    food_item_review: Mapped["FoodItemReview | None"] = relationship(
        back_populates="order_item",
        uselist=False,
        lazy="selectin",
    )
