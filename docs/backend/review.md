# Module 10 – Review

## Overview

The Review module is responsible for **customer feedback management** in the Food Delivery Platform.

It provides customer-facing APIs for:
- Creating restaurant reviews
- Creating food item reviews
- Updating restaurant reviews
- Updating food item reviews
- Deleting restaurant reviews
- Deleting food item reviews
- Listing restaurant reviews
- Listing food item reviews
- Uploading review images
- Deleting review images
- Listing review images

This module follows the standard layered architecture using the Repository Pattern, Service Layer, and Dependency Injection. It supports two types of reviews: restaurant reviews and food item reviews.

---

# Responsibilities

The Review module is responsible for:
- Restaurant review CRUD operations
- Food item review CRUD operations
- Review image management
- Review listing with pagination
- Duplicate review prevention
- Rating validation

The module is **not** responsible for:
- Order validation (assumes order exists)
- Order eligibility verification (deferred to future implementation)
- Rating aggregation (deferred to future implementation)
- Review moderation (deferred to future implementation)

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
└── review/
    ├── dependencies.py
    ├── exceptions.py
    ├── mapper.py
    ├── models/
    │   ├── food_item_review.py
    │   ├── food_item_review_image.py
    │   ├── restaurant_review.py
    │   └── restaurant_review_image.py
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
- Restaurant review CRUD workflow
- Food item review CRUD workflow
- Review image management
- Business validations
- Transaction management
- Duplicate review prevention

The service owns all review business logic.

---

## repository.py

Responsibilities:
- Database access
- Query execution
- Entity persistence
- Review listing with pagination
- Review image operations
- Join queries for restaurant and menu item filtering

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
- Image response transformation

The mapper isolates transformation logic from business logic.

---

## schemas.py

Contains:
- RestaurantReviewBase
- CreateRestaurantReviewRequest
- UpdateRestaurantReviewRequest
- RestaurantReviewResponse
- RestaurantReviewListResponse
- FoodItemReviewBase
- CreateFoodItemReviewRequest
- UpdateFoodItemReviewRequest
- FoodItemReviewResponse
- FoodItemReviewListResponse
- ReviewImageResponse
- UploadReviewImageResponse

Uses:
- Pydantic v2
- Field validation
- Rating range validation (1-5)
- from_attributes configuration

---

## dependencies.py

Provides:
- ReviewRepository
- ReviewService

Dependencies only compose objects.

---

## exceptions.py

Defines domain-specific review exceptions:
- FoodItemReviewAlreadyExistsException
- FoodItemReviewImageNotFoundException
- FoodItemReviewNotFoundException
- RestaurantReviewAlreadyExistsException
- RestaurantReviewImageNotFoundException
- RestaurantReviewNotFoundException

---

# Review Flow

## Create Restaurant Review

```text
Client
    │
    ▼
POST /reviews/restaurants
    │
    ▼
ReviewService.create_restaurant_review()
    │
    ├── Check for Existing Review by Order
    ├── Convert Request to Review
    ├── Save Review
    ├── Commit Transaction
    ▼
Return RestaurantReviewResponse
```

---

## Create Food Item Review

```text
Client
    │
    ▼
POST /reviews/food-items
    │
    ▼
ReviewService.create_food_item_review()
    │
    ├── Check for Existing Review by Order Item
    ├── Convert Request to Review
    ├── Save Review
    ├── Commit Transaction
    ▼
Return FoodItemReviewResponse
```

---

## Upload Review Image

```text
Client
    │
    ▼
POST /reviews/restaurants/{review_id}/images
    │
    ▼
ReviewService.upload_restaurant_review_image()
    │
    ├── Validate Review Exists
    ├── Create Image Entity
    ├── Save Image
    ├── Commit Transaction
    ▼
Return ReviewImageResponse
```

---

# API Endpoints

## Create Restaurant Review

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/reviews/restaurants` | Yes |

Creates a restaurant review for an order.

---

## Update Restaurant Review

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| PATCH | `/api/v1/reviews/restaurants/{review_id}` | Yes |

Updates an existing restaurant review.

---

## Delete Restaurant Review

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| DELETE | `/api/v1/reviews/restaurants/{review_id}` | Yes |

Deletes a restaurant review.

---

## List Restaurant Reviews

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/reviews/restaurants` | No |

Lists restaurant reviews with pagination.

---

## Create Food Item Review

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/reviews/food-items` | Yes |

Creates a food item review for an order item.

---

## Update Food Item Review

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| PATCH | `/api/v1/reviews/food-items/{review_id}` | Yes |

Updates an existing food item review.

---

## Delete Food Item Review

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| DELETE | `/api/v1/reviews/food-items/{review_id}` | Yes |

Deletes a food item review.

---

## List Food Item Reviews

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/reviews/food-items` | No |

