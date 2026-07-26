from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.review.exceptions import (
    FoodItemReviewAlreadyExistsException,
    FoodItemReviewImageNotFoundException,
    FoodItemReviewNotFoundException,
    RestaurantReviewAlreadyExistsException,
    RestaurantReviewImageNotFoundException,
    RestaurantReviewNotFoundException,
)
from app.review.mapper import ReviewMapper
from app.review.models.food_item_review import FoodItemReview
from app.review.models.food_item_review_image import FoodItemReviewImage
from app.review.models.restaurant_review import RestaurantReview
from app.review.models.restaurant_review_image import RestaurantReviewImage
from app.review.repository import ReviewRepository
from app.review.schemas import (
    CreateFoodItemReviewRequest,
    CreateRestaurantReviewRequest,
    FoodItemReviewListResponse,
    FoodItemReviewResponse,
    RestaurantReviewListResponse,
    RestaurantReviewResponse,
    ReviewImageResponse,
    UpdateFoodItemReviewRequest,
    UpdateRestaurantReviewRequest,
)


class ReviewService:
    def __init__(
        self,
        repository: ReviewRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._session = session
        self._mapper = ReviewMapper()

    async def _get_restaurant_review(
        self,
        review_id: UUID,
    ) -> RestaurantReview:
        review = await self._repository.get_restaurant_review(
            review_id,
        )

        if review is None:
            raise RestaurantReviewNotFoundException()

        return review

    async def _get_food_item_review(
        self,
        review_id: UUID,
    ) -> FoodItemReview:
        review = await self._repository.get_food_item_review(
            review_id,
        )

        if review is None:
            raise FoodItemReviewNotFoundException()

        return review

    async def create_restaurant_review(
        self,
        customer_id: UUID,
        request: CreateRestaurantReviewRequest,
    ) -> RestaurantReviewResponse:
        existing_review = await self._repository.get_restaurant_review_by_order(
            request.order_id,
        )

        if existing_review is not None:
            raise RestaurantReviewAlreadyExistsException()

        review = self._mapper.to_restaurant_review(
            request=request,
            customer_id=customer_id,
        )

        try:
            await self._repository.create_restaurant_review(
                review,
            )

            await self._session.commit()

            await self._session.refresh(
                review,
            )

            return self._mapper.to_restaurant_review_response(
                review,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def update_restaurant_review(
        self,
        review_id: UUID,
        request: UpdateRestaurantReviewRequest,
    ) -> RestaurantReviewResponse:
        review = await self._get_restaurant_review(
            review_id,
        )

        self._mapper.apply_restaurant_review_update(
            review,
            request,
        )

        await self._repository.update_restaurant_review(
            review,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                review,
            )

            return self._mapper.to_restaurant_review_response(
                review,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def delete_restaurant_review(
        self,
        review_id: UUID,
    ) -> None:
        review = await self._get_restaurant_review(
            review_id,
        )

        try:
            await self._repository.delete_restaurant_review(
                review,
            )

            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

    async def list_restaurant_reviews(
        self,
        restaurant_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> RestaurantReviewListResponse:
        reviews, total_count = await self._repository.list_restaurant_reviews(
            restaurant_id=restaurant_id,
            page=page,
            page_size=page_size,
        )

        return RestaurantReviewListResponse(
            reviews=[
                self._mapper.to_restaurant_review_response(
                    review,
                )
                for review in reviews
            ],
            total_count=total_count,
            page=page,
            page_size=page_size,
        )

    async def create_food_item_review(
        self,
        customer_id: UUID,
        request: CreateFoodItemReviewRequest,
    ) -> FoodItemReviewResponse:
        existing_review = await self._repository.get_food_item_review_by_order_item(
            request.order_item_id,
        )

        if existing_review is not None:
            raise FoodItemReviewAlreadyExistsException()

        review = self._mapper.to_food_item_review(
            request=request,
            customer_id=customer_id,
        )

        try:
            await self._repository.create_food_item_review(
                review,
            )

            await self._session.commit()

            await self._session.refresh(
                review,
            )

            return self._mapper.to_food_item_review_response(
                review,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def update_food_item_review(
        self,
        review_id: UUID,
        request: UpdateFoodItemReviewRequest,
    ) -> FoodItemReviewResponse:
        review = await self._get_food_item_review(
            review_id,
        )

        self._mapper.apply_food_item_review_update(
            review,
            request,
        )

        await self._repository.update_food_item_review(
            review,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                review,
            )

            return self._mapper.to_food_item_review_response(
                review,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def delete_food_item_review(
        self,
        review_id: UUID,
    ) -> None:
        review = await self._get_food_item_review(
            review_id,
        )

        try:
            await self._repository.delete_food_item_review(
                review,
            )

            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

    async def list_food_item_reviews(
        self,
        menu_item_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> FoodItemReviewListResponse:
        reviews, total_count = await self._repository.list_food_item_reviews(
            menu_item_id=menu_item_id,
            page=page,
            page_size=page_size,
        )

        return FoodItemReviewListResponse(
            reviews=[
                self._mapper.to_food_item_review_response(
                    review,
                )
                for review in reviews
            ],
            total_count=total_count,
            page=page,
            page_size=page_size,
        )

    async def upload_restaurant_review_image(
        self,
        review_id: UUID,
        image_url: str,
    ) -> ReviewImageResponse:
        await self._get_restaurant_review(
            review_id,
        )

        image = RestaurantReviewImage(
            review_id=review_id,
            image_url=image_url,
        )

        try:
            await self._repository.create_restaurant_review_image(
                image,
            )

            await self._session.commit()

            await self._session.refresh(
                image,
            )

            return self._mapper.to_review_image_response(
                image,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def list_restaurant_review_images(
        self,
        review_id: UUID,
    ) -> list[ReviewImageResponse]:
        await self._get_restaurant_review(
            review_id,
        )

        images = await self._repository.list_restaurant_review_images(
            review_id,
        )

        return [
            self._mapper.to_review_image_response(
                image,
            )
            for image in images
        ]

    async def delete_restaurant_review_image(
        self,
        image_id: UUID,
    ) -> None:
        image = await self._repository.get_restaurant_review_image(
            image_id,
        )

        if image is None:
            raise RestaurantReviewImageNotFoundException()

        try:
            await self._repository.delete_restaurant_review_image(
                image,
            )

            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

    async def upload_food_item_review_image(
        self,
        review_id: UUID,
        image_url: str,
    ) -> ReviewImageResponse:
        await self._get_food_item_review(
            review_id,
        )

        image = FoodItemReviewImage(
            review_id=review_id,
            image_url=image_url,
        )

        try:
            await self._repository.create_food_item_review_image(
                image,
            )

            await self._session.commit()

            await self._session.refresh(
                image,
            )

            return self._mapper.to_review_image_response(
                image,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def list_food_item_review_images(
        self,
        review_id: UUID,
    ) -> list[ReviewImageResponse]:
        await self._get_food_item_review(
            review_id,
        )

        images = await self._repository.list_food_item_review_images(
            review_id,
        )

        return [
            self._mapper.to_review_image_response(
                image,
            )
            for image in images
        ]

    async def delete_food_item_review_image(
        self,
        image_id: UUID,
    ) -> None:
        image = await self._repository.get_food_item_review_image(
            image_id,
        )

        if image is None:
            raise FoodItemReviewImageNotFoundException()

        try:
            await self._repository.delete_food_item_review_image(
                image,
            )

            await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise
