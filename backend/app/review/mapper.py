from uuid import UUID

from app.review.models.food_item_review import FoodItemReview
from app.review.models.food_item_review_image import FoodItemReviewImage
from app.review.models.restaurant_review import RestaurantReview
from app.review.models.restaurant_review_image import RestaurantReviewImage
from app.review.schemas import (
    CreateFoodItemReviewRequest,
    CreateRestaurantReviewRequest,
    FoodItemReviewResponse,
    RestaurantReviewResponse,
    ReviewImageResponse,
    UpdateFoodItemReviewRequest,
    UpdateRestaurantReviewRequest,
)


class ReviewMapper:
    def to_restaurant_review(
        self,
        request: CreateRestaurantReviewRequest,
        customer_id: UUID,
    ) -> RestaurantReview:
        return RestaurantReview(
            order_id=request.order_id,
            customer_id=customer_id,
            title=request.title,
            description=request.description,
            restaurant_rating=request.restaurant_rating,
            delivery_rating=request.delivery_rating,
        )

    def apply_restaurant_review_update(
        self,
        review: RestaurantReview,
        request: UpdateRestaurantReviewRequest,
    ) -> None:
        if request.title is not None:
            review.title = request.title

        if request.description is not None:
            review.description = request.description

        if request.restaurant_rating is not None:
            review.restaurant_rating = request.restaurant_rating

        if request.delivery_rating is not None:
            review.delivery_rating = request.delivery_rating

    def to_restaurant_review_response(
        self,
        review: RestaurantReview,
    ) -> RestaurantReviewResponse:
        return RestaurantReviewResponse.model_validate(
            review,
        )

    def to_food_item_review(
        self,
        request: CreateFoodItemReviewRequest,
        customer_id: UUID,
    ) -> FoodItemReview:
        return FoodItemReview(
            order_item_id=request.order_item_id,
            customer_id=customer_id,
            title=request.title,
            description=request.description,
            rating=request.rating,
        )

    def apply_food_item_review_update(
        self,
        review: FoodItemReview,
        request: UpdateFoodItemReviewRequest,
    ) -> None:
        if request.title is not None:
            review.title = request.title

        if request.description is not None:
            review.description = request.description

        if request.rating is not None:
            review.rating = request.rating

    def to_food_item_review_response(
        self,
        review: FoodItemReview,
    ) -> FoodItemReviewResponse:
        return FoodItemReviewResponse.model_validate(
            review,
        )

    def to_review_image_response(
        self,
        image: RestaurantReviewImage | FoodItemReviewImage,
    ) -> ReviewImageResponse:
        return ReviewImageResponse.model_validate(
            image,
        )
