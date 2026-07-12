import uuid
from typing import TYPE_CHECKING

from app.infrastructure.database import Base, TimestampMixin
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.customer.models.customer import Customer
    from app.order.models.order_item import OrderItem
    from app.review.models.food_item_review_image import (
        FoodItemReviewImage,
    )


class FoodItemReview(TimestampMixin, Base):
    __tablename__ = "food_item_reviews"

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order_items.order_item_id"),
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

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="ck_food_item_reviews_rating",
        ),
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="food_item_reviews",
        lazy="selectin",
    )

    order_item: Mapped["OrderItem"] = relationship(
        back_populates="food_item_review",
        lazy="selectin",
    )

    images: Mapped[list["FoodItemReviewImage"]] = relationship(
        back_populates="review",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
