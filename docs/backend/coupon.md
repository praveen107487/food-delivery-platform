# Module 8 – Coupon

## Module Overview

The Coupon module provides promotional discount functionality for the Food Delivery Platform. It is responsible for validating coupon codes, enforcing coupon business rules, and calculating the applicable discount for a customer's cart.

This module is designed as an **internal business module**. It does not expose public API endpoints of its own. Instead, it is consumed by the Cart module during coupon application and will later be reused by the Order module during checkout to perform final coupon validation before order creation.

---

# Objectives

* Validate coupon codes.
* Support Platform Coupons.
* Support Restaurant Coupons.
* Enforce coupon business rules.
* Calculate discounts.
* Integrate with Cart module.
* Provide reusable business logic for Checkout.

---

# Responsibilities

The Coupon module is responsible for:

* Coupon lookup.
* Coupon validation.
* Restaurant ownership verification.
* Coupon validity period verification.
* Coupon status verification.
* Minimum order amount validation.
* Discount calculation.

The module is **not responsible** for:

* Creating coupons.
* Updating coupons.
* Deleting coupons.
* Managing coupon campaigns.

Those features belong to future Admin and Restaurant Portal modules.

---

# Architecture

```
coupon
│
├── models
│   ├── platform_coupon.py
│   └── restaurant_coupon.py
│
├── repository.py
├── service.py
├── dependencies.py
├── exceptions.py
└── __init__.py
```

Architecture follows the same layered approach used throughout the backend.

```
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

The Customer application does not directly communicate with this module.

Instead:

```
Cart Router
      ↓
Cart Service
      ↓
Coupon Service
      ↓
Coupon Repository
```

---

# Coupon Types

## Platform Coupon

A Platform Coupon can be applied to any eligible restaurant.

Examples

* WELCOME50
* FREEDELIVERY
* SAVE100

Characteristics

* Managed by Platform.
* Valid across restaurants.
* No restaurant ownership validation.

---

## Restaurant Coupon

Restaurant Coupons are issued by a specific restaurant.

Examples

* PIZZA20
* BURGER100
* CAFE50

Characteristics

* Restaurant-specific.
* Can only be applied to carts belonging to the same restaurant.

---

# Coupon Validation Flow

```
Customer enters coupon
            │
            ▼
CouponService.validate_coupon()
            │
            ▼
Find coupon
            │
            ▼
Coupon exists?
            │
     No ───────► CouponNotFoundException
            │
           Yes
            │
Coupon ACTIVE?
            │
     No ───────► CouponInactiveException
            │
           Yes
            │
Within validity period?
            │
     No ───────► CouponExpiredException /
                 CouponNotYetActiveException
            │
           Yes
            │
Minimum order met?
            │
     No ───────► MinimumOrderAmountNotMetException
            │
           Yes
            │
Restaurant matches?
            │
     No ───────► RestaurantCouponMismatchException
            │
           Yes
            │
Coupon Valid
```

---

# Discount Calculation

Two discount strategies are supported.

## Percentage Discount

```
Discount = Subtotal × Percentage / 100
```

Example

```
Subtotal = ₹800

Coupon = 20%

Discount = ₹160
```

---

## Fixed Amount Discount

```
Subtotal = ₹700

Coupon = ₹150 OFF

Discount = ₹150
```

---

# Discount Safety Rules

The calculated discount is constrained to avoid invalid pricing.

Rules

* Discount cannot be negative.
* Discount cannot exceed subtotal.
* Final value rounded to two decimal places.

---

# Business Rules

## Coupon Exists

Coupon code must exist.

Failure

```
CouponNotFoundException
```

---

## Coupon Status

Only ACTIVE coupons are accepted.

Failure

```
CouponInactiveException
```

---

## Validity Period

Current UTC time must satisfy

```
valid_from <= now <= valid_until
```

Failures

* CouponNotYetActiveException
* CouponExpiredException

---

## Minimum Order Amount

Subtotal must satisfy

```
subtotal >= minimum_order_amount
```

Failure

```
MinimumOrderAmountNotMetException
```

---

## Restaurant Validation

Restaurant Coupons must belong to the same restaurant as the customer's cart.

Failure

```
RestaurantCouponMismatchException
```

---

# Cart Integration

Coupon APIs are exposed through the Cart module.

Available endpoints

```
POST   /api/v1/cart/coupon
DELETE /api/v1/cart/coupon
```

Flow

```
Cart Router
      ↓
Cart Service
      ↓
Coupon Service
      ↓
Coupon Repository
```

---

# Automatic Coupon Refresh

Whenever cart contents change, the applied coupon is automatically revalidated.

Triggered after

* Add Item
* Update Quantity
* Remove Item
* Clear Cart

If the coupon becomes invalid

* Coupon removed automatically.
* Discount reset to zero.

This prevents stale discount values.

---

# Exception Hierarchy

```
CouponException
│
├── CouponNotFoundException
├── CouponInactiveException
├── CouponExpiredException
├── CouponNotYetActiveException
├── MinimumOrderAmountNotMetException
└── RestaurantCouponMismatchException
```

---

# Dependency Injection

```
CouponRepository
        │
        ▼
CouponService
        │
        ▼
CartService
```

The Coupon module remains independent and reusable.

---

# Design Decisions

## Internal Module

The Coupon module does not expose public customer endpoints.

Reason

Coupons are meaningful only within the context of a Cart or Checkout.

---

## Reusable Service

Business logic is centralized inside CouponService.

Advantages

* Single source of truth.
* No duplicated validation.
* Reusable by Checkout.
* Easier maintenance.

---

## No Coupon Router

There is intentionally no

```
coupon/router.py
```

Customer operations occur through Cart.

Future Admin modules may introduce

```
/admin/coupons
```

or

```
/restaurants/{id}/coupons
```

for coupon management.

---

# Future Usage

During Module 9 (Order & Checkout)

The Order module will:

1. Receive the applied coupon.
2. Revalidate it.
3. Calculate the final discount.
4. Snapshot coupon information into the Order.
5. Persist immutable pricing.

This guarantees pricing consistency even if coupons change later.

---

# Summary

The Coupon module provides a centralized implementation for coupon validation and discount calculation while remaining independent from presentation logic.

It supports both Platform and Restaurant coupons, integrates seamlessly with the Cart module, and is designed for reuse during Checkout. The module enforces all coupon business rules through a dedicated service layer, ensuring consistent behavior across the application while keeping the customer-facing API simple and maintainable.
