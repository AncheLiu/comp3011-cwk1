from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class SavedReportCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200, description="Display name for the saved report preset.", examples=["Infernus Trend Report"])
    report_type: str = Field(min_length=1, max_length=50, description="Analytics type to generate, for example hero_overview or hero_trend.", examples=["hero_trend"])
    hero_id: int | None = Field(default=None, description="Hero to analyse when the report type is hero-specific.", examples=[1])
    region_mode: str | None = Field(default=None, max_length=50, description="Optional region filter reserved for future analytics extensions.", examples=["europe"])
    rank_min: int | None = Field(default=None, description="Optional lower rank bound.", examples=[7])
    rank_max: int | None = Field(default=None, description="Optional upper rank bound.", examples=[11])
    date_from: date | None = Field(default=None, description="Optional inclusive start date for trend-style reports.", examples=["2026-03-01"])
    date_to: date | None = Field(default=None, description="Optional inclusive end date for trend-style reports.", examples=["2026-03-19"])
    filters_json: dict[str, int | str | float | bool | None] | None = Field(default=None, description="Optional structured filter metadata kept with the report preset.", examples=[{"min_matches": 50}])


class SavedReportUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    report_type: str | None = Field(default=None, min_length=1, max_length=50)
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


class SavedReportResultRead(BaseModel):
    report_id: int = Field(description="Identifier of the saved report that generated this result.", examples=[1])
    name: str = Field(description="Saved report name.", examples=["Infernus Trend Report"])
    report_type: str = Field(description="Analytics type used to generate the result.", examples=["hero_trend"])
    result: dict[str, Any] = Field(description="Generated analytics payload returned from the selected report type.")
