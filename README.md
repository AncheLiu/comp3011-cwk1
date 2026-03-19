# Deadlock Meta Intelligence API

A data-driven web API for analysing public Deadlock game data. The project ingests community data about heroes, items and matches, stores it in a relational database, and exposes endpoints for querying hero performance, match trends, matchup statistics and user-defined resources.

## API Documentation

Formal API documentation is provided in:

- [Markdown API documentation](G:\uni_course\comp3011 web services\cwk1\comp3011-cwk1\docs\api-documentation.md)
- PDF API documentation at `docs/api-documentation.pdf` once exported for submission

Interactive OpenAPI documentation is also available through FastAPI:

- local: `http://127.0.0.1:8000/docs`
- deployed: [Render Swagger UI](https://deadlock-meta-intelligence-api-tjzo.onrender.com/docs)

## Submission Documents

- API documentation: `docs/api-documentation.pdf`
- Technical report: `docs/technical-report.pdf`
- GenAI supplementary material: `docs/genai-supplementary.pdf`
- Presentation slides: `docs/Anche Liu.pptx`

## Project Goals

This project aims to:

- import and store public Deadlock data in a structured SQL database
- provide REST API endpoints for querying heroes, matches and builds
- support CRUD operations for custom builds and saved reports
- generate analytics such as hero overview, matchup statistics, synergy insights and trend reports

## Current Features

- hero reference endpoints
- item listing endpoint
- match list and match detail endpoints
- community build list and detail endpoints
- community build cloning into editable custom builds
- custom build CRUD
- saved report CRUD and result generation
- hero meta analytics
- hero overview analytics
- hero trend analytics
- hero matchup analytics
- hero synergy analytics
- import scripts for heroes, items, recent matches and community builds
- automated API test coverage

## Implemented Endpoints

### Core

- `GET /`
- `GET /health`
- `GET /heroes`
- `GET /heroes/{hero_id}`
- `GET /items`
- `GET /matches`
- `GET /matches/{match_id}`
- `GET /community-builds`
- `GET /community-builds/{id}`
- `POST /community-builds/{id}/clone-to-custom`

### Custom Builds

- `POST /custom-builds`
- `GET /custom-builds`
- `GET /custom-builds/{id}`
- `PUT /custom-builds/{id}`
- `DELETE /custom-builds/{id}`

Custom builds now use a relational structure:

- `custom_builds` stores top-level build metadata
- `custom_build_items` stores ordered item entries
- `custom_build_abilities` stores ordered ability progression entries

This keeps the build model easier to extend for later PostgreSQL deployment and more advanced build comparison features.

### Saved Reports

- `POST /saved-reports`
- `GET /saved-reports`
- `GET /saved-reports/{id}`
- `GET /saved-reports/{id}/result`
- `PATCH /saved-reports/{id}`
- `DELETE /saved-reports/{id}`

### Analytics

- `GET /analytics/heroes/meta`
- `GET /analytics/heroes/{hero_id}/overview`
- `GET /analytics/heroes/{hero_id}/trend`
- `GET /analytics/heroes/{hero_id}/matchups`
- `GET /analytics/heroes/{hero_id}/synergies`

## Next Planned Features

- analytics filters such as region-based summaries
- community build summary analytics

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
G:\python\python.exe scripts/import_community_builds.py --hero-limit 3 --per-hero-limit 5
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
