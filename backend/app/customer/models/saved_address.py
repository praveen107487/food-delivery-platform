import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.customer.models.customer import Customer


class SavedAddress(TimestampMixin, Base):
    __tablename__ = "saved_addresses"

    __table_args__ = (
        CheckConstraint(
            "recipient_name <> ''",
            name="ck_saved_addresses_recipient_name_not_empty",
        ),
        CheckConstraint(
            "street <> ''",
            name="ck_saved_addresses_street_not_empty",
        ),
        CheckConstraint(
            "city <> ''",
            name="ck_saved_addresses_city_not_empty",
        ),
        CheckConstraint(
            "state <> ''",
            name="ck_saved_addresses_state_not_empty",
        ),
        CheckConstraint(
            "postal_code <> ''",
            name="ck_saved_addresses_postal_code_not_empty",
        ),
        Index(
            "ix_saved_addresses_customer_id",
            "customer_id",
        ),
        Index(
            "ix_saved_addresses_customer_default",
            "customer_id",
            "is_default",
        ),
    )

    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(50),
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

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="saved_addresses",
        lazy="selectin",
    )