Lists food item reviews with pagination.

---

## Upload Restaurant Review Image

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/reviews/restaurants/{review_id}/images` | Yes |

Uploads an image for a restaurant review.

---

## List Restaurant Review Images

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/reviews/restaurants/{review_id}/images` | No |

Lists all images for a restaurant review.

---

## Delete Restaurant Review Image

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| DELETE | `/api/v1/reviews/restaurants/images/{image_id}` | Yes |

Deletes a restaurant review image.

---

## Upload Food Item Review Image

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| POST | `/api/v1/reviews/food-items/{review_id}/images` | Yes |

Uploads an image for a food item review.

---

## List Food Item Review Images

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| GET | `/api/v1/reviews/food-items/{review_id}/images` | No |

Lists all images for a food item review.

---

## Delete Food Item Review Image

| Method | Endpoint | Authentication |
|----------|----------|----------------|
| DELETE | `/api/v1/reviews/food-items/images/{image_id}` | Yes |

Deletes a food item review image.

---

# Business Rules

Implemented business rules:
- One restaurant review per order
- One food item review per order item
- Ratings must be between 1 and 5
- Restaurant reviews include restaurant rating and delivery rating
- Food item reviews include single rating
- Reviews are ordered by creation date (newest first)
- Review images are ordered by upload date (oldest first)
- Review listing uses pagination
- Restaurant reviews are filtered by restaurant_id via order join
- Food item reviews are filtered by menu_item_id via order_item join

---

# Review Types

The module supports two types of reviews:

## Restaurant Review
- Linked to an order
- Includes restaurant rating (1-5)
- Includes delivery rating (1-5)
- Includes title and description
- Supports multiple images

## Food Item Review
- Linked to an order item
- Includes single rating (1-5)
- Includes title and description
- Supports multiple images

---

# Exception Handling

Business exceptions:
- RestaurantReviewAlreadyExistsException → 409 Conflict
- RestaurantReviewNotFoundException → 404 Not Found
- RestaurantReviewImageNotFoundException → 404 Not Found
- FoodItemReviewAlreadyExistsException → 409 Conflict
- FoodItemReviewNotFoundException → 404 Not Found
- FoodItemReviewImageNotFoundException → 404 Not Found

HTTP exceptions remain inside the router.

---

# Dependency Injection

Dependency providers:
```text
ReviewRepository

↓

ReviewService
```

Dependencies only compose objects.

No business logic is implemented inside dependencies.

---

# Transaction Management

The service layer controls transactions.

Example:
```text
Repository.create_restaurant_review()

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
- Join queries for filtering
- Pagination support

Repositories do not:
- Validate business rules
- Verify order eligibility
- Commit transactions
- Raise HTTP exceptions

---

# Service Layer

The service layer owns:
- Review creation logic
- Review update logic
- Review deletion logic
- Image management
- Duplicate prevention
- Transaction boundaries

This centralizes business logic and keeps routers thin.

---

# Mapper Pattern

The mapper handles:
- ORM to Pydantic schema conversion
- Schema to ORM conversion
- Partial update application
- Image response transformation

Benefits:
- Isolates transformation logic
- Keeps service layer focused on business logic
- Improves testability

---

# Design Decisions

## Separate Review Types

Restaurant and food item reviews are separate entities because:
- Different rating structures (restaurant has 2 ratings, food has 1)
- Different linkage (restaurant → order, food → order_item)
- Different use cases in UI
- Independent lifecycle

---

## Duplicate Prevention

One review per order/order_item because:
- Prevents spam reviews
- Ensures fair representation
- Simplifies rating calculation
- Improves data quality

---

## Review Images as Separate Entity

Images are separate from reviews because:
- Supports multiple images per review
- Independent image lifecycle
- Easier image management
- Future image processing capabilities

---

## Public Review Access

Review listing endpoints don't require authentication because:
- Helps customers make informed decisions
- Improves platform transparency
- Standard practice for review systems
- No sensitive data exposure

---

# Production Considerations

Current implementation includes:
- Restaurant review CRUD
- Food item review CRUD
- Review image management
- Duplicate prevention
- Rating validation
- Pagination support
- Transaction management

Future improvements may include:
- Order eligibility verification (delivered orders only)
- Rating aggregation and average calculation
- Review moderation system
- Review flagging/reporting
- Review helpfulness voting
- Review sorting options (most helpful, recent, highest rated)
- Image compression and optimization
- Image moderation
- Review analytics
- Review response from restaurants
- Review editing time window
- Review deletion policy
