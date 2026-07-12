from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.restaurant.dependencies import get_restaurant_service
from app.restaurant.exceptions import RestaurantNotFoundException
from app.restaurant.schemas import (
    MenuItemListResponse,
    MenuItemResponse,
    RestaurantDetailResponse,
    RestaurantListResponse,
    RestaurantSummaryResponse,
)
from app.restaurant.service import RestaurantService

restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)

menu_item_router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"],
)


@restaurant_router.get(
    "",
    response_model=RestaurantListResponse,
    status_code=status.HTTP_200_OK,
    summary="Browse restaurants",
)
async def get_restaurants(
    service: Annotated[
        RestaurantService,
        Depends(get_restaurant_service),
    ],
) -> RestaurantListResponse:
    restaurants = await service.get_restaurants()

    return RestaurantListResponse(
        restaurants=[
            RestaurantSummaryResponse.model_validate(restaurant)
            for restaurant in restaurants
        ],
    )


@restaurant_router.get(
    "/search",
    response_model=RestaurantListResponse,
    status_code=status.HTTP_200_OK,
    summary="Search restaurants",
)
async def search_restaurants(
    keyword: Annotated[
        str,
        Query(
            min_length=1,
            max_length=100,
            description="Search keyword",
        ),
    ],
    service: Annotated[
        RestaurantService,
        Depends(get_restaurant_service),
    ],
) -> RestaurantListResponse:
    restaurants = await service.search_restaurants(keyword)

    return RestaurantListResponse(
        restaurants=[
            RestaurantSummaryResponse.model_validate(restaurant)
            for restaurant in restaurants
        ],
    )


@restaurant_router.get(
    "/{restaurant_id}",
    response_model=RestaurantDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get restaurant details",
)
async def get_restaurant(
    restaurant_id: UUID,
    service: Annotated[
        RestaurantService,
        Depends(get_restaurant_service),
    ],
) -> RestaurantDetailResponse:
    try:
        restaurant = await service.get_restaurant(
            restaurant_id,
        )

        return RestaurantDetailResponse.model_validate(
            restaurant,
        )

    except RestaurantNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found.",
        ) from exc


@restaurant_router.get(
    "/{restaurant_id}/menu-items",
    response_model=MenuItemListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get restaurant menu",
)
async def get_menu_items(
    restaurant_id: UUID,
    service: Annotated[
        RestaurantService,
        Depends(get_restaurant_service),
    ],
) -> MenuItemListResponse:
    try:
        menu_items = await service.get_menu_items(
            restaurant_id,
        )

        return MenuItemListResponse(
            menu_items=[
                MenuItemResponse.model_validate(menu_item) for menu_item in menu_items
            ],
        )

    except RestaurantNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found.",
        ) from exc


@menu_item_router.get(
    "/search",
    response_model=MenuItemListResponse,
    status_code=status.HTTP_200_OK,
    summary="Search menu items",
)
async def search_menu_items(
    keyword: Annotated[
        str,
        Query(
            min_length=1,
            max_length=100,
            description="Search keyword",
        ),
    ],
    service: Annotated[
        RestaurantService,
        Depends(get_restaurant_service),
    ],
) -> MenuItemListResponse:
    menu_items = await service.search_menu_items(keyword)

    return MenuItemListResponse(
        menu_items=[
            MenuItemResponse.model_validate(menu_item) for menu_item in menu_items
        ],
    )
