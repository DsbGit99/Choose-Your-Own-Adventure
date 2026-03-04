from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base

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


class Story:
    pass
