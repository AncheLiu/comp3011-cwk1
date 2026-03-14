# API Draft

## Overview

This document outlines the implemented and planned REST API for the Deadlock Meta Intelligence API project.

The API is divided into three groups:

- base resource endpoints
- CRUD endpoints for user-managed resources
- analytics endpoints

All responses will use JSON.

Implemented endpoints in this document are marked as `Implemented`. Endpoints that are still part of the roadmap are marked as `Planned`.

## Error Response Format

Errors should use a consistent structure:

```json
{
  "error": {
    "code": "HERO_NOT_FOUND",
    "message": "Hero with id 999 was not found"
  }
}
```

Common status codes:

- `400 Bad Request`
- `404 Not Found`
- `409 Conflict`
- `422 Unprocessable Entity`
- `500 Internal Server Error`

## Base Resource Endpoints

### `GET /heroes` `Implemented`

Returns a list of heroes currently stored in the local database.

Example response:

```json
[
  {
    "id": 1,
    "name": "Infernus",
    "hero_type": "marksman",
    "complexity": 1,
    "image_small_url": "https://..."
  }
]
```

### `GET /heroes/{hero_id}` `Implemented`

Returns detailed information for a single hero.

Example response:

```json
{
  "id": 1,
  "name": "Infernus",
  "class_name": "hero_inferno",
  "role_text": "Lights up enemies and watches them burn",
  "playstyle_text": "Damage over time hero",
  "hero_type": "marksman",
  "complexity": 1
}
```

### `GET /items` `Implemented`

Returns a list of items and abilities currently stored in the local database.

### `GET /matches` `Planned`

Returns a paginated list of matches.

Query parameters:

- `hero_id`
- `region_mode`
- `game_mode`
- `date_from`
- `date_to`
- `limit`
- `offset`

Example response:

```json
{
  "items": [
    {
      "id": 66396892,
      "start_time": "2026-03-12T10:30:35Z",
      "region_mode": "row",
      "game_mode": "normal",
      "duration_seconds": 2140,
      "winning_team": 1
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

### `GET /matches/{match_id}` `Planned`

Returns detailed match information including participants.

Example response:

```json
{
  "id": 66396892,
  "start_time": "2026-03-12T10:30:35Z",
  "region_mode": "row",
  "participants": [
    {
      "account_id": 236599146,
      "hero_id": 1,
      "team": 1,
      "player_kills": 12,
      "player_deaths": 5,
      "player_assists": 9,
      "net_worth": 21500
    }
  ]
}
```

### `GET /community-builds` `Planned`

Returns community builds imported from public sources.

Query parameters:

- `hero_id`
- `name`
- `language`
- `sort_by`
- `limit`
- `offset`

## CRUD Endpoints

### `POST /custom-builds` `Implemented`

Creates a new custom build.

Example request body:

```json
{
  "title": "Afterburn Rush Build",
  "hero_id": 1,
  "author_name": "student",
  "playstyle_tag": "damage_over_time",
  "description": "Focus on sustained burn damage",
  "items_json": [968099481, 2081037738, 2480592370],
  "ability_order_json": [1593133799, 491391007, 3516947824],
  "notes": "Use against squishy teams"
}
```

### `GET /custom-builds` `Implemented`

Returns all custom builds currently stored in the local database.

### `GET /custom-builds/{id}` `Implemented`

Returns a single custom build.

### `PUT /custom-builds/{id}` `Implemented`

Updates an existing custom build.

### `DELETE /custom-builds/{id}` `Implemented`

Deletes a custom build.

Example response:

```json
{
  "message": "Custom build deleted successfully"
}
```

### `POST /saved-reports` `Implemented`

Creates a saved report definition.

Example request body:

```json
{
  "name": "Infernus Europe Meta Report",
  "report_type": "hero_meta",
  "hero_id": 1,
  "region_mode": "europe",
  "rank_min": 7,
  "rank_max": 11,
  "date_from": "2026-02-01",
  "date_to": "2026-03-01",
  "filters_json": {
    "min_matches": 50
  }
}
```

### `GET /saved-reports` `Implemented`

Returns saved report definitions.

### `GET /saved-reports/{id}` `Implemented`

Returns a single saved report definition.

### `PATCH /saved-reports/{id}` `Implemented`

Partially updates a saved report.

### `DELETE /saved-reports/{id}` `Implemented`

Deletes a saved report.

## Analytics Endpoints

### `GET /analytics/heroes/meta` `Planned`

Returns high-level hero meta data.

Query parameters:

- `region_mode`
- `date_from`
- `date_to`
- `sort_by`
- `limit`

Example response:

```json
{
  "items": [
    {
      "hero_id": 1,
      "hero_name": "Infernus",
      "matches": 435413,
      "wins": 212265,
      "losses": 223148,
      "win_rate": 48.75,
      "avg_kills": 7.55,
      "avg_deaths": 7.31,
      "avg_assists": 11.21
    }
  ]
}
```

### `GET /analytics/heroes/{hero_id}/overview` `Implemented`

Returns summary performance metrics for a hero, including matches, wins, losses, win rate, average kills, average deaths, average assists and average net worth.

### `GET /analytics/heroes/{hero_id}/trend` `Implemented`

Returns time-based hero trend data grouped by day.

Query parameters:

- `date_from`
- `date_to`

### `GET /analytics/heroes/{hero_id}/matchups` `Implemented`

Returns matchup performance against enemy heroes.

### `GET /analytics/heroes/{hero_id}/synergies` `Planned`

Returns synergy performance with allied heroes.

### `GET /analytics/heroes/{hero_id}/community-build-summary` `Planned`

Returns a summary of popular community builds for a hero.

### `POST /analytics/generate-report` `Planned`

Generates a report summary based on the provided filter set.

Example request body:

```json
{
  "report_type": "hero_meta",
  "hero_id": 1,
  "region_mode": "europe",
  "date_from": "2026-02-01",
  "date_to": "2026-03-01"
}
```
