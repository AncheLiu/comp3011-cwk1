from datetime import date, datetime

from pydantic import BaseModel, Field


class SavedReportCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    report_type: str = Field(min_length=1, max_length=50)
    hero_id: int | None = None
    region_mode: str | None = Field(default=None, max_length=50)
    rank_min: int | None = None
    rank_max: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    filters_json: dict[str, int | str | float | bool | None] | None = None


class SavedReportRead(BaseModel):
    id: int
    name: str
    report_type: str
    hero_id: int | None
    region_mode: str | None
    rank_min: int | None
    rank_max: int | None
    date_from: date | None
    date_to: date | None
    filters_json: dict[str, int | str | float | bool | None] | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
