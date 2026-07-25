from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.auth.dependencies import get_current_customer
from app.customer.dependencies import get_customer_service
from app.customer.models.customer import Customer
from app.customer.schemas import (
    CreateSavedAddressRequest,
    CustomerResponse,
    SavedAddressListResponse,
    SavedAddressResponse,
    UpdateCustomerRequest,
    UpdateSavedAddressRequest,
)
from app.customer.service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customer"])


@router.get(
    "/me",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile(
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> CustomerResponse:
    return await service.get_profile(
        current_customer.customer_id,
    )


@router.patch(
    "/me",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    request: UpdateCustomerRequest,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> CustomerResponse:
    return await service.update_profile(
        customer_id=current_customer.customer_id,
        request=request,
    )


@router.post(
    "/addresses",
    response_model=SavedAddressResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_address(
    request: CreateSavedAddressRequest,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> SavedAddressResponse:
    return await service.create_address(
        customer_id=current_customer.customer_id,
        request=request,
    )


@router.get(
    "/addresses",
    response_model=SavedAddressListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_addresses(
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> SavedAddressListResponse:
    return await service.list_addresses(
        customer_id=current_customer.customer_id,
    )


@router.get(
    "/addresses/{address_id}",
    response_model=SavedAddressResponse,
    status_code=status.HTTP_200_OK,
)
async def get_address(
    address_id: UUID,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> SavedAddressResponse:
    return await service.get_address(
        customer_id=current_customer.customer_id,
        address_id=address_id,
    )


@router.patch(
    "/addresses/{address_id}",
    response_model=SavedAddressResponse,
    status_code=status.HTTP_200_OK,
)
async def update_address(
    address_id: UUID,
    request: UpdateSavedAddressRequest,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> SavedAddressResponse:
    return await service.update_address(
        customer_id=current_customer.customer_id,
        address_id=address_id,
        request=request,
    )


@router.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_address(
    address_id: UUID,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> Response:
    await service.delete_address(
        customer_id=current_customer.customer_id,
        address_id=address_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.patch(
    "/addresses/{address_id}/default",
    response_model=SavedAddressResponse,
    status_code=status.HTTP_200_OK,
)
async def set_default_address(
    address_id: UUID,
    current_customer: Customer = Depends(
        get_current_customer,
    ),
    service: CustomerService = Depends(
        get_customer_service,
    ),
) -> SavedAddressResponse:
    return await service.set_default_address(
        customer_id=current_customer.customer_id,
        address_id=address_id,
    )
