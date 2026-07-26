from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)

from app.auth.dependencies import get_current_customer
from app.review.dependencies import get_review_service
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
from app.review.service import ReviewService

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "/restaurants",
    response_model=RestaurantReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_restaurant_review(
    request: CreateRestaurantReviewRequest,
    customer_id: UUID = Depends(
        get_current_customer,
    ),
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> RestaurantReviewResponse:
    return await service.create_restaurant_review(
        customer_id=customer_id,
        request=request,
    )


@router.patch(
    "/restaurants/{review_id}",
    response_model=RestaurantReviewResponse,
)
async def update_restaurant_review(
    review_id: UUID,
    request: UpdateRestaurantReviewRequest,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> RestaurantReviewResponse:
    return await service.update_restaurant_review(
        review_id=review_id,
        request=request,
    )


@router.delete(
    "/restaurants/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_restaurant_review(
    review_id: UUID,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> None:
    await service.delete_restaurant_review(
        review_id,
    )


@router.get(
    "/restaurants/{restaurant_id}",
    response_model=RestaurantReviewListResponse,
)
async def list_restaurant_reviews(
    restaurant_id: UUID,
    page: int = Query(
        1,
        ge=1,
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
    ),
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> RestaurantReviewListResponse:
    return await service.list_restaurant_reviews(
        restaurant_id=restaurant_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/food-items",
    response_model=FoodItemReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_food_item_review(
    request: CreateFoodItemReviewRequest,
    customer_id: UUID = Depends(
        get_current_customer,
    ),
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> FoodItemReviewResponse:
    return await service.create_food_item_review(
        customer_id=customer_id,
        request=request,
    )


@router.patch(
    "/food-items/{review_id}",
    response_model=FoodItemReviewResponse,
)
async def update_food_item_review(
    review_id: UUID,
    request: UpdateFoodItemReviewRequest,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> FoodItemReviewResponse:
    return await service.update_food_item_review(
        review_id=review_id,
        request=request,
    )


@router.delete(
    "/food-items/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_food_item_review(
    review_id: UUID,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> None:
    await service.delete_food_item_review(
        review_id,
    )


@router.get(
    "/food-items/{menu_item_id}",
    response_model=FoodItemReviewListResponse,
)
async def list_food_item_reviews(
    menu_item_id: UUID,
    page: int = Query(
        1,
        ge=1,
    ),
    page_size: int = Query(
        20,
        ge=1,
        le=100,
    ),
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> FoodItemReviewListResponse:
    return await service.list_food_item_reviews(
        menu_item_id=menu_item_id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/restaurants/{review_id}/images",
    response_model=ReviewImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_restaurant_review_image(
    review_id: UUID,
    image_url: str,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> ReviewImageResponse:
    return await service.upload_restaurant_review_image(
        review_id=review_id,
        image_url=image_url,
    )


@router.get(
    "/restaurants/{review_id}/images",
    response_model=list[ReviewImageResponse],
)
async def list_restaurant_review_images(
    review_id: UUID,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> list[ReviewImageResponse]:
    return await service.list_restaurant_review_images(
        review_id,
    )


@router.delete(
    "/restaurants/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_restaurant_review_image(
    image_id: UUID,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> None:
    await service.delete_restaurant_review_image(
        image_id,
    )


@router.post(
    "/food-items/{review_id}/images",
    response_model=ReviewImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_food_item_review_image(
    review_id: UUID,
    image_url: str,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> ReviewImageResponse:
    return await service.upload_food_item_review_image(
        review_id=review_id,
        image_url=image_url,
    )


@router.get(
    "/food-items/{review_id}/images",
    response_model=list[ReviewImageResponse],
)
async def list_food_item_review_images(
    review_id: UUID,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> list[ReviewImageResponse]:
    return await service.list_food_item_review_images(
        review_id,
    )


@router.delete(
    "/food-items/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_food_item_review_image(
    image_id: UUID,
    service: ReviewService = Depends(
        get_review_service,
    ),
) -> None:
    await service.delete_food_item_review_image(
        image_id,
    )
