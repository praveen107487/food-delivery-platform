from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class RestaurantSummaryResponse(BaseModel):
    restaurant_id: UUID
    restaurant_name: str
    description: str | None
    cuisine_type: str
    average_rating: Decimal | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RestaurantDetailResponse(RestaurantSummaryResponse):
    phone_number: str
    email: EmailStr | None
    street: str
    city: str
    state: str
    postal_code: str
    opening_time: time
    closing_time: time
    created_at: datetime
    updated_at: datetime


class MenuItemResponse(BaseModel):
    menu_item_id: UUID
    restaurant_id: UUID
    name: str
    description: str | None
    category: str
    image_url: str | None
    price: Decimal
    preparation_time: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RestaurantListResponse(BaseModel):
    restaurants: list[RestaurantSummaryResponse]


class MenuItemListResponse(BaseModel):
    menu_items: list[MenuItemResponse]
