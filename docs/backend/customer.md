# Module 7 – Customer

## Overview

The Customer module is responsible for **customer profile management** and **saved address management** in the Food Delivery Platform.

It provides customer-facing APIs for:
- Viewing and updating customer profile
- Creating saved delivery addresses
- Listing saved addresses
- Updating saved addresses
- Deleting saved addresses
- Setting a default address

This module follows the standard layered architecture using the Repository Pattern, Service Layer, and Dependency Injection.

---

# Responsibilities

The Customer module is responsible for:
- Customer profile retrieval
- Customer profile updates
- Saved address CRUD operations
- Default address management
- Address ownership validation

The module is **not** responsible for:
- Customer registration (handled by Authentication module)
- Customer authentication (handled by Authentication module)
- Address usage in orders (handled by Order module)
- Address validation during checkout (handled by Order module)

---

# Architecture

The module follows the project's standard layered architecture.

```text
HTTP Request
      │
      ▼
Router
      │
      ▼
Service
      │
      ▼
Repository
      │
      ▼
PostgreSQL
```

Each layer has a single responsibility.

---

# Folder Structure

```text
app/
└── customer/
    ├── dependencies.py
    ├── exceptions.py
    ├── mapper.py
    ├── models/
    │   ├── customer.py
    │   └── saved_address.py
    ├── repository.py
    ├── router.py
    ├── schemas.py
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
- Convert business exceptions into HTTP responses

The router contains no business logic.

---

## service.py

Responsibilities:
- Profile management workflow
- Address CRUD workflow
- Default address management
- Business validations
- Transaction management
- Address ownership verification

The service owns all customer business logic.

---

## repository.py

Responsibilities:
- Database access
- Query execution
- Entity persistence
- Address listing with pagination

Repository rules:
- No business logic
- No commits
- Uses flush()
- Returns ORM models

---

## mapper.py

Responsibilities:
- ORM model to schema conversion
- Schema to ORM model conversion
- Partial update application

The mapper isolates transformation logic from business logic.

---

## schemas.py

Contains:
- CustomerResponse
- UpdateCustomerRequest
- SavedAddressBase
- CreateSavedAddressRequest
- UpdateSavedAddressRequest
- SavedAddressResponse
- SavedAddressListResponse

Uses:
- Pydantic v2
- Field validation
- from_attributes configuration

---

## dependencies.py

Provides:
- CustomerRepository
- CustomerService
- Current authenticated customer

Dependencies only compose objects.

---

## exceptions.py

Defines domain-specific customer exceptions:
- CustomerNotFoundException
- SavedAddressNotFoundException
- AddressOwnershipException

---

# Customer Profile Flow

## Get Profile

```text
Client
    │
    ▼
GET /customers/me
    │
    ▼
CustomerService.get_profile()
    │
    ├── Retrieve Customer
    ├── Validate Customer Exists
    ▼
Return CustomerResponse
```

---

## Update Profile

```text
Client
    │
    ▼
PATCH /customers/me
    │
    ▼
CustomerService.update_profile()
    │
    ├── Retrieve Customer
    ├── Validate Customer Exists
    ├── Apply Partial Update
    ├── Save Changes
    ├── Commit Transaction
    ▼
Return Updated CustomerResponse
```

---

# Address Management Flow

## Create Address

```text
Client
    │
    ▼
POST /customers/addresses
    │
    ▼
CustomerService.create_address()
    │
    ├── Validate Customer Exists
    ├── Convert Request to Address
    ├── Set Default if First Address
    ├── Clear Default if Requested
    ├── Save Address
    ├── Commit Transaction
    ▼
Return SavedAddressResponse
```

---

## Set Default Address

```text
Client
    │
    ▼
PATCH /customers/addresses/{address_id}/default
    │
    ▼
CustomerService.set_default_address()
    │
    ├── Validate Address Ownership
    ├── Check Already Default
    ├── Clear All Default Flags
    ├── Set New Default
    ├── Save Changes
    ├── Commit Transaction
    ▼
