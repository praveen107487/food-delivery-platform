# Food Delivery Platform - API Reference

This document provides a comprehensive overview of all API endpoints available in the Food Delivery Platform backend.

## Base URL

```
http://localhost:8000
```

## API Version

```
/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

# Authentication Endpoints

## Register Customer

```http
POST /api/v1/auth/register
```

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "customer@example.com",
  "phone_number": "+1234567890",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**: AuthenticatedCustomerResponse

**Status Code**: 201 Created

---

## Login

```http
POST /api/v1/auth/login
```

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "customer@example.com",
  "password": "securepassword"
}
```

**Response**: TokenResponse (contains JWT access token)

**Status Code**: 200 OK

---

## Get Current Customer

```http
GET /api/v1/auth/me
```

**Authentication**: Required

**Response**: AuthenticatedCustomerResponse

**Status Code**: 200 OK

---

## Logout

```http
POST /api/v1/auth/logout
```

**Authentication**: Required

**Status Code**: 204 No Content

**Note**: Stateless JWT - client should discard the token

---

# Restaurant Endpoints

## Browse Restaurants

```http
GET /api/v1/restaurants
```

**Authentication**: Not required

**Query Parameters**:
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)
- `cuisine_type` (str, optional): Filter by cuisine type

**Response**: RestaurantListResponse

**Status Code**: 200 OK

---

## Search Restaurants

```http
GET /api/v1/restaurants/search
```

**Authentication**: Not required

**Query Parameters**:
- `keyword` (str, required): Search keyword
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)

**Response**: RestaurantListResponse

**Status Code**: 200 OK

---

## Get Restaurant Details

```http
GET /api/v1/restaurants/{restaurant_id}
```

**Authentication**: Not required

**Path Parameters**:
- `restaurant_id` (UUID): Restaurant ID

**Response**: RestaurantDetailResponse

**Status Code**: 200 OK

---

## Get Restaurant Menu

```http
GET /api/v1/restaurants/{restaurant_id}/menu-items
```

**Authentication**: Not required

**Path Parameters**:
- `restaurant_id` (UUID): Restaurant ID

**Query Parameters**:
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)

**Response**: MenuItemListResponse

**Status Code**: 200 OK

---

## Search Menu Items

```http
GET /api/v1/menu-items/search
```

**Authentication**: Not required

**Query Parameters**:
- `keyword` (str, required): Search keyword
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)

**Response**: MenuItemListResponse

**Status Code**: 200 OK

---

# Cart Endpoints

## Get Cart

```http
GET /api/v1/cart
```

**Authentication**: Required

**Response**: CartResponse

**Status Code**: 200 OK

---

## Add Item to Cart

```http
POST /api/v1/cart/items
```

**Authentication**: Required

**Query Parameters**:
- `menu_item_id` (UUID): Menu item ID
- `quantity` (int, required, min: 1)

**Response**: CartResponse

**Status Code**: 200 OK

---

## Update Cart Item

```http
PATCH /api/v1/cart/items/{cart_item_id}
```

**Authentication**: Required

**Path Parameters**:
- `cart_item_id` (UUID): Cart item ID

**Request Body**:
```json
{
  "quantity": 3
}
```

**Response**: CartResponse

**Status Code**: 200 OK

---

## Remove Cart Item

```http
DELETE /api/v1/cart/items/{cart_item_id}
```

**Authentication**: Required

**Path Parameters**:
- `cart_item_id` (UUID): Cart item ID

**Response**: CartResponse

**Status Code**: 200 OK

---

## Clear Cart

```http
DELETE /api/v1/cart
```

**Authentication**: Required

**Response**: CartResponse

**Status Code**: 200 OK

---

## Apply Coupon to Cart

```http
POST /api/v1/cart/coupon
```

**Authentication**: Required

**Request Body**:
```json
{
  "coupon_code": "SAVE20"
}
```

**Response**: CartResponse with applied discount

