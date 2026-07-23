from __future__ import annotations

from uuid import UUID

from app.customer.models.customer import Customer
from app.customer.models.saved_address import SavedAddress
from app.customer.schemas import (
    CreateSavedAddressRequest,
    CustomerResponse,
    SavedAddressResponse,
    UpdateCustomerRequest,
    UpdateSavedAddressRequest,
)


class CustomerMapper:
    @staticmethod
    def to_customer_response(
        customer: Customer,
    ) -> CustomerResponse:
        return CustomerResponse.model_validate(customer)

    @staticmethod
    def apply_customer_update(
        customer: Customer,
        request: UpdateCustomerRequest,
    ) -> Customer:
        updates = request.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(customer, field, value)

        return customer

    @staticmethod
    def to_saved_address(
        request: CreateSavedAddressRequest,
        customer_id: UUID,
    ) -> SavedAddress:
        return SavedAddress(
            customer_id=customer_id,
            **request.model_dump(),
        )

    @staticmethod
    def apply_saved_address_update(
        address: SavedAddress,
        request: UpdateSavedAddressRequest,
    ) -> SavedAddress:
        updates = request.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(address, field, value)

        return address

    @staticmethod
    def to_saved_address_response(
        address: SavedAddress,
    ) -> SavedAddressResponse:
        return SavedAddressResponse.model_validate(address)
