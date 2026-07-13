from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.cart.exceptions import (
    CartItemNotFoundException,
    CartNotFoundException,
    CartRestaurantMismatchException,
    MenuItemUnavailableException,
)
from app.cart.models import Cart, CartItem
from app.cart.repository import CartRepository
from app.restaurant.repository import RestaurantRepository
from app.shared.enums import CartStatus


class CartService:
    def __init__(
        self,
        repository: CartRepository,
        restaurant_repository: RestaurantRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._restaurant_repository = restaurant_repository
        self._session = session

    async def get_cart(
        self,
        customer_id: UUID,
    ) -> Cart:
        cart = await self._repository.get_active_cart(
            customer_id,
        )

        if cart is None:
            raise CartNotFoundException()

        return cart

    async def add_to_cart(
        self,
        customer_id: UUID,
        menu_item_id: UUID,
        quantity: int,
    ) -> Cart:
        menu_item = await self._restaurant_repository.get_menu_item_by_id(
            menu_item_id,
        )

        if menu_item is None:
            raise MenuItemUnavailableException()

        cart = await self._repository.get_active_cart(
            customer_id,
        )

        if cart is None:
            cart = Cart(
                customer_id=customer_id,
                restaurant_id=menu_item.restaurant_id,
                status=CartStatus.ACTIVE,
            )

            await self._repository.create_cart(cart)

        elif cart.restaurant_id != menu_item.restaurant_id:
            raise CartRestaurantMismatchException()

        cart_item = await self._repository.get_cart_item(
            cart.cart_id,
            menu_item.menu_item_id,
        )

        if cart_item is None:
            cart_item = CartItem(
                cart_id=cart.cart_id,
                menu_item_id=menu_item.menu_item_id,
                quantity=quantity,
                unit_price=menu_item.price,
            )

            await self._repository.add_cart_item(
                cart_item,
            )
        else:
            cart_item.quantity += quantity

            await self._repository.update_cart_item(
                cart_item,
            )

        try:
            await self._session.commit()

            return await self.get_cart(customer_id)

        except Exception:
            await self._session.rollback()
            raise

    async def update_cart_item(
        self,
        customer_id: UUID,
        cart_item_id: UUID,
        quantity: int,
    ) -> Cart:
        cart_item = await self._repository.get_cart_item_by_id(
            cart_item_id,
        )

        if cart_item is None:
            raise CartItemNotFoundException()

        cart = await self._repository.get_cart_by_id(
            cart_item.cart_id,
        )

        if cart is None or cart.customer_id != customer_id:
            raise CartNotFoundException()

        cart_item.quantity = quantity

        try:
            await self._repository.update_cart_item(
                cart_item,
            )

            await self._session.commit()

            return await self.get_cart(customer_id)

        except Exception:
            await self._session.rollback()
            raise

    async def remove_cart_item(
        self,
        customer_id: UUID,
        cart_item_id: UUID,
    ) -> Cart:
        cart_item = await self._repository.get_cart_item_by_id(
            cart_item_id,
        )

        if cart_item is None:
            raise CartItemNotFoundException()

        cart = await self._repository.get_cart_by_id(
            cart_item.cart_id,
        )

        if cart is None or cart.customer_id != customer_id:
            raise CartNotFoundException()

        try:
            await self._repository.remove_cart_item(
                cart_item,
            )

            await self._session.commit()

            return await self.get_cart(customer_id)

        except Exception:
            await self._session.rollback()
            raise

    async def clear_cart(
        self,
        customer_id: UUID,
    ) -> Cart:
        cart = await self._repository.get_active_cart(
            customer_id,
        )

        if cart is None:
            raise CartNotFoundException()

        try:
            await self._repository.clear_cart(
                cart.cart_id,
            )

            await self._session.commit()

            updated_cart = await self._repository.get_cart_by_id(
                cart.cart_id,
            )

            if updated_cart is None:
                raise CartNotFoundException()

            return updated_cart

        except Exception:
            await self._session.rollback()
            raise
