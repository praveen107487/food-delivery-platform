from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RestaurantReviewBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )
    description: str = Field(
        min_length=1,
        max_length=2000,
    )
    restaurant_rating: int = Field(
        ge=1,
        le=5,
    )
    delivery_rating: int = Field(
        ge=1,
        le=5,
    )


class CreateRestaurantReviewRequest(
    RestaurantReviewBase,
):
    order_id: UUID


class UpdateRestaurantReviewRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
    )
    restaurant_rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )
    delivery_rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )


class RestaurantReviewResponse(
    RestaurantReviewBase,
):
    model_config = ConfigDict(
        from_attributes=True,
    )

    review_id: UUID
    order_id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime


class RestaurantReviewListResponse(BaseModel):
    reviews: list[RestaurantReviewResponse]
    total_count: int
    page: int
    page_size: int


class FoodItemReviewBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )
    description: str = Field(
        min_length=1,
        max_length=2000,
    )
    rating: int = Field(
        ge=1,
        le=5,
    )


class CreateFoodItemReviewRequest(
    FoodItemReviewBase,
):
    order_item_id: UUID


class UpdateFoodItemReviewRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
    )
    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )


class FoodItemReviewResponse(
    FoodItemReviewBase,
):
    model_config = ConfigDict(
        from_attributes=True,
    )

    review_id: UUID
    order_item_id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime


class FoodItemReviewListResponse(BaseModel):
    reviews: list[FoodItemReviewResponse]
    total_count: int
    page: int
    page_size: int


class ReviewImageResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    image_id: UUID
    review_id: UUID
    image_url: str
    uploaded_at: datetime


class UploadReviewImageResponse(
    ReviewImageResponse,
):
    pass
