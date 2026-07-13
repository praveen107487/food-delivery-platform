from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Result, Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.restaurant.models.menu_item import MenuItem
from app.restaurant.models.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _restaurant_query(self) -> Select[tuple[Restaurant]]:
        return select(Restaurant)

    def _menu_item_query(self) -> Select[tuple[MenuItem]]:
        return select(MenuItem)

    async def get_restaurants(self) -> Sequence[Restaurant]:
        query = (
            self._restaurant_query()
            .where(Restaurant.is_active.is_(True))
            .order_by(Restaurant.restaurant_name.asc())
        )

        result: Result[tuple[Restaurant]] = await self._session.execute(query)

        return result.scalars().all()

    async def get_by_id(
        self,
        restaurant_id: UUID,
    ) -> Restaurant | None:
        query = self._restaurant_query().where(
            Restaurant.restaurant_id == restaurant_id,
            Restaurant.is_active.is_(True),
        )

        result: Result[tuple[Restaurant]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_menu_item_by_id(
        self,
        menu_item_id: UUID,
    ) -> MenuItem | None:
        query = self._menu_item_query().where(
            MenuItem.menu_item_id == menu_item_id,
            MenuItem.is_available.is_(True),
        )

        result: Result[tuple[MenuItem]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_menu_items(
        self,
        restaurant_id: UUID,
    ) -> Sequence[MenuItem]:
        query = (
            self._menu_item_query()
            .where(
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.is_available.is_(True),
            )
            .order_by(MenuItem.name.asc())
        )

        result: Result[tuple[MenuItem]] = await self._session.execute(query)

        return result.scalars().all()

    async def search_restaurants(
        self,
        keyword: str,
    ) -> Sequence[Restaurant]:
        search = f"%{keyword}%"

        query = (
            self._restaurant_query()
            .where(
                Restaurant.is_active.is_(True),
                or_(
                    Restaurant.restaurant_name.ilike(search),
                    Restaurant.cuisine_type.ilike(search),
                ),
            )
            .order_by(Restaurant.restaurant_name.asc())
        )

        result: Result[tuple[Restaurant]] = await self._session.execute(query)

        return result.scalars().all()

    async def search_menu_items(
        self,
        keyword: str,
    ) -> Sequence[MenuItem]:
        search = f"%{keyword}%"

        query = (
            self._menu_item_query()
            .where(
                MenuItem.is_available.is_(True),
                MenuItem.name.ilike(search),
            )
            .order_by(MenuItem.name.asc())
        )

        result: Result[tuple[MenuItem]] = await self._session.execute(query)

        return result.scalars().all()
