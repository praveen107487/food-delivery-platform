# Module 8 – Order

## Overview

The Order module is responsible for **order lifecycle management** in the Food Delivery Platform.

It provides customer-facing APIs for:
- Placing orders (checkout)
- Retrieving current active order
- Retrieving specific order details
- Listing order history
- Cancelling orders
- Viewing order timeline

This module follows the standard layered architecture using the Repository Pattern, Service Layer, and Dependency Injection. It implements order snapshotting to preserve historical data.

---

# Responsibilities

The Order module is responsible for:
- Order creation from cart
- Order status management
- Order lifecycle transitions
- Order snapshotting (address, coupon, items)
- Order cancellation
- Order history retrieval
- Order timeline tracking

The module is **not** responsible for:
- Cart management (handled by Cart module)
- Payment processing (handled by Payment module)
- Restaurant availability (handled by Restaurant module)
- Address validation (handled by Customer module)
- Coupon validation (handled by Coupon module)

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
└── order/
    ├── dependencies.py
    ├── exceptions.py
    ├── mapper.py
    ├── models/
    │   ├── applied_coupon_snapshot.py
    │   ├── delivery_address_snapshot.py
    │   ├── order.py
    │   ├── order_item.py
    │   └── order_status_history.py
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
- Checkout workflow
- Order creation
- Order cancellation
- Business validations
- Transaction management
- Cart status updates
- Order snapshot creation
- Pricing calculation

The service owns all order business logic.

---

## repository.py

Responsibilities:
- Database access
- Query execution
- Entity persistence
- Order listing with pagination
- Eager loading of related entities

Repository rules:
- No business logic
- No commits
- Uses flush()
- Returns ORM models

---

## mapper.py

Responsibilities:
- ORM model to schema conversion
- Order summary transformation
- Order details transformation
- Timeline transformation

The mapper isolates transformation logic from business logic.

---

## schemas.py

Contains:
- OrderItemResponse
- DeliveryAddressResponse
- AppliedCouponResponse
- OrderTimelineResponse
- OrderSummaryResponse
- OrderDetailsResponse
- CancelOrderRequest
- OrderListResponse
- CheckoutRequest

Uses:
- Pydantic v2
- Field validation
- from_attributes configuration

---

## dependencies.py

Provides:
- OrderRepository
- OrderService

Dependencies only compose objects.

---

## exceptions.py

Defines domain-specific order exceptions:
- ActiveCartNotFoundError
- ActiveOrderNotFoundError
- CheckoutValidationError
- EmptyCartError
- OrderNotFoundError

---

# Order Flow

## Checkout (Place Order)

```text
Client
    │
    ▼
POST /orders
    │
    ▼
OrderService.checkout()
    │
    ├── Retrieve Active Cart
    ├── Validate Cart Not Empty
    ├── Validate Delivery Address
    ├── Calculate Pricing
    ├── Generate Order Number
    ├── Create Order Entity
    ├── Create Order Items
    ├── Create Address Snapshot
    ├── Create Coupon Snapshot
    ├── Create Status History
    ├── Save Order
    ├── Update Cart Status to CHECKED_OUT
    ├── Commit Transaction
    ▼
Return OrderDetailsResponse
```

---

## Get Current Order

```text
Client
    │
    ▼
GET /orders/current
    │
    ▼
OrderService.get_current_order()
    │
    ├── Retrieve Active Order
    │   (Not DELIVERED or CANCELLED)
    ├── Validate Order Exists
    ▼
Return OrderSummaryResponse
```

---

## Cancel Order

```text
Client
    │
    ▼
POST /orders/{order_id}/cancel
    │
    ▼
OrderService.cancel_order()
    │
    ├── Retrieve Order
    ├── Validate Order Exists
    ├── Validate Cancellable Status
    │   (PENDING_PAYMENT or CONFIRMED)
    ├── Update Status to CANCELLED
    ├── Set Cancelled Timestamp
    ├── Add Status History Entry
    ├── Save Order
    ├── Commit Transaction
    ▼
Return OrderDetailsResponse
```

---

# API Endpoints

## Place Order

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/orders` | Yes |

Creates an order from the active cart.

---

## Get Current Order

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/orders/current` | Yes |

Returns the customer's currently active order.

---

## Get Order Details

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/orders/{order_id}` | Yes |

Returns detailed information for a specific order.

---

## List Order History

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/orders/history` | Yes |

Lists the customer's order history with pagination.

---

## Cancel Order

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/orders/{order_id}/cancel` | Yes |

Cancels a specific order.

---

## Get Order Timeline

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/orders/{order_id}/timeline` | Yes |