**Status Code**: 200 OK

---

## Remove Coupon from Cart

```http
DELETE /api/v1/cart/coupon
```

**Authentication**: Required

**Response**: CartResponse with discount removed

**Status Code**: 200 OK

---

# Coupon Endpoints

## Validate Coupon

```http
GET /api/v1/coupons/validate
```

**Authentication**: Required

**Query Parameters**:
- `coupon_code` (str): Coupon code to validate
- `restaurant_id` (UUID): Restaurant ID
- `subtotal` (float): Current cart subtotal

**Response**: CouponDetails or RestaurantCouponDetails

**Status Code**: 200 OK

**Error Responses**:
- 404: Coupon not found
- 400: Coupon inactive/expired/not yet active
- 400: Minimum order amount not met
- 400: Restaurant mismatch

---

# Customer Endpoints

## Get Profile

```http
GET /api/v1/customers/me
```

**Authentication**: Required

**Response**: CustomerResponse

**Status Code**: 200 OK

---

## Update Profile

```http
PATCH /api/v1/customers/me
```

**Authentication**: Required

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

**Response**: CustomerResponse

**Status Code**: 200 OK

---

## Create Saved Address

```http
POST /api/v1/customers/addresses
```

**Authentication**: Required

**Request Body**:
```json
{
  "label": "Home",
  "recipient_name": "John Doe",
  "phone_number": "+1234567890",
  "street": "123 Main St",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "delivery_instructions": "Ring doorbell",
  "is_default": true
}
```

**Response**: SavedAddressResponse

**Status Code**: 201 Created

---

## List Saved Addresses

```http
GET /api/v1/customers/addresses
```

**Authentication**: Required

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 20)

**Response**: SavedAddressListResponse

**Status Code**: 200 OK

---

## Get Saved Address

```http
GET /api/v1/customers/addresses/{address_id}
```

**Authentication**: Required

**Path Parameters**:
- `address_id` (UUID): Address ID

**Response**: SavedAddressResponse

**Status Code**: 200 OK

---

## Update Saved Address

```http
PATCH /api/v1/customers/addresses/{address_id}
```

**Authentication**: Required

**Path Parameters**:
- `address_id` (UUID): Address ID

**Request Body**:
```json
{
  "label": "Office",
  "recipient_name": "John Doe",
  "phone_number": "+1234567890",
  "street": "456 Work Ave",
  "city": "New York",
  "state": "NY",
  "postal_code": "10002",
  "delivery_instructions": "Leave at reception",
  "is_default": false
}
```

**Response**: SavedAddressResponse

**Status Code**: 200 OK

---

## Delete Saved Address

```http
DELETE /api/v1/customers/addresses/{address_id}
```

**Authentication**: Required

**Path Parameters**:
- `address_id` (UUID): Address ID

**Status Code**: 204 No Content

---

## Set Default Address

```http
PATCH /api/v1/customers/addresses/{address_id}/default
```

**Authentication**: Required

**Path Parameters**:
- `address_id` (UUID): Address ID

**Response**: SavedAddressResponse

**Status Code**: 200 OK

---

# Order Endpoints

## Place Order

```http
POST /api/v1/orders
```

**Authentication**: Required

**Request Body**:
```json
{
  "address_id": "uuid",
  "payment_method": "CREDIT_CARD",
  "delivery_instructions": "Leave at door"
}
```

**Response**: OrderDetailsResponse

**Status Code**: 201 Created

---

## Get Current Order

```http
GET /api/v1/orders/current
```

**Authentication**: Required

**Response**: OrderSummaryResponse

**Status Code**: 200 OK

---

## Get Order by ID

```http
GET /api/v1/orders/{order_id}
```

**Authentication**: Required

**Path Parameters**:
- `order_id` (UUID): Order ID

**Response**: OrderDetailsResponse

**Status Code**: 200 OK

---

## Get Order History

```http
GET /api/v1/orders/history
```

