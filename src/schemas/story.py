from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class StoryOptionsSchema(BaseModel):
    text: str
    node_id: int | None = None


class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: list[StoryOptionsSchema] = []

    model_config = SettingsConfigDict(from_attributes=True)


class StoryBase(BaseModel):
    title: int
    session_id: str | None = None

    model_config = SettingsConfigDict(from_attributes=True)


class CreateStoryRequest(BaseModel):
    theme: str


class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: dict[int, CompleteStoryNodeResponse]

    model_config = SettingsConfigDict(from_attributes=True)


# NOTE: model_config = SettingsConfigDict(from_attributes = True)
# enables Pydantic V2 models to populate fields directly from ORM object
# attributes
