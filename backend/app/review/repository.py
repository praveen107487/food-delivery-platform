from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models.order import Order
from app.order.models.order_item import OrderItem
from app.review.models.food_item_review import FoodItemReview
from app.review.models.food_item_review_image import FoodItemReviewImage
from app.review.models.restaurant_review import RestaurantReview
from app.review.models.restaurant_review_image import RestaurantReviewImage


class ReviewRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create_restaurant_review(
        self,
        review: RestaurantReview,
    ) -> RestaurantReview:
        self._session.add(review)
        await self._session.flush()
        return review

    async def get_restaurant_review(
        self,
        review_id: UUID,
    ) -> RestaurantReview | None:
        statement: Select[tuple[RestaurantReview]] = select(RestaurantReview).where(
            RestaurantReview.review_id == review_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_restaurant_review_by_order(
        self,
        order_id: UUID,
    ) -> RestaurantReview | None:
        statement: Select[tuple[RestaurantReview]] = select(RestaurantReview).where(
            RestaurantReview.order_id == order_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def update_restaurant_review(
        self,
        review: RestaurantReview,
    ) -> RestaurantReview:
        await self._session.flush()
        return review

    async def delete_restaurant_review(
        self,
        review: RestaurantReview,
    ) -> None:
        await self._session.delete(review)
        await self._session.flush()

    async def list_restaurant_reviews(
        self,
        restaurant_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[RestaurantReview], int]:
        offset = (page - 1) * page_size

        statement: Select[tuple[RestaurantReview]] = (
            select(RestaurantReview)
            .join(Order)
            .where(
                Order.restaurant_id == restaurant_id,
            )
            .order_by(
                RestaurantReview.created_at.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        result = await self._session.execute(statement)

        count_statement = (
            select(func.count(RestaurantReview.review_id))
            .select_from(RestaurantReview)
            .join(Order)
            .where(
                Order.restaurant_id == restaurant_id,
            )
        )

        count_result = await self._session.execute(count_statement)
        total_count = count_result.scalar_one()

        return list(result.scalars().all()), total_count

    async def create_food_item_review(
        self,
        review: FoodItemReview,
    ) -> FoodItemReview:
        self._session.add(review)
        await self._session.flush()
        return review

    async def get_food_item_review(
        self,
        review_id: UUID,
    ) -> FoodItemReview | None:
        statement: Select[tuple[FoodItemReview]] = select(FoodItemReview).where(
            FoodItemReview.review_id == review_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_food_item_review_by_order_item(
        self,
        order_item_id: UUID,
    ) -> FoodItemReview | None:
        statement: Select[tuple[FoodItemReview]] = select(FoodItemReview).where(
            FoodItemReview.order_item_id == order_item_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def update_food_item_review(
        self,
        review: FoodItemReview,
    ) -> FoodItemReview:
        await self._session.flush()
        return review

    async def delete_food_item_review(
        self,
        review: FoodItemReview,
    ) -> None:
        await self._session.delete(review)
        await self._session.flush()

    async def list_food_item_reviews(
        self,
        menu_item_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[FoodItemReview], int]:
        offset = (page - 1) * page_size

        statement: Select[tuple[FoodItemReview]] = (
            select(FoodItemReview)
            .join(OrderItem)
            .where(
                OrderItem.menu_item_id == menu_item_id,
            )
            .order_by(
                FoodItemReview.created_at.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        result = await self._session.execute(statement)

        count_statement = (
            select(func.count(FoodItemReview.review_id))
            .select_from(FoodItemReview)
            .join(OrderItem)
            .where(
                OrderItem.menu_item_id == menu_item_id,
            )
        )

        count_result = await self._session.execute(count_statement)
        total_count = count_result.scalar_one()

        return list(result.scalars().all()), total_count

    async def create_restaurant_review_image(
        self,
        image: RestaurantReviewImage,
    ) -> RestaurantReviewImage:
        self._session.add(image)
        await self._session.flush()
        return image

    async def get_restaurant_review_image(
        self,
        image_id: UUID,
    ) -> RestaurantReviewImage | None:
        statement: Select[tuple[RestaurantReviewImage]] = select(
            RestaurantReviewImage
        ).where(
            RestaurantReviewImage.image_id == image_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def list_restaurant_review_images(
        self,
        review_id: UUID,
    ) -> list[RestaurantReviewImage]:
        statement: Select[tuple[RestaurantReviewImage]] = (
            select(RestaurantReviewImage)
            .where(
                RestaurantReviewImage.review_id == review_id,
            )
            .order_by(
                RestaurantReviewImage.uploaded_at.asc(),
            )
        )
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def delete_restaurant_review_image(
        self,
        image: RestaurantReviewImage,
    ) -> None:
        await self._session.delete(image)
        await self._session.flush()

    async def create_food_item_review_image(
        self,
        image: FoodItemReviewImage,
    ) -> FoodItemReviewImage:
        self._session.add(image)
        await self._session.flush()
        return image

    async def get_food_item_review_image(
        self,
        image_id: UUID,
    ) -> FoodItemReviewImage | None:
        statement: Select[tuple[FoodItemReviewImage]] = select(
            FoodItemReviewImage
        ).where(
            FoodItemReviewImage.image_id == image_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def list_food_item_review_images(
        self,
        review_id: UUID,
    ) -> list[FoodItemReviewImage]:
        statement: Select[tuple[FoodItemReviewImage]] = (
            select(FoodItemReviewImage)
            .where(
                FoodItemReviewImage.review_id == review_id,
            )
            .order_by(
                FoodItemReviewImage.uploaded_at.asc(),
            )
        )
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def delete_food_item_review_image(
        self,
        image: FoodItemReviewImage,
    ) -> None:
        await self._session.delete(image)
        await self._session.flush()
