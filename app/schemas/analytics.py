from pydantic import BaseModel


class HeroOverviewRead(BaseModel):
    hero_id: int
    hero_name: str
    matches: int
    wins: int
    losses: int
    win_rate: float
    avg_kills: float
    avg_deaths: float
    avg_assists: float
    avg_net_worth: float


class HeroTrendPointRead(BaseModel):
    date: str
    matches: int
    wins: int
    losses: int
    win_rate: float
    avg_kills: float
    avg_deaths: float
    avg_assists: float


class HeroTrendRead(BaseModel):
    hero_id: int
    hero_name: str
    bucket: str
    points: list[HeroTrendPointRead]
