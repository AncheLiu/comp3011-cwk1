from datetime import datetime

from pydantic import BaseModel


class CommunityBuildRead(BaseModel):
    id: int
    hero_build_id: int
    hero_id: int
    author_account_id: int | None
    name: str
    description: str | None
    language: int | None
    version: int | None
    last_updated_timestamp: datetime | None
    publish_timestamp: datetime | None
    favorites_count: int | None

    model_config = {"from_attributes": True}


class CommunityBuildDetailRead(CommunityBuildRead):
    tags_json: list[int] | list[str] | None
    details_json: dict
