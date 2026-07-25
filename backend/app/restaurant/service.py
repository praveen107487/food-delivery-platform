from collections.abc import Sequence
from uuid import UUID

from app.restaurant.exceptions import RestaurantNotFoundException
from app.restaurant.models.menu_item import MenuItem
from app.restaurant.models.restaurant import Restaurant
from app.restaurant.repository import RestaurantRepository


class RestaurantService:
    def __init__(
        self,
        repository: RestaurantRepository,
    ) -> None:
        self._repository = repository

    async def get_restaurants(
        self,
        page: int = 1,
        page_size: int = 20,
        cuisine_type: str | None = None,
    ) -> tuple[Sequence[Restaurant], int]:
        return await self._repository.get_restaurants(
            page=page,
            page_size=page_size,
            cuisine_type=cuisine_type,
        )

    async def get_restaurant(
        self,
        restaurant_id: UUID,
    ) -> Restaurant:
        restaurant = await self._repository.get_by_id(restaurant_id)

        if restaurant is None:
            raise RestaurantNotFoundException("Restaurant not found.")

        return restaurant

    async def get_menu_items(
        self,
        restaurant_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[MenuItem], int]:
        await self.get_restaurant(restaurant_id)

        return await self._repository.get_menu_items(
            restaurant_id=restaurant_id,
            page=page,
            page_size=page_size,
        )

    async def search_restaurants(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[Restaurant], int]:
        return await self._repository.search_restaurants(
            keyword=keyword,
            page=page,
            page_size=page_size,
        )

    async def search_menu_items(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[MenuItem], int]:
        return await self._repository.search_menu_items(
            keyword=keyword,
            page=page,
            page_size=page_size,
        )
