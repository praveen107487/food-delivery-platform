import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin

if TYPE_CHECKING:
    from app.customer.models.customer import Customer
    from app.order.models.order import Order
    from app.review.models.restaurant_review_image import (
        RestaurantReviewImage,
    )


class RestaurantReview(TimestampMixin, Base):
    __tablename__ = "restaurant_reviews"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.order_id"),
        nullable=False,
        unique=True,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        default=None,
    )

    restaurant_rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    delivery_rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "restaurant_rating BETWEEN 1 AND 5",
            name="ck_restaurant_reviews_restaurant_rating",
        ),
        CheckConstraint(
            "delivery_rating BETWEEN 1 AND 5",
            name="ck_restaurant_reviews_delivery_rating",
        ),
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="restaurant_reviews",
        lazy="selectin",
    )

    order: Mapped["Order"] = relationship(
        back_populates="restaurant_review",
        lazy="selectin",
    )

    images: Mapped[list["RestaurantReviewImage"]] = relationship(
        back_populates="review",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
