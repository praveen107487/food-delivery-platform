from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: UUID
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    create_at: datetime
    updated_at: datetime


class UpdateCustomerRequest(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    phone_number: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )


class SavedAddressBase(BaseModel):
    label: str = Field(
        min_length=1,
        max_length=50,
    )
    recipient_name: str = Field(
        min_length=1,
        max_length=100,
    )
    phone_number: str = Field(
        min_length=7,
        max_length=20,
    )
    street: str = Field(
        min_length=1,
        max_length=255,
    )
    city: str = Field(
        min_length=1,
        max_length=100,
    )
    state: str = Field(
        min_length=1,
        max_length=100,
    )
    postal_code: str = Field(
        min_length=1,
        max_length=20,
    )
    delivery_instructions: str | None = Field(
        default=None,
        max_length=500,
    )
    is_default: bool = False


class CreateSavedAddressRequest(SavedAddressBase):
    pass


class UpdateSavedAddressRequest(BaseModel):
    label: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    recipient_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    phone_number: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )
    street: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    city: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    state: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    postal_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    delivery_instructions: str | None = Field(
        default=None,
        max_length=500,
    )
    is_default: bool | None = None


class SavedAddressResponse(SavedAddressBase):
    model_config = ConfigDict(from_attributes=True)

    address_id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime


class SavedAddressListResponse(BaseModel):
    items: list[SavedAddressResponse]
