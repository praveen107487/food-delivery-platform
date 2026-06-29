import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.cart.models.cart import Cart
    from app.restaurant.models.menu_item import MenuItem


class CartItem(TimestampMixin, Base):
    __tablename__ = "cart_items"

    cart_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("carts.cart_id"),
        nullable=False,
    )

    menu_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.menu_item_id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_cart_items_quantity_positive",
        ),
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_cart_items_quantity_positive",
        ),
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="cart_items",
        lazy="selectin",
    )

    menu_item: Mapped["MenuItem"] = relationship(
        back_populates="cart_items",
        lazy="selectin",
    )
