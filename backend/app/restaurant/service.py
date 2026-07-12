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
    ) -> Sequence[Restaurant]:
        return await self._repository.get_restaurants()

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
    ) -> Sequence[MenuItem]:
        await self.get_restaurant(restaurant_id)

        return await self._repository.get_menu_items(
            restaurant_id,
        )

    async def search_restaurants(
        self,
        keyword: str,
    ) -> Sequence[Restaurant]:
        return await self._repository.search_restaurants(
            keyword,
        )

    async def search_menu_items(
        self,
        keyword: str,
    ) -> Sequence[MenuItem]:
        return await self._repository.search_menu_items(
            keyword,
        )
