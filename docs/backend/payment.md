# Module 9 – Payment

## Overview

The Payment module is responsible for **payment processing** in the Food Delivery Platform.

It provides customer-facing APIs for:
- Initiating payment for an order
- Verifying payment completion
- Retrieving payment status
- Retrieving payment details
- Retrying failed payments
- Listing payment history for an order

This module follows the standard layered architecture using the Repository Pattern, Service Layer, and Dependency Injection. It integrates with external payment gateways for online payments.

---

# Responsibilities

The Payment module is responsible for:
- Payment initiation
- Payment verification
- Payment status tracking
- Payment retry logic
- Payment history
- Order status synchronization on payment success
- Payment gateway integration

The module is **not** responsible for:
- Order creation (handled by Order module)
- Cart management (handled by Cart module)
- Refund processing (deferred to future implementation)
- Payment gateway provider selection (currently hardcoded to Razorpay)

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
└── payment/
    ├── dependencies.py
    ├── exceptions.py
    ├── mapper.py
    ├── models/
    │   └── payment.py
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
- Payment initiation workflow
- Payment verification workflow
- Payment retry logic
- Business validations
- Transaction management
- Order status updates
- Payment gateway selection
- Gateway transaction verification

The service owns all payment business logic.

---

## repository.py

Responsibilities:
- Database access
- Query execution
- Entity persistence
- Payment listing by order
- Successful payment lookup

Repository rules:
- No business logic
- No commits
- Uses flush()
- Returns ORM models

---

## mapper.py

Responsibilities:
- ORM model to schema conversion
- Payment method mapping
- Payment status mapping
- Response transformation

The mapper isolates transformation logic from business logic.

---

## schemas.py

Contains:
- PaymentCreateRequest
- PaymentVerificationRequest
- PaymentRetryRequest
- PaymentInitiationResponse
- PaymentStatusResponse
- PaymentResponse
- PaymentHistoryResponse

Uses:
- Pydantic v2
- Field validation
- Literal types for enums
- Alias configuration for camelCase

---

## dependencies.py

Provides:
- PaymentRepository
- PaymentService

Dependencies only compose objects.

---

## exceptions.py

Defines domain-specific payment exceptions:
- PaymentAccessDeniedException
- PaymentAlreadySuccessfulException
- PaymentNotEligibleException
- PaymentNotFoundException
- PaymentRetryNotAllowedException
- PaymentVerificationFailedException

---

# Payment Flow

## Initiate Payment

```text
Client
    │
    ▼
POST /payments
    │
    ▼
PaymentService.create_payment()
    │
    ├── Retrieve Order
    ├── Validate Order Ownership
    ├── Validate Order is Payable
    │   (PENDING_PAYMENT status)
    ├── Check for Existing Successful Payment
    ├── Map Payment Method
    ├── Select Payment Gateway
    ├── Create Payment Entity
    ├── Save Payment
    ├── Commit Transaction
    ▼
Return PaymentInitiationResponse
```

---

## Verify Payment

```text
Client
    │
    ▼
POST /payments/{payment_id}/verify
    │
    ▼
PaymentService.verify_payment()
    │
    ├── Retrieve Payment
    ├── Validate Payment Ownership
    ├── Check Already Successful
    ├── Update Status to PROCESSING
    ├── Store Gateway Transaction ID
    ├── Verify with Gateway
    ├── If Verified:
    │   ├── Update Status to SUCCESS
    │   ├── Set Paid Timestamp
    │   ├── Update Order to CONFIRMED
    │   ├── Set Confirmed Timestamp
    │   └── Add Order Status History
    ├── If Failed:
    │   ├── Update Status to FAILED
    │   └── Set Failure Reason
    ├── Save Payment
    ├── Commit Transaction
    ▼
Return PaymentStatusResponse
```

---

## Retry Payment

```text
Client
    │
    ▼
POST /payments/{payment_id}/retry
    │
    ▼
PaymentService.retry_payment()
    │
    ├── Retrieve Payment
    ├── Validate Payment Ownership
    ├── Validate Payment is Failed
    ├── Retrieve Order
    ├── Validate Order is Payable
    ├── Map Payment Method
    ├── Select Payment Gateway
    ├── Create New Payment Entity
    ├── Save Payment
    ├── Commit Transaction
    ▼
Return PaymentInitiationResponse
```

---

# API Endpoints

## Initiate Payment

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/payments` | Yes |

Initiates a payment for an order.

---

## Get Payment

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/payments/{payment_id}` | Yes |

Returns detailed information for a specific payment.

---

## Verify Payment

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/payments/{payment_id}/verify` | Yes |

Verifies payment completion with the payment gateway.

---

## Get Payment Status

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/payments/{payment_id}/status` | Yes |

