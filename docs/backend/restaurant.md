# Module 6 – Restaurant

## Overview

The Restaurant module is responsible for **restaurant discovery** in the Food Delivery Platform.

It provides customer-facing APIs for:

- Browsing available restaurants
- Viewing restaurant details
- Viewing a restaurant's menu
- Searching restaurants
- Searching menu items

This module is **read-only** and does not perform any write operations. It establishes the standard architecture for feature modules using the Repository Pattern, Service Layer, and Dependency Injection.

---

# Objectives

- Provide restaurant discovery APIs
- Keep business logic separated from persistence
- Reuse the architectural pattern established by the Authentication module
- Serve as the template for future business modules

---

# Folder Structure

```text
app/
└── restaurant/
    ├── dependencies.py
    ├── exceptions.py
    ├── repository.py
    ├── router.py
    ├── schemas.py
    ├── service.py
    └── models/
        ├── restaurant.py
        └── menu_item.py
```

---

# Module Responsibilities

The Restaurant module is responsible for:

- Restaurant browsing
- Restaurant search
- Restaurant details
- Restaurant menu retrieval
- Menu item search

The module is **not** responsible for:

- Cart operations
- Ordering
- Coupons
- Reviews
- Authentication
- Payments

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

# Layer Responsibilities

## Router

Responsibilities:

- Receive HTTP requests
- Validate request parameters
- Resolve dependencies
- Call service methods
- Convert ORM models to Pydantic response schemas
- Convert business exceptions into HTTP responses

The router contains **no business logic**.

---

## Service

Responsibilities:

- Business orchestration
- Restaurant existence validation
- Business exception handling
- Repository coordination

The service:

- Does not execute SQL
- Does not know about FastAPI
- Returns ORM models

---

## Repository

Responsibilities:

- Execute SQLAlchemy queries
- Retrieve ORM models
- Encapsulate database access

The repository:

- Contains no business logic
- Never commits
- Never rolls back
- Never raises HTTP exceptions
- Returns ORM models

---

# Implemented Schemas

## RestaurantSummaryResponse

Used for restaurant listings.

Fields:

- restaurant_id
- restaurant_name
- description
- cuisine_type
- average_rating

---

## RestaurantDetailResponse

Extends RestaurantSummaryResponse with:

- phone_number
- email
- street
- city
- state
- postal_code
- opening_time
- closing_time

---

## MenuItemResponse

Represents a menu item.

Fields:

- menu_item_id
- name
- description
- category
- image_url
- price
- preparation_time

---

## Collection Responses

Implemented:

- RestaurantListResponse
- MenuItemListResponse

Collection responses wrap lists to support future pagination without changing the API contract.

---

# Repository Methods

Implemented methods:

```text
get_restaurants()

get_by_id()

get_menu_items()

search_restaurants()

search_menu_items()
```

Repository methods:

- Return ORM models
- Return Sequence[...] for collections
- Never commit
- Never contain business logic

---

# Service Methods

Implemented methods:

```text
get_restaurants()

get_restaurant()

get_menu_items()

search_restaurants()

search_menu_items()
```

Responsibilities include:

- Restaurant existence validation
- Business orchestration
- Repository coordination

---

# Dependency Injection

Dependency providers:

```text
RestaurantRepository

RestaurantService
```

Dependencies only compose objects.

No business logic is implemented inside dependencies.

---

# API Endpoints

## Browse Restaurants

```http
GET /api/v1/restaurants
```

Returns all active restaurants.

---

## Search Restaurants

```http
GET /api/v1/restaurants/search
```

Search restaurants by:

- Restaurant name
- Cuisine type

---

## Restaurant Details

```http
GET /api/v1/restaurants/{restaurant_id}
```

Returns detailed information for a single restaurant.

---

## Restaurant Menu

```http
GET /api/v1/restaurants/{restaurant_id}/menu-items
```

Returns available menu items for the restaurant.

---

## Search Menu Items

```http
GET /api/v1/menu-items/search
```

Search menu items by name.

---

# Business Rules

Implemented business rules:

- Only active restaurants are returned.
- Only available menu items are returned.
- Restaurant must exist before menu items can be retrieved.
- Invalid restaurant requests result in a business exception.

---

# Exception Handling

Business exception:

```text
RestaurantNotFoundException
```

Router converts this exception into:

```http
404 Not Found
```

HTTP exceptions remain inside the router.

---

# Architectural Decisions

## Repository Returns ORM Models

Repositories return SQLAlchemy ORM models.

They never return:

- Pydantic schemas
- JSON
- HTTP responses

---

## Service Returns ORM Models

Services return ORM models.

Routers perform the conversion to response schemas.

---

## Router Performs Response Mapping

ORM objects are converted using:

```python
ResponseSchema.model_validate(orm_object)
```

This keeps the API layer separate from the domain layer.

---

## Repository Never Commits

The Restaurant module is read-only.

Repositories never:

- commit
- rollback
- refresh

This keeps transaction management outside the persistence layer.

---

## Sequence Instead of List

Repository collection methods return:

```python
Sequence[T]
```

instead of:

```python
list[T]
```

This exposes an abstraction rather than a concrete collection implementation.

---

# Quality Standards

The module follows:

- SQLAlchemy 2.0 Async API
- FastAPI Dependency Injection
- Repository Pattern
- Service Layer Pattern
- Pydantic v2
- Ruff formatting
- mypy type checking
- Clean Architecture principles

---

# Verification

Verified:

- Restaurant browsing
- Restaurant details
- Restaurant menu
- Restaurant search
- Menu item search

Architecture verified:

- Repository Pattern
- Service Layer
- Dependency Injection
- ORM to Schema mapping

---

# Future Enhancements

Potential improvements:

- Pagination
- Restaurant filtering
- Sorting options
- Full-text search
- Search ranking
- Geographical search
- Restaurant availability based on opening hours
- Caching
- Performance optimization

---

# Module Status

**Status:** ✅ Completed

This module establishes the reusable read-only feature architecture that will be reused by future modules throughout the Food Delivery Platform.
