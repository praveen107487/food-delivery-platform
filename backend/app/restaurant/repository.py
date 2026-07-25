from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Result, Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.restaurant.models.menu_item import MenuItem
from app.restaurant.models.restaurant import Restaurant


class RestaurantRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _restaurant_query(self) -> Select[tuple[Restaurant]]:
        return select(Restaurant)

    def _menu_item_query(self) -> Select[tuple[MenuItem]]:
        return select(MenuItem)

    async def get_restaurants(
        self,
        page: int = 1,
        page_size: int = 20,
        cuisine_type: str | None = None,
    ) -> tuple[Sequence[Restaurant], int]:
        query = self._restaurant_query().where(Restaurant.is_active.is_(True))

        if cuisine_type:
            query = query.where(Restaurant.cuisine_type == cuisine_type)

        count_query = select(Restaurant.restaurant_id).where(
            Restaurant.is_active.is_(True)
        )
        if cuisine_type:
            count_query = count_query.where(Restaurant.cuisine_type == cuisine_type)

        count_result: Result = await self._session.execute(count_query)
        total_count = len(count_result.scalars().all())

        offset = (page - 1) * page_size
        query = (
            query.order_by(Restaurant.restaurant_name.asc())
            .offset(offset)
            .limit(page_size)
        )

        result: Result[tuple[Restaurant]] = await self._session.execute(query)

        return result.scalars().all(), total_count

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
        query = (
            self._menu_item_query()
            .options(selectinload(MenuItem.restaurant))
            .where(
                MenuItem.menu_item_id == menu_item_id,
                MenuItem.is_available.is_(True),
            )
        )

        result: Result[tuple[MenuItem]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_menu_items(
        self,
        restaurant_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[MenuItem], int]:
        query = self._menu_item_query().where(
            MenuItem.restaurant_id == restaurant_id,
            MenuItem.is_available.is_(True),
        )

        count_result: Result = await self._session.execute(
            select(MenuItem.menu_item_id).where(
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.is_available.is_(True),
            )
        )
        total_count = len(count_result.scalars().all())

        offset = (page - 1) * page_size
        query = query.order_by(MenuItem.name.asc()).offset(offset).limit(page_size)

        result: Result[tuple[MenuItem]] = await self._session.execute(query)

        return result.scalars().all(), total_count

    async def search_restaurants(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[Restaurant], int]:
        search = f"%{keyword}%"

        query = self._restaurant_query().where(
            Restaurant.is_active.is_(True),
            or_(
                Restaurant.restaurant_name.ilike(search),
                Restaurant.cuisine_type.ilike(search),
            ),
        )

        count_result: Result = await self._session.execute(
            select(Restaurant.restaurant_id).where(
                Restaurant.is_active.is_(True),
                or_(
                    Restaurant.restaurant_name.ilike(search),
                    Restaurant.cuisine_type.ilike(search),
                ),
            )
        )
        total_count = len(count_result.scalars().all())

        offset = (page - 1) * page_size
        query = (
            query.order_by(Restaurant.restaurant_name.asc())
            .offset(offset)
            .limit(page_size)
        )

        result: Result[tuple[Restaurant]] = await self._session.execute(query)

        return result.scalars().all(), total_count

    async def search_menu_items(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[Sequence[MenuItem], int]:
        search = f"%{keyword}%"

        query = self._menu_item_query().where(
            MenuItem.is_available.is_(True),
            MenuItem.name.ilike(search),
        )

        count_result: Result = await self._session.execute(
            select(MenuItem.menu_item_id).where(
                MenuItem.is_available.is_(True),
                MenuItem.name.ilike(search),
            )
        )
        total_count = len(count_result.scalars().all())

        offset = (page - 1) * page_size
        query = query.order_by(MenuItem.name.asc()).offset(offset).limit(page_size)

        result: Result[tuple[MenuItem]] = await self._session.execute(query)

        return result.scalars().all(), total_count
