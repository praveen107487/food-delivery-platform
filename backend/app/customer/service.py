from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.customer.exceptions import (
    AddressOwnershipException,
    CustomerNotFoundException,
    SavedAddressNotFoundException,
)
from app.customer.mapper import CustomerMapper
from app.customer.models.saved_address import SavedAddress
from app.customer.repository import CustomerRepository
from app.customer.schemas import (
    CreateSavedAddressRequest,
    CustomerResponse,
    SavedAddressListResponse,
    SavedAddressResponse,
    UpdateCustomerRequest,
    UpdateSavedAddressRequest,
)


class CustomerService:
    def __init__(
        self,
        repository: CustomerRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._mapper = CustomerMapper()
        self._session = session

    async def _get_owned_address(
        self,
        customer_id: UUID,
        address_id: UUID,
    ) -> SavedAddress:
        address = await self._repository.get_address_by_id(
            address_id,
        )

        if address is None:
            raise SavedAddressNotFoundException()

        if address.customer_id != customer_id:
            raise AddressOwnershipException()

        return address

    async def get_profile(
        self,
        customer_id: UUID,
    ) -> CustomerResponse:
        customer = await self._repository.get_by_id(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundException()

        return self._mapper.to_customer_response(
            customer,
        )

    async def update_profile(
        self,
        customer_id: UUID,
        request: UpdateCustomerRequest,
    ) -> CustomerResponse:
        customer = await self._repository.get_by_id(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundException()

        self._mapper.apply_customer_update(
            customer,
            request,
        )

        await self._repository.update(
            customer,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                customer,
            )

            return self._mapper.to_customer_response(
                customer,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def create_address(
        self,
        customer_id: UUID,
        request: CreateSavedAddressRequest,
    ) -> SavedAddressResponse:
        customer = await self._repository.get_by_id(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundException()

        addresses, _ = await self._repository.list_addresses(
            customer_id,
        )

        address = self._mapper.to_saved_address(
            request,
            customer_id,
        )

        if not addresses:
            address.is_default = True

        elif request.is_default:
            await self._repository.clear_default_address(
                customer_id,
            )

        await self._repository.create_address(
            address,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                address,
            )

            return self._mapper.to_saved_address_response(
                address,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def list_addresses(
        self,
        customer_id: UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> SavedAddressListResponse:
        customer = await self._repository.get_by_id(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundException()

        addresses, total_count = await self._repository.list_addresses(
            customer_id,
            page=page,
            page_size=page_size,
        )

        return SavedAddressListResponse(
            addresses=[
                self._mapper.to_saved_address_response(address) for address in addresses
            ],
            total_count=total_count,
            page=page,
            page_size=page_size,
        )

    async def get_address(
        self,
        customer_id: UUID,
        address_id: UUID,
    ) -> SavedAddressResponse:
        address = await self._get_owned_address(
            customer_id,
            address_id,
        )

        return self._mapper.to_saved_address_response(
            address,
        )

    async def update_address(
        self,
        customer_id: UUID,
        address_id: UUID,
        request: UpdateSavedAddressRequest,
    ) -> SavedAddressResponse:
        address = await self._get_owned_address(
            customer_id,
            address_id,
        )

        if request.is_default is True:
            await self._repository.clear_default_address(
                customer_id,
            )

        self._mapper.apply_saved_address_update(
            address,
            request,
        )

        await self._repository.update_address(
            address,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                address,
            )

            return self._mapper.to_saved_address_response(
                address,
            )

        except Exception:
            await self._session.rollback()
            raise

    async def delete_address(
        self,
        customer_id: UUID,
        address_id: UUID,
    ) -> None:
        address = await self._get_owned_address(
            customer_id,
            address_id,
        )

        was_default = address.is_default

        try:
            await self._repository.delete_address(
                address,
            )

            if was_default:
                remaining_address, _ = await self._repository.list_addresses(
                    customer_id,
                )
                if remaining_address:
                    new_default = remaining_address[0]
                    new_default.is_default = True

                    await self._repository.update_address(
                        new_default,
                    )

                await self._session.commit()

        except Exception:
            await self._session.rollback()
            raise

    async def set_default_address(
        self,
        customer_id: UUID,
        address_id: UUID,
    ) -> SavedAddressResponse:
        address = await self._get_owned_address(
            customer_id,
            address_id,
        )

        if address.is_default:
            return self._mapper.to_saved_address_response(
                address,
            )

        await self._repository.clear_default_address(
            customer_id,
        )

        address.is_default = True

        await self._repository.update_address(
            address,
        )

        try:
            await self._session.commit()

            await self._session.refresh(
                address,
            )

            return self._mapper.to_saved_address_response(
                address,
            )

        except Exception:
            await self._session.rollback()
            raise
