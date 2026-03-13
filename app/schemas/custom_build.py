from datetime import datetime

from pydantic import BaseModel, Field


class CustomBuildCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    hero_id: int
    author_name: str = Field(min_length=1, max_length=100)
    playstyle_tag: str | None = Field(default=None, max_length=50)
    description: str | None = None
    items_json: list[int] = Field(default_factory=list)
    ability_order_json: list[int] | None = None
    notes: str | None = None


class CustomBuildRead(BaseModel):
    id: int
    title: str
    hero_id: int
    author_name: str
    playstyle_tag: str | None
    description: str | None
    items_json: list[int]
    ability_order_json: list[int] | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
