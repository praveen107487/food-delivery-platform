import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.restaurant.models.restaurant import Restaurant


class MenuItem(TimestampMixin, Base):
    __tablename__ = "menu_items"

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
