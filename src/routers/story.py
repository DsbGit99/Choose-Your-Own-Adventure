import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from db.database import SessionLocal, get_db
from models.job import StoryJob
from models.story import Story, StoryNode
from schemas.job import StoryJobResponse
from schemas.story import (
    CompleteStoryNodeResponse,
    CompleteStoryResponse,
    CreateStoryRequest,
)

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


def get_session_id(session_id: str | None = Cookie(None)) -> None:
    # NOTE: Session ID is not about authentication, but rather is purposed for
    # identidying a particular browser session. Say, for instance, your browser
    # times out. The session ID allows you to releod the prvious state of your
    # session.

    if not session_id:
        session_id = str(uuid.uuid4())

    return session_id


@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> None:

    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id=job_id, session_id=session_id, theme=request.theme, status="pending"
    )

    db.add(job)
    db.commit()

    # TODO: Add background tasks, generate story
    background_tasks.add_task(
        generate_story_task(job_id=job_id, theme=request.theme, session_id=session_id)
    )

    return job


def generate_story_task(job_id: str, theme: str, session_id: str) -> None:
    # NOTE: Need to create a new session as not to block the db session in
    # create_story. We need these functions to be asynchronous. We can achieve
    # this without asyncio by simply generating an additional session and using
    # FastAPI's BackgroundTasks tracker.

    db = SessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            story = {}  # TODO: generate story

            job.story_id = 1  # TODO: update story_id
            job.status = "completed"
            job.completed_at = datetime.now(tz=UTC)
            db.commit()

        except Exception as e:  # noqa: BLE001
            job.story_id = 1  # TODO: update story_id
            job.status = "failed"
            job.error = str(e)
            db.commit()

    finally:
        db.close()


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Annotated[Session, Depends(get_db)]) -> Story:

    story = db.query(Story).filter(Story).filter(Story.id == story_id.first())

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # TODO: parse story
    return story


def build_complete_story_tree(db: Session, story: Story) -> None:
    pass
