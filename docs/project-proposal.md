# Project Proposal

## Project Title

Deadlock Meta Intelligence API

## Overview

This project is a Deadlock analytics web API built around publicly available community game data. It will collect and store structured information about heroes, matches, players and builds, then expose this information through a REST API for querying and analysis.

The project is intended to go beyond a basic CRUD API by combining database-backed storage, custom user-managed resources and analytical endpoints that reveal useful insights about the current game meta.

## Motivation

Deadlock is a strong topic for a data-driven API because it combines:

- structured hero and item metadata
- high-volume match statistics
- community-generated build information
- natural opportunities for analytics such as win rates, hero counters and synergy

This makes it suitable for demonstrating database design, API development, data processing and software engineering principles.

## Core Objectives

The project will:

1. import public Deadlock data into a relational database
2. provide clean API endpoints for base resources such as heroes, items and matches
3. support CRUD operations for user-created builds and saved reports
4. generate analytical summaries about hero performance and trends
5. provide clear API documentation and a technical explanation of design decisions

## Main Resources

### Imported Resources

- heroes
- items
- matches
- match participants
- community builds

### User-managed Resources

- custom builds
- saved reports

## Planned Analytics

The API will include analytical endpoints for:

- hero overview statistics
- hero matchup statistics
- hero synergy statistics
- time-based performance trends
- community build summaries

## Proposed Technology Stack

- FastAPI for the web API
- PostgreSQL for relational storage
- SQLAlchemy for ORM/database access
- Alembic for schema migrations
- Pytest for testing

## Expected Deliverables

- public GitHub repository with commit history
- runnable API project
- API documentation
- technical report
- presentation slides

## Data and Ethics Note

The project will use public community data only. Data sources will be cited in the technical report, and the project will make clear that it is not affiliated with or endorsed by Valve.
