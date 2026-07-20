# Cart Module Documentation

## Module Information

| Item           | Details                                |
| -------------- | -------------------------------------- |
| Module         | Cart                                   |
| Phase          | Phase 5 – Backend Development          |
| Status         | Completed                              |
| Architecture   | Layered Architecture                   |
| Pattern        | Repository → Service → Mapper → Router |
| Authentication | Required                               |
| API Prefix     | `/api/v1/cart`                         |

---

# Module Purpose

The Cart module allows authenticated customers to build and manage their shopping cart before placing an order.

The module ensures that:

* Every customer has at most one active cart.
* A cart belongs to exactly one restaurant.
* Menu items can only be added if they are currently available.
* Quantities can be updated.
* Items can be removed.
* The entire cart can be cleared.
* Cart totals are calculated dynamically.

The cart acts as the bridge between restaurant browsing and the checkout process.

---

# Business Rules

## Active Cart

A customer may have only one active cart.

If an active cart does not exist, a new one is created automatically when the customer adds the first menu item.

---

## Single Restaurant Cart

A cart may contain items from only one restaurant.

If a customer attempts to add a menu item from another restaurant while the cart already contains items, the request is rejected.

Reason:

* Prevents mixed restaurant orders.
* Simplifies order processing.
* Matches the product requirements.

---

## Menu Item Availability

Only available menu items may be added.

Unavailable or deleted menu items return an error.

---

## Adding Existing Items

If the same menu item already exists inside the cart,

the quantity is increased instead of creating another row.

Example:

Current Cart

* Burger ×2

Customer adds

* Burger ×1

Result

* Burger ×3

---

## Quantity Update

Updating quantity replaces the existing quantity.

Example

Current

Burger ×5

Update

Quantity = 2

Result

Burger ×2

---

## Remove Item

Removing an item deletes only that cart item.

The cart itself remains active.

---

## Clear Cart

Clearing the cart removes every cart item.

The active cart remains.

This allows customers to continue shopping without creating another cart.

---

# Module Structure

```text
cart/

├── models/
│   ├── cart.py
│   ├── cart_item.py
│   └── __init__.py
│
├── schemas.py
├── repository.py
├── service.py
├── mapper.py
├── router.py
├── dependencies.py
└── exceptions.py
```

---

# Layered Architecture

```text
HTTP Request
      │
      ▼
Router
      │
      ▼
Mapper
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

# Responsibilities

## Repository

Responsible only for database operations.

Implemented methods:

* get_active_cart()
* get_cart_by_id()
* create_cart()
* get_cart_item()
* get_cart_item_by_id()
* add_cart_item()
* update_cart_item()
* remove_cart_item()
* clear_cart()

Repositories do not contain:

* business rules
* validation
* HTTP logic

---

## Service

Responsible for business logic.

Implemented operations:

* get_cart()
* add_to_cart()
* update_cart_item()
* remove_cart_item()
* clear_cart()

Responsibilities:

* cart creation
* restaurant validation
* menu availability validation
* quantity updates
* transaction management
* exception handling

The service owns every database transaction.

---

## Mapper

The Cart module introduces a dedicated mapper layer.

Reason:

The response contains fields that do not directly exist inside ORM models.

Examples:

* restaurant_name
* subtotal
* menu_item_name
* total_price

Mapper functions:

* map_cart()
* map_cart_item()

The mapper converts ORM entities into API response DTOs.

---

## Router

Responsible for:

* request validation
* dependency injection
* calling services
* converting exceptions
* mapping ORM responses

No business logic exists inside routers.

---

# Dependency Injection

The module exposes:

## Repository Dependency

Returns

* CartRepository

---

## Service Dependency

Returns

* CartService

The Cart service also depends on:

* RestaurantRepository

to validate menu items.

---

# Exception Handling

Business Exceptions

* CartNotFoundException
* CartItemNotFoundException
* CartRestaurantMismatchException
* MenuItemUnavailableException

Routers translate these exceptions into HTTP responses.

---

# Repository Loading Strategy

The repository eagerly loads relationships using:

* selectinload()

Loaded relationships:

```text
Cart
 ├── Restaurant
 └── CartItems
        └── MenuItem
```

This prevents lazy-loading inside the service and mapper.

---

# API Endpoints

## Get Cart

```
GET /api/v1/cart
```

Authentication Required

Returns the customer's active cart.

---

## Add Item

```
POST /api/v1/cart/items
```

Authentication Required

Creates a cart if necessary.

Adds a menu item.

Increases quantity if the item already exists.

---

## Update Item Quantity

```
PATCH /api/v1/cart/items/{cart_item_id}
```

Authentication Required

Updates the quantity of an existing cart item.

---

## Remove Item

```
DELETE /api/v1/cart/items/{cart_item_id}
```

Authentication Required

Removes a single cart item.

---

## Clear Cart

```
DELETE /api/v1/cart
```

Authentication Required

Deletes every item from the cart.

The cart remains active.

---

# Transaction Strategy

All write operations follow the same pattern.

```python
try:
    ...

    await self._session.commit()

except Exception:
    await self._session.rollback()
    raise
```

Transactions are owned exclusively by the service layer.

---

# Response Mapping

Services return ORM entities.

Routers convert ORM entities into response DTOs using:

* map_cart()
* map_cart_item()

This keeps the service independent of API response models.

---

# Security

Every endpoint requires authentication.

Authentication is performed using:

* JWT Access Token
* Current Customer Dependency

Customers may access only their own carts.

---

# Integration with Other Modules

## Authentication Module

Used for:

* Current authenticated customer

---

## Restaurant Module

Used for:

* Menu item validation
* Restaurant validation

The Cart module reuses the RestaurantRepository instead of calling another service.

---

# Production Design Decisions

## One Active Cart Per Customer

Simplifies checkout.

Maintains a single source of truth.

---

## Single Restaurant Restriction

Prevents mixed restaurant orders.

Matches the product requirements.

---

## Dynamic Price Snapshot

The cart stores the unit price at the time the item is added.

Subtotal is calculated dynamically.

---

## Dedicated Mapper Layer

Introduced because the response model differs from the ORM model.

Avoids leaking ORM entities into API responses.

---

## Repository Reuse

The Cart module directly reuses the RestaurantRepository for persistence operations.

No service-to-service dependency was introduced.

---

# Code Quality

The module follows:

* Async SQLAlchemy
* SQLAlchemy 2.x
* FastAPI dependency injection
* Repository Pattern
* Service Layer Pattern
* Mapper Pattern
* Fully typed code
* UUID identifiers
* Decimal for monetary values
* Ruff compliant
* MyPy compliant
* Production-ready transaction handling

---

# Module Completion Checklist

* ✅ Schemas implemented
* ✅ Repository implemented
* ✅ Service implemented
* ✅ Mapper implemented
* ✅ Dependencies implemented
* ✅ Router implemented
* ✅ Exception handling implemented
* ✅ API integration completed
* ✅ Authentication integration completed
* ✅ Restaurant integration completed
* ✅ Business rules implemented
* ✅ Production review completed

---

# Module Summary

The Cart module provides a complete production-ready shopping cart implementation.

It follows the same layered architecture established in previous modules while introducing a dedicated Mapper layer for transforming ORM entities into API response DTOs. The module enforces all required business rules, integrates with Authentication and Restaurant modules, maintains strict transaction boundaries, and is designed to support the upcoming Checkout, Coupon, and Order modules.
