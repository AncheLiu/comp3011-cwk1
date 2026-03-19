# Custom Build Refactor Plan

## Goal

Refactor the `custom_builds` feature from JSON-based item and ability storage into a relational structure that is easier to query, validate, extend and deploy on PostgreSQL.

The new design should:

- replace `items_json` and `ability_order_json`
- introduce relational child tables for items and abilities
- support cleaner API contracts
- support future build comparison and recommendation features
- support optional linkage back to imported community builds

## Scope

This refactor affects:

- database models
- request and response schemas
- custom build CRUD endpoints
- tests
- API documentation

This refactor does not change:

- hero, item, match and analytics core modules
- `saved_reports`
- imported `community_builds` read endpoints

## Data Model Changes

### Existing Table To Modify

#### `custom_builds`

Keep:

- `id`
- `title`
- `hero_id`
- `author_name`
- `playstyle_tag`
- `description`
- `notes`
- `created_at`
- `updated_at`

Remove:

- `items_json`
- `ability_order_json`

Add:

- `source_community_build_id`

Final shape:

- `id` `BIGSERIAL PRIMARY KEY`
- `title` `VARCHAR(200) NOT NULL`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `author_name` `VARCHAR(100) NOT NULL`
- `playstyle_tag` `VARCHAR(50) NULL`
- `description` `TEXT NULL`
- `notes` `TEXT NULL`
- `source_community_build_id` `BIGINT NULL`
- `created_at` `TIMESTAMP NOT NULL`
- `updated_at` `TIMESTAMP NOT NULL`

### New Table

#### `custom_build_items`

Purpose:

- store build item rows as first-class relational records

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `build_id` `BIGINT NOT NULL REFERENCES custom_builds(id)`
- `item_id` `BIGINT NOT NULL REFERENCES items(id)`
- `category_name` `VARCHAR(100) NULL`
- `display_order` `INT NOT NULL`
- `is_optional` `BOOLEAN NOT NULL DEFAULT FALSE`
- `annotation` `TEXT NULL`

Constraints:

- `UNIQUE(build_id, display_order)`

Recommended indexes:

- `INDEX(build_id)`
- `INDEX(item_id)`

### New Table

#### `custom_build_abilities`

Purpose:

- store ability progression rows as first-class relational records

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `build_id` `BIGINT NOT NULL REFERENCES custom_builds(id)`
- `ability_id` `BIGINT NOT NULL`
- `display_order` `INT NOT NULL`
- `annotation` `TEXT NULL`

Constraints:

- `UNIQUE(build_id, display_order)`

Recommended indexes:

- `INDEX(build_id)`

## API Contract Changes

### Paths To Keep

- `POST /custom-builds`
- `GET /custom-builds`
- `GET /custom-builds/{id}`
- `PUT /custom-builds/{id}`
- `DELETE /custom-builds/{id}`

### New Recommended Path

- `POST /community-builds/{id}/clone-to-custom`

## New Request Shape

### Create / Update Payload

```json
{
  "title": "Afterburn Pressure Build",
  "hero_id": 1,
  "author_name": "student",
  "playstyle_tag": "damage_over_time",
  "description": "Pressure-focused build",
  "notes": "Use into sustain comps",
  "source_community_build_id": 1013,
  "items": [
    {
      "item_id": 968099481,
      "category_name": "Early Game",
      "display_order": 1,
      "is_optional": false,
      "annotation": "Lane pressure"
    }
  ],
  "abilities": [
    {
      "ability_id": 1593133799,
      "display_order": 1,
      "annotation": "First point"
    }
  ]
}
```

### New Detail Response Shape

```json
{
  "id": 1,
  "title": "Afterburn Pressure Build",
  "hero_id": 1,
  "hero_name": "Infernus",
  "author_name": "student",
  "playstyle_tag": "damage_over_time",
  "description": "Pressure-focused build",
  "notes": "Use into sustain comps",
  "source_community_build_id": 1013,
  "items": [
    {
      "id": 11,
      "item_id": 968099481,
      "item_name": "Toxic Bullets",
      "item_type": "weapon",
      "category_name": "Early Game",
      "display_order": 1,
      "is_optional": false,
      "annotation": "Lane pressure"
    }
  ],
  "abilities": [
    {
      "id": 21,
      "ability_id": 1593133799,
      "display_order": 1,
      "annotation": "First point"
    }
  ],
  "created_at": "2026-03-19T12:00:00Z",
  "updated_at": "2026-03-19T12:00:00Z"
}
```

## CRUD Behaviour

### Create

- create one `custom_builds` row
- insert all `custom_build_items`
- insert all `custom_build_abilities`

### Read List

- return build summary rows
- do not fully expand child rows by default
- include `item_count` and `ability_count`

### Read Detail

- expand item rows with item name and item type
- expand ability rows in display order

### Update

- update main build fields
- replace child item rows
- replace child ability rows

### Delete

- delete child rows first or rely on ORM cascade strategy
- delete main build row

## Community Build Clone Flow

### New Endpoint

- `POST /community-builds/{id}/clone-to-custom`

### Behaviour

- load the selected imported community build
- read `hero_id`, `name`, `description` and `details_json`
- create a draft `custom_builds` row
- create related item and ability child rows where data can be reasonably mapped

This endpoint is intended to create an editable starting point rather than a perfect 1:1 reproduction of every community build feature.

## Migration Strategy

Use a clean local rebuild instead of migrating existing local JSON build data.

Recommended steps:

1. update the models
2. remove the local SQLite database file
3. rerun import scripts
4. recreate custom build test data through the API

This is preferred because current custom build data is not a critical project asset and a clean rebuild reduces migration risk.

## PostgreSQL Alignment

This refactor is designed to support PostgreSQL deployment later.

Why it fits PostgreSQL well:

- cleaner relational joins
- easier indexing
- easier filtering and analytics over build parts
- better long-term maintainability than JSON-heavy storage

Recommended later deployment sequence:

1. complete refactor locally
2. verify tests on SQLite
3. switch environment configuration to PostgreSQL
4. rerun imports against PostgreSQL
5. deploy the application

## Implementation Plan

### Phase 1

- refactor models
- add child tables
- remove old JSON fields

### Phase 2

- redesign request/response schemas
- update custom build CRUD routes

### Phase 3

- add `clone-to-custom`

### Phase 4

- rewrite tests
- update API documentation
- update technical report references
