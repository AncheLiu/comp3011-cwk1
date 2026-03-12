# Data Sources

## Overview

This project uses publicly available Deadlock community data sources for academic purposes.

The project is not affiliated with or endorsed by Valve.

## Main Sources

### 1. Deadlock API

Primary source for:

- match metadata
- analytics summaries
- community build data
- player and leaderboard-related information

Reference:

- https://api.deadlock-api.com/docs
- https://api.deadlock-api.com/openapi.json

### 2. Deadlock Asset Endpoints

Used for static reference data such as:

- heroes
- items and abilities
- ranks

Reference:

- https://assets.deadlock-api.com/v2/heroes
- https://assets.deadlock-api.com/v2/items
- https://assets.deadlock-api.com/v2/ranks

## Planned Data Usage

### Heroes

Used to populate:

- `heroes`

Main fields:

- hero id
- name
- class name
- role and playstyle text
- hero type
- complexity
- images

### Items and Abilities

Used to populate:

- `items`

Main fields:

- item or ability id
- name
- type
- image
- hero linkage where relevant

### Matches

Used to populate:

- `matches`
- `match_participants`

Main fields:

- match id
- start time
- region
- game mode
- team result
- player hero selection
- kills, deaths, assists
- last hits, denies
- net worth

### Community Builds

Used to populate:

- `community_builds`

Main fields:

- build id
- hero id
- author account id
- build name
- description
- version
- popularity indicators

## Academic Use Note

All external sources used in the final project should be cited in the technical report.

Where possible, the project will store:

- the source URL
- the ingestion purpose
- the mapping from source fields to local tables

## Data Quality Considerations

Potential limitations of the source data include:

- missing or partial fields
- API changes over time
- community-maintained data quality variation
- uncertainty in unofficial mappings

These limitations should be discussed in the final technical report.
