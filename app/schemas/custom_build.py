from datetime import datetime

from pydantic import BaseModel, Field


class CustomBuildItemCreate(BaseModel):
    item_id: int = Field(description="Imported item identifier stored in the local items table.", examples=[968099481])
    category_name: str | None = Field(default=None, max_length=100, description="Optional display group such as Early Game or Core.", examples=["Early Game"])
    display_order: int = Field(ge=1, description="1-based ordering used when rendering the build.", examples=[1])
    is_optional: bool = Field(default=False, description="Marks the item as situational rather than core.", examples=[False])
    annotation: str | None = Field(default=None, description="Optional human-readable note for the item choice.", examples=["Main lane pressure item."])


class CustomBuildAbilityCreate(BaseModel):
    ability_id: int = Field(description="Ability identifier from imported Deadlock data.", examples=[1593133799])
    display_order: int = Field(ge=1, description="1-based order for skill progression.", examples=[1])
    annotation: str | None = Field(default=None, description="Optional note explaining the upgrade choice.", examples=["First point for lane control."])


class CustomBuildCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Human-readable name of the custom build.", examples=["Afterburn Pressure Build"])
    hero_id: int
    author_name: str = Field(min_length=1, max_length=100, description="Name shown as the creator of the build.", examples=["student"])
    playstyle_tag: str | None = Field(default=None, max_length=50, description="Short label describing the intended playstyle.", examples=["damage_over_time"])
    description: str | None = Field(default=None, description="Longer explanation of the build idea.", examples=["Pressure-focused Infernus build for sustained damage."])
    notes: str | None = Field(default=None, description="Optional free-form notes for strategy or matchup advice.", examples=["Use into sustain-heavy compositions."])
    source_community_build_id: int | None = Field(default=None, description="Original imported community build identifier if this build was cloned.", examples=[1013])
    items: list[CustomBuildItemCreate] = Field(default_factory=list, description="Ordered item rows included in the build.")
    abilities: list[CustomBuildAbilityCreate] = Field(default_factory=list, description="Ordered ability progression for the build.")


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