Returns the current status of a payment.

---

## Retry Payment

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/payments/{payment_id}/retry` | Yes |

Retries a failed payment by creating a new payment attempt.

---

## List Order Payments

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/orders/{order_id}/payments` | Yes |

Lists all payment attempts for a specific order.

---

# Business Rules

Implemented business rules:
- Payments can only be initiated for orders in PENDING_PAYMENT status
- Orders must have a positive grand total to be payable
- Customers can only access their own payments
- Only one successful payment per order
- Payment retry is only allowed for failed payments
- Successful payment automatically updates order to CONFIRMED status
- Payment verification requires gateway transaction ID
- Payment gateway is selected based on payment method (ONLINE → RAZORPAY, COD → None)
- Payment amount is always calculated from order grand_total (server-side)

---

# Payment Methods

Supported payment methods:
- **ONLINE** - Processed through payment gateway (Razorpay)
- **COD** - Cash on delivery (no gateway integration)

---

# Payment Lifecycle

Payments progress through the following statuses:

1. **INITIATED** - Payment record created, awaiting customer action
2. **PROCESSING** - Payment being verified with gateway
3. **SUCCESS** - Payment successfully completed
4. **FAILED** - Payment failed
5. **REFUND_PENDING** - Refund initiated (future)
6. **REFUNDED** - Refund completed (future)

---

# Exception Handling

Business exceptions:
- PaymentAccessDeniedException → 403 Forbidden
- PaymentAlreadySuccessfulException → 409 Conflict
- PaymentNotEligibleException → 400 Bad Request
- PaymentNotFoundException → 404 Not Found
- PaymentRetryNotAllowedException → 409 Conflict
- PaymentVerificationFailedException → 422 Unprocessable Entity

HTTP exceptions remain inside the router.

---

# Dependency Injection

Dependency providers:
```text
PaymentRepository

↓

PaymentService
```

Dependencies only compose objects.

No business logic is implemented inside dependencies.

---

# Transaction Management

The service layer controls transactions.

Example:
```text
Repository.create()

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
- Eager loading with selectinload

Repositories do not:
- Validate business rules
- Verify with payment gateway
- Commit transactions
- Raise HTTP exceptions

---

# Service Layer

The service layer owns:
- Payment initiation logic
- Payment verification logic
- Retry logic
- Order synchronization
- Gateway integration
- Transaction boundaries

This centralizes business logic and keeps routers thin.

---

# Mapper Pattern

The mapper handles:
- ORM to Pydantic schema conversion
- Payment method mapping (ONLINE/COD)
- Payment status mapping
- Response transformation with camelCase aliases

Benefits:
- Isolates transformation logic
- Keeps service layer focused on business logic
- Improves testability
- Handles API contract requirements

---

# Payment Gateway Integration

Current implementation:
- Hardcoded to Razorpay for ONLINE payments
- Gateway verification is simulated (checks if transaction ID is not empty)
- Future: Implement actual Razorpay SDK integration
- Future: Support multiple payment gateways
- Future: Gateway abstraction layer for provider switching

---

# Design Decisions

## Server-Side Amount Calculation

Payment amount is always from order grand_total because:
- Prevents client manipulation
- Ensures pricing consistency
- Maintains business logic ownership
- Security best practice

---

## Payment Retry Creates New Payment

Retry creates a new payment record instead of updating existing because:
- Preserves payment history
- Enables audit trail
- Prevents confusion about payment status
- Supports multiple retry attempts

---

## Order Status Synchronization

Successful payment automatically confirms order because:
- Maintains order lifecycle integrity
- Reduces manual intervention
- Provides immediate feedback
- Follows business workflow

---

## Gateway Transaction ID Required

Verification requires gateway transaction ID because:
- Prevents fraudulent payment claims
- Enables reconciliation with payment provider
- Supports audit requirements
- Security best practice

---

# Production Considerations

Current implementation includes:
- Payment initiation and verification
- Payment retry logic
- Order status synchronization
- Payment history tracking
- Transaction management
- Basic gateway integration (simulated)

Future improvements may include:
- Actual Razorpay SDK integration
- Multiple payment gateway support
- Refund processing
- Webhook handling for payment updates
- Payment analytics
- Fraud detection
- Payment method expansion (UPI, cards, wallets)
- Payment scheduling
- Partial payments
- Payment dispute handling

---

# Module Completion

Status: **Completed**

Implemented:
- Payment Infrastructure
- Payment Schemas
- Payment Repository
- Payment Service
- Payment Mapper
- Payment Dependencies
- Payment Router
- Router Integration
- Payment Initiation
- Payment Verification
- Payment Retry
- Payment Status Tracking
- Order Synchronization
- Gateway Integration (Basic)
