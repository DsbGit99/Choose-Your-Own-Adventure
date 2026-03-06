from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # There will be a one-to-many relationship between a Story and its nodes.
    nodes = relationship("StoryNode", back_populates="story")


class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"))
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, default=list)

    story = relationship("Story", back_populates="nodes")


# NOTE: SQL Alchemy is an Object Relational Mapping (ORM).
# Similar to how we mapped the .env variables into Settings in config.py,
# SQL Alchemy maps data into Python classes such that we don't have to write SQL.

# story name
# theme
# first option
# children: [go left, go right]

# text
# options: []

# ...our stories will have a branching structure, similar to a binary tree
# (but can we have more than two options?)
