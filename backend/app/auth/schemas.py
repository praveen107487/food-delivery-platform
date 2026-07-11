import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from app.auth.constants import AUTHORIZATION_SCHEME
from app.shared.types import NameStr, PasswordStr, PhoneNumberStr


class CustomerRegistrationRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    first_name: NameStr
    last_name: NameStr
    phone_number: PhoneNumberStr


class CustomerLoginRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = AUTHORIZATION_SCHEME


class AuthenticatedCustomerResponse(BaseModel):
    customer_id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)
