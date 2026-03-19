from datetime import datetime

from pydantic import BaseModel, Field


class CustomBuildItemCreate(BaseModel):
    item_id: int
    category_name: str | None = Field(default=None, max_length=100)
    display_order: int = Field(ge=1)
    is_optional: bool = False
    annotation: str | None = None


class CustomBuildAbilityCreate(BaseModel):
    ability_id: int
    display_order: int = Field(ge=1)
    annotation: str | None = None


class CustomBuildCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    hero_id: int
    author_name: str = Field(min_length=1, max_length=100)
    playstyle_tag: str | None = Field(default=None, max_length=50)
    description: str | None = None
    notes: str | None = None
    source_community_build_id: int | None = None
    items: list[CustomBuildItemCreate] = Field(default_factory=list)
    abilities: list[CustomBuildAbilityCreate] = Field(default_factory=list)


class CustomBuildListRead(BaseModel):
    id: int
    title: str
    hero_id: int
    hero_name: str
    author_name: str
    playstyle_tag: str | None
    source_community_build_id: int | None
    item_count: int
    ability_count: int
    created_at: datetime
    updated_at: datetime


class CustomBuildItemRead(BaseModel):
    id: int
    item_id: int
    item_name: str
    item_type: str
    category_name: str | None
    display_order: int
    is_optional: bool
    annotation: str | None


class CustomBuildAbilityRead(BaseModel):
    id: int
    ability_id: int
    display_order: int
    annotation: str | None


class CustomBuildRead(BaseModel):
    id: int
    title: str
    hero_id: int
    hero_name: str
    author_name: str
    playstyle_tag: str | None
    description: str | None
    notes: str | None
    source_community_build_id: int | None
    items: list[CustomBuildItemRead]
    abilities: list[CustomBuildAbilityRead]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
