from pydantic import BaseModel


class HeroRead(BaseModel):
    id: int
    name: str
    class_name: str
    hero_type: str | None
    complexity: int | None
    image_small_url: str | None

    model_config = {"from_attributes": True}
