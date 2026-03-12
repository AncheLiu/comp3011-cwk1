# Database Design

## Overview

The database is designed around four layers:

- static reference data
- imported fact data
- user-managed CRUD data
- precomputed analytics data

This structure keeps the system easy to explain, extend and query.

## Static Reference Tables

### `heroes`

Stores hero metadata imported from public Deadlock community sources.

Fields:

- `id` `INT PRIMARY KEY`
- `name` `VARCHAR(100) NOT NULL`
- `class_name` `VARCHAR(120) NOT NULL UNIQUE`
- `role_text` `TEXT NULL`
- `playstyle_text` `TEXT NULL`
- `hero_type` `VARCHAR(50) NULL`
- `complexity` `INT NULL`
- `image_small_url` `TEXT NULL`
- `image_card_url` `TEXT NULL`
- `is_selectable` `BOOLEAN NOT NULL DEFAULT TRUE`
- `raw_json` `JSONB NULL`
- `created_at` `TIMESTAMP NOT NULL`
- `updated_at` `TIMESTAMP NOT NULL`

### `items`

Stores item and ability data imported from public sources.

Fields:

- `id` `BIGINT PRIMARY KEY`
- `name` `VARCHAR(150) NOT NULL`
- `class_name` `VARCHAR(150) NOT NULL UNIQUE`
- `item_type` `VARCHAR(50) NOT NULL`
- `hero_id` `INT NULL REFERENCES heroes(id)`
- `image_url` `TEXT NULL`
- `raw_json` `JSONB NULL`
- `created_at` `TIMESTAMP NOT NULL`
- `updated_at` `TIMESTAMP NOT NULL`

### `ranks`

Stores rank definitions.

Fields:

- `tier` `INT PRIMARY KEY`
- `name` `VARCHAR(50) NOT NULL`
- `color` `VARCHAR(20) NULL`
- `raw_json` `JSONB NULL`

## Imported Fact Tables

### `matches`

Stores match-level data.

Fields:

- `id` `BIGINT PRIMARY KEY`
- `start_time` `TIMESTAMP NOT NULL`
- `game_mode` `VARCHAR(50) NOT NULL`
- `match_mode` `VARCHAR(50) NOT NULL`
- `region_mode` `VARCHAR(50) NOT NULL`
- `duration_seconds` `INT NULL`
- `winning_team` `SMALLINT NULL`
- `net_worth_team_0` `INT NULL`
- `net_worth_team_1` `INT NULL`
- `objectives_mask_team0` `INT NULL`
- `objectives_mask_team1` `INT NULL`
- `source` `VARCHAR(50) NOT NULL DEFAULT 'deadlock_api'`
- `ingested_at` `TIMESTAMP NOT NULL`

### `match_participants`

Stores player-level performance within matches.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `match_id` `BIGINT NOT NULL REFERENCES matches(id)`
- `account_id` `BIGINT NOT NULL`
- `team` `SMALLINT NOT NULL`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `hero_level` `INT NULL`
- `match_result` `SMALLINT NULL`
- `player_kills` `INT NOT NULL DEFAULT 0`
- `player_deaths` `INT NOT NULL DEFAULT 0`
- `player_assists` `INT NOT NULL DEFAULT 0`
- `last_hits` `INT NOT NULL DEFAULT 0`
- `denies` `INT NOT NULL DEFAULT 0`
- `net_worth` `INT NULL`
- `player_damage` `BIGINT NULL`
- `damage_taken` `BIGINT NULL`
- `boss_damage` `BIGINT NULL`
- `creep_damage` `BIGINT NULL`
- `neutral_damage` `BIGINT NULL`
- `shots_hit` `BIGINT NULL`
- `shots_missed` `BIGINT NULL`

Constraints:

- `UNIQUE(match_id, account_id)`

### `community_builds`

