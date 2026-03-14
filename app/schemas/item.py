from pydantic import BaseModel


class ItemRead(BaseModel):
    id: int
    name: str
    class_name: str
    item_type: str
    hero_id: int | None
    image_url: str | None

    model_config = {"from_attributes": True}
