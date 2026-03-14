# Deadlock Meta Intelligence API

A data-driven web API for analysing public Deadlock game data. The project ingests community data about heroes, items and matches, stores it in a relational database, and exposes endpoints for querying hero performance, match trends, matchup statistics and user-defined resources.

## Project Goals

This project aims to:

- import and store public Deadlock data in a structured SQL database
- provide REST API endpoints for querying heroes, matches and builds
- support CRUD operations for custom builds and saved reports
- generate analytics such as hero overview, matchup statistics, synergy insights and trend reports

## Current Features

- hero reference endpoints
- item listing endpoint
- custom build CRUD
- saved report CRUD and result generation
- hero overview analytics
- hero trend analytics
- hero matchup analytics
- import scripts for heroes, items and recent matches
- automated API test coverage

## Implemented Endpoints

### Core

- `GET /`
- `GET /health`
- `GET /heroes`
- `GET /heroes/{hero_id}`
- `GET /items`

### Custom Builds

- `POST /custom-builds`
- `GET /custom-builds`
- `GET /custom-builds/{id}`
- `PUT /custom-builds/{id}`
- `DELETE /custom-builds/{id}`

### Saved Reports

- `POST /saved-reports`
- `GET /saved-reports`
- `GET /saved-reports/{id}`
- `GET /saved-reports/{id}/result`
- `PATCH /saved-reports/{id}`
- `DELETE /saved-reports/{id}`

### Analytics

- `GET /analytics/heroes/{hero_id}/overview`
- `GET /analytics/heroes/{hero_id}/trend`
- `GET /analytics/heroes/{hero_id}/matchups`

## Next Planned Features

- match listing and match detail endpoints
- broader analytics endpoints such as hero meta summaries
- PostgreSQL deployment configuration

## Tech Stack

- FastAPI
- SQLite for local development
- PostgreSQL as the intended target deployment database
- SQLAlchemy
- Pydantic
- Pytest

## Data Sources

This project uses publicly available Deadlock community data, including:

- Deadlock API
- Deadlock asset endpoints for heroes, items and ranks

## Data Import Scripts

Run these from the project root:

```bash
G:\python\python.exe scripts/import_heroes.py
G:\python\python.exe scripts/import_items.py
G:\python\python.exe scripts/import_matches.py --limit 5
```

These scripts import public Deadlock reference and match data into the local database before the analytics endpoints are queried.

## Repository Structure

```text
app/
docs/
scripts/
tests/
```

## Test Status

The current automated API test suite passes locally with:

```bash
G:\python\python.exe -m pytest
```
