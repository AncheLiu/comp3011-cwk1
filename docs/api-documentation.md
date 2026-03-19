# Deadlock Meta Intelligence API Documentation

## 1. Overview

Deadlock Meta Intelligence API is a FastAPI-based web service for importing, storing, and analysing public Deadlock community data. The system combines imported reference data, imported match data, user-managed build data, and analytics endpoints in a single REST API.

This API supports:

- imported hero, item, match, and community build resources
- relational custom build CRUD
- saved report CRUD and generated report results
- analytics endpoints for hero meta, overview, trends, matchups, and synergies

## 2. Base URLs

Example deployed API base URL:

```text
https://deadlock-meta-intelligence-api-tjzo.onrender.com
```

Example local development base URL:

```text
http://127.0.0.1:8000
```

Interactive OpenAPI documentation is available at:

```text
/docs
```

## 3. Authentication

This API currently does not require authentication.

## 4. Response Format

All endpoints return JSON.

Successful responses return either:

- a JSON object
- a JSON array

## 5. Error Handling

The API uses standard HTTP status codes. Common responses include:

- `200 OK`
- `201 Created`
- `400 Bad Request`
- `404 Not Found`
- `422 Unprocessable Entity`
- `500 Internal Server Error`

Typical error payloads currently use FastAPI's default structure with a `detail` field, for example:

```json
{
  "detail": "Hero with id 999 was not found."
}
```

## 6. Endpoint Groups

- Core Resources
- Community Builds
- Custom Builds
- Saved Reports
- Analytics

---

## 7. Core Resources

### `GET /`

Purpose:
- Returns a simple service welcome message.

Example response:

```json
{
  "message": "Deadlock Meta Intelligence API"
}
```

### `GET /health`

Purpose:
- Returns a simple health status used for service checks and deployment monitoring.

Example response:

```json
{
  "status": "ok"
}
```

### `GET /heroes`

Purpose:
- Returns imported hero reference data stored in the local database.

Parameters:
- none

Example response:

```json
[
  {
    "id": 1,
    "name": "Infernus",
    "class_name": "hero_inferno",
    "hero_type": "marksman",
    "complexity": 1,
    "image_small_url": "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/inferno_sm.png"
  }
]
```

### `GET /heroes/{hero_id}`

Purpose:
- Returns detailed information for one imported hero.

Path parameters:
- `hero_id` `integer`

Success response:
- `200 OK`

Error responses:
- `404 Not Found` if the hero does not exist

Example response:

```json
{
  "id": 1,
  "name": "Infernus",
  "class_name": "hero_inferno",
  "role_text": "Lights enemies on fire and sustains pressure over time.",
  "playstyle_text": "Damage-over-time ranged pressure hero.",
  "hero_type": "marksman",
  "complexity": 1,
  "image_small_url": "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/inferno_sm.png"
}
```

### `GET /items`

Purpose:
- Returns imported item and ability reference data stored in the local database.

Parameters:
- none

Example response:

```json
[
  {
    "id": 968099481,
    "name": "Toxic Bullets",
    "class_name": "item_toxic_bullets",
    "item_type": "weapon"
  }
]
```

### `GET /matches`

Purpose:
- Returns imported match records.

Query parameters:
- `hero_id` `integer` optional
- `region_mode` `string` optional
- `date_from` `date` optional
- `date_to` `date` optional

Success response:
- `200 OK`

Example response:

```json
[
  {
    "id": 46255248,
    "start_time": "2026-03-19T00:30:00Z",
    "game_mode": "1",
    "match_mode": "normal",
    "region_mode": "europe",
    "duration_seconds": 2907,
    "winning_team": 1
  }
]
```

### `GET /matches/{match_id}`

Purpose:
- Returns detailed information for one imported match, including participant-level performance records.

Path parameters:
- `match_id` `integer`

Success response:
- `200 OK`

Error responses:
- `404 Not Found` if the match does not exist

Example response:

```json
{
  "id": 46255248,
  "start_time": "2026-03-19T00:30:00Z",
  "game_mode": "1",
  "match_mode": "normal",
  "region_mode": "europe",
  "duration_seconds": 2907,
  "winning_team": 1,
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

---

## 8. Community Builds

### `GET /community-builds`

Purpose:
- Returns imported community builds from public Deadlock data sources.

Query parameters:
- `hero_id` `integer` optional

Success response:
- `200 OK`

Error responses:
- `404 Not Found` if the requested hero does not exist

Example response:

```json
[
  {
    "id": 1,
    "hero_build_id": 1013,
    "hero_id": 1,
    "author_account_id": 29436163,
    "name": "Zieth Infernus",
    "description": "Example build",
    "language": 0,
    "version": 21,
    "favorites_count": 100
  }
]
```

### `GET /community-builds/{id}`

Purpose:
- Returns one imported community build snapshot including imported tag and detail payloads.

Path parameters:
- `id` `integer`

Success response:
- `200 OK`

Error responses:
- `404 Not Found` if the build does not exist

Example response:

```json
{
  "id": 1,
  "hero_build_id": 1013,
  "hero_id": 1,
  "author_account_id": 29436163,
  "name": "Zieth Infernus",
  "description": "Example build",
  "language": 0,
  "version": 21,
  "favorites_count": 100,
  "tags_json": [1, 2],
  "details_json": {
    "mod_categories": [
      {
        "name": "Early Game",
        "mods": [
          {
            "ability_id": 968099481,
            "annotation": "Start here"
          }
        ]
      }
    ]
  }
}
```

### `POST /community-builds/{id}/clone-to-custom`

Purpose:
- Creates an editable custom build draft from an imported community build.

Behaviour:
- copies the hero and description
- stores the original `hero_build_id` as `source_community_build_id`
- extracts ordered item rows from imported mod categories
- extracts ordered ability progression from imported ability order data

Path parameters:
- `id` `integer`

Success response:
- `201 Created`

Error responses:
- `404 Not Found` if the community build does not exist
- `404 Not Found` if the referenced hero does not exist locally

Example response:

```json
{
  "id": 12,
  "title": "Zieth Infernus (Custom Copy)",
  "hero_id": 1,
  "hero_name": "Infernus",
  "author_name": "student",
  "playstyle_tag": null,
  "description": "Example build",
  "notes": "Cloned from imported community build.",
  "source_community_build_id": 1013,
  "items": [
    {
      "id": 31,
      "item_id": 968099481,
      "item_name": "Toxic Bullets",
      "item_type": "weapon",
      "category_name": "Early Game",
      "display_order": 1,
      "is_optional": false,
      "annotation": "Start here"
    }
  ],
  "abilities": [
    {
      "id": 44,
      "ability_id": 1593133799,
      "display_order": 1,
      "annotation": "First point"
    }
  ],
  "created_at": "2026-03-19T06:00:00Z",
  "updated_at": "2026-03-19T06:00:00Z"
}
```

---

## 9. Custom Builds

The custom build model uses a relational structure:

- `custom_builds`
- `custom_build_items`
- `custom_build_abilities`

This allows ordered item rows, ordered ability progression, and easier future extension for build comparison and frontend presentation.

### `POST /custom-builds`

Purpose:
- Creates a new custom build with ordered item rows and ability progression rows.

Request body:

```json
{
  "title": "Afterburn Pressure Build",
  "hero_id": 1,
  "author_name": "student",
  "playstyle_tag": "damage_over_time",
  "description": "Pressure-focused Infernus build",
  "notes": "Use into sustain-heavy compositions.",
  "source_community_build_id": 1013,
  "items": [
    {
      "item_id": 968099481,
      "category_name": "Early Game",
      "display_order": 1,
      "is_optional": false,
      "annotation": "Main lane pressure item."
    },
    {
      "item_id": 2081037738,
      "category_name": "Core",
      "display_order": 2,
      "is_optional": false,
      "annotation": "Primary damage spike."
    }
  ],
  "abilities": [
    {
      "ability_id": 1593133799,
      "display_order": 1,
      "annotation": "First point for lane control."
    },
    {
      "ability_id": 491391007,
      "display_order": 2,
      "annotation": "Second point."
    }
  ]
}
```

Success response:
- `201 Created`

Error responses:
- `404 Not Found` if the hero does not exist
- `404 Not Found` if any referenced item does not exist
- `422 Unprocessable Entity` if the request body is invalid

### `GET /custom-builds`

Purpose:
- Returns summary rows for all custom builds.

Response includes:
- top-level build metadata
- `hero_name`
- `item_count`
- `ability_count`

Example response:

```json
[
  {
    "id": 12,
    "title": "Afterburn Pressure Build",
    "hero_id": 1,
    "hero_name": "Infernus",
    "author_name": "student",
    "playstyle_tag": "damage_over_time",
    "source_community_build_id": 1013,
    "item_count": 2,
    "ability_count": 2,
    "created_at": "2026-03-19T06:00:00Z",
    "updated_at": "2026-03-19T06:00:00Z"
  }
]
```

### `GET /custom-builds/{id}`

Purpose:
- Returns one custom build with expanded item and ability details.

Path parameters:
- `id` `integer`

Success response:
- `200 OK`

Error responses:
- `404 Not Found` if the build does not exist

Example response:

```json
{
  "id": 12,
  "title": "Afterburn Pressure Build",
  "hero_id": 1,
  "hero_name": "Infernus",
  "author_name": "student",
  "playstyle_tag": "damage_over_time",
  "description": "Pressure-focused Infernus build",
  "notes": "Use into sustain-heavy compositions.",
  "source_community_build_id": 1013,
  "items": [
    {
      "id": 31,
      "item_id": 968099481,
      "item_name": "Toxic Bullets",
      "item_type": "weapon",
      "category_name": "Early Game",
      "display_order": 1,
      "is_optional": false,
      "annotation": "Main lane pressure item."
    }
  ],
  "abilities": [
    {
      "id": 44,
      "ability_id": 1593133799,
      "display_order": 1,
      "annotation": "First point for lane control."
    }
  ],
  "created_at": "2026-03-19T06:00:00Z",
  "updated_at": "2026-03-19T06:00:00Z"
}
```

### `PUT /custom-builds/{id}`

Purpose:
- Fully replaces an existing custom build, including all item rows and ability progression rows.

Path parameters:
- `id` `integer`

Request body:
- same structure as `POST /custom-builds`

Success response:
- `200 OK`

Error responses:
- `404 Not Found` if the build does not exist
- `404 Not Found` if the hero or any referenced item does not exist
- `422 Unprocessable Entity` if the request body is invalid

### `DELETE /custom-builds/{id}`

Purpose:
- Deletes a custom build and its related item and ability rows.

Path parameters:
- `id` `integer`

Success response:

```json
{
  "message": "Custom build deleted successfully"
}
```

Error responses:
- `404 Not Found` if the build does not exist

---

## 10. Saved Reports

Saved reports store reusable analytics presets that can later generate actual result payloads.

### `POST /saved-reports`

Purpose:
- Creates a reusable saved report definition.

Request body:

```json
{
  "name": "Infernus Trend Report",
  "report_type": "hero_trend",
  "hero_id": 1,
  "region_mode": "europe",
  "rank_min": 7,
  "rank_max": 11,
  "date_from": "2026-03-01",
  "date_to": "2026-03-19",
  "filters_json": {
    "min_matches": 50
  }
}
```

Success response:
- `201 Created`

Error responses:
- `404 Not Found` if the referenced hero does not exist

### `GET /saved-reports`

Purpose:
- Returns all saved report presets.

### `GET /saved-reports/{id}`

Purpose:
- Returns one saved report preset.

Error responses:
- `404 Not Found` if the report does not exist

### `GET /saved-reports/{id}/result`

Purpose:
- Generates analytics output from a saved report preset.

Currently supported `report_type` values:

- `hero_meta`
- `hero_overview`
- `hero_trend`
- `hero_matchups`
- `hero_synergies`

Success response:
- `200 OK`

Error responses:
- `400 Bad Request` if the report is missing required fields such as `hero_id`
- `400 Bad Request` if the report type is unsupported
- `404 Not Found` if the saved report does not exist

Example response:

```json
{
  "report_id": 2,
  "name": "Infernus Trend Report",
  "report_type": "hero_trend",
  "result": {
    "hero_id": 1,
    "hero_name": "Infernus",
    "bucket": "day",
    "points": [
      {
        "date": "2026-03-19",
        "matches": 12,
        "wins": 7,
        "losses": 5,
        "win_rate": 58.33,
        "avg_kills": 8.5,
        "avg_deaths": 6.1,
        "avg_assists": 11.0
      }
    ]
  }
}
```

### `PATCH /saved-reports/{id}`

Purpose:
- Partially updates a saved report preset.

Error responses:
- `404 Not Found` if the report does not exist
- `404 Not Found` if the new `hero_id` does not exist

### `DELETE /saved-reports/{id}`

Purpose:
- Deletes a saved report preset.

Example response:

```json
{
  "message": "Saved report deleted successfully"
}
```

---

## 11. Analytics

### `GET /analytics/heroes/meta`

Purpose:
- Returns a ranked overview of imported hero performance across all stored match records.

Query parameters:
- `sort_by` `string` optional  
  Supported values:
  - `win_rate`
  - `matches`
  - `avg_kills`
- `limit` `integer` optional, default `10`, maximum `50`

Example response:

```json
{
  "items": [
    {
      "hero_id": 1,
      "hero_name": "Infernus",
      "matches": 120,
      "wins": 58,
      "losses": 62,
      "win_rate": 48.33,
      "avg_kills": 7.42,
      "avg_deaths": 6.91,
      "avg_assists": 10.13
    }
  ]
}
```

### `GET /analytics/heroes/{hero_id}/overview`

Purpose:
- Returns aggregate performance metrics for one hero.

Path parameters:
- `hero_id` `integer`

Error responses:
- `404 Not Found` if the hero does not exist

### `GET /analytics/heroes/{hero_id}/trend`

Purpose:
- Returns day-by-day performance trend data for one hero.

Path parameters:
- `hero_id` `integer`

Query parameters:
- `date_from` `date` optional
- `date_to` `date` optional

Error responses:
- `404 Not Found` if the hero does not exist

### `GET /analytics/heroes/{hero_id}/matchups`

Purpose:
- Returns matchup statistics against enemy heroes.

Path parameters:
- `hero_id` `integer`

Error responses:
- `404 Not Found` if the hero does not exist

### `GET /analytics/heroes/{hero_id}/synergies`

Purpose:
- Returns synergy statistics with allied heroes.

Path parameters:
- `hero_id` `integer`

Error responses:
- `404 Not Found` if the hero does not exist

---

## 12. Notes on Imported Data

This project combines two data categories:

### Imported public data

- heroes
- items and abilities
- matches
- match participants
- community builds

These are imported from public Deadlock community sources using Python scripts.

### User-managed data

- custom builds
- saved reports

These are created and modified through CRUD endpoints exposed by the API.

---

## 13. Data Import Workflow

Example import commands:

```bash
G:\python\python.exe scripts/import_heroes.py
G:\python\python.exe scripts/import_items.py
G:\python\python.exe scripts/import_matches.py --limit 5
G:\python\python.exe scripts/import_community_builds.py --hero-limit 3 --per-hero-limit 5
```

For deployed environments, the same scripts can be executed locally with `DATABASE_URL` pointed at the hosted PostgreSQL instance.

---

## 14. Deployment Note

The API supports:

- local SQLite development
- PostgreSQL-backed deployment

The current deployed version is intended for Render with a PostgreSQL database and FastAPI served through Uvicorn.
