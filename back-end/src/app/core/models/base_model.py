from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.db import db


class BaseModel(db.Model):
    """Base class to handle database model defaults
    for example including default timestamps and a primary key
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, comment="Primary key for the resource")
    created_at = Column(
        DateTime,
        server_default=func.now(),
        comment="Records the time the record was created",
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Records the time the record was last updated",
    )