**Authentication**: Required

**Query Parameters**:
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)

**Response**: OrderListResponse

**Status Code**: 200 OK

---

# Payment Endpoints

## Create Payment

```http
POST /api/v1/payments
```

**Authentication**: Required

**Request Body**:
```json
{
  "order_id": "uuid",
  "payment_method": "CREDIT_CARD"
}
```

**Response**: PaymentInitiationResponse

**Status Code**: 201 Created

---

## Get Payment

```http
GET /api/v1/payments/{payment_id}
```

**Authentication**: Required

**Path Parameters**:
- `payment_id` (UUID): Payment ID

**Response**: PaymentResponse

**Status Code**: 200 OK

---

## Verify Payment

```http
POST /api/v1/payments/{payment_id}/verify
```

**Authentication**: Required

**Path Parameters**:
- `payment_id` (UUID): Payment ID

**Request Body**:
```json
{
  "transaction_reference": "txn_123456"
}
```

**Response**: PaymentStatusResponse

**Status Code**: 200 OK

---

## Get Payment Status

```http
GET /api/v1/payments/{payment_id}/status
```

**Authentication**: Required

**Path Parameters**:
- `payment_id` (UUID): Payment ID

**Response**: PaymentStatusResponse

**Status Code**: 200 OK

---

## Retry Payment

```http
POST /api/v1/payments/{payment_id}/retry
```

**Authentication**: Required

**Path Parameters**:
- `payment_id` (UUID): Payment ID

**Request Body**:
```json
{
  "payment_method": "CREDIT_CARD"
}
```

**Response**: PaymentInitiationResponse

**Status Code**: 200 OK

---

# Review Endpoints

## Create Restaurant Review

```http
POST /api/v1/reviews/restaurants
```

**Authentication**: Required

**Request Body**:
```json
{
  "order_id": "uuid",
  "title": "Great food!",
  "description": "The pizza was delicious",
  "restaurant_rating": 5,
  "delivery_rating": 4
}
```

**Response**: RestaurantReviewResponse

**Status Code**: 201 Created

---

## Update Restaurant Review

```http
PATCH /api/v1/reviews/restaurants/{review_id}
```

**Authentication**: Required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "restaurant_rating": 4,
  "delivery_rating": 5
}
```

**Response**: RestaurantReviewResponse

**Status Code**: 200 OK

---

## Delete Restaurant Review

```http
DELETE /api/v1/reviews/restaurants/{review_id}
```

**Authentication**: Required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Status Code**: 204 No Content

---

## List Restaurant Reviews

```http
GET /api/v1/reviews/restaurants/{restaurant_id}
```

**Authentication**: Not required

**Path Parameters**:
- `restaurant_id` (UUID): Restaurant ID

**Query Parameters**:
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)

**Response**: RestaurantReviewListResponse

**Status Code**: 200 OK

---

## Create Food Item Review

```http
POST /api/v1/reviews/food-items
```

**Authentication**: Required

**Request Body**:
```json
{
  "order_item_id": "uuid",
  "title": "Amazing burger",
  "description": "Juicy and flavorful",
  "rating": 5
}
```

**Response**: FoodItemReviewResponse

**Status Code**: 201 Created

---

## Update Food Item Review

```http
PATCH /api/v1/reviews/food-items/{review_id}
```

**Authentication**: Required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Request Body**:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "rating": 4
}
```

**Response**: FoodItemReviewResponse

**Status Code**: 200 OK

---

## Delete Food Item Review

```http
DELETE /api/v1/reviews/food-items/{review_id}
```

**Authentication**: Required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Status Code**: 204 No Content

---

## List Food Item Reviews

```http
GET /api/v1/reviews/food-items/{menu_item_id}
```

**Authentication**: Not required

**Path Parameters**:
- `menu_item_id` (UUID): Menu item ID

**Query Parameters**:
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)

**Response**: FoodItemReviewListResponse

