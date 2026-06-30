import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.order.models.order import Order


class DeliveryAddressSnapshot(TimestampMixin, Base):
    __tablename__ = "delivery_address_snapshots"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        primary_key=True,
        nullable=False,
    )

    recipient_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
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

    delivery_instructions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    __table_args__ = (
        CheckConstraint(
            "recipient_name <> ''",
            name="ck_delivery_address_recipient_name_not_empty",
        ),
        CheckConstraint(
            "street <> ''",
            name="ck_delivery_address_street_not_empty",
        ),
        CheckConstraint(
            "city <> ''",
            name="ck_delivery_address_city_not_empty",
        ),
        CheckConstraint(
            "state <> ''",
            name="ck_delivery_address_state_not_empty",
        ),
        CheckConstraint(
            "postal_code <> ''",
            name="ck_delivery_address_postal_code_not_empty",
        ),
    )

    order: Mapped["Order"] = relationship(
        back_populates="delivery_address_snapshot",
        lazy="selectin",
    )