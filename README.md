# Deadlock Meta Intelligence API

A data-driven web API for analysing public Deadlock game data. The project ingests community data about heroes, matches and builds, stores it in a relational database, and exposes endpoints for querying hero performance, match trends, build references and user-defined reports.

## Project Goals

This project aims to:

- import and store public Deadlock data in a structured SQL database
- provide REST API endpoints for querying heroes, matches and builds
- support CRUD operations for custom builds and saved reports
- generate analytics such as hero overview, matchup statistics, synergy insights and trend reports

## Planned Features

- hero and item reference endpoints
- match listing and match detail endpoints
- community build search
- custom build CRUD
- saved report CRUD
- hero analytics endpoints
- trend and matchup analysis
- generated API documentation

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest

## Data Sources

This project uses publicly available Deadlock community data, including:

- Deadlock API
- Deadlock asset endpoints for heroes, items and ranks

## Repository Structure

```text
app/
docs/
scripts/
tests/
```
