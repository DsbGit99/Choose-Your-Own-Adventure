from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class StoryOptionsSchema(BaseModel):
    text: str
    node_id: Optional[int] = None


class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []

    model_config = SettingsConfigDict(from_attributes=True)


class StoryBase(BaseModel):
    title: int
    session_id: Optional[str] = None

    model_config = SettingsConfigDict(from_attributes=True)


class CreateStoryRequest(BaseModel):
    theme: str


class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    model_config = SettingsConfigDict(from_attributes=True)


# NOTE: model_config = SettingsConfigDict(from_attributes = True)
# enables Pydantic V2 models to populate fields directly from ORM object attributes
