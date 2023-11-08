import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, String, create_engine
from sqlalchemy.util.preloaded import orm

Base =orm.declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    update_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    def __repr__(self):
        return f'{self.__class__.__name__}'




