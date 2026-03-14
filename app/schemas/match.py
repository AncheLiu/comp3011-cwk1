from datetime import datetime

from pydantic import BaseModel


class MatchRead(BaseModel):
    id: int
    start_time: datetime
    game_mode: str
    match_mode: str
    region_mode: str
    duration_seconds: int | None
    winning_team: int | None

    model_config = {"from_attributes": True}


class MatchParticipantRead(BaseModel):
    account_id: int
    team: int
    hero_id: int
    hero_name: str | None
    hero_level: int | None
    match_result: int | None
    player_kills: int
    player_deaths: int
    player_assists: int
    last_hits: int
    denies: int
    net_worth: int | None
    player_damage: int | None
    damage_taken: int | None
    boss_damage: int | None
    creep_damage: int | None
    neutral_damage: int | None
    shots_hit: int | None
    shots_missed: int | None


class MatchDetailRead(BaseModel):
    id: int
    start_time: datetime
    game_mode: str
    match_mode: str
    region_mode: str
    duration_seconds: int | None
    winning_team: int | None
    net_worth_team_0: int | None
    net_worth_team_1: int | None
    objectives_mask_team0: int | None
    objectives_mask_team1: int | None
    participants: list[MatchParticipantRead]
