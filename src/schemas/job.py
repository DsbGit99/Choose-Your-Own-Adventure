from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class StoryJobBase(BaseModel):
    theme: str


class StoryJobResponse(BaseModel):
    job_id: int
    status: str
    created_at: datetime
    story_id: Optional[int]
    completed_at: Optional[datetime]
    error: Optional[str]

    model_config = SettingsConfigDict(from_attributes=True)


class StoryJobCreate(StoryJobBase):
    pass