Stores imported community build snapshots.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `hero_build_id` `BIGINT NOT NULL`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `author_account_id` `BIGINT NULL`
- `name` `VARCHAR(200) NOT NULL`
- `description` `TEXT NULL`
- `language` `INT NULL`
- `version` `INT NULL`
- `last_updated_timestamp` `TIMESTAMP NULL`
- `publish_timestamp` `TIMESTAMP NULL`
- `favorites_count` `INT NULL`
- `tags_json` `JSONB NULL`
- `details_json` `JSONB NOT NULL`
- `created_at` `TIMESTAMP NOT NULL`

Constraints:

- `UNIQUE(hero_build_id, version)`

## User-managed CRUD Tables

### `custom_builds`

Stores builds created by users of the API.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `title` `VARCHAR(200) NOT NULL`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `author_name` `VARCHAR(100) NOT NULL`
- `playstyle_tag` `VARCHAR(50) NULL`
- `description` `TEXT NULL`
- `items_json` `JSONB NOT NULL`
- `ability_order_json` `JSONB NULL`
- `notes` `TEXT NULL`
- `created_at` `TIMESTAMP NOT NULL`
- `updated_at` `TIMESTAMP NOT NULL`

### `saved_reports`

Stores reusable report filter definitions.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `name` `VARCHAR(200) NOT NULL`
- `report_type` `VARCHAR(50) NOT NULL`
- `hero_id` `INT NULL REFERENCES heroes(id)`
- `region_mode` `VARCHAR(50) NULL`
- `rank_min` `INT NULL`
- `rank_max` `INT NULL`
- `date_from` `DATE NULL`
- `date_to` `DATE NULL`
- `filters_json` `JSONB NULL`
- `created_at` `TIMESTAMP NOT NULL`
- `updated_at` `TIMESTAMP NOT NULL`

## Precomputed Analytics Tables

### `hero_daily_stats`

Stores daily aggregated hero performance metrics.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `stat_date` `DATE NOT NULL`
- `matches` `INT NOT NULL`
- `wins` `INT NOT NULL`
- `losses` `INT NOT NULL`
- `win_rate` `NUMERIC(5,2) NOT NULL`
- `avg_kills` `NUMERIC(8,2) NULL`
- `avg_deaths` `NUMERIC(8,2) NULL`
- `avg_assists` `NUMERIC(8,2) NULL`
- `avg_net_worth` `NUMERIC(12,2) NULL`
- `avg_damage` `NUMERIC(12,2) NULL`
- `avg_last_hits` `NUMERIC(10,2) NULL`
- `computed_at` `TIMESTAMP NOT NULL`

Constraints:

- `UNIQUE(hero_id, stat_date)`

### `hero_matchups`

Stores precomputed matchup performance.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `enemy_hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `matches` `INT NOT NULL`
- `wins` `INT NOT NULL`
- `losses` `INT NOT NULL`
- `win_rate` `NUMERIC(5,2) NOT NULL`
- `last_computed_at` `TIMESTAMP NOT NULL`

Constraints:

- `UNIQUE(hero_id, enemy_hero_id)`

### `hero_synergies`

Stores precomputed ally synergy performance.

Fields:

- `id` `BIGSERIAL PRIMARY KEY`
- `hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `ally_hero_id` `INT NOT NULL REFERENCES heroes(id)`
- `matches` `INT NOT NULL`
- `wins` `INT NOT NULL`
- `losses` `INT NOT NULL`
- `win_rate` `NUMERIC(5,2) NOT NULL`
- `last_computed_at` `TIMESTAMP NOT NULL`

Constraints:

- `UNIQUE(hero_id, ally_hero_id)`

## Relationship Summary

Main relationships:

- `heroes -> items`
- `heroes -> match_participants`
- `matches -> match_participants`
- `heroes -> community_builds`
- `heroes -> custom_builds`
- `heroes -> saved_reports`
- `heroes -> hero_daily_stats`
- `heroes -> hero_matchups`
- `heroes -> hero_synergies`

## Design Rationale

This schema supports the coursework goals by combining:

- imported public game data
- user-defined CRUD resources
- analytics-focused precomputed tables

It is intended to show database modelling, API-oriented design and justification of architectural decisions.
