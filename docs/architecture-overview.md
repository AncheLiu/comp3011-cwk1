# Architecture Overview

## System Goal

The project is designed as a data-driven web API for Deadlock analytics. It combines public community data, user-managed resources and derived analytics in a single backend service.

## High-level Structure

The application is organised into these main layers:

- `app/api`
- `app/core`
- `app/db`
- `app/models`
- `app/schemas`
- `app/repositories`
- `app/services`
- `app/tasks`

## Layer Responsibilities

### `app/api`

Defines API routes and request entry points.

Responsibilities:

- expose REST endpoints
- validate request flow
- connect HTTP requests to business logic

### `app/core`

Stores application configuration and global settings.

Responsibilities:

- settings management
- environment configuration
- application-level constants

### `app/db`

Defines database infrastructure.

Responsibilities:

- SQLAlchemy base
- engine creation
- session management

### `app/models`

Contains ORM models that represent the database schema.

Responsibilities:

- define tables
- define relationships
- represent persisted application state

### `app/schemas`

Contains Pydantic models for request and response validation.

Responsibilities:

- shape API input and output
- separate internal ORM models from external API contracts

### `app/repositories`

Will contain reusable database access logic.

Responsibilities:

- encapsulate common queries
- reduce repeated database access code

### `app/services`

Will contain business and analytics logic.

Responsibilities:

- calculate hero statistics
- generate derived reports
- combine multiple repository operations

### `app/tasks`

Will contain background-style tasks and import logic.

Responsibilities:

- import public data
- precompute analytics tables
- refresh cached or aggregated data

## Data Design Strategy

The database design follows four categories:

- static reference data
- imported match fact data
- user-managed CRUD data
- precomputed analytics data

This is intended to support both coursework requirements and practical API performance.

## Why This Structure Was Chosen

This structure was chosen because it:

- separates concerns clearly
- supports incremental development
- makes testing easier
- makes technical decisions easier to explain in the report and oral exam

## Database Environment Strategy

The project currently supports SQLite for local development because it reduces setup overhead during early implementation.

PostgreSQL is still the intended target database for a more production-style deployment because it is more suitable for:

- relational integrity
- more realistic backend deployment
- future analytics expansion

## Implemented Architecture Notes

The current implementation already includes:

- route modules for heroes, items, custom builds, saved reports and analytics
- SQLAlchemy models for heroes, items, matches, match participants, custom builds and saved reports
- import scripts for heroes, items and recent match samples
- analytics endpoints built directly on the imported match fact tables
- isolated API tests using a shared in-memory SQLite test database

## Future Architectural Extensions

Planned future improvements include:

- repository layer implementation
- service layer for hero analytics
- broader ETL coverage and refresh jobs
- precomputed analytics jobs
- migration support using Alembic
