from uuid import UUID

from sqlalchemy import Result, Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.cart.models import Cart, CartItem
from app.shared.enums import CartStatus


class CartRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _cart_query(self) -> Select[tuple[Cart]]:
        return select(Cart).options(
            selectinload(Cart.restaurant),
            selectinload(Cart.cart_items).selectinload(
                CartItem.menu_item,
            ),
        )

    async def get_active_cart(
        self,
        customer_id: UUID,
    ) -> Cart | None:
        query = self._cart_query().where(
            Cart.customer_id == customer_id,
            Cart.status == CartStatus.ACTIVE,
        )

        result: Result[tuple[Cart]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_cart_by_id(
        self,
        cart_id: UUID,
    ) -> Cart | None:
        query = self._cart_query().where(
            Cart.cart_id == cart_id,
        )

        result: Result[tuple[Cart]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def create_cart(
        self,
        cart: Cart,
    ) -> Cart:
        self._session.add(cart)

        await self._session.flush()

        return cart

    async def get_cart_item(
        self,
        cart_id: UUID,
        menu_item_id: UUID,
    ) -> CartItem | None:
        query = (
            select(CartItem)
            .options(
                selectinload(CartItem.menu_item),
            )
            .where(
                CartItem.cart_id == cart_id,
                CartItem.menu_item_id == menu_item_id,
            )
        )

        result: Result[tuple[CartItem]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_cart_item_by_id(
        self,
        cart_item_id: UUID,
    ) -> CartItem | None:
        query = (
            select(CartItem)
            .options(
                selectinload(CartItem.menu_item),
                selectinload(CartItem.cart).selectinload(
                    Cart.restaurant,
                ),
            )
            .where(
                CartItem.cart_item_id == cart_item_id,
            )
        )

        result: Result[tuple[CartItem]] = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def add_cart_item(
        self,
        cart_item: CartItem,
    ) -> CartItem:
        self._session.add(cart_item)

        await self._session.flush()

        return cart_item

    async def update_cart_item(
        self,
        cart_item: CartItem,
    ) -> CartItem:
        await self._session.flush()

        return cart_item

    async def remove_cart_item(
        self,
        cart_item: CartItem,
    ) -> None:
        await self._session.delete(cart_item)

        await self._session.flush()

    async def clear_cart(
        self,
        cart_id: UUID,
    ) -> None:
        statement = delete(CartItem).where(
            CartItem.cart_id == cart_id,
        )

        await self._session.execute(statement)

        await self._session.flush()

    async def update_cart_status(
        self,
        cart: Cart,
    ) -> Cart:
        await self._session.flush()

        return cart
