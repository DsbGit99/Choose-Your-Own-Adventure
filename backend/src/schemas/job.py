from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class StoryJobBase(BaseModel):
    theme: str


class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: int | None
    completed_at: datetime | None
    error: str | None

    model_config = SettingsConfigDict(from_attributes=True)


class StoryJobCreate(StoryJobBase):
    pass
