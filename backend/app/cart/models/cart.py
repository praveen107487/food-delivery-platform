import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin
from app.shared.enums import CartStatus

if TYPE_CHECKING:
    from app.cart.models.cart_item import CartItem
    from app.customer.models.customer import Customer
    from app.restaurant.models.restaurant import Restaurant


class Cart(TimestampMixin, Base):
    __tablename__ = "carts"

    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customer_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    status: Mapped[CartStatus] = mapped_column(
        Enum(CartStatus, name="cart_status"),
        nullable=False,
        default=CartStatus.ACTIVE,
    )
    
    customer: Mapped["Customer"] = relationship(
        back_populates="carts",
        lazy="selectin",
    )

    restaurant: Mapped["Restaurant"] = relationship(
        back_populates="carts",
        lazy="selectin",
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
