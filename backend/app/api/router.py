from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.cart.router import router as cart_router
from app.customer.router import router as customer_router
from app.order.router import router as order_router
from app.payment.router import router as payment_router
from app.restaurant.router import (
    menu_item_router,
    restaurant_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(restaurant_router)
api_router.include_router(menu_item_router)
api_router.include_router(cart_router)
api_router.include_router(customer_router)
api_router.include_router(order_router)
api_router.include_router(payment_router)
