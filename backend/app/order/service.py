from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.cart.repository import CartRepository
from app.customer.repository import CustomerRepository
from app.order.exceptions import (
    ActiveCartNotFoundError,
    ActiveOrderNotFoundError,
    CheckoutValidationError,
    EmptyCartError,
    OrderNotFoundError,
)
from app.order.mapper import OrderMapper
from app.order.models import (
    AppliedCouponSnapshot,
    DeliveryAddressSnapshot,
    Order,
    OrderItem,
    OrderStatusHistory,
)
from app.order.repository import OrderRepository
from app.order.schemas import (
    CancelOrderRequest,
    CheckoutRequest,
    OrderDetailsResponse,
    OrderSummaryResponse,
    OrderTimelineResponse,
)
from app.shared.enums import CartStatus, OrderStatus


class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        cart_repository: CartRepository,
        customer_repository: CustomerRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._cart_repository = cart_repository
        self._customer_repository = customer_repository
        self._session = session

    async def get_current_order(
        self,
        customer_id: UUID,
    ) -> OrderSummaryResponse:
        order = await self._repository.get_current_order(
            customer_id=customer_id,
        )

        if order is None:
            raise ActiveOrderNotFoundError()

        return OrderMapper.to_summary_response(order)

    async def get_order(
        self,
        customer_id: UUID,
        order_id: UUID,
    ) -> OrderDetailsResponse:
        order = await self._repository.get_order(
            customer_id=customer_id,
            order_id=order_id,
        )

        if order is None:
            raise OrderNotFoundError()

        return OrderMapper.to_details_response(order)

    async def get_order_timeline(
        self,
        customer_id: UUID,
        order_id: UUID,
    ) -> list[OrderTimelineResponse]:
        order = await self._repository.get_order(
            customer_id=customer_id,
            order_id=order_id,
        )

        if order is None:
            raise OrderNotFoundError()

        return OrderMapper.to_timeline_response(
            order.status_history,
        )

    async def list_orders(
        self,
        customer_id: UUID,
        page: int,
        page_size: int,
    ) -> Sequence[OrderSummaryResponse]:
        orders = await self._repository.list_orders(
            customer_id=customer_id,
            page=page,
            page_size=page_size,
        )

        return [OrderMapper.to_summary_response(order) for order in orders]

    async def cancel_order(
        self,
        customer_id: UUID,
        order_id: UUID,
        request: CancelOrderRequest,
    ) -> OrderDetailsResponse:
        order = await self._repository.get_order(
            customer_id=customer_id,
            order_id=order_id,
        )

        if order is None:
            raise OrderNotFoundError()

        cancellable_statuses = {
            OrderStatus.PENDING_PAYMENT,
            OrderStatus.CONFIRMED,
        }

        if order.current_status not in cancellable_statuses:
            raise CheckoutValidationError(
                "Order cannot be cancelled in its current state."
            )

        now = datetime.now(UTC)
        order.current_status = OrderStatus.CANCELLED
        order.cancelled_at = now

        order.status_history.append(
            OrderStatusHistory(
                order_id=order.order_id,
                status=OrderStatus.CANCELLED,
                created_at=now,
                reason=getattr(request, "reason", None),
            )
        )

        await self._repository.save(order)
        await self._session.commit()
        await self._session.refresh(order)

        return OrderMapper.to_details_response(order)

    async def checkout(
        self,
        customer_id: UUID,
        request: CheckoutRequest,
    ) -> OrderDetailsResponse:
        cart = await self._cart_repository.get_active_cart(
            customer_id=customer_id,
        )

        if cart is None:
            raise ActiveCartNotFoundError()

        if not cart.cart_items:
            raise EmptyCartError()

        address = await self._customer_repository.get_address_by_id_and_customer(
            address_id=request.delivery_address_id,
            customer_id=customer_id,
        )

        if address is None:
            raise CheckoutValidationError("Invalid delivery address.")

        subtotal = Decimal("0.00")
        for cart_item in cart.cart_items:
            item_total = cart_item.unit_price * cart_item.quantity
            subtotal += item_total

        discount = cart.discount_amount
        delivery_fee = Decimal("0.00")
        tax_amount = Decimal("0.00")
        grand_total = subtotal - discount + delivery_fee + tax_amount

        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        customer_suffix = customer_id.hex[:8].upper()
        order_number = f"ORD-{timestamp}-{customer_suffix}"

        now = datetime.now(UTC)
        order = Order(
            order_number=order_number,
            customer_id=customer_id,
            restaurant_id=cart.restaurant_id,
            restaurant_name=cart.restaurant.restaurant_name,
            subtotal=subtotal,
            discount_amount=discount,
            delivery_fee=delivery_fee,
            tax_amount=tax_amount,
            grand_total=grand_total,
            payment_method=request.payment_method,
            current_status=OrderStatus.PENDING_PAYMENT,
        )

        for cart_item in cart.cart_items:
            item_total = cart_item.unit_price * cart_item.quantity
            order_item = OrderItem(
                order_id=order.order_id,
                menu_item_id=cart_item.menu_item_id,
                food_name=cart_item.menu_item.name,
                unit_price=cart_item.unit_price,
                quantity=cart_item.quantity,
                total_price=item_total,
            )
            order.order_items.append(order_item)

        delivery_address_snapshot = DeliveryAddressSnapshot(
            order_id=order.order_id,
            recipient_name=address.recipient_name,
            phone_number=address.phone_number,
            street=address.street,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            delivery_instructions=address.delivery_instructions,
        )
        order.delivery_address_snapshot = delivery_address_snapshot

        if cart.applied_coupon_code:
            applied_coupon_snapshot = AppliedCouponSnapshot(
                order_id=order.order_id,
                coupon_code=cart.applied_coupon_code,
                coupon_type="PLATFORM",
                discount_type="PERCENTAGE",
                discount_value=Decimal("0.00"),
                actual_discount_applied=discount,
            )
            order.applied_coupon_snapshot = applied_coupon_snapshot

        status_history = OrderStatusHistory(
            order_id=order.order_id,
            status=OrderStatus.PENDING_PAYMENT,
            created_at=now,
        )
        order.status_history.append(status_history)

        try:
            await self._repository.create_order(order)

            cart.status = CartStatus.CHECKED_OUT
            await self._cart_repository.update_cart_status(cart)

            await self._session.commit()
            await self._session.refresh(order)

            return OrderMapper.to_details_response(order)

        except Exception:
            await self._session.rollback()
            raise
