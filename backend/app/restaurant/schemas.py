from datetime import time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


class RestaurantSummaryResponse(BaseModel):
    restaurant_id: UUID
    restaurant_name: str
    description: str | None
    cuisine_type: str
    average_rating: Decimal | None


class RestaurantDetailResponse(RestaurantSummaryResponse):
    phone_number: str
    email: EmailStr | None
    street: str
    city: str
    state: str
    postal_code: str
    opening_time: time
    closing_time: time


class MenuItemResponse(BaseModel):
    menu_item_id: UUID
    name: str
    description: str | None
    category: str
    image_url: str | None
    price: Decimal
    preparation_time: int


class RestaurantListResponse(BaseModel):
    restaurants: list[RestaurantSummaryResponse]


class MenuItemListResponse(BaseModel):
    menu_items: list[MenuItemResponse]
