from decimal import Decimal
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
from app.coupon.exceptions import CouponException
from app.coupon.service import CouponService
from app.restaurant.repository import RestaurantRepository
from app.shared.enums import CartStatus


class CartService:
    def __init__(
        self,
        repository: CartRepository,
        restaurant_repository: RestaurantRepository,
        coupon_service: CouponService,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._restaurant_repository = restaurant_repository
        self._coupon_service = coupon_service
        self._session = session

    def _calculate_subtotal(
        self,
        cart: Cart,
    ) -> Decimal:
        return sum(
            (item.unit_price * item.quantity for item in cart.cart_items),
            start=Decimal("0.00"),
        )

    async def _refresh_coupon(
        self,
        cart: Cart,
    ) -> None:
        if cart.applied_coupon_code is None:
            cart.discount_amount = Decimal("0.00")
            return

        subtotal = self._calculate_subtotal(cart)

        try:
            coupon = await self._coupon_service.validate_coupon(
                coupon_code=cart.applied_coupon_code,
                restaurant_id=cart.restaurant_id,
                subtotal=subtotal,
            )

            cart.discount_amount = self._coupon_service.calculate_discount(
                coupon,
                subtotal,
            )

        except CouponException:
            cart.applied_coupon_code = None
            cart.discount_amount = Decimal("0.00")

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

            await self._repository.create_cart(
                cart,
            )

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

        await self._session.refresh(
            cart,
            attribute_names=["cart_items"],
        )

        try:
            await self._refresh_coupon(
                cart,
            )

            await self._session.commit()

            return await self.get_cart(
                customer_id,
            )

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

        await self._repository.update_cart_item(
            cart_item,
        )

        cart = await self._repository.get_cart_by_id(
            cart.cart_id,
        )

        if cart is None:
            raise CartNotFoundException()

        try:
            await self._refresh_coupon(
                cart,
            )

            await self._session.commit()

            return await self.get_cart(
                customer_id,
            )

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

        cart_id = cart.cart_id

        try:
            await self._repository.remove_cart_item(
                cart_item,
            )

            cart = await self._repository.get_cart_by_id(
                cart_id,
            )

            if cart is None:
                raise CartNotFoundException()

            await self._refresh_coupon(
                cart,
            )

            await self._session.commit()

            return await self.get_cart(
                customer_id,
            )

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

            cart.applied_coupon_code = None
            cart.discount_amount = Decimal("0.00")

            await self._session.commit()

            return await self.get_cart(
                customer_id,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def apply_coupon(
        self,
        customer_id: UUID,
        coupon_code: str,
    ) -> Cart:
        cart = await self._repository.get_active_cart(
            customer_id,
        )

        if cart is None:
            raise CartNotFoundException()

        subtotal = self._calculate_subtotal(
            cart,
        )

        coupon = await self._coupon_service.validate_coupon(
            coupon_code=coupon_code,
            restaurant_id=cart.restaurant_id,
            subtotal=subtotal,
        )

        cart.applied_coupon_code = coupon_code

        cart.discount_amount = self._coupon_service.calculate_discount(
            coupon,
            subtotal,
        )

        try:
            await self._session.commit()

            return await self.get_cart(
                customer_id,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def remove_coupon(
        self,
        customer_id: UUID,
    ) -> Cart:
        cart = await self._repository.get_active_cart(
            customer_id,
        )

        if cart is None:
            raise CartNotFoundException()

        cart.applied_coupon_code = None
        cart.discount_amount = Decimal("0.00")

        try:
            await self._session.commit()

            return await self.get_cart(
                customer_id,
            )

        except Exception:
            await self._session.rollback()
            raise
