import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from app.infrastructure.database import Base
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.review.models.restaurant_review import RestaurantReview


class RestaurantReviewImage(Base):
    __tablename__ = "restaurant_review_images"

    image_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("restaurant_reviews.review_id"),
        nullable=False,
    )

    image_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    review: Mapped["RestaurantReview"] = relationship(
        back_populates="images",
        lazy="selectin",
    )