Returns the status timeline for a specific order.

---

# Business Rules

Implemented business rules:
- Orders can only be placed from active carts
- Empty carts cannot be checked out
- Delivery address must belong to the customer
- Pricing is calculated server-side
- Order number is auto-generated with timestamp
- Cart status changes to CHECKED_OUT after order creation
- Orders can only be cancelled in PENDING_PAYMENT or CONFIRMED status
- Order snapshots preserve historical data (address, coupon, items)
- Current order is the most recent non-delivered/cancelled order
- Order status history tracks all status transitions

---

# Order Snapshotting

The module implements snapshotting to preserve historical data:

## Delivery Address Snapshot
- Captures delivery address at order time
- Preserves address even if customer deletes it later
- Includes recipient name, phone, street, city, state, postal code, instructions

## Applied Coupon Snapshot
- Captures coupon details at order time
- Preserves coupon information even if coupon expires
- Includes coupon code, type, discount type, discount value, actual discount

## Order Item Snapshot
- Captures menu item details at order time
- Preserves item name and price even if restaurant changes menu
- Includes menu_item_id, food_name, unit_price, quantity, total_price

---

# Exception Handling

Business exceptions:
- ActiveCartNotFoundError → 404 Not Found
- ActiveOrderNotFoundError → 404 Not Found
- CheckoutValidationError → 400 Bad Request
- EmptyCartError → 400 Bad Request
- OrderNotFoundError → 404 Not Found

HTTP exceptions remain inside the router.

---

# Dependency Injection

Dependency providers:
```text
OrderRepository

↓

OrderService
```

Dependencies only compose objects.

No business logic is implemented inside dependencies.

---

# Transaction Management

The service layer controls transactions.

Example:
```text
Repository.create_order()

↓

flush()

↓

CartRepository.update_cart_status()

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
- Eager loading with selectinload
- Pagination support

Repositories do not:
- Validate business rules
- Calculate pricing
- Commit transactions
- Raise HTTP exceptions

---

# Service Layer

The service layer owns:
- Checkout workflow
- Order creation logic
- Cancellation rules
- Pricing calculation
- Snapshot creation
- Transaction boundaries
- Cart coordination

This centralizes business logic and keeps routers thin.

---

# Mapper Pattern

The mapper handles:
- ORM to Pydantic schema conversion
- Order summary transformation
- Order details transformation
- Timeline transformation

Benefits:
- Isolates transformation logic
- Keeps service layer focused on business logic
- Improves testability

---

# Order Lifecycle

Orders progress through the following statuses:

1. **PENDING_PAYMENT** - Order created, awaiting payment
2. **CONFIRMED** - Payment successful, restaurant confirmed
3. **PREPARING** - Restaurant preparing food
4. **READY_FOR_PICKUP** - Food ready for delivery
5. **OUT_FOR_DELIVERY** - Delivery partner on the way
6. **DELIVERED** - Order successfully delivered
7. **CANCELLED** - Order cancelled by customer

Status transitions are tracked in `order_status_history`.

---

# Design Decisions

## Order Snapshotting

Selected because:
- Preserves historical data integrity
- Allows menu/restaurant changes without affecting past orders
- Enables accurate order history and reporting
- Supports audit trails

---

## Order Number Generation

Auto-generated with timestamp and customer ID because:
- Human-readable order identifiers
- Unique across all orders
- Sortable by creation time
- Includes customer reference for support

---

## Cart Status Update on Checkout

Cart status changes to CHECKED_OUT because:
- Prevents cart reuse
- Maintains cart lifecycle integrity
- Enables cart archival
- Supports future cart history features

---

## Cancellable Status Restriction

Only PENDING_PAYMENT and CONFIRMED can be cancelled because:
- Prevents cancellation after preparation starts
- Protects restaurant resources
- Reduces food waste
- Maintains business logic integrity

---

# Production Considerations

Current implementation includes:
- Order creation and management
- Order snapshotting
- Order cancellation
- Order timeline tracking
- Order history with pagination
- Transaction management
- Eager loading optimization

Future improvements may include:
- Real-time order status updates (WebSocket)
- Order modification before confirmation
- Partial refunds
- Order reordering
- Order scheduling
- Order splitting
- Advanced order filtering
- Order analytics
- Restaurant order management interface

---

# Module Completion

Status: **Completed**

Implemented:
- Order Infrastructure
- Order Schemas
- Order Repository
- Order Service
- Order Mapper
- Order Dependencies
- Order Router
- Router Integration
- Order Snapshotting
- Order Cancellation
- Order Timeline
- Order History
- Pricing Calculation
- Cart Coordination