Return SavedAddressResponse
```

---

## Delete Address

```text
Client
    │
    ▼
DELETE /customers/addresses/{address_id}
    │
    ▼
CustomerService.delete_address()
    │
    ├── Validate Address Ownership
    ├── Check if Default
    ├── Delete Address
    ├── Set New Default if Needed
    ├── Commit Transaction
    ▼
Return 204 No Content
```

---

# API Endpoints

## Get Profile

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/customers/me` | Yes |

Returns the authenticated customer's profile.

---

## Update Profile

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| PATCH | `/api/v1/customers/me` | Yes |

Updates the authenticated customer's profile.

---

## Create Address

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/customers/addresses` | Yes |

Creates a new saved address for the customer.

---

## List Addresses

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/customers/addresses` | Yes |

Lists all saved addresses for the customer with pagination.

---

## Get Address

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/customers/addresses/{address_id}` | Yes |

Returns a specific saved address.

---

## Update Address

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| PATCH | `/api/v1/customers/addresses/{address_id}` | Yes |

Updates a specific saved address.

---

## Delete Address

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| DELETE | `/api/v1/customers/addresses/{address_id}` | Yes |

Deletes a specific saved address.

---

## Set Default Address

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| PATCH | `/api/v1/customers/addresses/{address_id}/default` | Yes |

Sets a specific address as the default address.

---

# Business Rules

Implemented business rules:
- Customers can only access their own addresses
- First address created is automatically set as default
- Only one default address per customer
- When setting a new default, previous default is cleared
- When deleting default address, first remaining address becomes new default
- Addresses are sorted with default address first
- All address fields except delivery_instructions are required

---

# Exception Handling

Business exceptions:
- CustomerNotFoundException → 404 Not Found
- SavedAddressNotFoundException → 404 Not Found
- AddressOwnershipException → 403 Forbidden

HTTP exceptions remain inside the router.

---

# Dependency Injection

Dependency providers:
```text
CustomerRepository

↓

CustomerService
```

Dependencies only compose objects.

No business logic is implemented inside dependencies.

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
- Pagination support

Repositories do not:
- Validate business rules
- Verify ownership
- Commit transactions
- Raise HTTP exceptions

---

# Service Layer

The service layer owns:
- Profile management rules
- Address management rules
- Ownership validation
- Default address logic
- Transaction boundaries

This centralizes business logic and keeps routers thin.

---

# Mapper Pattern

The mapper handles:
- ORM to Pydantic schema conversion
- Pydantic schema to ORM conversion
- Partial update application

Benefits:
- Isolates transformation logic
- Keeps service layer focused on business logic
- Improves testability

---

# Design Decisions

## Mapper for Complex Transformations

Selected because:
- Customer and address entities require field mapping
- Partial updates need careful handling
- Keeps service layer clean
- Improves testability

---

## Default Address Auto-Selection

First address is automatically set as default because:
- Improves user experience
- Ensures at least one default address exists
- Reduces manual configuration steps

---

## Default Address Reassignment on Delete

When default is deleted, first remaining becomes default because:
- Maintains data integrity
- Ensures at least one default address exists
- Prevents checkout failures

---

## Address Ownership Validation

Service validates ownership because:
- Security requirement
- Prevents unauthorized access
- Centralized business rule

---

# Production Considerations

Current implementation includes:
- Profile management
- Address CRUD operations
- Default address management
- Ownership validation
- Transaction management
- Pagination support

Future improvements may include:
- Address validation (geocoding)
- Address suggestions
- Address verification
- Multiple address types (home, work, other)
- Address sharing between family members
- Address import from contacts

---

# Module Completion

Status: **Completed**

Implemented:
- Customer Infrastructure
- Customer Schemas
- Customer Repository
- Customer Service
- Customer Mapper
- Customer Dependencies
- Customer Router
- Router Integration
- Address Management
- Default Address Logic
- Ownership Validation
