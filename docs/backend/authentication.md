# Module 5 – Authentication

## Overview

The Authentication module is responsible for customer identity verification and access control within the Food Delivery Platform.

It provides secure customer registration, login, and authentication using JSON Web Tokens (JWT). The module follows a layered architecture and separates concerns through the Repository Pattern, Service Layer, and Dependency Injection.

This module acts as the entry point for all authenticated customer operations.

---

# Responsibilities

The Authentication module is responsible for:

- Customer Registration
- Customer Login
- Password Hashing
- Password Verification
- JWT Access Token Generation
- JWT Validation
- Current Authenticated Customer Retrieval

The module is **not** responsible for:

- Authorization (Roles & Permissions)
- Token Revocation
- Refresh Tokens
- Session Management
- Social Login
- OTP Authentication

These capabilities may be introduced in future modules.

---

# Architecture

The Authentication module follows the project's standard layered architecture.

```text
HTTP Request
        │
        ▼
Authentication Router
        │
        ▼
Authentication Service
        │
        ▼
Authentication Repository
        │
        ▼
PostgreSQL
```

Each layer has a single responsibility.

---

# Folder Structure

```text
app/
└── auth/
    ├── constants.py
    ├── dependencies.py
    ├── exceptions.py
    ├── repository.py
    ├── router.py
    ├── schemas.py
    ├── security.py
    └── service.py
```

---

# Component Responsibilities

## router.py

Responsibilities:

- Expose REST endpoints
- Request validation
- Dependency injection
- Delegate requests to the service layer

The router contains no business logic.

---

## service.py

Responsibilities:

- Registration workflow
- Login workflow
- Customer authentication
- Business validations
- Transaction management

The service owns all authentication business logic.

---

## repository.py

Responsibilities:

- Database access
- Query execution
- Entity persistence

Repository rules:

- No business logic
- No commits
- Uses flush()
- Returns ORM models

---

## security.py

Responsibilities:

- Password hashing
- Password verification
- JWT generation
- JWT validation

Security logic is isolated from business logic.

---

## schemas.py

Contains:

- CustomerRegistrationRequest
- CustomerLoginRequest
- TokenResponse
- AuthenticatedCustomerResponse

Uses:

- Pydantic v2
- Annotated
- Shared validation types

---

## dependencies.py

Provides:

- AuthenticationRepository
- AuthenticationService
- Current authenticated customer
- OAuth2 Bearer token extraction

Dependencies only compose objects.

---

## exceptions.py

Defines domain-specific authentication exceptions.

Examples:

- CustomerAlreadyExistsException
- InvalidCredentialsException
- InvalidTokenException
- TokenExpiredException

---

# Authentication Flow

## Customer Registration

```text
Client
    │
    ▼
POST /auth/register
    │
    ▼
AuthenticationService.register()
    │
    ├── Check existing email
    ├── Hash password
    ├── Create Customer
    ├── Save Customer
    ├── Commit Transaction
    ▼
Return Customer
```

---

## Customer Login

```text
Client
    │
    ▼
POST /auth/login
    │
    ▼
AuthenticationService.login()
    │
    ├── Find customer
    ├── Verify password
    ├── Generate JWT
    ▼
Return Access Token
```

---

## Current Customer

```text
Request
    │
Authorization Header
    │
Bearer Token
    │
    ▼
OAuth2PasswordBearer
    │
    ▼
AuthenticationService.get_current_customer()
    │
    ├── Decode JWT
    ├── Validate Token
    ├── Retrieve Customer
    ▼
Return Customer
```

---

# API Endpoints

## Register

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/auth/register` | No |

Registers a new customer account.

---

## Login

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/auth/login` | No |

Authenticates a customer and returns a JWT access token.

---

## Current Customer

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/auth/me` | Yes |

Returns the authenticated customer's profile.

---

## Logout

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/auth/logout` | Yes |

Status:

**Deferred**

The API exists in the system design but has not been implemented.

The current implementation uses stateless JWT authentication.

A production-ready logout mechanism requires additional infrastructure such as:

- Token blacklist
- Refresh token rotation
- Redis session storage
- Token versioning

This endpoint will be implemented in a future security enhancement module.

---

# Security Design

Passwords are never stored in plain text.

Passwords are hashed before persistence.

Password verification uses secure hash comparison.

JWTs are digitally signed.

Every protected endpoint validates the access token before accessing business resources.

---

# Dependency Injection

Authentication uses FastAPI's dependency injection system.

Dependencies provided:

```text
get_authentication_repository()

↓

get_authentication_service()

↓

get_current_customer()
```

This keeps routers lightweight and improves testability.

---

# Transaction Management

The service layer controls transactions.

Example:

```text
Repository.save()

↓

flush()

↓

Service.commit()

↓

refresh()

↓

Return Entity
```

Repositories never commit transactions.

---

# Repository Pattern

Repository responsibilities:

- Read operations
- Write operations
- Persistence only

Repositories do not:

- Validate business rules
- Generate JWTs
- Hash passwords
- Commit transactions

---

# Service Layer

The service layer owns:

- Registration rules
- Login rules
- Authentication rules
- Transaction boundaries

This centralizes business logic and keeps routers thin.

---

# Design Decisions

## JWT Authentication

Selected because:

- Stateless
- Scalable
- Simple deployment
- Widely adopted
- Suitable for REST APIs

---

## Repository Pattern

Provides:

- Separation of concerns
- Testability
- Clean persistence layer

---

## Service Layer

Provides:

- Centralized business rules
- Better maintainability
- Easier testing

---

## Dependency Injection

Provides:

- Loose coupling
- Reusable components
- Easier unit testing

---

# Production Considerations

Current implementation includes:

- Password hashing
- Password verification
- JWT authentication
- Layered architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Clean separation of concerns

Future improvements may include:

- Refresh Tokens
- Token Revocation
- Redis Blacklisting
- Email Verification
- Password Reset
- Rate Limiting
- Account Lockout
- Multi-Factor Authentication
- OAuth Providers

---

# Module Completion

Status:

**Completed**

Implemented:

- Authentication Infrastructure
- Authentication Schemas
- Authentication Repository
- Authentication Service
- Authentication Dependencies
- Authentication Router
- Router Integration

Deferred:

- Logout
- Refresh Tokens
- Token Revocation

These features require additional infrastructure and will be implemented in future modules.
