from datetime import datetime, date
from typing import Optional
from sqlalchemy import Enum, Column, DateTime
from sqlmodel import SQLModel, Field


class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class Person(SQLModel, table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    sex: Sex
    birth_date: date
    birth_place: str
    country: str

    create_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False))
