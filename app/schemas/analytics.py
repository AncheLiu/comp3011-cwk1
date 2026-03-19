from pydantic import BaseModel, Field


class HeroOverviewRead(BaseModel):
    hero_id: int = Field(description="Hero identifier.", examples=[1])
    hero_name: str = Field(description="Hero display name.", examples=["Infernus"])
    matches: int = Field(description="Number of imported participant records for this hero.", examples=[120])
    wins: int = Field(description="Matches won by this hero.", examples=[58])
    losses: int = Field(description="Matches lost by this hero.", examples=[62])
    win_rate: float = Field(description="Win rate percentage across imported matches.", examples=[48.33])
    avg_kills: float = Field(description="Average kills per imported match.", examples=[7.42])
    avg_deaths: float = Field(description="Average deaths per imported match.", examples=[6.91])
    avg_assists: float = Field(description="Average assists per imported match.", examples=[10.13])
    avg_net_worth: float = Field(description="Average net worth per imported match.", examples=[18432.55])


class HeroTrendPointRead(BaseModel):
    date: str = Field(description="Calendar date bucket.", examples=["2026-03-19"])
    matches: int = Field(description="Matches in this time bucket.", examples=[12])
    wins: int = Field(description="Wins in this time bucket.", examples=[7])
    losses: int = Field(description="Losses in this time bucket.", examples=[5])
    win_rate: float = Field(description="Win rate percentage for this bucket.", examples=[58.33])
    avg_kills: float = Field(description="Average kills in this bucket.", examples=[8.5])
    avg_deaths: float = Field(description="Average deaths in this bucket.", examples=[6.1])
    avg_assists: float = Field(description="Average assists in this bucket.", examples=[11.0])


class HeroTrendRead(BaseModel):
    hero_id: int = Field(description="Hero identifier.", examples=[1])
    hero_name: str = Field(description="Hero display name.", examples=["Infernus"])
    bucket: str = Field(description="Time aggregation bucket used by the endpoint.", examples=["day"])
    points: list[HeroTrendPointRead] = Field(description="Trend points ordered by date.")


class HeroMatchupRead(BaseModel):
    enemy_hero_id: int
    enemy_hero_name: str
    matches: int
    wins: int
    losses: int
    win_rate: float


class HeroMatchupsRead(BaseModel):
    hero_id: int
    hero_name: str
    items: list[HeroMatchupRead]


class HeroSynergyRead(BaseModel):
    ally_hero_id: int
    ally_hero_name: str
    matches: int
    wins: int
    losses: int
    win_rate: float


class HeroSynergiesRead(BaseModel):
    hero_id: int
    hero_name: str
    items: list[HeroSynergyRead]


class HeroMetaEntryRead(BaseModel):
    hero_id: int
    hero_name: str
    matches: int
    wins: int
    losses: int
    win_rate: float
    avg_kills: float
    avg_deaths: float
    avg_assists: float


class HeroMetaRead(BaseModel):
    items: list[HeroMetaEntryRead] = Field(description="Ranked list of heroes for the selected meta sort.")
