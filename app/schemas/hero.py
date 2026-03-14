from pydantic import BaseModel


class HeroRead(BaseModel):
    id: int
    name: str
    class_name: str
    hero_type: str | None
    complexity: int | None
    image_small_url: str | None

    model_config = {"from_attributes": True}


class HeroDetailRead(BaseModel):
    id: int
    name: str
    class_name: str
    role_text: str | None
    playstyle_text: str | None
    hero_type: str | None
    complexity: int | None
    image_small_url: str | None
    image_card_url: str | None
    is_selectable: bool

    model_config = {"from_attributes": True}
