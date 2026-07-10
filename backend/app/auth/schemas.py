from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerRegistrationRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone_number: str = Field(min_length=10, max_length=20)


class CustomerLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class AuthenticatedCustomerResponse(BaseModel):
    customer_id: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)