**Status Code**: 200 OK

---

## Upload Restaurant Review Image

```http
POST /api/v1/reviews/restaurants/{review_id}/images
```

**Authentication**: Required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Request Body**:
```json
{
  "image_url": "https://example.com/image.jpg"
}
```

**Response**: ReviewImageResponse

**Status Code**: 201 Created

---

## List Restaurant Review Images

```http
GET /api/v1/reviews/restaurants/{review_id}/images
```

**Authentication**: Not required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Response**: list[ReviewImageResponse]

**Status Code**: 200 OK

---

## Delete Restaurant Review Image

```http
DELETE /api/v1/reviews/restaurants/images/{image_id}
```

**Authentication**: Required

**Path Parameters**:
- `image_id` (UUID): Image ID

**Status Code**: 204 No Content

---

## Upload Food Item Review Image

```http
POST /api/v1/reviews/food-items/{review_id}/images
```

**Authentication**: Required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Request Body**:
```json
{
  "image_url": "https://example.com/image.jpg"
}
```

**Response**: ReviewImageResponse

**Status Code**: 201 Created

---

## List Food Item Review Images

```http
GET /api/v1/reviews/food-items/{review_id}/images
```

**Authentication**: Not required

**Path Parameters**:
- `review_id` (UUID): Review ID

**Response**: list[ReviewImageResponse]

**Status Code**: 200 OK

---

## Delete Food Item Review Image

```http
DELETE /api/v1/reviews/food-items/images/{image_id}
```

**Authentication**: Required

**Path Parameters**:
- `image_id` (UUID): Image ID

**Status Code**: 204 No Content

---

# Notification Endpoints

## List Notifications

```http
GET /api/v1/notifications
```

**Authentication**: Required

**Query Parameters**:
- `page` (int, default: 1, min: 1)
- `page_size` (int, default: 20, min: 1, max: 100)
- `is_read` (bool, optional): Filter by read status
- `type` (NotificationType, optional): Filter by notification type

**Response**: NotificationListResponse

**Status Code**: 200 OK

---

## Get Notification

```http
GET /api/v1/notifications/{notification_id}
```

**Authentication**: Required

**Path Parameters**:
- `notification_id` (UUID): Notification ID

**Response**: NotificationResponse

**Status Code**: 200 OK

---

## Mark Notification as Read

```http
PATCH /api/v1/notifications/{notification_id}/read
```

**Authentication**: Required

**Path Parameters**:
- `notification_id` (UUID): Notification ID

**Response**: NotificationResponse

**Status Code**: 200 OK

---

## Mark All Notifications as Read

```http
PATCH /api/v1/notifications/read-all
```

**Authentication**: Required

**Response**: MarkAllNotificationsReadResponse

**Status Code**: 200 OK

---

# Health Check

## Database Connection Test

```http
GET /database-test
```

**Authentication**: Not required

**Response**: boolean (true if connected)

**Status Code**: 200 OK

---

# API Documentation

Interactive API documentation is available via Swagger UI:

```
http://localhost:8000/docs
```

ReDoc documentation is also available:

```
http://localhost:8000/redoc
```

---

# Error Responses

All endpoints may return standard error responses:

## 400 Bad Request
Invalid request data or validation error

## 401 Unauthorized
Missing or invalid authentication token

## 403 Forbidden
Valid authentication but insufficient permissions

## 404 Not Found
Resource not found

## 409 Conflict
Resource conflict (e.g., duplicate entry)

## 422 Unprocessable Entity
Request well-formed but contains semantic errors

## 500 Internal Server Error
Unexpected server error

---

# Rate Limiting

Rate limiting is not currently implemented but may be added in future updates.

---

# Pagination

Most list endpoints support pagination with the following parameters:

- `page`: Page number (starting from 1)
- `page_size`: Number of items per page (typically max 100)

Responses include:
- `total_count`: Total number of items
- `page`: Current page number
- `page_size`: Items per page
