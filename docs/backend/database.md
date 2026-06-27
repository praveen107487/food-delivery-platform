# Database Infrastructure

## Overview

The Food Delivery Platform uses **PostgreSQL** as its relational database and **SQLAlchemy 2.0 Async ORM** as the database access layer.

The database infrastructure is centralized inside the `app/infrastructure/database` package. This layer is responsible for creating and managing database connections, sessions, and transaction boundaries for the entire application.

All feature modules communicate with PostgreSQL through this shared infrastructure. Business modules must never create database connections directly.

---

# Architecture

```
FastAPI Request
       │
       ▼
Dependency Injection
       │
       ▼
AsyncSession
       │
       ▼
SQLAlchemy Engine
       │
       ▼
Connection Pool
       │
       ▼
PostgreSQL
```

The database infrastructure is part of the Infrastructure layer in the application's Platform-Oriented Modular Monolith architecture.

---

# Folder Structure

```
app/
└── infrastructure/
    └── database/
        ├── __init__.py
        ├── engine.py
        ├── session.py
        ├── dependencies.py
        └── health.py
```

## File Responsibilities

### engine.py

Creates and configures the shared SQLAlchemy Engine.

Responsibilities:

* Create the Engine
* Configure the PostgreSQL driver
* Configure connection pooling
* Provide a single Engine instance for the application

---

### session.py

Creates the Async Session Factory.

Responsibilities:

* Configure AsyncSession
* Create request-scoped sessions
* Configure transaction behavior

---

### dependencies.py

Provides FastAPI dependencies.

Responsibilities:

* Create an AsyncSession for each request
* Yield the session to the application
* Ensure proper cleanup after the request completes

---

### health.py

Provides database health utilities.

Responsibilities:

* Verify database connectivity
* Execute lightweight health-check queries
* Support future health endpoints

---

### **init**.py

Marks the directory as a Python package and exposes shared database infrastructure components when appropriate.

---

# Request Lifecycle

Every incoming HTTP request follows the lifecycle below.

```
HTTP Request

↓

Create AsyncSession

↓

Borrow Connection From Pool

↓

Execute SQL Operations

↓

Commit or Rollback

↓

Close Session

↓

Return Connection To Pool

↓

HTTP Response
```

Each request receives its own database session.

Database sessions are never shared between concurrent requests.

---

# Transaction Management

Database operations are executed inside a transaction.

If every operation succeeds:

```
BEGIN

↓

Business Operations

↓

COMMIT
```

If an error occurs:

```
BEGIN

↓

Business Operations

↓

ERROR

↓

ROLLBACK
```

This guarantees that partial changes are never persisted to the database.

---

# Connection Pool

The SQLAlchemy Engine manages a pool of reusable PostgreSQL connections.

Instead of creating a new physical database connection for every request:

1. A connection is borrowed from the pool.
2. The request performs its database operations.
3. The connection is returned to the pool.

This significantly reduces connection overhead and improves application scalability.

---

# Session Lifecycle

The AsyncSession represents a single unit of work.

A session is:

* Created when a request begins
* Used for all database operations during that request
* Committed or rolled back
* Closed after the request completes

A session should never be reused across multiple HTTP requests.

---

# Design Principles

The database infrastructure follows these principles:

* One SQLAlchemy Engine per application.
* One AsyncSession per request.
* Engine-managed connection pooling.
* Dependency Injection for session management.
* Infrastructure separated from business logic.
* Transaction boundaries managed by AsyncSession.
* Shared infrastructure reused by all feature modules.

---

# Future Extensions

This infrastructure provides the foundation for future backend modules, including:

* SQLAlchemy ORM Models
* Alembic Database Migrations
* Repository Layer
* Authentication
* Order Processing
* Payment Management
* Integration Testing
* Production Monitoring

No business logic should be implemented inside the database infrastructure layer.
