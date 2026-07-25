from decimal import Decimal

from app.cart.models import Cart, CartItem
from app.cart.schemas import (
    CartItemResponse,
    CartPricing,
    CartResponse,
)


def map_cart_item(
    cart_item: CartItem,
) -> CartItemResponse:
    return CartItemResponse(
        cart_item_id=cart_item.cart_item_id,
        menu_item_id=cart_item.menu_item_id,
        menu_item_name=cart_item.menu_item.name,
        quantity=cart_item.quantity,
        unit_price=cart_item.unit_price,
        total_price=cart_item.quantity * cart_item.unit_price,
    )


def map_cart(
    cart: Cart,
) -> CartResponse:
    items = [map_cart_item(item) for item in cart.cart_items]

    subtotal = sum(
        (item.total_price for item in items),
        start=Decimal("0.00"),
    )

    discount = cart.discount_amount
    delivery_fee = Decimal("0.00")
    tax_amount = Decimal("0.00")

    total = subtotal - discount + delivery_fee + tax_amount

    pricing = CartPricing(
        subtotal=subtotal,
        discount=discount,
        delivery_fee=delivery_fee,
        tax_amount=tax_amount,
        total=total,
    )

    return CartResponse(
        cart_id=cart.cart_id,
        restaurant_id=cart.restaurant_id,
        restaurant_name=cart.restaurant.restaurant_name,
        applied_coupon_code=cart.applied_coupon_code,
        items=items,
        pricing=pricing,
    )
